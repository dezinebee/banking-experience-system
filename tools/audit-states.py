#!/usr/bin/env python3
"""Transaction-state contract audit — doc 06 §6's claim, made executable.

Doc 06 says: *"The state names are the stable API: a 'pending' transaction is the
same concept in the UI, the event stream and the copy deck."* That was a sentence in
a document. Three artefacts disagreed about what the states even were — doc 07's
table defined 13, doc 06's prose listed 12, and the tokens emitted 10 — and no
component read the state tokens at all, so "Refunded" shipped styled as success and
was pixel-identical to "Completed".

This audit makes the claim falsifiable. The canonical list is doc 07 §4's contract
table — the normative state machine — and every other artefact must agree with it:

  S1  doc 07's table is parseable and is the single source of the state list
  S2  every state has a colour token AND a tint token in transaction.*
  S3  every state has a badge variant in bes.css that reads those tokens
  S4  every state has a JS registry entry with an icon and EN + AR labels
  S5  no state colour lives outside transaction.* — one namespace, or the claim is false
  S6  UNKNOWN never offers retry, and only a confirmed failure does (doc 07's prime directive)
  S7  the JS registry and doc 07's table contain exactly the same names
  S8  no two states share both a colour and a glyph (colour never alone)
  S9  no page hand-rolls a state badge with a generic status class

Exit 1 on any violation.
"""
import json, re, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors, notes = [], []

# ---------------------------------------------------------------- S1 canonical list
spec = (ROOT / "docs" / "system" / "07-financial-semantics.md").read_text()
section = spec[spec.index("## 4."):spec.index("## 5.")]
rows = re.findall(r"^\|\s*\*{0,2}([a-z]+)\*{0,2}\s*\|", section, re.M)
CANON = [r for r in rows if r not in ("state",)]
if len(CANON) < 10:
    errors.append(f"S1 could not parse doc 07 §4's state table (found {len(CANON)} rows) — "
                  f"the audit's source of truth is that table; if its shape changed, this "
                  f"audit must be updated deliberately, not bypassed")
    CANON = []
else:
    notes.append(f"S1 canonical states from doc 07 §4: {len(CANON)} — {', '.join(CANON)}")

# ---------------------------------------------------------------- S2 tokens
tokens = json.loads((ROOT / "tokens" / "tokens.json").read_text())
tx = {k: v for k, v in tokens["semantic"].get("transaction", {}).items() if not k.startswith("$")}
for state in CANON:
    if state not in tx:
        errors.append(f"S2 state `{state}` has no `transaction.{state}` colour token")
    if state + "Tint" not in tx:
        errors.append(f"S2 state `{state}` has no `transaction.{state}Tint` — a badge "
                      f"cannot be built from the state alone")

# ---------------------------------------------------------------- S3 badge variants
bes_css = (ROOT / "assets" / "bes.css").read_text()
for state in CANON:
    rule = re.search(r"\.bes-badge--" + state + r"\b[^{]*\{([^}]*)\}", bes_css)
    if not rule:
        errors.append(f"S3 no `.bes-badge--{state}` — the state exists as a token and as "
                      f"prose, but a product cannot render it")
    else:
        body = rule.group(1)
        if f"--bes-transaction-{state}" not in body:
            errors.append(f"S3 `.bes-badge--{state}` does not read `transaction.{state}` — "
                          f"a badge wired to a different namespace is how Refunded ended up "
                          f"styled as success")

# ---------------------------------------------------------------- S4/S6/S7 JS registry
bes_js = (ROOT / "assets" / "bes.js").read_text()
reg = re.search(r"BES\.TRANSACTION_STATES\s*=\s*\{(.*?)\n  \};", bes_js, re.S)
if not reg:
    errors.append("S4 no BES.TRANSACTION_STATES registry in bes.js")
    entries = {}
