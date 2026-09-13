#!/usr/bin/env python3
"""Brand theme compiler: tokens/themes/<id>.json -> assets/themes/<id>.css

Doc 30's acceptance test is that a brand change is describable entirely as token
values — "if it requires touching component internals, it's rejected." This
compiler is what makes that testable rather than aspirational:

  * a theme is deep-merged onto the core token set and compiled by exactly the
    same rules (tokens/emit.py), so a brand cannot be built by different logic
    than the core it overrides;
  * only the variables whose values actually DIFFER from core are emitted, so
    the output file is the measure of how much a brand had to say;
  * a theme that fails to produce a difference, or that references a token that
    does not exist, fails the build.

Run: python3 tokens/build-theme.py [id ...]     (default: every theme found)
"""
import json, sys, pathlib, copy, datetime

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from emit import emit_all, block                                # noqa: E402

ROOT = HERE.parent
CORE = json.loads((HERE / "tokens.json").read_text())
OUTDIR = ROOT / "assets" / "themes"


def deep_merge(base, over):
    out = copy.deepcopy(base)
    for k, v in over.items():
        if str(k).startswith("$"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out


def derive_arabic_metrics(merged, theme):
    """A brand that restates a type step must not silently keep core's Arabic
    metrics for it — doc 02's optical adjustment is +1px size, +2px line."""
    for step, v in theme.get("type", {}).items():
        if str(step).startswith("$") or step not in merged["type"]:
            continue
        target = merged["type"][step]
        if "arSize" not in target:
            continue
        if "arSize" in v:
            continue
        if "size" in v:
            target["arSize"] = f"{int(str(v['size']).rstrip('px')) + 1}px"
        if "line" in v:
            target["arLine"] = f"{int(str(v['line']).rstrip('px')) + 2}px"


def compile_theme(path):
    theme = json.loads(path.read_text())
    meta = theme.get("$meta", {})
    tid = meta.get("id") or path.stem
    merged = deep_merge(CORE, theme)
    derive_arabic_metrics(merged, theme)

    core_blocks, core_err = emit_all(CORE)
    brand_blocks, brand_err = emit_all(merged)
    errors = [f"{tid}: {e}" for e in brand_err]
    if core_err:
        errors += [f"core: {e}" for e in core_err]

    def delta(name, indent="  "):
        base = dict(core_blocks[name]) if name != "dens" else None
        pairs = brand_blocks[name]
        out = [(n, v) for n, v in pairs if base.get(n) != v]
        return out

    d_prim = delta("prim")
    d_light = delta("sem_light")
    d_dark = delta("sem_dark")
    d_type = delta("type")
    d_ar = delta("ar")
    d_comp = delta("comp")
    d_dens = {m: [(n, v) for n, v in brand_blocks["dens"][m]
                  if dict(core_blocks["dens"][m]).get(n) != v] for m in ("comfortable", "standard", "compact")}

    total = (len(d_prim) + len(d_light) + len(d_dark) + len(d_type)
             + len(d_ar) + len(d_comp) + sum(len(v) for v in d_dens.values()))
    if total == 0:
        errors.append(f"{tid}: theme overrides nothing — it is identical to core")

    if errors:
        return tid, None, errors, 0

    # Two scopes, deliberately: on <html> for a whole product, and on any element
    # for a subtree — which is what makes a side-by-side brand comparison possible
    # at all. Custom properties inherit, so the nearer ancestor wins.
    root_sel = f':root[data-brand="{tid}"]'
    sel = f'{root_sel}, [data-brand="{tid}"]'
    parts = [f"""/* ============================================================
   {meta.get('name', tid)} — brand theme for the Banking Experience System
   GENERATED from tokens/themes/{path.name} — do not edit by hand.

   {meta.get('note', '')}

   This file is TOKEN VALUES ONLY: {total} variables, no selectors of its own
   beyond the brand scope, no properties, no rules. That is doc 30's contract —
   if a brand needed a rule, the gap would be in the system, not the theme.
   Apply with <html data-brand="{tid}"> for a whole product, or on any element
   to brand a subtree — the two columns of brand-proof.html are one page.
   Generated {datetime.date.today()}.
   ============================================================ */"""]

    body = []
    if d_prim:
        body.append("  /* primitives — the brand palette, type stack, shape and motion */\n" + block(d_prim))
    if d_light:
        body.append("  /* semantic overrides — light */\n" + block(d_light))
    if d_type:
        body.append("  /* type scale */\n" + block(d_type))
    if d_dens["standard"]:
        body.append("  /* density — standard */\n" + block(d_dens["standard"]))
    if d_comp:
        body.append("  /* component tier */\n" + block(d_comp))
    parts.append(sel + " {\n" + "\n\n".join(body) + "\n}")

    if d_dark:
        dark_sel = (f'{root_sel}:not([data-theme="light"]), '
                    f':root:not([data-theme="light"]) [data-brand="{tid}"]')
        parts.append("@media (prefers-color-scheme: dark) {\n"
                     f"  {dark_sel} {{\n" + block(d_dark, "    ") + "\n  }\n}")
        parts.append(f'{root_sel}[data-theme="dark"], :root[data-theme="dark"] [data-brand="{tid}"] {{\n'
                     + block(d_dark) + "\n}")
    for mode in ("comfortable", "compact"):
        if d_dens[mode]:
            parts.append(f'{root_sel}[data-density="{mode}"], '
                         f':root[data-density="{mode}"] [data-brand="{tid}"] {{\n'
                         + block(d_dens[mode]) + "\n}")
    if d_ar:
        parts.append(f"/* Arabic optical metrics for the brand's own scale */\n"
                     f'[data-brand="{tid}"]:lang(ar), [data-brand="{tid}"] :lang(ar) {{\n'
                     + block(d_ar) + "\n}")

    OUTDIR.mkdir(parents=True, exist_ok=True)
    (OUTDIR / f"{tid}.css").write_text("\n\n".join(parts) + "\n")
    return tid, OUTDIR / f"{tid}.css", [], total


def main():
    wanted = sys.argv[1:]
    files = sorted((HERE / "themes").glob("*.json"))
    if wanted:
        files = [f for f in files if f.stem in wanted]
    if not files:
        print("no themes found in tokens/themes/")
        return 0
    failed = False
    for f in files:
        tid, out, errors, total = compile_theme(f)
        if errors:
            failed = True
            print(f"THEME BUILD FAILED — {tid}:")
            for e in errors:
                print("  ✗", e)
        else:
            print(f"wrote themes/{tid}.css: {total} token overrides, 0 rules, validated OK")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
