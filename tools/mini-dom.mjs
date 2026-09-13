/* Minimal DOM good enough to bind and drive BES behaviors in Node — no dependencies,
   consistent with the library's own dependency-free stance.

   It exists because the defects that reached v1.0.1 were all in the seam between CSS,
   JS and markup, and a pure-function test suite cannot see that seam: the mask selector
   did not match its own markup, and the currency input never linked its error text to
   the field. Both are structural, and both are caught here.

   Scope is deliberately narrow — element/text nodes, class and attribute access, the
   compound selectors initAll actually uses, and click dispatch. It is a regression
   harness, not a browser: anything depending on layout, innerHTML parsing or real event
   propagation belongs in a browser-based test instead. */

const CAMEL = (s) => s.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
const KEBAB = (s) => s.replace(/[A-Z]/g, (c) => "-" + c.toLowerCase());

class TextNode {
  constructor(text) { this.nodeType = 3; this.data = text; this.parentNode = null; }
  get textContent() { return this.data; }
  set textContent(v) { this.data = String(v); }
}

class Element {
  constructor(tagName) {
    this.nodeType = 1;
    this.tagName = String(tagName).toUpperCase();
    this.childNodes = [];
    this.parentNode = null;
    this.attributes = new Map();
    this._listeners = new Map();
    this.tabIndex = 0;
    const self = this;
    this.dataset = new Proxy({}, {
      get: (_, k) => self.attributes.get("data-" + KEBAB(String(k))),
      set: (_, k, v) => { self.attributes.set("data-" + KEBAB(String(k)), String(v)); return true; },
      has: (_, k) => self.attributes.has("data-" + KEBAB(String(k))),
      deleteProperty: (_, k) => self.attributes.delete("data-" + KEBAB(String(k))),
    });
    this.classList = {
      contains: (c) => self._classes().includes(c),
      add: (c) => { const s = self._classes(); if (!s.includes(c)) { s.push(c); self.className = s.join(" "); } },
      remove: (c) => { self.className = self._classes().filter((x) => x !== c).join(" "); },
      toggle: (c, force) => {
        const on = force === undefined ? !self.classList.contains(c) : !!force;
        on ? self.classList.add(c) : self.classList.remove(c);
        return on;
      },
    };
  }
  _classes() { return (this.className || "").split(/\s+/).filter(Boolean); }
  get className() { return this.attributes.get("class") || ""; }
  set className(v) { this.attributes.set("class", String(v)); }
  get id() { return this.attributes.get("id") || ""; }
  set id(v) { this.attributes.set("id", String(v)); }

  setAttribute(n, v) { this.attributes.set(n, String(v)); }
  getAttribute(n) { return this.attributes.has(n) ? this.attributes.get(n) : null; }
  hasAttribute(n) { return this.attributes.has(n); }
  removeAttribute(n) { this.attributes.delete(n); }

  appendChild(node) {
    if (node.parentNode) node.parentNode.removeChild(node);
    node.parentNode = this;
    this.childNodes.push(node);
    return node;
  }
  insertBefore(node, ref) {
    if (node.parentNode) node.parentNode.removeChild(node);
    node.parentNode = this;
    const i = ref ? this.childNodes.indexOf(ref) : -1;
    i === -1 ? this.childNodes.push(node) : this.childNodes.splice(i, 0, node);
    return node;
  }
  removeChild(node) {
    const i = this.childNodes.indexOf(node);
    if (i !== -1) { this.childNodes.splice(i, 1); node.parentNode = null; }
    return node;
  }

  get textContent() { return this.childNodes.map((n) => n.textContent).join(""); }
  set textContent(v) {
    this.childNodes.forEach((n) => { n.parentNode = null; });
    this.childNodes = [];
    if (v !== "") this.appendChild(new TextNode(String(v)));
  }

  _descendants() {
    const out = [];
    for (const n of this.childNodes) {
      if (n.nodeType !== 1) continue;
      out.push(n, ...n._descendants());
    }
    return out;
  }
  matches(sel) { return parseSelector(sel).every((p) => p(this)); }
  querySelectorAll(sel) {
    const groups = String(sel).split(",").map((s) => s.trim()).filter(Boolean);
    return this._descendants().filter((el) => groups.some((g) => {
      try { return el.matches(g); } catch { return false; }
    }));
  }
  querySelector(sel) { return this.querySelectorAll(sel)[0] || null; }
  closest(sel) {
    let el = this;
    while (el) { if (el.nodeType === 1 && el.matches(sel)) return el; el = el.parentNode; }
    return null;
  }

  addEventListener(type, fn) {
    if (!this._listeners.has(type)) this._listeners.set(type, []);
    this._listeners.get(type).push(fn);
  }
  dispatch(type, event = {}) {
    // no bubbling — behaviors under test bind directly to their own element
    const e = { type, target: this, preventDefault() {}, stopPropagation() {}, ...event };
    (this._listeners.get(type) || []).forEach((fn) => fn.call(this, e));
    return e;
  }
  dispatchEvent(ev) { return this.dispatch(ev.type, ev); }
  click() { return this.dispatch("click"); }
  focus() {}
  setSelectionRange() {}
}

/* Compound selectors only: tag, #id, .class, [attr], [attr="value"].
   That covers every selector initAll passes; anything else throws and is skipped. */
function parseSelector(sel) {
  const parts = [];
  const re = /([.#]?[\w-]+)|\[([\w-]+)(?:=["']?([^\]"']*)["']?)?\]/g;
  let m, consumed = 0;
  while ((m = re.exec(sel))) {
    consumed += m[0].length;
    if (m[1]) {
      const t = m[1];
      if (t[0] === ".") parts.push((el) => el._classes().includes(t.slice(1)));
      else if (t[0] === "#") parts.push((el) => el.id === t.slice(1));
      else parts.push((el) => el.tagName === t.toUpperCase());
    } else {
      const [name, val] = [m[2], m[3]];
      parts.push(val === undefined
        ? (el) => el.hasAttribute(name)
        : (el) => el.getAttribute(name) === val);
    }
  }
  if (consumed !== sel.replace(/\s+/g, "").length) throw new Error("unsupported selector: " + sel);
  return parts;
}

export function createDocument() {
  const byId = new Map();
  const body = new Element("body");
  const documentElement = new Element("html");
  const doc = {
    readyState: "complete",
    body,
    documentElement,
    createElement: (t) => new Element(t),
    createTextNode: (t) => new TextNode(t),
    addEventListener() {},
    getElementById: (id) => body.querySelector(`[id="${id}"]`) || byId.get(id) || null,
    querySelector: (s) => body.querySelector(s),
    querySelectorAll: (s) => body.querySelectorAll(s),
  };
  return doc;
}

export { Element, TextNode };

/* Build a small tree from a compact spec: el("bdi", {id:"x"}, "text", el(...)) */
export function el(tag, attrs = {}, ...children) {
  const node = new Element(tag);
  for (const [k, v] of Object.entries(attrs)) node.setAttribute(k, v);
  for (const c of children) node.appendChild(typeof c === "string" ? new TextNode(c) : c);
  return node;
}
