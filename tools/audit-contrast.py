#!/usr/bin/env python3
"""WCAG 2.x contrast audit.

Two parts, deliberately:

  A. CONTRACT pairings — a hand-written list of pairings the token system promises.
     Cheap, readable, and a useful statement of intent.

  B. DERIVED pairings — the colour every element in the shipped HTML actually ends up
     with, computed by matching the stylesheets against the real element tree (see
     tools/css_model.py) and resolving var() chains per scheme.

Part A cannot see a pairing nobody thought to list. That is exactly how a 1.00:1 toast
shipped in v1.0.1: the background came from one rule and the colour from another, and
no line of the list described the combination. Part B derives the pairing from the
artefacts, so it does not need anyone to have anticipated it.

Output: docs/audits/contrast-report.md   Exit 1 on any failure.
"""
import json, re, sys, pathlib, datetime
from collections import defaultdict

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from css_model import (build_var_maps, parse_stylesheet, parse_html, HEX)

ROOT = pathlib.Path(__file__).resolve().parent.parent
T = json.loads((ROOT / "tokens" / "tokens.json").read_text())
P = T["primitive"]


def lum(hexc):
    hexc = hexc.lstrip("#")
    if len(hexc) == 3:
        hexc = "".join(c * 2 for c in hexc)
    r, g, b = (int(hexc[i:i + 2], 16) / 255 for i in (0, 2, 4))
    def f(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def ratio(a, b):
    la, lb = lum(a), lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ================================================================ part A

def resolve_json(ref):
    m = re.fullmatch(r"\{(\w+)\.(\w+)\}", str(ref))
    return P[m.group(1)][m.group(2)] if m else ref


def sem(path, mode):
    node = T["semantic"]
    for k in path.split("."):
        node = node[k]
    return resolve_json(node[mode])


PAIRS = [
 ("text.primary","surface.primary",4.5,"Body text on base surface"),
 ("text.primary","surface.secondary",4.5,"Body text on secondary surface"),
 ("text.primary","surface.tertiary",4.5,"Body text on tertiary fills"),
 ("text.secondary","surface.primary",4.5,"Secondary text on base"),
 ("text.secondary","surface.secondary",4.5,"Secondary text on secondary surface"),
 ("text.link","surface.primary",4.5,"Links on base"),
 ("text.onAction","action.primary",4.5,"Button label on primary action"),
 ("action.primary","surface.primary",3.0,"Primary action vs base (non-text)"),
 ("action.destructive","surface.primary",4.5,"Destructive text/border on base"),
 ("border.focus","surface.primary",3.0,"Focus ring vs base"),
 ("border.input","surface.primary",3.0,"Control boundaries (inputs, PIN, upload)"),
 ("status.success","status.successTint",4.5,"Success badge text on tint"),
 ("status.warning","status.warningTint",4.5,"Warning badge text on tint"),
 ("status.error","status.errorTint",4.5,"Error badge text on tint"),
 ("status.info","status.infoTint",4.5,"Info badge text on tint"),
 ("status.error","surface.primary",4.5,"Error text on base"),
 ("financial.income","surface.primary",4.5,"Income amounts on base"),
 ("financial.negative","surface.primary",4.5,"Negative amounts on base"),
 ("financial.reserved","surface.primary",4.5,"Reserved amounts on base"),
 # Every canonical transaction state on its own tint. These are the pairings a badge
 # actually creates, so the contract asserts all 13 rather than the four someone
 # happened to list — which is how "refunded" went unchecked while styled as success.
 ("transaction.draft","transaction.draftTint",4.5,"State badge: draft"),
 ("transaction.review","transaction.reviewTint",4.5,"State badge: review"),
 ("transaction.authentication","transaction.authenticationTint",4.5,"State badge: authentication"),
 ("transaction.processing","transaction.processingTint",4.5,"State badge: processing"),
 ("transaction.pending","transaction.pendingTint",4.5,"State badge: pending"),
 ("transaction.completed","transaction.completedTint",4.5,"State badge: completed"),
 ("transaction.failed","transaction.failedTint",4.5,"State badge: failed"),
 ("transaction.unknown","transaction.unknownTint",4.5,"State badge: unknown"),
 ("transaction.blocked","transaction.blockedTint",4.5,"State badge: blocked"),
 ("transaction.reversed","transaction.reversedTint",4.5,"State badge: reversed"),
 ("transaction.refunded","transaction.refundedTint",4.5,"State badge: refunded"),
 ("transaction.disputed","transaction.disputedTint",4.5,"State badge: disputed"),
 ("transaction.cancelled","transaction.cancelledTint",4.5,"State badge: cancelled"),
 ("chart.cat1","surface.primary",3.0,"Chart series 1 (non-text)"),
 ("chart.cat2","surface.primary",3.0,"Chart series 2 (non-text)"),
 ("chart.cat3","surface.primary",3.0,"Chart series 3 (non-text)"),
 ("chart.cat4","surface.primary",3.0,"Chart series 4 (non-text)"),
 ("chart.cat5","surface.primary",3.0,"Chart series 5 (non-text)"),
 ("chart.cat6","surface.primary",3.0,"Chart series 6 (non-text)"),
 ("chart.cat7","surface.primary",3.0,"Chart series 7 (non-text)"),
]

contract_rows, contract_fails = [], 0
for mode in ("light", "dark"):
    for fg, bg, minimum, ctx in PAIRS:
        try:
            f, b = sem(fg, mode), sem(bg, mode)
            r = ratio(f, b)
            ok = r >= minimum
            contract_fails += 0 if ok else 1
            contract_rows.append((mode, fg, bg, f, b, r, minimum, ok, ctx))
        except Exception as ex:
            contract_fails += 1
            contract_rows.append((mode, fg, bg, "?", "?", 0, minimum, False, f"ERROR {ex}"))

# ================================================================ part B

# Score core, then every brand. A theme is the one change that can silently
# break contrast everywhere at once — doc 30 promises brands cannot break
# accessibility, and this is what turns that into a build gate rather than a
# hope. Each brand is scored against the same element tree as core.
TOKENS_CSS = (ROOT / "assets" / "tokens.css").read_text()
THEMES = sorted((ROOT / "assets" / "themes").glob("*.css"))
BRANDS = [("core", TOKENS_CSS)] + [
    (t.stem, TOKENS_CSS + "\n" + t.read_text()) for t in THEMES]

SHEETS = ["bes.css", "site.css", "gallery.css"]
rules, order, unsupported_selectors = [], 0, 0
for name in SHEETS:
    got, order, unsup = parse_stylesheet((ROOT / "assets" / name).read_text(), name, order)
    rules += got
    unsupported_selectors += unsup

# Static pages, plus the runtime surfaces captured by tools/test-dom.mjs. The toast, the
# open combobox, the date grid and the chart table exist in no hand-written file — before
# the snapshots existed no static gate had ever scored them, which is precisely how a
# 1.00:1 toast shipped. Run `node tools/test-dom.mjs` before this audit.
SNAPSHOTS = sorted((ROOT / "docs" / "audits" / "dom-snapshots").glob("*.html"))
PAGES = (sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("pages/*.html"))
         + sorted(ROOT.glob("components/*.html")) + SNAPSHOTS)
