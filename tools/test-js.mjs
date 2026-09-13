#!/usr/bin/env node
/* Unit tests for BES money/text utilities. Run: node tools/test-js.mjs */
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

import { createDocument, el } from "./mini-dom.mjs";

// A real (if small) DOM, so behaviors can be bound and driven — not just pure functions.
// The v1.0.1 defects all lived in the CSS/JS/markup seam that stubs cannot reach.
global.window = { matchMedia: () => ({ matches: false }), BES: undefined };
global.matchMedia = global.window.matchMedia;
global.CustomEvent = class { constructor(type, init = {}) { this.type = type; this.detail = init.detail; } };
global.document = createDocument();
try { global.navigator = {}; } catch (e) { /* node >=21: navigator exists */ }
const src = readFileSync(join(dirname(fileURLToPath(import.meta.url)), "..", "assets", "bes.js"), "utf8");
eval(src);
const BES = global.window.BES;

let pass = 0, fail = 0;
function ok(cond, name) {
  if (cond) { pass++; } else { fail++; console.error(`✗ ${name}`); }
}
function eq(actual, expected, name) {
  const ok = Object.is(actual, expected) || (Number.isNaN(expected) && Number.isNaN(actual));
  if (ok) { pass++; } else { fail++; console.error(`✗ ${name}\n    expected ${JSON.stringify(expected)} got ${JSON.stringify(actual)}`); }
}

// ---- formatAmount ----
eq(BES.formatAmount(25000), "AED 25,000.00", "format basic");
eq(BES.formatAmount(-1250.5), "−AED 1,250.50", "format negative true-minus");
eq(BES.formatAmount(0), "AED 0.00", "format zero");
eq(BES.formatAmount(5000, {showPlus:true}), "+AED 5,000.00", "format showPlus");
eq(BES.formatAmount(0, {showPlus:true}), "AED 0.00", "no plus on zero");
eq(BES.formatAmount(1000, {currency:"JPY"}), "JPY 1,000", "ISO precision JPY=0");
eq(BES.formatAmount(1.2345, {currency:"KWD"}), "KWD 1.235", "ISO precision KWD=3 rounds");
eq(BES.formatAmount(2.675), "AED 2.68", "binary-float rounding fixed (2.675)");
eq(BES.formatAmount(NaN), "AED —", "NaN guarded");
eq(BES.formatAmount(Infinity), "AED —", "Infinity guarded");

// ---- parseAmount ----
eq(BES.parseAmount("AED 1,250.50"), 1250.5, "parse currency+grouping");
eq(BES.parseAmount("−AED 500.00"), -500, "parse true-minus (the sign bug)");
eq(BES.parseAmount("-500"), -500, "parse ascii minus");
eq(BES.parseAmount("(500)"), -500, "parse parenthesized negative");
eq(BES.parseAmount("٥٫٥"), 5.5, "Arabic decimal separator (the 10x bug)");
eq(BES.parseAmount("١٬٢٥٠٫٥٠"), 1250.5, "Arabic thousands+decimal");
eq(BES.parseAmount("۵۰۰"), 500, "Extended Arabic-Indic digits");
eq(BES.parseAmount("٥٠٠"), 500, "Arabic-Indic digits");
eq(BES.parseAmount(""), NaN, "empty → NaN");
eq(BES.parseAmount("abc"), NaN, "garbage → NaN");
eq(BES.parseAmount("AED"), NaN, "currency with no amount → NaN");
eq(BES.parseAmount("25000"), 25000, "bare integer");
eq(BES.parseAmount("₹250,800"), 250800, "symbol prefix");
eq(BES.parseAmount("1250.50 AED"), 1250.5, "currency suffix");
eq(BES.parseAmount("+500"), 500, "explicit plus");

