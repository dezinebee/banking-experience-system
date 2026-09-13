#!/usr/bin/env python3
"""System-consistency audit: catches drift between tokens, component CSS,
JS, and the demos/docs that consume them.
Checks:
  C1  var(--bes-*) referenced anywhere but not defined in tokens.css
  C2  tokens defined in tokens.css but never referenced (informational)
  C3  physical left/right properties in bes.css (logical-only rule)
  C4  raw hex colors in bes.css outside the whitelisted blocks
  C5  bes-* classes used in HTML but absent from bes.css
  C6  bes-* classes defined in bes.css but never used anywhere (informational)
  C7  :root:not([data-theme="light"]) rules outside a prefers-color-scheme: dark block
  C8  hardcoded px: font-size/radius must be zero; spacing is ratcheted
  C9  every version string agrees with tokens.json $meta.version
Exit 1 on C1/C3/C4/C5/C7/C8/C9 errors; C2/C6 are warnings."""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent

tokens_css = (ROOT/"assets"/"tokens.css").read_text()
bes_css = (ROOT/"assets"/"bes.css").read_text()
defined_vars = set(re.findall(r"(--bes-[\w-]+)\s*:", tokens_css))

html_files = list(ROOT.glob("*.html")) + list(ROOT.glob("pages/*.html")) + list(ROOT.glob("components/*.html"))
all_css = bes_css + (ROOT/"assets"/"site.css").read_text() + (ROOT/"assets"/"gallery.css").read_text()
all_js  = (ROOT/"assets"/"bes.js").read_text() + (ROOT/"assets"/"gallery.js").read_text()
all_html = "".join(f.read_text() for f in html_files)

errors, warnings = [], []

# C1 undefined vars
used_vars = set(re.findall(r"var\((--bes-[\w-]+)", all_css + all_js + all_html + tokens_css))
for v in sorted(used_vars - defined_vars):
    # fallback-tolerant: var(--x, fallback) counts as soft, still flag
    errors.append(f"C1 undefined token referenced: {v}")

# C2 unused tokens (informational)
unused = sorted(v for v in defined_vars if v not in used_vars)
if unused:
    warnings.append(f"C2 {len(unused)} tokens defined but unreferenced (ok if reserved): " + ", ".join(unused[:12]) + (" …" if len(unused)>12 else ""))

# C3 physical properties in bes.css
for i, line in enumerate(bes_css.split("\n"), 1):
    if re.search(r"(?<![-\w])(margin|padding|border)-(left|right)\s*:", line) or \
       re.search(r"(?<![-\w])(left|right)\s*:", line) or \
       re.search(r"text-align\s*:\s*(left|right)\b", line):
        errors.append(f"C3 physical property in bes.css:{i}: {line.strip()[:80]}")

# C4 raw colour in bes.css. The card-art whitelist is gone: the card face used to
# be the one place a literal was tolerated, and it is now fully tokenised
# (cardArt.from/to/ink/badgeBg/frozenBg), so component CSS carries no raw colour
# at all and a brand can restyle the card without editing a rule.
for i, line in enumerate(bes_css.split("\n"), 1):
    if line.strip().startswith("/*"): continue
    for lit in re.findall(r"#[0-9A-Fa-f]{3,8}\b", line) + re.findall(r"rgba?\([\d.,\s]+\)", line):
        errors.append(f"C4 raw colour in bes.css:{i}: {lit} — use a token")

# C5 classes used but not defined
defined_classes = set(re.findall(r"\.(bes-[\w-]+)", all_css))
used_classes = set(re.findall(r'class="([^"]+)"', all_html))
used_bes = set()
for cl in used_classes:
    for c in cl.split():
        if c.startswith("bes-"): used_bes.add(c)
# classes referenced from JS: classList ops, className assignments, and class= inside
# template strings. A literal that is being concatenated — classList.add("bes-badge--" + name)
# — is a prefix, not a class; counting it produced a phantom ".bes-badge--".
for m in re.findall(r'classList\.(?:add|remove|toggle|contains)\(\s*["\'](bes-[\w-]+)["\']\s*(\+?)', all_js):
    if m[1] != "+":
        used_bes.add(m[0])
for m in re.findall(r'className\s*=\s*["\']([^"\']+)["\']', all_js):
    for c in m.split():
        if c.startswith("bes-"): used_bes.add(c)
for m in re.findall(r'class=\\?["\']([^"\'\\]+)', all_js):
    for c in m.split():
        if c.startswith("bes-"): used_bes.add(c)
for c in sorted(used_bes - defined_classes):
    errors.append(f"C5 class used but not in bes.css: .{c}")

# C6 defined but unused (informational)
never_used = sorted(defined_classes - used_bes)
if never_used:
    warnings.append(f"C6 {len(never_used)} classes defined but not used in site/demos (ok if library-only): " + ", ".join("."+c for c in never_used[:15]) + (" …" if len(never_used)>15 else ""))

# C7 system-preference branch must be guarded by the media query.
# Unguarded, :root:not([data-theme="light"]) also matches the default un-stamped
# document — which is what every page ships — so a dark-mode override silently
# applies in light mode. This shipped as a 1.00:1 toast in v1.0.1.
for css_name in ("bes.css", "site.css", "gallery.css", "tokens.css"):
    text = (ROOT/"assets"/css_name).read_text()
    # blank out comments, preserving line numbers
    text = re.sub(r"/\*.*?\*/", lambda m: "\n"*m.group(0).count("\n"), text, flags=re.S)
    depth, dark_at = 0, None
    for i, line in enumerate(text.split("\n"), 1):
        stripped = line.strip()
        if re.search(r"@media[^{]*prefers-color-scheme\s*:\s*dark", line):
            dark_at = depth
        opens, closes = line.count("{"), line.count("}")
        if 'not([data-theme="light"])' in line and dark_at is None:
            errors.append(f'C7 unguarded system-dark rule in {css_name}:{i}: '
                          f'{stripped[:70]} — wrap in @media (prefers-color-scheme: dark)')
        depth += opens - closes
        if dark_at is not None and depth <= dark_at:
            dark_at = None