if not SNAPSHOTS:
    print("WARNING: no DOM snapshots found — runtime-only surfaces (toast, combobox, "
          "date grid, chart tables) are NOT being scored. Run: node tools/test-dom.mjs",
          file=sys.stderr)

unresolved = defaultdict(int)
MERGED, DEREF = None, None


def color_value(raw, scheme):
    raw = raw.strip()
    if HEX.match(raw):
        return raw[:7]
    m = re.search(r"var\((--bes-[\w-]+)(?:\s*,\s*([^)]+))?\)", raw)
    if m:
        got = DEREF(m.group(0), scheme)
        if got:
            return got
        unresolved["var"] += 1
        return None
    if raw.lower() in ("inherit", "currentcolor", "transparent", "none", "unset", "initial"):
        return None
    unresolved["literal:" + raw.split("(")[0][:16]] += 1
    return None


def background_of(decls, scheme):
    for prop in ("background-color", "background"):
        if prop in decls:
            return color_value(decls[prop], scheme), decls[prop].strip()
    return None, None


TEXTLESS = {"html", "body", "head", "script", "style", "meta", "link", "title",
            "svg", "path", "rect", "circle", "line", "g", "polyline", "br", "hr",
            "img", "source", "track", "input", "select", "textarea"}

findings = defaultdict(lambda: {"count": 0, "example": None})
checked = skipped_disabled = 0
brand_totals = {}