// ---- parseAmount: ambiguous input must be rejected, not guessed (v1.0.2) ----
// Each of these previously returned a confident, wrong number. A wrong amount is worse
// than no amount: the old contract claimed NaN for ambiguous input and never delivered it.
eq(BES.parseAmount("2026-08-31"), NaN, "date is not an amount (was −20260831)");
eq(BES.parseAmount("Ref-4471 AED 300"), NaN, "reference number is not an amount (was −4471300)");
eq(BES.parseAmount("AED 12 - fee"), NaN, "trailing sign is not a negative (was −12)");
eq(BES.parseAmount("1.234,56"), NaN, "locale-ambiguous separators (was 1.23456)");
eq(BES.parseAmount("1 234,56"), NaN, "space grouping + comma decimal (was 123456)");
eq(BES.parseAmount("1.234.567,89"), NaN, "European grouping → ambiguous");
eq(BES.parseAmount("1,23"), NaN, "malformed grouping");
eq(BES.parseAmount("1,234,567.89"), 1234567.89, "valid grouping still parses");
eq(BES.parseAmount("- 500"), -500, "leading sign with space");
eq(BES.parseAmount(NaN), NaN, "NaN number → NaN");
eq(BES.parseAmount(Infinity), NaN, "Infinity → NaN");

// ---- localISO: a calendar date is local, never UTC (v1.0.2) ----
// toISOString() shifted the day backwards in every UTC+ zone, including Asia/Dubai,
// which broke month-boundary keyboard navigation in the date picker.
eq(BES.localISO(new Date(2026, 7, 1)), "2026-08-01", "first of month stays local");
eq(BES.localISO(new Date(2026, 0, 1)), "2026-01-01", "new year stays local");
eq(BES.localISO(new Date(2026, 11, 31)), "2026-12-31", "year end stays local");

// ---- round-trip invariant (the release blocker) ----
for (const v of [0, 1, -1, 0.05, -0.05, 999999.99, -999999.99, 1250.5, -1250.5]) {
  eq(BES.parseAmount(BES.formatAmount(v)), Math.round(v*100)/100, `round-trip ${v}`);
}

// ---- esc / tpl ----
eq(BES.esc('<img src=x onerror=alert(1)>'), "&lt;img src=x onerror=alert(1)&gt;", "esc strips XSS vector");
eq(BES.esc('a"b\'c&d'), "a&quot;b&#39;c&amp;d", "esc quotes+amp");
eq(BES.tpl("Hello {n}", {n: "M$& Sons"}), "Hello M$& Sons", "tpl immune to $-patterns");
eq(BES.tpl("{a}+{b}", {a:1, b:2}), "1+2", "tpl multi");
eq(BES.tpl("{missing}", {}), "{missing}", "tpl leaves unknown keys");

// ---- currencyPrecision ----
eq(BES.currencyPrecision("AED"), 2, "precision default");
eq(BES.currencyPrecision("BHD"), 3, "precision BHD");

// ================================================================
// Money value type
// ================================================================
const { Money } = BES;
const M = (v, c = "AED", o) => Money.of(v, c, o);

// ---- exactness: the whole reason the type exists ----
eq(M("0.10").add(M("0.20")).toMajorString(), "0.30", "0.1 + 0.2 is exact");
eq(M("0.10").add(M("0.20")).minor, 30, "…and stored as minor units");
eq(M("1250.50").minor, 125050, "decimal string → minor units");
eq(Money.fromMinor(125050, "AED").toMajorString(), "1250.50", "minor units → decimal string");
eq(M("1000000.00").subtract(M("999999.99")).toMajorString(), "0.01", "no drift at scale");
eq(M("0.00").toMajorString(), "0.00", "zero keeps its precision");
eq(M("-0.05").toMajorString(), "-0.05", "negative minor amounts");
eq(M("1000", "JPY").minor, 1000, "JPY: 0 minor digits");
eq(M("1.234", "KWD").minor, 1234, "KWD: 3 minor digits");