else:
    body = reg.group(1)
    entries = {}
    for m in re.finditer(r"^\s{4}(\w+):\s*st\((.*?)\)(?:,|\s*$)", body, re.S | re.M):
        entries[m.group(1)] = m.group(2)
    for state in CANON:
        if state not in entries:
            errors.append(f"S4 state `{state}` is not in BES.TRANSACTION_STATES — "
                          f"a product has no label or glyph for it")
            continue
        args = entries[state]
        if "ICON." not in args:
            errors.append(f"S4 state `{state}` has no glyph — colour would be carrying the "
                          f"state alone for states that share a hue")
        strings = re.findall(r'"([^"]*)"', args)
        arabic = [s for s in strings if re.search(r"[؀-ۿ]", s)]
        english = [s for s in strings if re.search(r"[A-Za-z]", s)]
        if not english:
            errors.append(f"S4 state `{state}` has no English label")
        if not arabic:
            errors.append(f"S4 state `{state}` has no Arabic label — doc 29 §5: a string "
                          f"without an AR pair fails the content gate")
    for extra in sorted(set(entries) - set(CANON)):
        errors.append(f"S7 `{extra}` is in the JS registry but not in doc 07 §4's table — "
                      f"the code and the spec disagree about what the states are")

    # S6 the prime directive, as a property of the data
    for state, args in entries.items():
        retry = "allowsRetry: true" in args
        if state == "unknown" and retry:
            errors.append("S6 UNKNOWN allows retry. A rail that has gone quiet may still be "
                          "holding a successful transfer; retry is a double-send. doc 07 §4")
        if retry and state != "failed":
            errors.append(f"S6 `{state}` allows retry — doc 07's prime directive limits retry "
                          f"to a confirmed failure")
    if "allowsRetry: true" not in entries.get("failed", ""):
        errors.append("S6 `failed` does not allow retry — a confirmed failure is exactly the "
                      "state where retry is safe and expected")
    if not re.search(r"data-bes-retry", bes_js):
        errors.append("S6 nothing enforces the no-retry rule at runtime — the registry says "
                      "allowsRetry but no binder acts on it")

# ---------------------------------------------------------------- S8 distinguishability
# States may share a hue — completed/refunded are both green because they are related.
# What they may not do is share a hue AND a glyph: then only the label separates them,
# which is the failure "colour never carries meaning alone" is meant to prevent, and
# exactly how Refunded and Completed became indistinguishable in the first place.
by_look = {}
for state in CANON:
    args = entries.get(state, "")
    icon = (re.search(r"ICON\.(\w+)", args) or [None, None])[1]
    hue = tx.get(state, {}).get("light")
    if not icon or not hue:
        continue
    key = (hue, icon)
    if key in by_look:
        errors.append(f"S8 `{state}` and `{by_look[key]}` share both a colour ({hue}) and a "
                      f"glyph (ICON.{icon}) — only the label would tell them apart, which is "
                      f"colour-and-shape carrying nothing. Give one of them its own mark.")
    by_look[key] = state

# ---------------------------------------------------------------- S9 no hand-rolled states
# A badge whose visible label is a canonical state's label must be rendered as that
# state — via `data-bes-state` or the matching variant. Hand-rolling one with a generic
# status class is how "Refunded" and "Completed" both ended up as `.bes-badge--success`
# across the demos while the tokens sat unused.
label_of = {}
for state in CANON:
    args = entries.get(state, "")
    strings = re.findall(r'"([^"]*)"', args)
    en = next((x for x in strings if re.search(r"[A-Za-z]", x)), None)
    if en:
        label_of[en.lower()] = state
BADGE = re.compile(r'<span[^>]*class="([^"]*bes-badge[^"]*)"([^>]*)>([^<]{0,60})</span>')
for f in sorted(ROOT.glob("*.html")) + sorted(ROOT.glob("components/*.html")):
    for m in BADGE.finditer(f.read_text()):
        classes, attrs, text = m.group(1), m.group(2), m.group(3).strip()
        state = label_of.get(text.lower())
        if not state or "data-bes-state" in attrs:
            continue
        if f"bes-badge--{state}" not in classes:
            errors.append(f"S9 {f.name} renders the label \"{text}\" with `{classes.strip()}` — "
                          f"that is the canonical `{state}` state. Use "
                          f'data-bes-state="{state}" so colour, glyph and label come from one place.')