def font_min(decls_stack):
    """WCAG large-text threshold, from the winning font-size/weight."""
    size, weight = None, "400"
    for decls in decls_stack:
        if "font-size" in decls:
            m = re.match(r"([\d.]+)px", decls["font-size"].strip())
            if m:
                size = float(m.group(1))
        if "font-weight" in decls:
            weight = decls["font-weight"]
    if size is None:
        return 4.5
    try:
        bold = int(re.sub(r"\D", "", str(weight)) or 400) >= 700
    except ValueError:
        bold = False
    return 3.0 if (size >= 24 or (size >= 18.66 and bold)) else 4.5


PARSED = [(page, parse_html(page.read_text())) for page in PAGES]

for BRAND, brand_css in BRANDS:
  MERGED, DEREF = build_var_maps(brand_css)
  brand_start = checked
  for page, elements in PARSED:
      for el in elements:
          if el.tag in TEXTLESS:
              continue
          matched = sorted((r for r in rules if r.selector.matches(el)), key=lambda r: r.sort_key)
          if not matched:
              continue
          for scheme in ("light", "dark"):
              active = [r for r in matched if scheme in r.schemes]
              if not active:
                  continue

              # foreground: last rule that sets a resolvable colour, per state
              base_fg = base_rule = None
              state_fgs = []
              for r in active:
                  if "color" not in r.decls:
                      continue
                  subj = r.selector.subject
                  if subj.disabled:
                      continue                       # WCAG exempts disabled controls
                  c = color_value(r.decls["color"], scheme)
                  if not c:
                      continue
                  if subj.states:
                      state_fgs.append((c, r))
                  else:
                      base_fg, base_rule = c, r
              candidates = ([(base_fg, base_rule)] if base_fg else []) + state_fgs
              if not candidates:
                  continue

              # background: nearest ancestor (self first) with a resolvable background
              bg = bg_raw = bg_owner = None
              node = el
              while node is not None and bg is None:
                  node_rules = sorted((r for r in rules if r.selector.matches(node)
                                       and scheme in r.schemes
                                       and not r.selector.subject.disabled),
                                      key=lambda r: r.sort_key)
                  for r in reversed(node_rules):
                      val, raw = background_of(r.decls, scheme)
                      if val:
                          bg, bg_raw, bg_owner = val, raw, r
                          break
                      if raw is not None:
                          unresolved["background"] += 1
                  node = node.parent
              assumed = False
              if bg is None:
                  bg = DEREF("var(--bes-surface-primary)", scheme)
                  bg_raw, assumed = "page ground", True
                  if not bg:
                      continue

              decls_stack = [r.decls for r in active]
              minimum = font_min(decls_stack)

              for fg, rule in candidates:
                  checked += 1
                  r_val = ratio(fg, bg)
                  if r_val >= minimum:
                      continue
                  sel = rule.selector.text
                  key = (BRAND, scheme, sel, rule.decls["color"].strip(), bg_raw, round(r_val, 2))
                  f = findings[key]
                  f["count"] += 1
                  if f["example"] is None:
                      f["example"] = {
                          "page": page.relative_to(ROOT).as_posix(),
                          "line": el.line,
                          "tag": el.tag,
                          "cls": " ".join(sorted(el.classes))[:60],
                          "min": minimum,
                          "fg": fg, "bg": bg,
                          "src": f"{rule.source}:{rule.line}",
                          "bg_src": f"{bg_owner.source}:{bg_owner.line}" if bg_owner else "—",
                          "assumed": assumed,
                      }

  brand_totals[BRAND] = checked - brand_start

derived_fails = sum(f["count"] for f in findings.values())

# ================================================================ report

out = ROOT / "docs" / "audits"
out.mkdir(parents=True, exist_ok=True)
total_contract = len(contract_rows)
lines = [
 "# Contrast Audit Report",
 "",
 f"**Generated:** {datetime.date.today()} by `tools/audit-contrast.py` (re-run on every token, CSS or markup change)",
 "**Method:** WCAG 2.x relative-luminance contrast ratio.",
 "",
 "| Part | Scope | Result |",
 "|---|---|---|",
 f"| A — contract | {total_contract} declared token pairings, both schemes | "
 + ("✅ all pass" if contract_fails == 0 else f"❌ {contract_fails} failures") + " |",
 f"| B — derived | {checked} element/state colourings across {len(PAGES)} pages × 2 schemes, "
 f"resolved through {len(rules)} rules in {', '.join(SHEETS)} | "
 + ("✅ all pass" if derived_fails == 0 else f"❌ {len(findings)} distinct failures ({derived_fails} occurrences)") + " |",
 "",
 "Part B is the gate that matters: it computes what each element in the shipped HTML "
 "actually resolves to, so it catches combinations nobody listed. Part A remains as a "
 "statement of intent.",
 "",
 "## Part A — declared token contract",
 "",
 "| Mode | Foreground | Background | Values | Ratio | Min | Result | Context |",
 "|---|---|---|---|---|---|---|---|",
]
for mode, fg, bg, f, b, r, minimum, ok, ctx in contract_rows:
    lines.append(f"| {mode} | `{fg}` | `{bg}` | {f} / {b} | {r:.2f} | {minimum} | "
                 f"{'✅' if ok else '❌ FAIL'} | {ctx} |")