// A float in is read through its decimal text, never its binary value.
eq(M(8.165, "AED", { rounding: "half-up" }).toMajorString(), "8.17",
   "float input read as written (was 8.16 — the double is 8.16499999…)");
eq(M(1.005, "AED", { rounding: "half-up" }).toMajorString(), "1.01", "float input 1.005");
eq(M(0.1 + 0.2, "AED", { rounding: "half-even" }).toMajorString(), "0.30",
   "17-decimal float repr does not overflow the scaler");

// ---- rounding is never implicit ----
eq(M("1.005").isValid(), false, "losing a fil needs an explicit mode — invalid without one");
eq(M("1.00").isValid(), true, "exact input needs no mode");
eq(M("1.005", "AED", { rounding: "half-even" }).toMajorString(), "1.00", "half-even rounds to even");
eq(M("1.015", "AED", { rounding: "half-even" }).toMajorString(), "1.02", "half-even rounds to even, up");
eq(M("1.0050001", "AED", { rounding: "half-even" }).toMajorString(), "1.01",
   "sticky bit: just above the tie is not a tie");
eq(M("1.005", "AED", { rounding: "half-up" }).toMajorString(), "1.01", "half-up");
eq(M("1.005", "AED", { rounding: "half-down" }).toMajorString(), "1.00", "half-down");
eq(M("-1.005", "AED", { rounding: "half-up" }).toMajorString(), "-1.01", "half-up is away from zero");
eq(M("0.004", "AED", { rounding: "ceil" }).toMajorString(), "0.01", "ceil");
eq(M("-0.004", "AED", { rounding: "ceil" }).toMajorString(), "0.00",
   "ceil toward positive — and zero has no sign, so no '−AED 0.00' on screen");
eq(M("-0.001", "AED", { rounding: "half-up" }).format(), "AED 0.00",
   "a rounded-away negative renders as plain zero (was '−AED 0.00')");
eq(M("-0.004", "AED", { rounding: "floor" }).toMajorString(), "-0.01", "floor");
eq(M("0.009", "AED", { rounding: "down" }).toMajorString(), "0.00", "down truncates");
eq(M("0.001", "AED", { rounding: "up" }).toMajorString(), "0.01", "up is away from zero");
eq(M("1.005", "AED", { rounding: "nonsense" }).isValid(), false, "unknown mode is not a silent default");

// ---- arithmetic ----
eq(M("100.00").add(M("50.00", "USD")).isValid(), false, "cross-currency add is invalid, not coerced");
eq(M("100.00").compare(M("100.00")), 0, "compare equal");
eq(M("100.00").compare(M("100.01")), -1, "compare less");
eq(M("500.00", "USD").multiply("3.6730", { rounding: "half-even" }).toMajorString(), "1836.50",
   "FX rate applied as exact decimal, not the nearest double");
eq(M("100.00").multiply("0.025", { rounding: "half-even" }).toMajorString(), "2.50", "2.5% fee");
eq(M("100.00").divide(3, { rounding: "half-even" }).toMajorString(), "33.33", "divide rounds");
eq(M("1.00").multiply(0.5, { rounding: "half-even" }).toMajorString(), "0.50", "numeric factor accepted");

// ---- allocation: splitting money must not create or destroy fils ----
{
  const parts = M("100.00").allocate(3);
  eq(parts.map((p) => p.toMajorString()).join(" "), "33.34 33.33 33.33", "largest-remainder split");
  eq(parts.reduce((a, b) => a.add(b)).toMajorString(), "100.00", "…and the parts sum to the whole");
  const seven = M("100.00").allocate(7);
  eq(seven.reduce((a, b) => a.add(b)).toMajorString(), "100.00", "7-way split still sums exactly");
  const weighted = M("5000.00").allocate([70, 30]);
  eq(weighted.map((p) => p.toMajorString()).join(" "), "3500.00 1500.00", "weighted split");
  eq(M("0.05").allocate(3).reduce((a, b) => a.add(b)).toMajorString(), "0.05",
     "a 5-fil split across 3 still sums to 5 fils");
}

