#!/usr/bin/env python3
"""Static accessibility audit over all BES HTML.
Machine-checkable subset of WCAG 2.2 AA; the human protocols in
docs/testing/ cover what static analysis cannot (screen readers, zoom, AT).
Output: docs/audits/a11y-report.md  Exit 1 on errors (warnings pass)."""
import re, sys, pathlib, datetime
from html.parser import HTMLParser

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = sorted(list(ROOT.glob("*.html")) + list(ROOT.glob("pages/*.html")) + list(ROOT.glob("components/*.html")))

VOID = {"img","input","br","hr","meta","link","area","base","col","embed","source","track","wbr"}

class Auditor(HTMLParser):
    def __init__(self, fname):
        super().__init__(convert_charrefs=True)
        self.f = fname; self.errors = []; self.warnings = []
        self.ids = {}; self.labels_for = set(); self.described = set()
        self.inputs = []  # (id, aria-label, aria-labelledby, type, line)
        self.buttons = [] # (has_text, aria_label, line)
        self.imgs = []
        self.headings = []
        self.lang = None; self.title = False
        self._btn_depth = 0; self._btn_text = False; self._btn_attrs = None; self._btn_line = 0
        self._in_svg = 0; self._label_depth = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs); line = self.getpos()[0]
        if tag == "html": self.lang = a.get("lang")
        if tag == "title": self.title = True
        if "id" in a:
            self.ids.setdefault(a["id"], []).append(line)
        if tag == "label":
            self._label_depth += 1
            if "for" in a: self.labels_for.add(a["for"])
        for key in ("aria-describedby","aria-labelledby","aria-controls"):
            if key in a:
                for ref in a[key].split(): self.described.add((ref, line, key))
        if tag == "svg": self._in_svg += 1
        if tag == "img": self.imgs.append(("alt" in a, line))
        if tag in ("input","select","textarea") and a.get("type") not in ("hidden","submit","button"):
            wrapped = self._label_depth > 0  # implicit association via wrapping <label>
            self.inputs.append((a.get("id"), a.get("aria-label"), a.get("aria-labelledby"), a.get("type","text"), line, wrapped))
        if tag == "button":
            self._btn_depth += 1; self._btn_text = False; self._btn_attrs = a; self._btn_line = line
        if re.fullmatch(r"h[1-6]", tag) and not self._in_svg:
            self.headings.append((int(tag[1]), line))
        if tag == "a" and not a.get("href") and "role" not in a:
            self.warnings.append(f"L{line}: <a> without href")

    def handle_endtag(self, tag):
        if tag == "svg": self._in_svg = max(0, self._in_svg - 1)
        if tag == "label": self._label_depth = max(0, self._label_depth - 1)
        if tag == "button" and self._btn_depth:
            self._btn_depth -= 1
            a = self._btn_attrs or {}
            if not self._btn_text and not a.get("aria-label") and not a.get("aria-labelledby"):
                self.errors.append(f"L{self._btn_line}: button with no accessible name (no text, no aria-label)")

    def handle_data(self, data):
        if self._btn_depth and data.strip(): self._btn_text = True

results = []
total_err = 0
for f in FILES:
    aud = Auditor(f)
    aud.feed(f.read_text(encoding="utf-8"))
    # post checks
    if not aud.lang: aud.errors.append("html element missing lang attribute")
    if not aud.title: aud.errors.append("missing <title>")
    for _id, lines in aud.ids.items():
        if len(lines) > 1: aud.errors.append(f"duplicate id '{_id}' at lines {lines}")
    for ref, line, key in aud.described:
        if ref not in aud.ids: aud.errors.append(f"L{line}: {key} references missing id '{ref}'")
    for iid, al, alb, typ, line, wrapped in aud.inputs:
        if not ((iid and iid in aud.labels_for) or al or alb or wrapped):
            aud.errors.append(f"L{line}: input[type={typ}] has no label association")
    for has_alt, line in aud.imgs:
        if not has_alt: aud.errors.append(f"L{line}: img missing alt")
    # heading order: first heading level ok; no jumps > 1 downward
    prev = 0
    for lvl, line in aud.headings:
        if prev and lvl > prev + 1:
            aud.warnings.append(f"L{line}: heading level jumps h{prev}→h{lvl}")
        prev = lvl
    total_err += len(aud.errors)
    results.append((f.relative_to(ROOT), aud.errors, aud.warnings))

out = ROOT/"docs"/"audits"; out.mkdir(parents=True, exist_ok=True)
lines = ["# Static Accessibility Audit",
 "",
 f"**Generated:** {datetime.date.today()} by `tools/audit-a11y.py` over {len(FILES)} HTML files.",
 "**Checks:** lang attribute, page title, duplicate ids, dangling aria references, unlabeled form controls, unnamed buttons, images without alt, heading-order jumps.",
 "**Out of scope for static analysis** (covered by docs/testing/ human protocols): screen-reader output quality, focus order in practice, 200% zoom reflow, contrast-in-context (see contrast-report.md for token-level), touch-target rendering, RTL visual review.",
 ""]
clean = [str(r[0]) for r in results if not r[1] and not r[2]]
lines.append(f"**Result:** {'✅ 0 errors' if total_err==0 else f'❌ {total_err} errors'} · {sum(len(r[2]) for r in results)} warnings · {len(clean)}/{len(FILES)} files fully clean")
lines.append("")
for path, errs, warns in results:
    if errs or warns:
        lines.append(f"### {path}")
        for e in errs: lines.append(f"- ❌ {e}")
        for w in warns: lines.append(f"- ⚠️ {w}")
        lines.append("")
(out/"a11y-report.md").write_text("\n".join(lines))
print(f"{total_err} errors, {sum(len(r[2]) for r in results)} warnings across {len(FILES)} files -> docs/audits/a11y-report.md")
for path, errs, warns in results:
    for e in errs: print(f"ERR {path}: {e}")
sys.exit(1 if total_err else 0)
