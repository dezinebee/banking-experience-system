#!/usr/bin/env python3
"""Brand-theme contract audit — doc 30's acceptance test, made executable.

Doc 30 states the test plainly: "a brand change is describable entirely as token
values… if it requires touching component internals, it's rejected." Until a theme
existed that claim was untested; this makes it a build gate.

A theme file must be TOKEN VALUES ONLY:
  T1  every declaration is a custom property (--bes-*) — no real CSS properties
  T2  every selector is scoped to this brand — a theme cannot restyle core
  T3  no @import, no font/keyframe/layer at-rules — a theme adds no machinery
  T4  every token it sets already exists in core — a theme retunes, never invents
  T5  the theme actually overrides something, and its source is a JSON token file
  T6  the generated CSS matches its source (no hand-editing a generated file)

Exit 1 on any violation.
"""
import json, re, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
TOKENS_CSS = (ROOT / "assets" / "tokens.css").read_text()
CORE_VARS = set(re.findall(r"(--bes-[\w-]+)\s*:", TOKENS_CSS))
THEME_DIR = ROOT / "assets" / "themes"
SRC_DIR = ROOT / "tokens" / "themes"

errors, notes = [], []
themes = sorted(THEME_DIR.glob("*.css")) if THEME_DIR.exists() else []

if not themes:
    errors.append("T5 no brand theme exists — doc 30's multi-brand contract is untested. "
                  "A system that has never been themed does not know whether it can be.")

RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")

for css_path in themes:
    tid = css_path.stem
    text = re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css_path.read_text(), flags=re.S)

    # T3 at-rules other than the scheme/density media queries
    for at in re.findall(r"@([a-zA-Z-]+)", text):
        if at != "media":
            errors.append(f"T3 {tid}.css uses @{at} — a theme supplies values, not machinery")

    declared = 0
    for m in RULE.finditer(text):
        sel_raw, body = m.group(1).strip(), m.group(2)
        if sel_raw.startswith("@"):
            continue
        for sel in sel_raw.split(","):
            sel = sel.strip()
            if not sel:
                continue
            # T2 every selector carries the brand scope
            if f'[data-brand="{tid}"]' not in sel:
                errors.append(f"T2 {tid}.css has an unscoped selector `{sel[:60]}` — "
                              f"a theme may only speak about its own brand")
        for decl in body.split(";"):
            decl = decl.strip()
            if not decl:
                continue
            prop = decl.split(":", 1)[0].strip()
            # T1 custom properties only
            if not prop.startswith("--"):
                errors.append(f"T1 {tid}.css declares `{prop}` — that is a CSS property, "
                              f"not a token value. Doc 30 rejects a brand that needs a rule: "
                              f"the gap is in the system, not the theme")
                continue
            # T4 no inventing tokens the components do not read
            if prop not in CORE_VARS:
                errors.append(f"T4 {tid}.css sets `{prop}`, which core does not define — "
                              f"a component reads core's tokens, so this value can never apply")
            declared += 1

    if declared == 0:
        errors.append(f"T5 {tid}.css overrides no tokens")
    else:
        notes.append(f"{tid}: {declared} token overrides, 0 CSS properties, "
                     f"{len(set(re.findall(r'--bes-([a-zA-Z]+)', text)))} token families touched")

    # T5/T6 provenance: generated from a JSON source, and still in sync with it
    src = SRC_DIR / f"{tid}.json"
    if not src.exists():
        errors.append(f"T5 {tid}.css has no source at tokens/themes/{tid}.json — "
                      f"a theme is compiled from tokens, not written as CSS")
    else:
        before = css_path.read_text()
        r = subprocess.run([sys.executable, str(ROOT / "tokens" / "build-theme.py"), tid],
                           capture_output=True, text=True)
        if r.returncode != 0:
            errors.append(f"T6 {tid} does not rebuild: {r.stdout.strip() or r.stderr.strip()}")
        elif css_path.read_text() != before:
            errors.append(f"T6 {tid}.css differs from what its source compiles to — "
                          f"the generated file was hand-edited, or the commit is stale")

out = ROOT / "docs" / "audits" / "theme-report.md"
out.parent.mkdir(parents=True, exist_ok=True)
lines = ["# Brand Theme Contract Audit", "",
         "Doc 30: *\"a brand change is describable entirely as token values… if it requires "
         "touching component internals, it's rejected.\"* This audit is that sentence, executable.",
         "",
         f"**Result:** {'✅ PASS' if not errors else f'❌ {len(errors)} violations'} · "
         f"{len(themes)} theme(s) checked", ""]
for e in errors:
    lines.append(f"- ❌ {e}")
for n in notes:
    lines.append(f"- ℹ️ {n}")
lines += ["", "## What is checked", "",
          "| ID | Rule |", "|---|---|",
          "| T1 | Every declaration is a `--bes-*` custom property — no CSS properties |",
          "| T2 | Every selector is scoped to the brand — a theme cannot restyle core |",
          "| T3 | No `@import`, `@font-face`, `@keyframes` or `@layer` — values, not machinery |",
          "| T4 | Every token set already exists in core — a theme retunes, never invents |",
          "| T5 | At least one theme exists, from a JSON source, and it overrides something |",
          "| T6 | The generated CSS still matches what its source compiles to |",
          "",
          "Contrast for every brand is scored separately by `tools/audit-contrast.py`, which "
          "runs the full derived audit once per theme — a brand that breaks AA fails the build."]
out.write_text("\n".join(lines))
print(f"{len(errors)} violations, {len(themes)} theme(s) -> docs/audits/theme-report.md")
for e in errors[:20]:
    print("ERR", e)
for n in notes:
    print("OK ", n)
sys.exit(1 if errors else 0)