// ---- the ceiling is a wall, not a slope ----
eq(M("99999999999999999").isValid(), false, "beyond MAX_SAFE_INTEGER minor units → invalid");
eq(M(1e21).isValid(), false, "huge exponential → invalid, never approximated");
eq(M(1e-7).isValid(), false, "tiny exponential → invalid (below any minor unit)");
eq(M(1e21, "AED", { rounding: "half-even" }).isValid(), false,
   "…and a rounding mode does not make an out-of-range number acceptable");
eq(M(NaN).isValid(), false, "NaN → invalid");
eq(M(Infinity).isValid(), false, "Infinity → invalid");
eq(M("abc").isValid(), false, "garbage → invalid");
eq(M("").isValid(), false, "empty → invalid");
eq(M("1.005").format(), "AED —", "an invalid Money renders as — , never as a plausible number");

// ---- parse → Money, exactly ----
eq(Money.parse("AED 1,250.50").minor, 125050, "parse currency + grouping to minor units");
eq(Money.parse("١٬٢٥٠٫٥٠").minor, 125050, "parse Arabic-Indic digits and separators");
eq(Money.parse("(500)").toMajorString(), "-500.00", "accounting parentheses");
eq(Money.parse("2026-08-31").isValid(), false, "a date is still not an amount");
eq(Money.parse("1.234,56").isValid(), false, "locale-ambiguous input is still rejected");

// ---- rendering through Intl ----
eq(M("25000.00").format(), "AED 25,000.00", "default render matches the house form");
eq(M("-1250.50").format(), "−AED 1,250.50", "true minus U+2212, not a hyphen");
eq(M("5000.00").format({ showPlus: true }), "+AED 5,000.00", "showPlus");
eq(M("0.00").format({ showPlus: true }), "AED 0.00", "no plus on zero");
eq(M("25000.00").format({ currencyDisplay: "none" }), "25,000.00", "amount without the code");
eq(M("1000", "JPY").format(), "JPY 1,000", "JPY renders with no decimals");
eq(M("1.234", "KWD").format(), "KWD 1.234", "KWD renders three");

// Arabic-Indic output — parsed since v1.0.1, but until now impossible to render.
// doc 29 §2: display-only preference, never mixed within a screen.
eq(M("25000.00").format({ locale: "ar-AE", numerals: "arab" }), "AED ٢٥٬٠٠٠٫٠٠",
   "Eastern Arabic numerals on request");
eq(M("25000.00").format({ locale: "ar-AE" }), "AED 25,000.00",
   "…and Western digits remain the default in Arabic (doc 29 §2)");
eq(Money.parse(M("25000.00").format({ locale: "ar-AE", numerals: "arab" })).minor, 2500000,
   "round-trip: what we render in Eastern numerals, we can parse back");

// Compact form for summaries and chart axes (doc 13 bars it from authorise/review/receipt)
eq(M("1500.00").formatCompact({ currencyDisplay: "none" }), "1.5K",
   "compact axis label states the real number (was '2K' for 1500)");
eq(M("1250000.00").formatCompact({ currencyDisplay: "none" }), "1.25M", "compact millions");

// Spoken form for accessible names (doc 13: the name is the spoken form)
ok(/minus/.test(M("-1250.50").toSpoken()), "spoken form carries the sign as a word");
ok(/dirham/i.test(M("-1250.50").toSpoken()), "spoken form names the currency, not the code");

// ---- wire format ----
eq(JSON.stringify(M("1250.50")), '{"currency":"AED","minor":125050,"precision":2}',
   "serialises as minor units — the form a bank API should exchange");

// ---- the legacy façade keeps its contract ----
eq(BES.formatAmount("1250.5"), "AED 1,250.50", "formatAmount now accepts decimal strings (was 'AED —')");
eq(BES.formatAmount(Money.fromMinor(125050, "AED")), "AED 1,250.50", "formatAmount accepts a Money");