lines += ["", "## Part B — derived from the artefacts", ""]
if derived_fails == 0:
    lines.append(f"✅ **{checked} element colourings computed and scored; none below threshold.**")
else:
    lines.append(f"❌ **{len(findings)} distinct failures across {derived_fails} elements.**")
    lines += ["", "| Brand · scheme | Selector | Colour | On | Values | Ratio | Min | Instances | First seen |",
              "|---|---|---|---|---|---|---|---|---|"]
    for key in sorted(findings, key=lambda k: findings[k]["example"] and -findings[k]["count"]):
        brand, scheme, sel, fg_raw, bg_raw, r_val = key
        e = findings[key]["example"]
        note = " *(ground assumed)*" if e["assumed"] else ""
        lines.append(
            f"| {brand} · {scheme} | `{sel}` | `{fg_raw}`<br>{e['src']} | `{bg_raw}`{note}<br>{e['bg_src']} | "
            f"{e['fg']} / {e['bg']} | **{r_val:.2f}** | {e['min']} | {findings[key]['count']} | "
            f"{e['page']}:{e['line']} |")

lines += ["", "## Scope notes",
 f"- Part B walked {len(PAGES)} HTML pages, matched {len(rules)} rules from "
 f"{', '.join('`'+s+'`' for s in SHEETS)}, and scored {checked} element colourings per the cascade "
 "(specificity, then source order).",
 "- Backgrounds are taken from the nearest ancestor that declares a resolvable one; where the "
 "whole chain declares none, the page ground is assumed and the row is marked.",
 f"- Unresolved and therefore unscored: "
 + (", ".join(f"{v}× {k}" for k, v in sorted(unresolved.items(), key=lambda kv: -kv[1])[:6]) or "none")
 + ". These are gradients, `rgba()`, `currentColor` and keywords — they need a rendering engine, "
 "and they are counted here rather than hidden.",
 f"- {unsupported_selectors} selectors used syntax the matcher does not model and were skipped.",
 "- `:disabled` rules are exempt per WCAG 1.4.3. Hover and focus states are scored — a state "
 "the user can reach is a state that has to be readable.",
 "- Rules qualified `:root:not([data-theme=\"light\"])` outside a `prefers-color-scheme: dark` "
 "block are scored in **both** schemes, because that is what they do — see consistency audit C7.",
 "- Large-text threshold (3:1) applies at ≥24px, or ≥18.66px at weight ≥700, from the winning "
 "`font-size`/`font-weight`.",
 "- Chart series are held to the 3:1 non-text minimum in Part A; data is never conveyed by colour alone.",
 "- This audit covers colour contrast only. Focus visibility, target size and reflow are covered by "
 "the static audit, the DOM tests and the human protocols."]

(out / "contrast-report.md").write_text("\n".join(lines))
fails = contract_fails + derived_fails
print(f"contract {total_contract - contract_fails}/{total_contract} pass · "
      f"derived {checked - derived_fails}/{checked} pass "
      f"({len(findings)} distinct) -> docs/audits/contrast-report.md")
for row in contract_rows:
    if not row[7]:
        print("FAIL(contract):", row[0], row[1], "on", row[2], f"{row[5]:.2f} < {row[6]}")
for key in sorted(findings, key=lambda k: -findings[k]["count"]):
    brand, scheme, sel, fg_raw, bg_raw, r_val = key
    e = findings[key]["example"]
    print(f"FAIL(derived) {brand:6} {scheme:5} {r_val:5.2f} < {e['min']}  {sel}  [{fg_raw} on {bg_raw}]  "
          f"×{findings[key]['count']}  {e['page']}:{e['line']}")
sys.exit(1 if fails else 0)
