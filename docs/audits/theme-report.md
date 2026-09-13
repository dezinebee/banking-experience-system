# Brand Theme Contract Audit

Doc 30: *"a brand change is describable entirely as token values… if it requires touching component internals, it's rejected."* This audit is that sentence, executable.

**Result:** ✅ PASS · 1 theme(s) checked

- ℹ️ sadu: 116 token overrides, 0 CSS properties, 21 token families touched

## What is checked

| ID | Rule |
|---|---|
| T1 | Every declaration is a `--bes-*` custom property — no CSS properties |
| T2 | Every selector is scoped to the brand — a theme cannot restyle core |
| T3 | No `@import`, `@font-face`, `@keyframes` or `@layer` — values, not machinery |
| T4 | Every token set already exists in core — a theme retunes, never invents |
| T5 | At least one theme exists, from a JSON source, and it overrides something |
| T6 | The generated CSS still matches what its source compiles to |

Contrast for every brand is scored separately by `tools/audit-contrast.py`, which runs the full derived audit once per theme — a brand that breaks AA fails the build.