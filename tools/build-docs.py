#!/usr/bin/env python3
"""BES docs-site generator: docs/*.md -> pages/*.html
Run from anywhere: python3 tools/build-docs.py
Embeds live examples (tools/demos.py) into matching pages."""
import markdown, re, html, sys, pathlib

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
from demos import DEMOS, SECTIONS
import json as _json
ASSET_V = _json.loads((pathlib.Path(__file__).resolve().parent.parent/'tokens'/'tokens.json').read_text())['$meta']['version']
from sitenav import (STRAT, SYS, GALLERY, ORDER, MDMAP,
                     build_sidenav, build_topbar, build_status_banner)

PAGES = ROOT / "pages"; PAGES.mkdir(exist_ok=True)



md = markdown.Markdown(extensions=["tables","fenced_code"])

def convert(path, slug):
    text = (ROOT/"docs"/path).read_text(encoding="utf-8")
    md.reset()
    body = md.convert(text)
    body = body.replace("<table>", '<div class="tbl-wrap"><table>').replace("</table>", "</table></div>")
    def rl(m):
        fn = m.group(1).split("/")[-1]
        return 'href="%s.html"' % MDMAP[fn] if fn in MDMAP else m.group(0)
    body = re.sub(r'href="([^"]+\.md)"', rl, body)
    if slug in DEMOS:
        demo = ('<section class="ex ex--doc"><h2 style="border:none;padding-top:0">Live example</h2>'
                '<div class="demo bes">' + DEMOS[slug] + '</div>'
                '<details><summary>Code</summary><pre><code>' + html.escape(DEMOS[slug].strip()) + '</code></pre></details></section>')
        i = body.find("</p>")
        body = body[:i+4] + "\n" + demo + body[i+4:] if i != -1 else demo + body
    if slug in SECTIONS:
        blocks = ""
        for t, h in SECTIONS[slug]:
            blocks += ('<section class="ex ex--doc"><h2 style="border:none;padding-top:0">' + t + '</h2>'
                       '<div class="demo bes">' + h + '</div>'
                       '<details><summary>Code</summary><pre><code>' + html.escape(h.strip()) + '</code></pre></details></section>')
        body += ('<hr/><h2>All components in this family — live</h2>'
                 '<p>Every component from this specification, rendered by the coded library. Expand "Code" to copy the markup.</p>' + blocks)
    return body

TPL = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Banking Experience System</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Arabic:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="../assets/site.css?v={av}">
<link rel="stylesheet" href="../assets/tokens.css?v={av}">
<link rel="stylesheet" href="../assets/bes.css?v={av}">
<link rel="stylesheet" href="../assets/gallery.css?v={av}">
</head>
<body>
{topbar}
</div>
{statusbar}
<div class="shell">
<nav class="side" aria-label="Documentation">
{nav}
</nav>
<main>
<div class="content">
<div class="crumb">{crumb}</div>
{body}
<div class="pgnav">{prev}{next}</div>
</div>
<footer class="site"><span>Banking Experience System · v{av}</span><span>Examples use fictional data</span></footer>
</main>
</div>
<script src="../assets/bes.js?v={av}"></script>
<script src="../assets/gallery.js?v={av}"></script>
</body>
</html>"""

for i, (grp, f, slug, label) in enumerate(ORDER):
    body = convert(f, slug)
    m = re.search(r"<h1>(.*?)</h1>", body)
    title = html.unescape(re.sub(r"<.*?>", "", m.group(1))) if m else label
    prev_l = next_l = ""
    if i > 0:
        _, _, ps, pl = ORDER[i-1]
        prev_l = f'<a href="{ps}.html"><span class="lbl">Previous</span>{html.escape(pl)}</a>'
    if i < len(ORDER)-1:
        _, _, ns, nl = ORDER[i+1]
        next_l = f'<a class="next" href="{ns}.html"><span class="lbl">Next</span>{html.escape(nl)}</a>'
    page = TPL.format(av=ASSET_V, topbar=build_topbar("../", "docs"), statusbar=build_status_banner("../"),
                      title=html.escape(title), nav=build_sidenav("../", slug), crumb=html.escape(grp),
                      body=body, prev=prev_l, next=next_l)
    (PAGES/f"{slug}.html").write_text(page, encoding="utf-8")

# Standalone docs that sit outside ORDER but still belong on the site. Without
# this, figma-build-spec.md was a complete specification that nothing linked to.
for _slug, _src, _title, _crumb in [
    ("figma-build-spec", "figma-build-spec.md", "Figma library spec", "Design assets"),
]:
    _b = md.reset().convert((ROOT/"docs"/_src).read_text(encoding="utf-8"))
    _b = _b.replace("<table>", '<div class="tbl-wrap"><table>').replace("</table>", "</table></div>")
    _b = re.sub(r'href="([^"]+)\.md"', lambda m: f'href="{MDMAP.get(m.group(1).split("/")[-1], m.group(1))}.html"', _b)
    (PAGES/f"{_slug}.html").write_text(
        TPL.format(av=ASSET_V, topbar=build_topbar("../", "docs"), statusbar=build_status_banner("../"),
                   title=html.escape(_title), nav=build_sidenav("../", _slug),
                   crumb=html.escape(_crumb), body=_b, prev="", next=""),
        encoding="utf-8")

# STATUS.md rendered as a real page. The banner on every page points here, and a
# link to raw .md would be served as plain text by GitHub Pages.
_status_md = (ROOT/"STATUS.md").read_text(encoding="utf-8")
_status_body = md.reset().convert(_status_md)
_status_body = _status_body.replace("<table>", '<div class="tbl-wrap"><table>').replace("</table>", "</table></div>")
_status_body = re.sub(r'href="(?!http|#)([^"]*?)\.md"', r'href="../\1.md"', _status_body)
(PAGES/"status.html").write_text(
    TPL.format(av=ASSET_V, topbar=build_topbar("../", "docs"), statusbar=build_status_banner("../"),
               title="Status &amp; verification", nav=build_sidenav("../", "status"),
               crumb="Verification", body=_status_body, prev="", next=""),
    encoding="utf-8")

demo_count = sum(1 for _,_,s,_ in ORDER if s in DEMOS)
print(f"built {len(ORDER)} pages + status.html, {demo_count} with embedded live examples")
unused = set(DEMOS) - {s for _,_,s,_ in ORDER}
if unused: print("WARNING unused demo keys:", unused)
