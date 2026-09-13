#!/usr/bin/env python3
"""A small CSS/HTML model shared by the audits.

Enough of a cascade to answer one question honestly: for each element that actually
exists in the shipped HTML, what foreground and background colour does it end up with,
in each scheme? That is the question a hand-written pairing list cannot answer, and the
question that would have caught the 1.00:1 toast in v1.0.1.

What it models: selector matching (tag, class, id, attribute, descendant/child),
specificity, source order, scheme-scoped rules (`@media (prefers-color-scheme: dark)`,
`[data-theme]`), var() resolution through the token chain, and background inheritance
up the ancestor chain.

What it does not model: shorthand expansion beyond `background`, `!important`,
cascade layers, computed opacity, gradients, `rgba()` compositing. Those are counted
and reported as unscored rather than silently dropped — the tool never pretends to
know a colour it could not resolve.
"""
import re
from html.parser import HTMLParser
from collections import defaultdict

HEX = re.compile(r"^#[0-9A-Fa-f]{3,8}$")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link",
        "meta", "param", "source", "track", "wbr"}


def strip_comments(css):
    return re.sub(r"/\*.*?\*/", lambda m: "\n" * m.group(0).count("\n"), css, flags=re.S)


# ---------------------------------------------------------------- tokens

def build_var_maps(tokens_css):
    """--bes-* → flat hex, per scheme, following var() chains."""
    css = strip_comments(tokens_css)
    raw = {"light": {}, "dark": {}}
    depth, dark_at, block = 0, None, None
    for line in css.split("\n"):
        if re.search(r"@media[^{]*prefers-color-scheme\s*:\s*dark", line):
            dark_at = depth
        if re.match(r"\s*:root\b", line):
            block = "dark" if ('[data-theme="dark"]' in line or dark_at is not None) else "light"
        for name, value in re.findall(r"(--bes-[\w-]+)\s*:\s*([^;]+);", line):
            if block:
                raw[block][name] = value.strip()
        depth += line.count("{") - line.count("}")
        if dark_at is not None and depth <= dark_at:
            dark_at = None
        if depth == 0:
            block = None
    merged = {"light": dict(raw["light"]), "dark": {**raw["light"], **raw["dark"]}}

    def deref(value, scheme, seen=()):
        if value is None:
            return None
        value = value.strip()
        if HEX.match(value):
            return value[:7]
        m = re.fullmatch(r"var\((--bes-[\w-]+)(?:\s*,\s*(.+))?\)", value)
        if not m:
            return None
        name, fallback = m.group(1), m.group(2)
        if name in seen:
            return None
        if name in merged[scheme]:
            got = deref(merged[scheme][name], scheme, seen + (name,))
            if got:
                return got
        return deref(fallback, scheme, seen + (name,)) if fallback else None

    return merged, deref


# ---------------------------------------------------------------- selectors

COMPOUND = re.compile(r"""
    (?P<tag>^[a-zA-Z][\w-]*)
  | \#(?P<id>[\w-]+)
  | \.(?P<cls>[\w-]+)
  | \[(?P<attr>[\w-]+)(?:(?P<op>[~^|$*]?=)"?(?P<val>[^\]"]*)"?)?\]
  | ::(?P<pel>[\w-]+)
  | :(?P<pcl>[\w-]+)(?:\((?P<arg>[^()]*)\))?
""", re.X)

STATE_PSEUDO = {"hover", "focus", "focus-visible", "focus-within", "active", "target"}
DISABLED_PSEUDO = {"disabled"}
STRUCTURAL_PSEUDO = {"first-child", "last-child", "only-child", "nth-child",
                     "first-of-type", "last-of-type", "checked", "not", "is",
                     "where", "has", "lang", "root", "empty", "default", "indeterminate"}


class Compound:
    __slots__ = ("tag", "id", "classes", "attrs", "pseudo_el", "states",
                 "disabled", "unsupported")

    def __init__(self, text):
        self.tag = None
        self.id = None
        self.classes = set()
        self.attrs = []          # (name, op, value)
        self.pseudo_el = None
        self.states = set()
        self.disabled = False
        self.unsupported = False
        pos = 0
        for m in COMPOUND.finditer(text):
            if m.start() != pos:
                self.unsupported = True
            pos = m.end()
            if m.group("tag"):
                self.tag = m.group("tag").lower()
            elif m.group("id"):
                self.id = m.group("id")
            elif m.group("cls"):
                self.classes.add(m.group("cls"))
            elif m.group("attr"):
                name, val = m.group("attr"), m.group("val")
                self.attrs.append((name, m.group("op"), val))
                # WCAG 1.4.3 exempts disabled controls however the state is expressed;
                # bes.js marks non-focusable days with aria-disabled, not the property
                if name == "disabled" or (name == "aria-disabled" and val == "true"):
                    self.disabled = True
            elif m.group("pel"):
                self.pseudo_el = m.group("pel")
            elif m.group("pcl"):
                p = m.group("pcl")
                if p in STATE_PSEUDO:
                    self.states.add(p)
                elif p in DISABLED_PSEUDO:
                    self.disabled = True
                elif p not in STRUCTURAL_PSEUDO:
                    self.unsupported = True
        if pos != len(text):
            self.unsupported = True

    def matches(self, el):
        if self.tag and el.tag != self.tag:
            return False
        if self.id and el.attrs.get("id") != self.id:
            return False
        if not self.classes <= el.classes:
            return False
        for name, op, val in self.attrs:
            if name not in el.attrs:
                return False
            if op == "=" and el.attrs[name] != val:
                return False
            if op == "~=" and val not in el.attrs[name].split():
                return False
        return True

    @property
    def specificity(self):
        return (1 if self.id else 0,
                len(self.classes) + len(self.attrs) + len(self.states) + (1 if self.disabled else 0),
                (1 if self.tag else 0) + (1 if self.pseudo_el else 0))


