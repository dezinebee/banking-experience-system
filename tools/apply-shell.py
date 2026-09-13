#!/usr/bin/env python3
"""Wrap showcase, journey and gallery pages in the same shell (topbar + sidebar + main)
that docs pages use. Idempotent: re-running replaces the generated topbar/sidebar."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from sitenav import build_sidenav, build_topbar, build_status_banner

ROOT = pathlib.Path(__file__).resolve().parent.parent

def wrap(path, prefix, section, active):
    p = ROOT / path
    s = p.read_text()
    topbar = build_topbar(prefix, section) + "\n</div>"
    nav = f'<nav class="side" aria-label="Site">\n{build_sidenav(prefix, active)}\n</nav>'
    # replace existing topbar (with or without menu-btn)
    s = re.sub(r'<div class="topbar">.*?</div>\n(?:  <a class="pill.*?\n)*(?:  <button id="langBtn".*?\n)?</div>',
               "@@TOPBAR@@", s, count=1, flags=re.S)
    if "@@TOPBAR@@" not in s:  # fallback: topbar as a single balanced block on one nesting level
        s = re.sub(r'<div class="topbar">(?:[^<]|<(?!/div>)|</(?!div>))*?</div>', "@@TOPBAR@@", s, count=1, flags=re.S)
    if "@@TOPBAR@@" not in s:
        raise SystemExit(f"{path}: topbar not found")
    # The topbar is the same four pills on every page. Page-level controls — the
    # language toggle on the bilingual pages — live in the page, not up here.
    # Draft status strip, same one build-docs.py puts on the generated pages.
    # Drop any existing strip first, then emit it with the topbar in one
    # substitution — the topbar contains a <div class="spacer"></div>, so
    # searching for its closing tag would find the spacer's instead.
    s = re.sub(r'\s*<div class="statusbar"[^>]*>.*?</div>', "", s, count=1, flags=re.S)
    s = s.replace("@@TOPBAR@@", topbar + "\n" + build_status_banner(prefix))
    if 'class="shell"' in s:
        if '<nav class="side"' in s:
            # already wrapped: just refresh the nav
            s = re.sub(r'<nav class="side"[^>]*>.*?</nav>', nav, s, count=1, flags=re.S)
        else:
            # shell was hand-written without a sidebar: .shell is a 280px/1fr grid,
            # so <main> would otherwise render inside the empty 280px nav column.
            s = re.sub(r'(<div class="shell">\s*)',
                       lambda m: m.group(1) + nav + "\n", s, count=1)
    else:
        # open shell right after topbar, close before first bottom-level <script src=
        s = s.replace("</div>", "</div>\n<div class=\"shell\">\n" + nav + "\n<main>", 1) \
            if s.startswith("<div class=\"topbar\">") else s
        # robust: insert after the (new) topbar close
        idx = s.index("</div>", s.index('<div class="topbar">')) + len("</div>")
        s = s[:idx] + "\n<div class=\"shell\">\n" + nav + "\n<main>" + s[idx:]
        # close before trailing scripts / body end
        m = re.search(r'\n(<script src="[^"]*bes\.js">)', s)
        close_at = m.start() if m else s.rindex("</body>")
        s = s[:close_at] + "\n</main>\n</div>" + s[close_at:]
    p.write_text(s)
    print("shelled:", path)

wrap("showcase.html", "", "showcase", "showcase")
wrap("journey-remittance.html", "", "journey", "journey")
wrap("brand-proof.html", "", None, "brand-proof")
for slug in ["index","actions","forms","money","transactions","patterns","advanced"]:
    wrap(f"components/{slug}.html", "../", "components", f"gallery:{slug}")
print("done")