# ---------------------------------------------------------------- S5 one namespace
other = []
for ns in ("financial", "status"):
    for k in tokens["semantic"].get(ns, {}):
        if k.startswith("$"):
            continue
        base = k[:-4] if k.endswith("Tint") else k
        if base in CANON:
            other.append(f"{ns}.{k}")
if other:
    errors.append("S5 transaction states also live outside `transaction.*`: "
                  + ", ".join(other) + ". Two namespaces for one concept means the state "
                  "name is not the stable API — a component can read either and drift.")

# ---------------------------------------------------------------- report
out = ROOT / "docs" / "audits" / "state-report.md"
out.parent.mkdir(parents=True, exist_ok=True)
lines = ["# Transaction State Contract Audit", "",
         "Doc 06 §6: *\"The state names are the stable API: a 'pending' transaction is the "
         "same concept in the UI, the event stream and the copy deck.\"* This audit is that "
         "sentence, executable. The canonical list is doc 07 §4's normative contract table; "
         "every other artefact must agree with it.", "",
         f"**Result:** {'✅ PASS' if not errors else f'❌ {len(errors)} violations'} · "
         f"{len(CANON)} canonical states", ""]
for e in errors:
    lines.append(f"- ❌ {e}")
for n in notes:
    lines.append(f"- ℹ️ {n}")

if CANON and not errors:
    lines += ["", "## The contract, per state", "",
              "| State | Colour token | Tint | Badge | Glyph | EN | AR | Retry |",
              "|---|---|---|---|---|---|---|---|"]
    for state in CANON:
        args = entries.get(state, "")
        strings = re.findall(r'"([^"]*)"', args)
        en = next((s for s in strings if re.search(r"[A-Za-z]", s)), "—")
        ar = next((s for s in strings if re.search(r"[؀-ۿ]", s)), "—")
        icon = (re.search(r"ICON\.(\w+)", args) or [None, "—"])[1]
        retry = "yes" if "allowsRetry: true" in args else "no"
        lines.append(f"| `{state}` | ✅ | ✅ | `.bes-badge--{state}` | `{icon}` | {en} | {ar} | {retry} |")
    lines += ["",
              "Arabic labels are machine-drafted and flagged unreviewed system-wide until the "
              "native review in `docs/testing/arabic-rtl-review.md` passes — see STATUS.md.",
              "",
              "`completed` and `refunded` share green; `processing`, `pending` and `unknown` "
              "share teal. That is deliberate — they are related states — and it is exactly why "
              "the glyph and label come from the registry rather than from the caller."]

lines += ["", "## What is checked", "", "| ID | Rule |", "|---|---|",
          "| S1 | Doc 07 §4's table parses and is the single source of the state list |",
          "| S2 | Every state has a `transaction.*` colour **and** tint token |",
          "| S3 | Every state has a badge variant reading those tokens |",
          "| S4 | Every state has a registry entry with a glyph and EN + AR labels |",
          "| S5 | No transaction state colour lives outside `transaction.*` |",
          "| S6 | UNKNOWN never offers retry; only a confirmed failure does; a binder enforces it |",
          "| S7 | The JS registry and doc 07's table contain exactly the same names |",
          "| S8 | No two states share both a colour and a glyph — sharing a hue is fine, sharing both is not |",
          "| S9 | No page labels a badge with a state name while styling it as generic status |"]
out.write_text("\n".join(lines))
print(f"{len(errors)} violations, {len(CANON)} canonical states -> docs/audits/state-report.md")
for e in errors[:25]:
    print("ERR", e)
for n in notes:
    print("OK ", n)
sys.exit(1 if errors else 0)