class Selector:
    def __init__(self, text):
        self.text = text.strip()
        self.compounds = []
        self.unsupported = False
        parts = re.split(r"\s*([>+~])\s*|\s+", self.text)
        parts = [p for p in parts if p and p not in (">", "+", "~")]
        if not parts:
            self.unsupported = True
            return
        for p in parts:
            c = Compound(p)
            if c.unsupported:
                self.unsupported = True
            self.compounds.append(c)

    @property
    def subject(self):
        return self.compounds[-1] if self.compounds else None

    @property
    def specificity(self):
        a = b = c = 0
        for comp in self.compounds:
            x, y, z = comp.specificity
            a, b, c = a + x, b + y, c + z
        return (a, b, c)

    def matches(self, el):
        """Descendant matching, rightmost first. Combinators are treated as
        descendant — a deliberate over-match: it can only widen what is scored."""
        if self.unsupported or not self.compounds:
            return False
        if not self.compounds[-1].matches(el):
            return False
        remaining = self.compounds[:-1]
        node = el.parent
        while remaining and node is not None:
            if remaining[-1].matches(node):
                remaining = remaining[:-1]
            node = node.parent
        return not remaining


# ---------------------------------------------------------------- stylesheet

THEME_DARK = re.compile(r'\[data-theme="dark"\]')
THEME_NOT_LIGHT = re.compile(r':not\(\[data-theme="light"\]\)')
RULE = re.compile(r"([^{}]+)\{([^{}]*)\}")


class Rule:
    __slots__ = ("selector", "decls", "schemes", "line", "source", "order")

    def __init__(self, selector, decls, schemes, line, source, order):
        self.selector = selector
        self.decls = decls
        self.schemes = schemes
        self.line = line
        self.source = source
        self.order = order

    @property
    def sort_key(self):
        return (self.selector.specificity, self.order)


def parse_stylesheet(css_text, source, start_order=0):
    css = strip_comments(css_text)
    line_starts = [0]
    for ln in css.split("\n"):
        line_starts.append(line_starts[-1] + len(ln) + 1)

    def line_of(pos):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if line_starts[mid] <= pos:
                lo = mid + 1
            else:
                hi = mid
        return lo

    # spans of @media (prefers-color-scheme: dark)
    dark_spans, depth, start = [], 0, None
    for m in re.finditer(r"@media[^{]*\{|\{|\}", css):
        tok = m.group(0)
        if tok.startswith("@media"):
            if start is None and re.search(r"prefers-color-scheme\s*:\s*dark", tok):
                start, depth = m.start(), 1
            elif start is not None:
                depth += 1
        elif tok == "{":
            if start is not None:
                depth += 1
        else:
            if start is not None:
                depth -= 1
                if depth == 0:
                    dark_spans.append((start, m.end()))
                    start = None

    def in_dark(pos):
        return any(a <= pos < b for a, b in dark_spans)

    rules, order, unsupported = [], start_order, 0
    for m in RULE.finditer(css):
        sel_raw, body = m.group(1).strip(), m.group(2)
        if not sel_raw or sel_raw.startswith("@"):
            continue
        decls = {}
        for prop, val in re.findall(r"([-\w]+)\s*:\s*([^;]+)", body):
            decls[prop.strip().lower()] = val.strip()
        if not decls:
            continue
        for sel_text in sel_raw.split(","):
            sel_text = sel_text.strip()
            if not sel_text or sel_text.startswith(":root") and len(sel_text.split()) == 1:
                continue
            sel = Selector(sel_text)
            if sel.unsupported:
                unsupported += 1
                continue
            if in_dark(m.start()) or THEME_DARK.search(sel_text):
                schemes = ("dark",)
            else:
                # includes :root:not([data-theme="light"]) outside the media query,
                # which really does apply to the default un-stamped document
                schemes = ("light", "dark")
            order += 1
            rules.append(Rule(sel, decls, schemes, line_of(m.start(1)), source, order))
    return rules, order, unsupported


# ---------------------------------------------------------------- HTML

class El:
    __slots__ = ("tag", "attrs", "classes", "parent", "children", "line")

    def __init__(self, tag, attrs, parent, line):
        self.tag = tag
        self.attrs = attrs
        self.classes = set((attrs.get("class") or "").split())
        self.parent = parent
        self.children = []
        self.line = line


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = El("#document", {}, None, 0)
        self.stack = [self.root]
        self.elements = []

    def handle_starttag(self, tag, attrs):
        el = El(tag, {k: (v or "") for k, v in attrs}, self.stack[-1], self.getpos()[0])
        self.stack[-1].children.append(el)
        self.elements.append(el)
        if tag not in VOID:
            self.stack.append(el)

    def handle_startendtag(self, tag, attrs):
        el = El(tag, {k: (v or "") for k, v in attrs}, self.stack[-1], self.getpos()[0])
        self.stack[-1].children.append(el)
        self.elements.append(el)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return


def parse_html(text):
    tb = TreeBuilder()
    try:
        tb.feed(text)
    except Exception:
        pass
    return tb.elements