# C8 hardcoded px where a token exists.
#
# font-size and border-radius are now RETIRED to zero: every one of the 93 font
# sizes reads the type scale (or a component token) and every radius reads the
# component tier, so a brand can retune type and silhouette without touching
# component CSS — which is doc 30's acceptance test. They stay at zero: a new
# literal is an error, not a note.
#
# Spacing is still a ratchet. Retiring it needs a decision the type scale did not:
# the space scale is a 4px grid and the CSS uses 6/10/14/18px throughout, so
# retiring it means either widening the scale to 2px steps or restyling. That is
# a design decision, not a mechanical substitution, so the number stays visible
# and may only fall.
ZERO = {"font-size": r"font-size:\s*([\d.]+)px",
        "border-radius": r"border-radius:\s*([\d.]+)px"}
BASELINE = {"spacing": 135}

bes_nc = re.sub(r"/\*.*?\*/", "", bes_css, flags=re.S)   # no comments
for what, pattern in ZERO.items():
    found = re.findall(pattern, bes_nc)
    if found:
        errors.append(
            f"C8 {len(found)} hardcoded {what} literal(s) in bes.css ({', '.join(sorted(set(found))[:6])}px). "
            f"This property is fully tokenised — use the type scale or a component token.")

px_space = [m for m in re.findall(
    r"(?:^|[;{\s])(?:padding|margin|gap|row-gap|column-gap|inset)(?:-(?:block|inline)"
    r"(?:-(?:start|end))?)?\s*:\s*([^;}]+)", bes_nc)
    if re.search(r"\d+px", m) and "var(" not in m]
n = len(px_space)
if n > BASELINE["spacing"]:
    errors.append(
        f"C8 hardcoded spacing literals in bes.css went UP: {n} (baseline {BASELINE['spacing']}). "
        f"Use a space token, or lower the baseline in tools/audit-consistency.py with the "
        f"reduction in the same commit.")
elif n < BASELINE["spacing"]:
    warnings.append(
        f"C8 hardcoded spacing literals down to {n} (baseline {BASELINE['spacing']}) — "
        f"lower BASELINE['spacing'] to {n} to lock the gain in.")

# C9 version agreement. tokens.json $meta.version is the single source; the doc
# subtitles, the generated footers and package.json all restate it. They drifted
# once already — the site claimed "v1.0 Draft" in 60 places while package.json
# said 2.0.0 — so the agreement is now a gate rather than a habit.
import json as _json
VERSION = _json.loads((ROOT/"tokens"/"tokens.json").read_text())["$meta"]["version"]
if _json.loads((ROOT/"package.json").read_text())["version"] != VERSION:
    errors.append(f"C9 package.json version != tokens.json $meta.version ({VERSION})")

_semver = re.compile(r"v?(\d+\.\d+(?:\.\d+)?(?:[-.][0-9A-Za-z.]+)?)")
# Every doc, not just system/ and strategy/ — figma-build-spec.md sat outside
# those two folders and kept claiming v1.0 with nothing to catch it. Generated
# reports under audits/ restate findings from older releases as history, so they
# are excluded; everything else states the current version.
_docs = [p for p in sorted(ROOT.glob("docs/**/*.md"))
         if "audits" not in p.relative_to(ROOT).parts]
for md in _docs:
    # the version lives in the title block: first 6 lines, on a line that names the system
    for i, line in enumerate(md.read_text().split("\n")[:6], 1):
        if "Banking Experience System" not in line and not line.startswith("Version"):
            continue
        for found in _semver.findall(line):
            if found != VERSION:
                errors.append(f"C9 {md.relative_to(ROOT)}:{i} says v{found}, expected v{VERSION}")

# The shipped library's own headers. These are what a consumer reads after
# downloading the release zip, so they have to name the version they are.
for asset in ("assets/bes.css", "assets/bes.js", "assets/tokens.css"):
    head = "\n".join((ROOT/asset).read_text().split("\n")[:6])
    for line in head.split("\n"):
        # "v1.0.1: scrutiny fixes …" is history, not a version claim; only the
        # title line (the one naming the system) states the current version.
        if "Banking Experience System" not in line:
            continue
        for found in _semver.findall(line):
            if found != VERSION:
                errors.append(f"C9 {asset} header says v{found}, expected v{VERSION}")

for page in sorted(ROOT.glob("pages/*.html")):
    for foot in re.findall(r'<footer class="site">.*?</footer>', page.read_text(), re.S):
        for found in _semver.findall(foot):
            if found != VERSION:
                errors.append(f"C9 {page.relative_to(ROOT)} footer says v{found}, expected v{VERSION}")

out = ROOT/"docs"/"audits"/"consistency-report.md"
lines = ["# Consistency Audit", "",
         f"**Result:** {'✅ PASS' if not errors else f'❌ {len(errors)} errors'} · {len(warnings)} informational notes", ""]
for e in errors: lines.append(f"- ❌ {e}")
for w in warnings: lines.append(f"- ℹ️ {w}")
out.write_text("\n".join(lines))
print(f"{len(errors)} errors, {len(warnings)} notes -> docs/audits/consistency-report.md")
for e in errors[:40]: print("ERR", e)
for w in warnings: print("NOTE", w[:200])
sys.exit(1 if errors else 0)