// ---- DOM: balance masking actually hides the balance (v1.0.2) ----
// Amounts are authored with the digits as a bare text node inside <bdi>. The old rule
// (`.bes-masked > *:not(.cur)`) matched element children only, so "Hide balance" left
// the amount fully visible and fully in the accessibility tree while reporting success.
{
  const bal = el("bdi", { id: "t-bal", class: "bes-amount" },
                 el("span", { class: "cur" }, "AED"), " 25,000.00");
  const btn = el("button", { "data-bes-mask": "t-bal", "aria-pressed": "false",
                             "aria-label": "Hide balance" });
  const root = el("div", {}, btn, bal);
  document.body.appendChild(root);
  BES.init(document.body);

  const val = bal.querySelector(".bes-mask-val");
  eq(!!val, true, "mask: value wrapped in an element the CSS can reach");
  eq(val && val.parentNode === bal, true, "mask: wrapper is a direct child (`> .bes-mask-val`)");
  eq(val && val.textContent.trim(), "25,000.00", "mask: wrapper holds the digits");
  eq(bal.querySelector(".cur").textContent, "AED", "mask: currency label left outside the wrapper");

  btn.click();
  eq(bal.classList.contains("bes-masked"), true, "mask: masked class applied on click");
  eq(btn.getAttribute("aria-pressed"), "true", "mask: button state reflects masking");
  eq(bal.querySelector("[data-mask-sr]").textContent, "Balance hidden",
     "mask: screen readers get replacement text, not the amount");
  eq(bal.getAttribute("aria-label"), null,
     "mask: no aria-label on <bdi> — a generic cannot carry a name");

  btn.click();
  eq(bal.classList.contains("bes-masked"), false, "mask: unmasks on second click");
  eq(bal.querySelector("[data-mask-sr]").textContent, "", "mask: replacement text cleared when shown");
  eq(bal.textContent.includes("25,000.00"), true, "mask: value preserved across the cycle");
}

// ---- DOM: currency input errors are reachable by assistive tech (v1.0.2) ----
// The old code set aria-invalid and wrote a message into an element with no id, no live
// region and no association — WCAG 3.3.1 and 4.1.3 both failing on the money control.
{
  const input = el("input", { "data-bes-currency": "", "data-max": "25000",
                              "data-currency": "AED", type: "text" });
  input.value = "";
  const ctx = el("div", { class: "bes-context-line" }, "Available AED 25,000.00");
  const field = el("div", { class: "bes-field" }, input, ctx);
  document.body.appendChild(field);
  BES.init(document.body);

  eq(!!ctx.id, true, "currency input: context line has an id");
  eq(input.getAttribute("aria-describedby"), ctx.id,
     "currency input: field points at its context line");
  eq(ctx.getAttribute("aria-live"), "polite", "currency input: context line announces changes");
  eq(ctx.dataset.initial, "Available AED 25,000.00", "currency input: initial text captured for restore");

  input.value = "30,000";
  input.dispatch("input");
  eq(input.getAttribute("aria-invalid"), "true", "currency input: over-max marks the field invalid");
  eq(ctx.textContent, "Exceeds available balance by AED 5,000.00",
     "currency input: reason is stated, not just the invalid state");
  eq(ctx.classList.contains("bes-context-line--error"), true, "currency input: error styling applied");

  input.value = "1,000";
  input.dispatch("input");
  eq(input.getAttribute("aria-invalid"), null, "currency input: valid amount clears the invalid state");
  eq(ctx.textContent, "Leaves AED 24,000.00", "currency input: headroom shown when valid");

  input.value = "";
  input.dispatch("input");
  eq(input.getAttribute("aria-invalid"), null,
     "currency input: an empty field is incomplete, not in error");
  eq(ctx.textContent, "Available AED 25,000.00",
     "currency input: original context restored, not the stale error");
}

console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
