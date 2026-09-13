#!/usr/bin/env node
/* Component behaviour tests in a real DOM (jsdom), plus snapshot generation.
   Run: node tools/test-dom.mjs

   Why this exists
   ---------------
   Half of BES only exists at runtime. The toast, the combobox listbox, the date grid,
   the chart SVG and its table equivalent are all built by bes.js and appear in no HTML
   file. Every static gate — the markup audit, the contrast audit, the consistency audit
   — walks files on disk, so none of them has ever seen those surfaces. That is the same
   blind spot that let a 1.00:1 toast ship: not "nobody listed the pairing", but "the
   element was never on disk to be scored".

   So this file does two jobs:
     1. asserts component behaviour by driving it (keyboard, clicks, paste), and
     2. writes the resulting DOM to docs/audits/dom-snapshots/, which the contrast
        audit then walks alongside the static pages.

   Run it before the audits. `npm run gates` enforces that order. */

import { readFileSync, writeFileSync, mkdirSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";
import { JSDOM } from "jsdom";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const BES_JS = readFileSync(join(ROOT, "assets", "bes.js"), "utf8");
const SNAP_DIR = join(ROOT, "docs", "audits", "dom-snapshots");

let pass = 0, fail = 0;
const failures = [];
function ok(cond, name) {
  if (cond) pass++;
  else { fail++; failures.push(name); console.error(`✗ ${name}`); }
}
function eq(actual, expected, name) {
  const good = Object.is(actual, expected);
  if (good) pass++;
  else {
    fail++; failures.push(name);
    console.error(`✗ ${name}\n    expected ${JSON.stringify(expected)} got ${JSON.stringify(actual)}`);
  }
}

/* Build a document with bes.js loaded and initialised over `body`.
   `now` pins what the fixture believes the current instant is. The date picker
   stamps aria-current="date" from `new Date()`, so without pinning, its snapshot
   embeds the machine's calendar day — the drift gate would then fail on the next
   day, and `npm run gates` (which runs this file under UTC and again under
   TZ=Asia/Dubai) could write two different snapshots within one invocation. */
function mount(body, { dir = "ltr", lang = "en", now = null } = {}) {
  const dom = new JSDOM(
    `<!doctype html><html lang="${lang}" dir="${dir}"><head><title>fixture</title></head>` +
    `<body class="bes">${body}</body></html>`,
    { runScripts: "outside-only", pretendToBeVisual: true }
  );
  const { window } = dom;
  // jsdom has no layout, so offsetParent is always null; the focus trap filters on it
  Object.defineProperty(window.HTMLElement.prototype, "offsetParent", {
    get() { return this.ownerDocument.body.contains(this) ? this.parentNode : null; },
  });
  // jsdom implements no layout; these are the only two layout APIs bes.js calls
  window.Element.prototype.scrollIntoView = function () {};
  window.Element.prototype.getBoundingClientRect = function () {
    return { top: 0, left: 0, right: 0, bottom: 0, width: 100, height: 20, x: 0, y: 0 };
  };
  if (now != null) {
    const RealDate = window.Date;
    // `now` is [year, monthIndex, day, …] and is built in LOCAL time on purpose.
    // The picker derives "today" from local getFullYear/getMonth/getDate, and no
    // single UTC instant is the same calendar day everywhere — the world spans 26
    // hours of offsets, so UTC-11 and UTC+14 would disagree. Pinning the local
    // date makes the snapshot identical in every zone.
    const FIXED = new RealDate(...now).getTime();
    class PinnedDate extends RealDate {
      constructor(...args) { args.length === 0 ? super(FIXED) : super(...args); }
      static now() { return FIXED; }
    }
    window.Date = PinnedDate;
  }
  window.eval(BES_JS);
  window.BES.init(window.document.body);
  return { dom, window, document: window.document, BES: window.BES };
}

function key(el, k, init = {}) {
  const ev = new el.ownerDocument.defaultView.KeyboardEvent("keydown",
    { key: k, bubbles: true, cancelable: true, ...init });
  el.dispatchEvent(ev);
  return ev;
}

const snapshots = [];
function snapshot(name, document) {
  snapshots.push({ name, html: document.body.innerHTML });
}

/* ================================================================ toast
   Built entirely by JS — it has never appeared in any file the audits read. */
{
  const { window, document, BES } = mount(
    `<button class="bes-btn bes-btn--secondary" data-bes-toast="IBAN copied">Show toast</button>`
  );
  document.querySelector("[data-bes-toast]").click();
  const toast = document.querySelector(".bes-toast");
  ok(!!toast, "toast: appears on click");
  ok(!!document.querySelector("#bes-live-polite, [aria-live]"), "toast: a live region exists to announce it");
  eq(toast && toast.textContent.trim(), "IBAN copied", "toast: carries its message");
  snapshot("toast", document);
  window.close();
}

/* ================================================================ combobox */
{
  const { window, document } = mount(`
    <div class="bes-combo">
      <label class="bes-label" for="cb">Recipient bank</label>
      <input class="bes-input" id="cb" role="combobox" aria-expanded="false"
             aria-controls="cb-list" autocomplete="off">
      <ul class="bes-combo-list" id="cb-list" role="listbox" hidden>
        <li data-value="enbd">Emirates NBD</li>
        <li data-value="adcb">ADCB</li>
        <li data-value="fab">First Abu Dhabi Bank</li>
        <li class="empty" hidden>No bank found — check the SWIFT code</li>
      </ul>
    </div>`);
  const input = document.getElementById("cb");
  input.focus();
  input.value = "ad";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  const visible = [...document.querySelectorAll("#cb-list li")].filter((li) => !li.hidden);
  ok(visible.length >= 1, "combobox: filters to matching options");
  key(input, "ArrowDown");
  const active = input.getAttribute("aria-activedescendant");
  ok(!!active && !!document.getElementById(active),
     "combobox: ArrowDown sets aria-activedescendant to a real option");
  snapshot("combobox-open", document);

  // zero results — the recovery message must stay in the accessibility tree
  input.value = "zzzz";
  input.dispatchEvent(new window.Event("input", { bubbles: true }));
  const empty = document.querySelector("#cb-list li.empty");
  ok(empty && !empty.hidden, "combobox: shows the zero-results message");
  ok(empty && empty.getAttribute("role") !== "presentation",
     "combobox: zero-results message is not removed from the a11y tree");
  snapshot("combobox-empty", document);
  window.close();
}

/* ================================================================ date picker */
{
  const { window, document } = mount(
    `<div class="bes-datepicker" data-bes-datepicker id="dp" data-year="2026" data-month="7"
          data-disabled-days="0" data-disabled-note="Sundays are non-processing days"></div>`,
    // Pinned so aria-current="date" lands on a fixed day. 12 Sept 2026 is a
    // Saturday inside the rendered month and is not a disabled day, so the
    // snapshot exercises the today-outline against a selectable cell.
    { now: [2026, 8, 12, 12, 0, 0] });
  const grid = document.querySelector(".bes-dp-grid");
  ok(!!grid, "date picker: renders a grid");

  const disabled = [...document.querySelectorAll("[data-iso]")]
    .filter((b) => b.getAttribute("aria-disabled") === "true");
  ok(disabled.length > 0, "date picker: marks non-processing days");
  ok(disabled.every((b) => b.disabled || b.hasAttribute("data-disabled")),
     "date picker: disabled days carry a state the CSS can select on");

  // month-boundary keyboard navigation — the UTC bug's symptom was focus loss
  const roving = document.querySelector('[data-iso][tabindex="0"]');
  ok(!!roving, "date picker: exactly one day is in the tab order");
  const startIso = roving.dataset.iso;
  roving.focus();
  for (let i = 0; i < 40; i++) key(document.activeElement || roving, "ArrowRight");
  const landed = document.activeElement;
  ok(landed && landed.hasAttribute("data-iso"),
     "date picker: focus stays on a day after crossing a month boundary");
  ok(landed && landed.dataset.iso !== startIso, "date picker: focus actually moved");
  snapshot("datepicker", document);
  window.close();
}

/* ================================================================ modal */
{
  const { window, document } = mount(`
    <button class="bes-btn bes-btn--primary" data-bes-open="m1">Open confirm dialog</button>
    <div class="bes-scrim" id="m1" role="dialog" aria-modal="true" aria-labelledby="m1t">
      <div class="bes-modal">
        <h3 id="m1t">Send AED 5,000.00 to Rajesh Kumar?</h3>
        <div class="actions">
          <button class="bes-btn bes-btn--secondary" data-bes-close="m1">Cancel</button>
          <button class="bes-btn bes-btn--primary" id="m1ok">Send</button>
        </div>
      </div>
    </div>`);
  const scrim = document.getElementById("m1");
  const trigger = document.querySelector("[data-bes-open]");
  trigger.focus();
  trigger.click();
  ok(scrim.classList.contains("open"), "modal: opens");
  eq(scrim.getAttribute("aria-modal"), "true", "modal: marked aria-modal while open");
  ok(scrim.contains(document.activeElement), "modal: focus moves inside on open");

  key(document.activeElement, "Escape");
  ok(!scrim.classList.contains("open"), "modal: Escape closes");
  eq(scrim.getAttribute("aria-modal"), null,
     "modal: aria-modal removed on close (a closed dialog must not claim it)");
  eq(document.activeElement, trigger, "modal: focus returns to the trigger");
  snapshot("modal-closed", document);
  window.close();
}

/* ================================================================ PIN entry */
{
  const { window, document } = mount(`
    <div class="bes-pin" data-bes-pin>
      <input type="password" inputmode="numeric" maxlength="1" aria-label="PIN digit 1">
      <input type="password" inputmode="numeric" maxlength="1" aria-label="PIN digit 2">
      <input type="password" inputmode="numeric" maxlength="1" aria-label="PIN digit 3">
      <input type="password" inputmode="numeric" maxlength="1" aria-label="PIN digit 4">
    </div>`);
  const cells = [...document.querySelectorAll(".bes-pin input")];

  // WCAG 3.3.8 permits a cognitive-function test only when an assist exists — paste is it
  const paste = new window.Event("paste", { bubbles: true, cancelable: true });
  paste.clipboardData = { getData: () => "٤٢٧٩" };   // Arabic-Indic digits
  cells[0].dispatchEvent(paste);
  eq(cells.map((c) => c.value).join(""), "4279",
     "PIN: paste accepted and Arabic-Indic digits converted (WCAG 3.3.8 assist)");
  snapshot("pin", document);
  window.close();
}

/* ================================================================ sortable table */
{
  const { window, document } = mount(`
    <table class="bes-table" data-bes-sortable>
      <thead><tr><th data-sort="text">Payee</th><th class="num" data-sort="num">Amount (AED)</th></tr></thead>
      <tbody>
        <tr><td>Etisalat</td><td class="num">843.50</td></tr>
        <tr><td>DEWA</td><td class="num">250,000.00</td></tr>
        <tr><td>Salik</td><td class="num">—</td></tr>
        <tr><td>Refund</td><td class="num">−340.00</td></tr>
      </tbody>
    </table>`);
  const th = document.querySelector('th[data-sort="num"]');
  const btn = th.querySelector("button");
  ok(!!btn, "sortable table: header is a real button (keyboard + AT operable)");
  btn.click();
  eq(th.getAttribute("aria-sort"), "ascending", "sortable table: aria-sort reflects direction");
  const order = [...document.querySelectorAll("tbody tr")].map((r) => r.cells[0].textContent);
  eq(order[0], "Refund", "sortable table: negatives sort below zero, not as large positives");
  ok(order.indexOf("DEWA") === order.length - 1, "sortable table: largest amount sorts last");
  snapshot("table-sorted", document);
  window.close();
}

/* ================================================================ charts */
{
  const { window, document } = mount(`<div id="c1"></div><div id="c2"></div>`);
  const { BES } = window;
  if (typeof BES.chartBar === "function") {
    BES.chartBar(document.getElementById("c1"), [
      { label: "Jan", value: 8200 }, { label: "Feb", value: -4000 }, { label: "Mar", value: 12500 },
    ], { label: "Net cash flow by month", currency: "AED" });
    const svg = document.querySelector("#c1 svg");
    ok(!!svg, "chart: renders");
    ok(!!document.querySelector("#c1 details, #c1 table"),
       "chart: ships a table equivalent (data never conveyed by shape alone)");
    const tableText = (document.querySelector("#c1 details, #c1 table") || {}).textContent || "";
    ok(tableText.includes("−AED 4,000.00"),
       "chart: the table equivalent states the negative with the house true-minus");
    ok(tableText.includes("AED 12,500.00"),
       "chart: the table equivalent formats through the one money formatter");
    const axis = [...document.querySelectorAll("#c1 svg text")].map((t) => t.textContent);
    ok(!axis.some((t) => /^\d+K$/.test(t) && t !== "0K"),
       "chart: axis labels are not rounded to a different number than the gridline");
    snapshot("chart-bar", document);
  }
  window.close();
}

/* ================================================================ tabs */
{
  const { window, document } = mount(`
    <div class="bes-tabs" role="tablist" aria-label="Account views">
      <button role="tab" id="t1" aria-controls="p1" aria-selected="true" tabindex="0">Transactions</button>
      <button role="tab" id="t2" aria-controls="p2" aria-selected="false" tabindex="-1">Statements</button>
    </div>
    <div role="tabpanel" id="p1" aria-labelledby="t1">…</div>
    <div role="tabpanel" id="p2" aria-labelledby="t2" hidden>…</div>`);
  const [t1, t2] = [document.getElementById("t1"), document.getElementById("t2")];
  t1.focus();
  key(t1, "ArrowRight");
  eq(document.activeElement, t2, "tabs: ArrowRight moves focus (roving tabindex)");
  eq(t2.getAttribute("aria-selected"), "true", "tabs: selection follows focus");
  eq(t1.getAttribute("tabindex"), "-1", "tabs: only the selected tab is in the tab order");
  snapshot("tabs", document);
  window.close();
}

/* ================================================================ transaction states
   The system's signature idea. Until now UNKNOWN existed as prose plus one
   hand-built screen, and "Refunded" rendered identically to "Completed". */
{
  const states = ["draft", "review", "authentication", "processing", "pending", "completed",
                  "failed", "unknown", "blocked", "reversed", "refunded", "disputed", "cancelled"];
  const { window, document, BES } = mount(
    states.map((s) => `<span class="bes-badge" data-bes-state="${s}"></span>`).join("\n") +
    `<div class="bes-result" data-bes-state="unknown">
       <div class="ic"></div><h3></h3><p class="money-state"></p>
       <button class="bes-btn bes-btn--primary" data-bes-retry>Try again</button>
       <button class="bes-btn bes-btn--secondary" id="u-support">Contact support</button>
     </div>
     <div class="bes-result" data-bes-state="failed">
       <div class="ic"></div><h3></h3><p class="money-state"></p>
       <button class="bes-btn bes-btn--primary" data-bes-retry id="f-retry">Try again</button>
     </div>`);

  eq(Object.keys(BES.TRANSACTION_STATES).length, 13, "states: all 13 canonical states registered");

  for (const s of states) {
    const el = document.querySelector(`[data-bes-state="${s}"].bes-badge`);
    ok(el && el.classList.contains(`bes-badge--${s}`), `states: ${s} gets its own badge variant`);
    ok(el && el.querySelector("svg.glyph"), `states: ${s} renders a glyph, so colour is not alone`);
    ok(el && el.textContent.trim().length > 0, `states: ${s} renders a label`);
  }

  // the two collisions the review named, now actually distinguishable
  const completed = document.querySelector('[data-bes-state="completed"]');
  const refunded = document.querySelector('[data-bes-state="refunded"]');
  ok(completed.className !== refunded.className,
     "states: Refunded is not styled as Completed (they shared a class before)");
  ok(completed.querySelector("svg.glyph").innerHTML !== refunded.querySelector("svg.glyph").innerHTML,
     "states: …and they carry different glyphs, since they share a hue");
  const processing = document.querySelector('[data-bes-state="processing"]');
  const unknown = document.querySelector('[data-bes-state="unknown"].bes-badge');
  ok(processing.querySelector("svg.glyph").innerHTML !== unknown.querySelector("svg.glyph").innerHTML,
     "states: UNKNOWN is distinguishable from Processing");
  eq(unknown.textContent.trim(), "Checking status",
     "states: UNKNOWN never says 'failed' — doc 07's prime directive");

  // doc 07 §4: a quiet rail may still be holding a successful transfer
  const unknownResult = document.querySelector('.bes-result[data-bes-state="unknown"]');
  eq(unknownResult.querySelector("[data-bes-retry]"), null,
     "states: a retry control is removed from an UNKNOWN result (double-send risk)");
  ok(!!document.getElementById("u-support"),
     "states: …and the other recovery actions are left alone");
  ok(unknownResult.querySelector(".money-state").textContent.includes("safe"),
     "states: UNKNOWN states where the money is");
  ok(!!document.getElementById("f-retry"),
     "states: a confirmed failure keeps retry — that is the one state where it is safe");
  ok(document.querySelector('.bes-result[data-bes-state="failed"] .money-state')
       .textContent.includes("No money"),
     "states: FAILED states that no money moved");

  snapshot("transaction-states", document);
  window.close();
}

/* ================================================================ states in Arabic */
{
  const { window, document } = mount(
    `<span class="bes-badge" data-bes-state="unknown"></span>` +
    `<span class="bes-badge" data-bes-state="refunded"></span>`,
    { dir: "rtl", lang: "ar" });
  const unknown = document.querySelector('[data-bes-state="unknown"]');
  ok(/[؀-ۿ]/.test(unknown.textContent),
     "states (AR): the label comes from the registry in Arabic, not English");
  snapshot("transaction-states-rtl", document);
  window.close();
}

/* ================================================================ RTL sanity */
{
  const { window, document } = mount(`
    <div class="bes-tabs" role="tablist" aria-label="طرق العرض">
      <button role="tab" id="r1" aria-controls="q1" aria-selected="true" tabindex="0">الحوالات</button>
      <button role="tab" id="r2" aria-controls="q2" aria-selected="false" tabindex="-1">الكشوف</button>
    </div>
    <div role="tabpanel" id="q1" aria-labelledby="r1">…</div>
    <div role="tabpanel" id="q2" aria-labelledby="r2" hidden>…</div>`,
    { dir: "rtl", lang: "ar" });
  const [r1, r2] = [document.getElementById("r1"), document.getElementById("r2")];
  r1.focus();
  key(r1, "ArrowLeft");
  eq(document.activeElement, r2, "tabs (RTL): ArrowLeft advances — direction-aware keyboard");
  snapshot("tabs-rtl", document);
  window.close();
}

/* ================================================================ snapshots out */
mkdirSync(SNAP_DIR, { recursive: true });
for (const { name, html } of snapshots) {
  writeFileSync(join(SNAP_DIR, `${name}.html`),
    `<!doctype html>\n<html lang="en"><head><meta charset="utf-8">\n` +
    `<title>DOM snapshot — ${name}</title></head>\n<body class="bes">\n${html}\n</body></html>\n`);
}
writeFileSync(join(SNAP_DIR, "README.md"),
  "# DOM snapshots\n\n" +
  "Generated by `tools/test-dom.mjs` — **do not edit by hand.**\n\n" +
  "These are the surfaces `bes.js` builds at runtime: the toast, the open combobox and its\n" +
  "zero-results state, the date grid, a closed modal, PIN entry, a sorted table, a chart with\n" +
  "its table equivalent, and tabs in both directions. None of them exists in any hand-written\n" +
  "HTML file, so before these snapshots existed no static gate had ever scored them — which is\n" +
  "how a 1.00:1 toast shipped in v1.0.1.\n\n" +
  "`tools/audit-contrast.py` walks this directory alongside `pages/` and `components/`.\n" +
  "Regenerate with `node tools/test-dom.mjs`; CI fails if the committed output has drifted.\n\n" +
  `Snapshots: ${snapshots.map((s) => "`" + s.name + "`").join(" · ")}\n`);

console.log(`\n${pass} passed, ${fail} failed · ${snapshots.length} snapshots -> docs/audits/dom-snapshots/`);
if (fail) console.error("\nFailing:\n  " + failures.join("\n  "));
process.exit(fail ? 1 : 0);
