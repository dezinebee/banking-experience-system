/* BES gallery: auto code extraction + preview controls */
(function () {
  "use strict";
  // Extract each .demo's markup into its sibling <pre><code>
  function esc(s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;"); }
  function dedent(html) {
    var lines = html.replace(/^\n+|\s+$/g, "").split("\n");
    var indents = lines.filter(function (l) { return l.trim(); })
      .map(function (l) { return l.match(/^\s*/)[0].length; });
    var min = Math.min.apply(null, indents.length ? indents : [0]);
    return lines.map(function (l) { return l.slice(min); }).join("\n");
  }
  document.querySelectorAll(".ex").forEach(function (ex) {
    var demo = ex.querySelector(".demo");
    var code = ex.querySelector("pre code");
    if (demo && code && !code.textContent.trim()) {
      code.innerHTML = esc(dedent(demo.innerHTML));
    }
  });

  // Preview controls (theme / direction / density)
  function bindSet(id, fn) {
    var set = document.getElementById(id);
    if (!set) return;
    set.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        set.querySelectorAll("button").forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        fn(b.dataset.v);
      });
    });
  }
  if (!window.BES) return;
  bindSet("ctl-theme", function (v) { BES.setTheme(v); });
  bindSet("ctl-density", function (v) { BES.setDensity(v); });
  bindSet("ctl-dir", function (v) {
    // Direction preview applies to demo canvases only (page chrome stays LTR English)
    document.querySelectorAll(".ex .demo").forEach(function (d) {
      d.setAttribute("dir", v);
      d.setAttribute("lang", v === "rtl" ? "ar" : "en");
    });
  });
})();

/* Declarative charts for doc-page demos: data-bes-chart='{"type":"bar","data":[...],"opts":{...}}' */
(function () {
  if (!window.BES) return;
  document.querySelectorAll("[data-bes-chart]").forEach(function (el) {
    try {
      var cfg = JSON.parse(el.getAttribute("data-bes-chart"));
      var fn = { bar: BES.chartBar, line: BES.chartLine, donut: BES.chartDonut }[cfg.type];
      if (fn) fn(el, cfg.data, cfg.opts || {});
    } catch (e) { /* leave empty container */ }
  });
})();
