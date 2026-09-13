#!/usr/bin/env python3
"""Shared token emission — used by build-tokens.py (core) and build-theme.py (brands).

One implementation, so a brand theme can never be compiled by different rules than
the core it overrides. Everything here is pure: give it a token dict, get back the
CSS variable blocks and any validation errors.
"""
import re

REF = re.compile(r"\{(\w+)\.(\w+)\}")
REF_ANY = re.compile(r"\{([\w.]+)\}")
MODES = ("comfortable", "standard", "compact")


def emit_all(T):
    """Return (blocks, errors). blocks is a dict of name -> [(var, value), ...]."""
    P = T["primitive"]
    errors = []

    def prim_var(g, k):
        return f"--bes-{g}-{k}"

    def emit_value(v, ctx):
        """Primitive refs emit as var() chains — that is the theming cascade:
        override a primitive once and every semantic token following it moves."""
        m = REF.fullmatch(str(v))
        if m:
            g, k = m.group(1), m.group(2)
            if g in P and k in P[g]:
                return f"var({prim_var(g, k)})"
            errors.append(f"{ctx}: unresolvable reference {v!r}")
        elif "{" in str(v):
            errors.append(f"{ctx}: malformed reference {v!r}")
        return v

    # -- primitives: every group, no hardcoded list --
    prim = []
    for grp, obj in P.items():
        for k, v in obj.items():
            if str(k).startswith("$"):
                continue
            prim.append((prim_var(grp, k), v))

    # -- semantic: light/dark both required, emitted as var() chains --
    sem_light, sem_dark = [], []

    def walk_sem(prefix, obj):
        for k, v in obj.items():
            if str(k).startswith("$"):
                continue
            name = f"--bes-{prefix}-{k}"
            if isinstance(v, dict) and ("light" in v or "dark" in v):
                ctx = f"semantic.{prefix}.{k}"
                if "light" not in v:
                    errors.append(f"{ctx}: missing light value")
                if "dark" not in v:
                    errors.append(f"{ctx}: missing dark value")
                if "light" in v:
                    sem_light.append((name, emit_value(v["light"], ctx)))
                if "dark" in v:
                    sem_dark.append((name, emit_value(v["dark"], ctx)))
            elif isinstance(v, dict):
                walk_sem(f"{prefix}-{k}", v)
            else:
                sem_light.append((name, emit_value(v, f"semantic.{prefix}.{k}")))

    for grp, obj in T["semantic"].items():
        walk_sem(grp, obj)

    # -- density: all keys, all three modes required --
    dens = {m: [] for m in MODES}
    for k, v in T["density"].items():
        if str(k).startswith("$"):
            continue
        for m in MODES:
            if m not in v:
                errors.append(f"density.{k}: missing mode '{m}'")
                continue
            dens[m].append((f"--bes-density-{k}", v[m]))

    # -- type scale + Arabic optical metrics --
    typ, ar = [], []
    for k, v in T["type"].items():
        if str(k).startswith("$"):
            continue
        typ += [(f"--bes-type-{k}-size", v["size"]),
                (f"--bes-type-{k}-line", v["line"]),
                (f"--bes-type-{k}-weight", v["weight"])]
        if "arSize" in v:
            ar += [(f"--bes-type-{k}-size", v["arSize"]),
                   (f"--bes-type-{k}-line", v["arLine"])]

    # -- component tier: may reference anything emitted above it --
    known = {n for n, _ in prim} | {n for n, _ in sem_light} \
        | {n for n, _ in dens["standard"]} | {n for n, _ in typ}
    comp = []

    def emit_component(v, ctx):
        m = REF_ANY.fullmatch(str(v).strip())
        if not m:
            if "{" in str(v):
                errors.append(f"{ctx}: malformed reference {v!r}")
            return v
        name = "--bes-" + m.group(1).replace(".", "-")
        if name not in known:
            errors.append(f"{ctx}: unresolvable reference {v!r} (no {name})")
        return f"var({name})"

    def walk_comp(prefix, obj):
        for k, v in obj.items():
            if str(k).startswith("$"):
                continue
            if isinstance(v, dict):
                walk_comp(f"{prefix}-{k}", v)
            else:
                comp.append((f"--bes-{prefix}-{k}",
                             emit_component(v, f"component.{prefix}.{k}")))

    for grp, obj in T.get("component", {}).items():
        if str(grp).startswith("$"):
            continue
        walk_comp(grp, obj)

    return ({"prim": prim, "sem_light": sem_light, "sem_dark": sem_dark,
             "dens": dens, "type": typ, "ar": ar, "comp": comp}, errors)


def block(pairs, indent="  "):
    return "\n".join(f"{indent}{n}: {v};" for n, v in pairs)
