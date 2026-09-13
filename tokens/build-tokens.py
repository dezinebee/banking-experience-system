#!/usr/bin/env python3
"""BES token compiler: tokens.json -> ../assets/tokens.css

Emission lives in tokens/emit.py and is shared with the brand-theme compiler, so
a brand can never be built by different rules than the core it overrides.
Guarantees: every {ref} resolves or the build FAILS; every semantic colour defines
both light and dark or the build FAILS; semantic values that reference primitives
emit as var() chains, so overriding a primitive once cascades everywhere.
Run: python3 tokens/build-tokens.py"""
import json, sys, pathlib

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from emit import emit_all, block                                # noqa: E402

SRC = HERE / "tokens.json"
OUT = HERE.parent / "assets" / "tokens.css"
T = json.loads(SRC.read_text())
B, ERRORS = emit_all(T)

if ERRORS:
    print(f"TOKEN BUILD FAILED — {len(ERRORS)} errors:")
    for e in ERRORS:
        print("  ✗", e)
    sys.exit(1)

css = f"""/* ============================================================
   Banking Experience System — design tokens v{T["$meta"]["version"]}
   GENERATED from tokens/tokens.json — do not edit by hand.
   Tiers: primitive -> semantic -> component (doc 06).
   Theming: semantic and component tokens reference the tier above via var()
   chains, so a brand theme overrides values once and everything cascades.
   Scheme via prefers-color-scheme / [data-theme]. Density via [data-density].
   Arabic metrics via :lang(ar). Brands: assets/themes/<id>.css.
   ============================================================ */
:root {{
{block(B["prim"])}

  /* semantic — light (var() chains into primitives) */
{block(B["sem_light"])}

  /* density — standard */
{block(B["dens"]["standard"])}

  /* type scale */
{block(B["type"])}

  /* component tier — brand-overridable, scoped to one component each */
{block(B["comp"])}
}}

@media (prefers-color-scheme: dark) {{
  :root:not([data-theme="light"]) {{
{block(B["sem_dark"], "    ")}
  }}
}}
:root[data-theme="dark"] {{
{block(B["sem_dark"])}
}}

:root[data-density="comfortable"] {{
{block(B["dens"]["comfortable"])}
}}
:root[data-density="compact"] {{
{block(B["dens"]["compact"])}
}}

/* Arabic optical metrics (doc 02 §2) */
:lang(ar) {{
{block(B["ar"])}

  /* Latin tracking breaks Arabic cursive joining — the component token is the
     override point, so no rule has to win a specificity fight to undo it. */
  --bes-cardArt-track: 0;
  --bes-cardArt-trackWide: 0;
}}
"""
OUT.write_text(css)
print(f"wrote {OUT.name}: {len(B['prim'])} primitives, {len(B['sem_light'])} semantic (light), "
      f"{len(B['comp'])} component, validated OK")
