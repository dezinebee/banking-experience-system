/* ============================================================
   Banking Experience System — behaviors (bes.js) v2.0.0-draft
   Vanilla, dependency-free. Progressive enhancement.
   v1.0.1: scrutiny fixes — XSS-safe interpolation, sign-safe
   money parsing (incl. Arabic separators/extended digits),
   ARIA-complete combobox/datepicker/sort/switch, leak-free
   modal/drawer with real focus traps, double-bind guards,
   live announcements, scoped behaviors.
   ============================================================ */
(function () {
  "use strict";
  var BES = (window.BES = window.BES || {});
  var PRM = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- escaping (all user-derived text MUST pass through) ---------- */
  BES.esc = function (s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;").replace(/'/g, "&#39;");
  };
  // template replace immune to $-pattern semantics
  BES.tpl = function (str, map) {
    return str.replace(/\{(\w+)\}/g, function (_, k) {
      return map[k] != null ? map[k] : "{" + k + "}";
    });
  };

  /* ---------- announcements (single shared live region) ---------- */
  function liveRegion(assertive) {
    var id = assertive ? "bes-live-assertive" : "bes-live-polite";
    var el = document.getElementById(id);
    if (!el) {
      el = document.createElement("div");
      el.id = id;
      el.className = "bes-vh";
      el.setAttribute("role", assertive ? "alert" : "status");
      el.setAttribute("aria-live", assertive ? "assertive" : "polite");
      document.body.appendChild(el);
    }
    return el;
  }
  BES.announce = function (msg, assertive) {
    var el = liveRegion(assertive);
    el.textContent = "";
    // force re-announcement of identical strings
    setTimeout(function () { el.textContent = msg; }, 30);
  };
  if (document.readyState === "loading")
    document.addEventListener("DOMContentLoaded", function () { liveRegion(false); liveRegion(true); });
  else { liveRegion(false); liveRegion(true); }

  /* ---------- theme & direction ---------- */
  BES.setTheme = function (mode) {
    var r = document.documentElement;
    if (mode === "system") r.removeAttribute("data-theme");
    else r.setAttribute("data-theme", mode);
  };
  BES.setDensity = function (mode) {
    var r = document.documentElement;
    if (mode === "standard") r.removeAttribute("data-density");
    else r.setAttribute("data-density", mode);
  };
  BES.setDirection = function (dir, lang) {
    document.documentElement.setAttribute("dir", dir);
    if (lang) document.documentElement.setAttribute("lang", lang);
  };

  /* ================= money =================================================
     Money is a value type, not a number.

     A balance is an exact quantity of minor units — fils, cents, paise — and
     `number` cannot hold one. 0.1 + 0.2 is 0.30000000000000004; 8.165 rounds
     down because its nearest double is 8.16499999999999914734871708787977695465
     Every float amount in a banking UI is a rounding error waiting for a large
     enough number, and the failure mode is silent: a total that is off by a fil
     looks exactly like a total that is right.

     So BES stores an integer count of minor units and does exact integer
     arithmetic. Floats appear in exactly one place — the boundary where a host
     app hands us a `number` — and that conversion goes through the decimal text
     of the float, never its binary value.

     Rounding is never implicit. Any operation that could lose a fil requires a
     named mode; without one it returns an invalid Money rather than a plausible
     wrong answer. Half-even ("banker's") is the financial default where a policy
     must be chosen, because half-up is biased upward over many transactions.

     Rendering goes through Intl.NumberFormat, which is what makes grouping,
     locale separators and Eastern Arabic numerals correct rather than
     hand-rolled. Sign and currency placement stay house rules (doc 13): a true
     minus U+2212, code before the amount, one LTR-isolated run in both
     directions.

     Ceiling: Number.MAX_SAFE_INTEGER minor units — about 90 trillion AED. Above
     that a Money is invalid, never approximate. If a treasury surface ever needs
     more, the representation moves to BigInt and this comment is the reason why.
     ======================================================================== */

  var PRECISION = {           // ISO 4217 minor units; default 2
    JPY: 0, KRW: 0, VND: 0, CLP: 0, ISK: 0,
    KWD: 3, BHD: 3, OMR: 3, TND: 3, JOD: 3, IQD: 3, LYD: 3
  };
  BES.currencyPrecision = function (code) {
    return PRECISION[code] != null ? PRECISION[code] : 2;
  };

  /* ---- rounding modes: exact, on an integer quotient + remainder ----------
     q = trunc(n/d), r = n - q*d, all integers. `neg` is the sign of the true
     quotient. Each mode decides only whether to step the magnitude away from
     zero by one unit. */
  var ROUNDING = {
    "half-even": function (q, r2, d, neg) {          // banker's — unbiased
      if (r2 > d) return 1;
      if (r2 < d) return 0;
      return q % 2 === 0 ? 0 : 1;
    },
    "half-up":   function (q, r2, d) { return r2 >= d ? 1 : 0; },
    "half-down": function (q, r2, d) { return r2 > d ? 1 : 0; },
    "up":        function (q, r2) { return r2 > 0 ? 1 : 0; },      // away from zero
    "down":      function () { return 0; },                        // toward zero
    "ceil":      function (q, r2, d, neg) { return r2 > 0 && !neg ? 1 : 0; },
    "floor":     function (q, r2, d, neg) { return r2 > 0 && neg ? 1 : 0; }
  };
  BES.roundingModes = Object.keys(ROUNDING);

  /* Divide integer `n` by positive integer `d`, rounding per mode. Exact. */
  function divRound(n, d, mode) {
    var fn = ROUNDING[mode];
    if (!fn) return NaN;
    var neg = (n < 0);
    var a = Math.abs(n);
    var q = Math.floor(a / d);
    var r = a - q * d;
    var step = fn(q, r * 2, d, neg);   // compare 2r against d to avoid halves
    var out = q + step;
    return neg ? -out : out;
  }

  /* Split a decimal string into { neg, digits, scale } with no float involved. */
  function decimalParts(str) {
    var m = /^([+−-])?(\d+)(?:\.(\d+))?$/.exec(String(str).trim());
    if (!m) return null;
    var frac = m[3] || "";
    return { neg: m[1] === "-" || m[1] === "−", digits: m[2] + frac, scale: frac.length };
  }

  /* Scale a { digits, scale } to `precision` decimal places, exactly. */
  function toMinor(parts, precision, mode) {
    var digits = parts.digits.replace(/^0+(?=\d)/, "");
    if (parts.scale <= precision) {
      digits += new Array(precision - parts.scale + 1).join("0");
      if (digits.length > 15) return NaN;                 // beyond safe integer
      var v = Number(digits);
      if (!Number.isSafeInteger(v)) return NaN;
      return parts.neg ? -v : v;
    }
    // more decimals than the currency allows — this is where a fil gets lost,
    // so it only proceeds with an explicit mode
    if (!mode) return NaN;
    var fn = ROUNDING[mode];
    if (!fn) return NaN;
    var keep = digits.length - (parts.scale - precision);
    var wholeStr = keep > 0 ? digits.slice(0, keep) : "0";
    var rest = keep > 0 ? digits.slice(keep) : digits;
    if (keep < 0) rest = new Array(-keep + 1).join("0") + rest;
    if (wholeStr.length > 15) return NaN;
    var whole = Number(wholeStr);
    // Decide from the first dropped digit plus a sticky bit for everything after
    // it. Reading the whole tail as one integer would overflow on a long float
    // repr — 0.1 + 0.2 stringifies to 17 decimals — and lose to the very
    // imprecision this type exists to avoid.
    var head = rest.length ? Number(rest.charAt(0)) : 0;
    var sticky = /[1-9]/.test(rest.slice(1)) ? 1 : 0;
    var step = fn(whole, head * 2 + sticky, 10, parts.neg);
    var out = whole + step;
    if (!Number.isSafeInteger(out)) return NaN;
    return parts.neg ? -out : out;
  }

  /* ---- the type ---------------------------------------------------------- */
  function Money(minor, currency, precision) {
    this.minor = minor;
    this.currency = currency;
    this.precision = precision;
  }
  Money.prototype.isValid = function () { return Number.isSafeInteger(this.minor); };
  Money.prototype.isZero = function () { return this.minor === 0; };
  Money.prototype.isNegative = function () { return this.minor < 0; };
  Money.prototype.negate = function () { return new Money(-this.minor, this.currency, this.precision); };
  Money.prototype.abs = function () { return new Money(Math.abs(this.minor), this.currency, this.precision); };

  function sameCurrency(a, b) {
    return a.isValid() && b && b.isValid() && a.currency === b.currency;
  }
  Money.prototype.add = function (other) {
    if (!sameCurrency(this, other)) return new Money(NaN, this.currency, this.precision);
    return new Money(this.minor + other.minor, this.currency, this.precision);
  };
  Money.prototype.subtract = function (other) {
    if (!sameCurrency(this, other)) return new Money(NaN, this.currency, this.precision);
    return new Money(this.minor - other.minor, this.currency, this.precision);
  };
  Money.prototype.compare = function (other) {
    if (!sameCurrency(this, other)) return NaN;
    return this.minor < other.minor ? -1 : this.minor > other.minor ? 1 : 0;
  };
  Money.prototype.equals = function (other) { return this.compare(other) === 0; };

  /* Multiply by a rate or ratio. The factor is taken as decimal text so an FX
     rate of 3.6730 is exactly 36730/10000, not the nearest double. */
  Money.prototype.multiply = function (factor, opts) {
    opts = opts || {};
    var parts = decimalParts(typeof factor === "number" ? String(factor) : factor);
    if (!parts || !this.isValid()) return new Money(NaN, this.currency, this.precision);
    var scale = Math.pow(10, parts.scale);
    var f = Number(parts.digits);
    if (!Number.isSafeInteger(f)) return new Money(NaN, this.currency, this.precision);
    var product = this.minor * f;
    if (!Number.isSafeInteger(product)) return new Money(NaN, this.currency, this.precision);
    if (parts.neg) product = -product;
    var out = parts.scale === 0 ? product : divRound(product, scale, opts.rounding || "half-even");
    return new Money(out, this.currency, this.precision);
  };
  Money.prototype.divide = function (divisor, opts) {
    opts = opts || {};
    var d = Number(divisor);
    if (!this.isValid() || !isFinite(d) || d === 0) return new Money(NaN, this.currency, this.precision);
    var parts = decimalParts(String(Math.abs(d)));
    if (!parts) return new Money(NaN, this.currency, this.precision);
    var scale = Math.pow(10, parts.scale);
    var n = this.minor * scale;
    if (!Number.isSafeInteger(n)) return new Money(NaN, this.currency, this.precision);
    var out = divRound(d < 0 ? -n : n, Number(parts.digits), opts.rounding || "half-even");
    return new Money(out, this.currency, this.precision);
  };

  /* Split into parts whose sum is exactly this amount. Largest-remainder, so
     AED 100.00 across three ways is 33.34 / 33.33 / 33.33 — never 33.33 × 3
     with a fil unaccounted for. Weights default to an even split. */
  Money.prototype.allocate = function (weights) {
    var self = this;
    var ws = [];
    if (Array.isArray(weights)) ws = weights.slice();
    else for (var n = 0; n < weights; n++) ws.push(1);
    if (!this.isValid() || !ws.length) return [];
    var total = ws.reduce(function (a, b) { return a + b; }, 0);
    if (!total) return [];
    var shares = ws.map(function (w) {
      var exact = self.minor * w / total;
      return { floor: Math.floor(exact), rem: exact - Math.floor(exact) };
    });
    var allocated = shares.reduce(function (a, s) { return a + s.floor; }, 0);
    var left = self.minor - allocated;
    var order = shares.map(function (s, i) { return i; })
      .sort(function (a, b) { return shares[b].rem - shares[a].rem; });
    for (var i = 0; i < left; i++) shares[order[i % order.length]].floor += 1;
    return shares.map(function (s) { return new Money(s.floor, self.currency, self.precision); });
  };

  /* Exact decimal text — the wire and comparison form. Never a float. */
  Money.prototype.toMajorString = function () {
    if (!this.isValid()) return "";
    var neg = this.minor < 0;
    var digits = String(Math.abs(this.minor));
    if (this.precision === 0) return (neg ? "-" : "") + digits;
    while (digits.length <= this.precision) digits = "0" + digits;
    var cut = digits.length - this.precision;
    return (neg ? "-" : "") + digits.slice(0, cut) + "." + digits.slice(cut);
  };
  Money.prototype.toJSON = function () {
    return { currency: this.currency, minor: this.minor, precision: this.precision };
  };
  Money.prototype.toString = function () { return this.format(); };
  /* Escape hatch for maths BES does not own (chart geometry, percentages).
     Never round-trip money through this — it is lossy by definition. */
  Money.prototype.toNumber = function () {
    return this.isValid() ? this.minor / Math.pow(10, this.precision) : NaN;
  };

  /* ---- construction ------------------------------------------------------ */
  BES.Money = Money;
  Money.fromMinor = function (minor, currency) {
    currency = currency || "AED";
    return new Money(Number.isSafeInteger(minor) ? minor : NaN,
                     currency, BES.currencyPrecision(currency));
  };
  /* From decimal text ("1250.50") or a number. A number is read through its
     shortest decimal representation — the digits the author wrote — because its
     binary value is already not the amount they meant. */
  Money.of = function (value, currency, opts) {
    opts = opts || {};
    currency = currency || "AED";
    var precision = opts.precision != null ? opts.precision : BES.currencyPrecision(currency);
    if (value instanceof Money) return value;
    var text;
    if (typeof value === "number") {
      if (!isFinite(value)) return new Money(NaN, currency, precision);
      // Exponential reprs ("1e+21", "1e-7") are rejected by decimalParts below —
      // that regex is the single gate, so there is no second guard here to drift
      // out of step with it. Both are out of banking display range regardless.
      text = String(value);
    } else {
      text = String(value == null ? "" : value).trim();
    }
    var parts = decimalParts(text);
    if (!parts) return new Money(NaN, currency, precision);
    return new Money(toMinor(parts, precision, opts.rounding), currency, precision);
  };

  /* ---- rendering (Intl) --------------------------------------------------
     Grouping, decimal separators and numbering systems are locale data, not
     string manipulation. Sign and currency placement remain house rules. */
  var nfCache = {};
  function numberFormat(locale, precision, opts) {
    var key = locale + "|" + precision + "|" + (opts.notation || "") + "|" + (opts.useGrouping !== false);
    if (nfCache[key]) return nfCache[key];
    var cfg = { useGrouping: opts.useGrouping !== false };
    if (opts.notation === "compact") {
      cfg.notation = "compact";
      cfg.compactDisplay = "short";
      cfg.maximumFractionDigits = 2;
    } else {
      cfg.minimumFractionDigits = precision;
      cfg.maximumFractionDigits = precision;
    }
    var nf;
    try { nf = new Intl.NumberFormat(locale, cfg); }
    catch (e) { nf = new Intl.NumberFormat(undefined, cfg); }
    nfCache[key] = nf;
    return nf;
  }
  /* doc 29 §2: Western digits are the default for financial figures; Eastern
     Arabic digits are an explicit display-only preference, never mixed within a
     screen. `numerals: "arab"` is that preference, expressed as a locale
     extension so Intl produces the separators to match. */
  function localeFor(opts) {
    var locale = opts.locale || "en-AE";
    if (opts.numerals && !/-u-.*nu-/.test(locale)) locale += "-u-nu-" + opts.numerals;
    return locale;
  }

  Money.prototype.format = function (opts) {
    opts = opts || {};
    if (!this.isValid()) return (opts.currencyDisplay === "none" ? "" : this.currency + " ") + "—";
    var neg = this.minor < 0;
    var body = numberFormat(localeFor(opts), this.precision, opts)
      .format(Math.abs(this.minor) / Math.pow(10, this.precision));
    var sign = neg ? "−" : (opts.showPlus && this.minor > 0 ? "+" : "");
    if (opts.currencyDisplay === "none") return sign + body;
    if (opts.currencyDisplay === "symbol") {
      var sym = "";
      try {
        sym = new Intl.NumberFormat(localeFor(opts), {
          style: "currency", currency: this.currency, currencyDisplay: "narrowSymbol",
          minimumFractionDigits: 0, maximumFractionDigits: 0
        }).formatToParts(0).filter(function (p) { return p.type === "currency"; })
          .map(function (p) { return p.value; }).join("");
      } catch (e) { sym = this.currency; }
      return sign + (sym || this.currency) + " " + body;
    }
    return sign + this.currency + " " + body;
  };
  /* Summary and chart-axis form only — doc 13 forbids abbreviation on
     authorize, review and receipt surfaces. */
  Money.prototype.formatCompact = function (opts) {
    opts = opts || {};
    var o = {};
    for (var k in opts) o[k] = opts[k];
    o.notation = "compact";
    return this.format(o);
  };
  /* doc 13: the accessible name is the spoken form, not the glyphs. */
  Money.prototype.toSpoken = function (opts) {
    opts = opts || {};
    if (!this.isValid()) return "amount unavailable";
    var locale = opts.locale || "en-AE";
    var spoken;
    try {
      spoken = new Intl.NumberFormat(locale, {
        style: "currency", currency: this.currency, currencyDisplay: "name",
        minimumFractionDigits: this.precision, maximumFractionDigits: this.precision
      }).format(Math.abs(this.minor) / Math.pow(10, this.precision));
    } catch (e) {
      spoken = this.format({ locale: locale });
    }
    return (this.minor < 0 ? (opts.minusWord || "minus") + " " : "") + spoken;
  };

  /* ---- back-compatible façade -------------------------------------------
     formatAmount/parseAmount predate the Money type and are used across the
     journey, gallery and charts. They keep their signatures and now route
     through Money, so there is one implementation of money formatting in the
     system — which is what doc 13 says there must be.

     Note the rounding default differs by purpose, deliberately: formatAmount is
     display-only and defaults to half-up (the intuitive reading of a printed
     figure, and the pre-existing contract). Money.multiply/divide default to
     half-even, because rounding that runs over many transactions must not be
     biased in one direction. Anything that moves money should state its mode. */
  BES.formatAmount = function (value, opts) {
    opts = opts || {};
    var currency = opts.currency || "AED";
    var m = value instanceof Money
      ? value
      : Money.of(value, currency, { precision: opts.precision, rounding: opts.rounding || "half-up" });
    return m.format({
      locale: opts.locale, numerals: opts.numerals, showPlus: opts.showPlus,
      currencyDisplay: opts.currencyDisplay, useGrouping: opts.useGrouping
    });
  };

  /* Strict parse — money must be unambiguous or it is rejected.
     Accepts: an optional leading sign (ASCII hyphen, true minus U+2212, plus),
     accounting parentheses, a currency code or symbol as prefix or suffix, comma
     grouping, a single dot decimal, Arabic-Indic ٠-٩ and Extended ۰-۹ digits,
     Arabic decimal ٫ and thousands ٬.
     Returns NaN for anything else — dates, reference numbers, locale-ambiguous
     separators ("1.234,56"), a sign that is not leading, or more than one numeric
     run. A wrong amount is worse than no amount, so this never guesses. */
  var MONEY_RE = /^(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?$/;
  function normalizeMoneyText(str) {
    if (typeof str !== "string") return null;
    var s = str
      .replace(/[٠-٩]/g, function (d) { return String(d.charCodeAt(0) - 0x0660); })
      .replace(/[۰-۹]/g, function (d) { return String(d.charCodeAt(0) - 0x06F0); })
      .replace(/٫/g, ".")                            // Arabic decimal separator
      .replace(/٬/g, ",")                            // Arabic thousands separator
      .replace(/[\u00A0\u2007\u2009\u202F]/g, " ")   // non-breaking / thin spaces
      .replace(/[\u200E\u200F\u061C]/g, "")          // bidi marks
      .trim();
    if (!s) return null;
    var neg = false;
    var paren = /^\(([^()]*)\)$/.exec(s);
    if (paren) { neg = true; s = paren[1].trim(); }
    var sign = /^([+\-−➖])\s*/.exec(s);
    if (sign) { if (sign[1] !== "+") neg = true; s = s.slice(sign[0].length); }
    // strip a currency code or symbol from either end — never a sign, digit or separator
    var affix = /^[^\d.,+\-−()]+/.exec(s);
    if (affix) s = s.slice(affix[0].length).trim();
    affix = /[^\d.,+\-−()]+$/.exec(s);
    if (affix) s = s.slice(0, s.length - affix[0].length).trim();
    if (!MONEY_RE.test(s)) return null;
    return (neg ? "-" : "") + s.replace(/,/g, "");
  }
  /* Text → Money, exactly. The parse path a product should use. */
  Money.parse = function (str, currency, opts) {
    opts = opts || {};
    currency = currency || "AED";
    if (str instanceof Money) return str;
    var text = normalizeMoneyText(str);
    if (text === null) {
      return new Money(NaN, currency,
                       opts.precision != null ? opts.precision : BES.currencyPrecision(currency));
    }
    return Money.of(text, currency, opts);
  };
  /* Legacy numeric parse. Returns a float, so it is lossy by construction —
     kept for existing callers; new code should use Money.parse. */
  BES.parseAmount = function (str) {
    if (typeof str === "number") return isFinite(str) ? str : NaN;
    var text = normalizeMoneyText(str);
    if (text === null) return NaN;
    var v = parseFloat(text);
    return isFinite(v) ? v : NaN;
  };

  /* ---------- dates ---------- */
  // A calendar date is a local concept. toISOString() converts to UTC first, which shifts
  // the day backwards across every UTC+ zone — including Asia/Dubai, where 1 August
  // resolves to "2026-07-31". Always derive a date key from the local fields.
  BES.localISO = function (dt) {
    return dt.getFullYear() + "-" + String(dt.getMonth() + 1).padStart(2, "0") +
           "-" + String(dt.getDate()).padStart(2, "0");
  };

  /* ---------- bind guard ---------- */
  function guard(el, key) {
    key = "besBound" + key;
    if (el.dataset[key]) return true;
    el.dataset[key] = "1";
    return false;
  }

  /* ---------- currency input ---------- */
  var ctxSeq = 0;
  function bindCurrencyInput(el) {
    if (guard(el, "Cur")) return;
    // Associate the context line with the field once, at bind time. Without this the
    // validation message is set but never reachable: the field goes aria-invalid with
    // no reason attached (WCAG 3.3.1) and the change is never announced (WCAG 4.1.3).
    var bindField = el.closest(".bes-field");
    var bindCtx = bindField && bindField.querySelector(".bes-context-line");
    if (bindCtx) {
      if (!bindCtx.id) bindCtx.id = "bes-ctx-" + (++ctxSeq);
      var described = (el.getAttribute("aria-describedby") || "").split(/\s+/).filter(Boolean);
      if (described.indexOf(bindCtx.id) === -1) {
        described.push(bindCtx.id);
        el.setAttribute("aria-describedby", described.join(" "));
      }
      if (bindCtx.dataset.initial == null) bindCtx.dataset.initial = bindCtx.textContent.trim();
      if (!bindCtx.hasAttribute("aria-live")) {
        bindCtx.setAttribute("role", "status");
        bindCtx.setAttribute("aria-live", "polite");
      }
    }
    el.addEventListener("input", function () {
      var caretFromEnd = el.value.length - (el.selectionStart || 0);
      var txt = el.value
        .replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); })
        .replace(/[۰-۹]/g, function (d) { return "۰۱۲۳۴۵۶۷۸۹".indexOf(d); })
        .replace(/٫/g, ".")
        .replace(/[^0-9.]/g, "");
      var parts = txt.split(".");
      if (parts.length > 2) parts = [parts[0], parts.slice(1).join("")];
      parts[0] = parts[0].replace(/^0+(?=\d)/, "").replace(/\B(?=(\d{3})+(?!\d))/g, ",");
      var precision = el.dataset.precision != null ? +el.dataset.precision
                    : BES.currencyPrecision(el.dataset.currency || "AED");
      if (parts[1] != null) parts[1] = parts[1].slice(0, precision);
      var next = precision === 0 ? parts[0] : parts.join(".");
      if (next !== el.value) {
        el.value = next;
        var pos = Math.max(0, el.value.length - caretFromEnd);
        try { el.setSelectionRange(pos, pos); } catch (e) {}
      }
      // Balance arithmetic is exact: "leaves" and "exceeds by" used to be float
      // subtraction on money, which is how a fil goes missing from a figure the
      // user is about to authorise against.
      var cur = el.dataset.currency || "AED";
      var maxM = el.dataset.max ? Money.parse(el.dataset.max, cur) : null;
      var field = el.closest(".bes-field");
      var ctx = field && field.querySelector(".bes-context-line");
      var valM = Money.parse(el.value, cur);
      var val = valM.isValid() ? valM.toNumber() : NaN;
      var max = maxM && maxM.isValid() ? maxM.toNumber() : null;
      if (ctx && maxM && maxM.isValid()) {
        if (el.value === "" || !valM.isValid() || valM.minor <= 0) {
          ctx.classList.remove("bes-context-line--error");
          ctx.textContent = el.dataset.emptyMsg || ctx.dataset.initial || "";
          // an empty or not-yet-valid field is incomplete, not in error — doc 27:
          // don't accuse the user of a mistake they haven't finished making
          el.removeAttribute("aria-invalid");
        } else if (valM.compare(maxM) > 0) {
          ctx.classList.add("bes-context-line--error");
          ctx.textContent = BES.tpl(el.dataset.overMsg || "Exceeds available balance by {x}",
                                    { x: valM.subtract(maxM).format({ locale: el.dataset.locale }) });
          el.setAttribute("aria-invalid", "true");
        } else {
          ctx.classList.remove("bes-context-line--error");
          ctx.textContent = BES.tpl(el.dataset.leftMsg || "Leaves {x}",
                                    { x: maxM.subtract(valM).format({ locale: el.dataset.locale }) });
          el.removeAttribute("aria-invalid");
        }
      }
      el.dispatchEvent(new CustomEvent("bes:amount", { detail: val, bubbles: true }));
    });
  }

  /* ================= transaction states ====================================
     The canonical lifecycle from doc 07 §4, as data.

     These 13 names are the stable API: the same string identifies a state in the
     UI, the token set, the event stream and the copy deck. Until now that was a
     sentence in a document — the tokens existed, no component read them, and the
     one place UNKNOWN was ever rendered was hand-built inside a single page. So
     "Refunded" shipped styled as success and was pixel-identical to "Completed",
     and UNKNOWN was indistinguishable from "Processing".

     Two rules are encoded here rather than described:

     1. Colour never carries a state on its own. completed/refunded share green and
        processing/pending/unknown share teal — deliberately, because they are
        genuinely related. What tells them apart is the paired glyph and the label,
        which is why both come from this table and not from the caller.

     2. UNKNOWN offers no retry. A rail that has gone quiet may still be holding a
        successful transfer; a retry button is a double-send waiting to happen. The
        binder removes one if a product adds it, because a missing button is a
        smaller failure than sending someone's money twice.
     ======================================================================== */

  var ICON = {
    check:   '<path d="M2.5 6.4L5 8.9l4.5-6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    clock:   '<circle cx="6" cy="6" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M6 3.4V6l1.8 1.3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
    query:   '<circle cx="6" cy="6" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M4.7 4.7a1.35 1.35 0 112 1.15V7" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M6.7 8.9h-.02" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>',
    cross:   '<path d="M3.2 3.2l5.6 5.6M8.8 3.2L3.2 8.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    hold:    '<rect x="2.4" y="5.2" width="7.2" height="5" rx="1" stroke="currentColor" stroke-width="1.3"/><path d="M4.2 5.2V3.9a1.8 1.8 0 013.6 0v1.3" stroke="currentColor" stroke-width="1.3"/>',
    inflight: '<path d="M1.6 6h6.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><path d="M6.2 3.6L8.9 6l-2.7 2.4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/><path d="M10.4 3.4v5.2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>',
    pause:   '<circle cx="6" cy="6" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M4.9 4.3v3.4M7.1 4.3v3.4" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
    refund:  '<path d="M9.4 8.6A3.4 3.4 0 006 3.2H2.6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M4.4 1.4L2.4 3.2l2 1.8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/><path d="M7.6 9.8h3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>',
    ret:     '<path d="M9.4 8.6A3.4 3.4 0 006 3.2H2.6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/><path d="M4.4 1.4L2.4 3.2l2 1.8" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>',
    draft:   '<path d="M2.6 9.4l.5-2 5-5 1.5 1.5-5 5-2 .5z" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/>',
    review:  '<path d="M2.4 6S3.9 3.2 6 3.2 9.6 6 9.6 6 8.1 8.8 6 8.8 2.4 6 2.4 6z" stroke="currentColor" stroke-width="1.3"/><circle cx="6" cy="6" r="1.15" stroke="currentColor" stroke-width="1.1"/>',
    flag:    '<path d="M3.2 10.2V2.2m0 .6h5.4l-1.2 2 1.2 2H3.2" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/>',
    slash:   '<circle cx="6" cy="6" r="4.6" stroke="currentColor" stroke-width="1.4"/><path d="M3.2 8.8l5.6-5.6" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>'
  };

  function st(icon, en, ar, opts) {
    opts = opts || {};
    return {
      icon: icon, label: { en: en, ar: ar },
      terminal: !!opts.terminal,
      // doc 07: FAILED is only shown on confirmed failure; UNKNOWN must resolve and
      // must never offer an action that could send the money a second time
      allowsRetry: !!opts.allowsRetry,
      money: opts.money || null
    };
  }

  /* Arabic strings are machine-drafted and flagged unreviewed system-wide until the
     native review in docs/testing/arabic-rtl-review.md passes (see STATUS.md). The
     four that already existed in doc 27's glossary are carried over verbatim. */
  BES.TRANSACTION_STATES = {
    draft:          st(ICON.draft,  "Not sent yet",        "لم تُرسل بعد"),
    review:         st(ICON.review, "In review",           "قيد المراجعة"),
    authentication: st(ICON.hold,   "Awaiting authentication", "بانتظار المصادقة"),
    processing:     st(ICON.inflight,  "Processing",          "قيد التنفيذ",
                       { money: { en: "Money is on its way", ar: "الأموال في طريقها" } }),
    pending:        st(ICON.clock,  "Pending",             "قيد المعالجة",
                       { money: { en: "Money has left your account", ar: "غادرت الأموال حسابك" } }),
    completed:      st(ICON.check,  "Completed",           "تم التحويل", { terminal: true }),
    failed:         st(ICON.cross,  "Failed",              "فشلت",
                       { terminal: true, allowsRetry: true,
                         money: { en: "No money was deducted", ar: "لم يُخصم أي مبلغ" } }),
    unknown:        st(ICON.query,  "Checking status",     "نتحقق من الحالة",
                       { money: { en: "Your money is safe — we'll confirm shortly",
                                  ar: "أموالك آمنة — سنؤكد قريبًا" } }),
    blocked:        st(ICON.pause,   "Additional checks required", "مطلوب تحققات إضافية"),
    reversed:       st(ICON.ret,    "Reversed",            "تم عكس العملية", { terminal: true }),
    refunded:       st(ICON.refund,    "Refunded",            "تم الاسترداد",   { terminal: true }),
    disputed:       st(ICON.flag,   "Disputed",            "قيد الاعتراض"),
    cancelled:      st(ICON.slash,  "Cancelled",           "أُلغيت",
                       { terminal: true,
                         money: { en: "No money moved", ar: "لم تتحرك أي أموال" } })
  };
  BES.state = function (name) { return BES.TRANSACTION_STATES[name] || null; };

  function localeOf(el) {
    var node = el.closest ? el.closest("[lang]") : null;
    var lang = (node && node.getAttribute("lang")) ||
               document.documentElement.getAttribute("lang") || "en";
    return lang.slice(0, 2) === "ar" ? "ar" : "en";
  }
  function stateGlyph(spec) {
    // aria-hidden: the visible label already carries the state for assistive tech.
    // The glyph is what separates two states that share a hue on screen.
    return '<svg class="ic glyph" viewBox="0 0 12 12" fill="none" aria-hidden="true">' + spec.icon + "</svg>";
  }

  /* <span class="bes-badge" data-bes-state="unknown"></span> — the product names the
     state and gets the colour, the glyph and the label from one table, so a status
     cannot drift between two screens. */
  function bindStateBadge(el) {
    if (guard(el, "State")) return;
    var name = el.getAttribute("data-bes-state");
    var spec = BES.state(name);
    if (!spec) return;
    var lang = localeOf(el);
    for (var k in BES.TRANSACTION_STATES) el.classList.remove("bes-badge--" + k);
    el.classList.add("bes-badge", "bes-badge--" + name);
    var label = el.getAttribute("data-bes-label") || spec.label[lang];
    el.innerHTML = stateGlyph(spec) + BES.esc(label);
  }

  /* <div class="bes-result" data-bes-state="unknown" data-bes-money="…"> */
  function bindStateResult(el) {
    if (guard(el, "Result")) return;
    var name = el.getAttribute("data-bes-state");
    var spec = BES.state(name);
    if (!spec) return;
    var lang = localeOf(el);
    for (var k in BES.TRANSACTION_STATES) el.classList.remove("bes-result--" + k);
    el.classList.add("bes-result", "bes-result--" + name);

    var money = el.getAttribute("data-bes-money") || (spec.money && spec.money[lang]) || "";
    var head = el.querySelector("h1, h2, h3");
    if (head && !head.textContent.trim()) head.textContent = spec.label[lang];
    var ic = el.querySelector(".ic");
    if (ic && !ic.innerHTML.trim()) ic.innerHTML = stateGlyph(spec);
    var slot = el.querySelector(".money-state");
    if (slot && !slot.textContent.trim() && money) slot.textContent = money;

    if (!spec.allowsRetry) {
      var retries = el.querySelectorAll('[data-bes-retry]');
      Array.prototype.forEach.call(retries, function (b) {
        // A quiet rail may still be holding a successful transfer. Removing the
        // control is the smaller failure; leaving it is a double-send.
        b.parentNode && b.parentNode.removeChild(b);
        if (window.console && console.warn) {
          console.warn('[BES] removed a retry control from a "' + name + '" result. ' +
            "doc 07 §4: only a confirmed failure may offer retry.");
        }
      });
    }
  }

  /* ---------- balance masking (class-based; no stale snapshots) ---------- */
  // The value is moved into its own element on bind. Amounts are authored as bare text
  // nodes inside <bdi> ("<span class=cur>AED</span> 25,000.00"), which a CSS child
  // selector cannot reach and which <bdi> cannot carry an aria-label for — so masking
  // by selector alone left the balance both visible and in the accessibility tree.
  function maskValueEl(target) {
    var valEl = target.querySelector(".bes-mask-val");
    if (valEl) return valEl;
    var moved = [];
    for (var i = 0; i < target.childNodes.length; i++) {
      var n = target.childNodes[i];
      if (n.nodeType === 1 && (n.classList.contains("cur") || n.hasAttribute("data-mask-sr"))) continue;
      if (n.nodeType !== 1 && n.nodeType !== 3) continue;
      moved.push(n);
    }
    if (!moved.length) return null;
    valEl = document.createElement("span");
    valEl.className = "bes-mask-val";
    target.insertBefore(valEl, moved[0]);
    for (var j = 0; j < moved.length; j++) valEl.appendChild(moved[j]);
    return valEl;
  }
  function bindMask(btn) {
    if (guard(btn, "Mask")) return;
    var target = document.getElementById(btn.getAttribute("data-bes-mask"));
    if (!target) return;
    var valEl = maskValueEl(target);
    if (!valEl) return;
    var srEl = target.querySelector("[data-mask-sr]");
    if (!srEl) {
      srEl = document.createElement("span");
      srEl.className = "bes-vh";
      srEl.setAttribute("data-mask-sr", "");
      target.appendChild(srEl);
    }
    var remaskTimer = null;
    function setMasked(masked) {
      target.classList.toggle("bes-masked", masked);
      // display:none removes the digits from layout AND the accessibility tree;
      // the visually-hidden span is what a screen reader reads in their place
      srEl.textContent = masked ? (btn.dataset.maskedLabel || "Balance hidden") : "";
      btn.setAttribute("aria-pressed", masked ? "true" : "false");
      BES.announce(masked ? (btn.dataset.maskedLabel || "Balance hidden")
                          : (btn.dataset.shownLabel || "Balance shown"));
      if (remaskTimer) { clearTimeout(remaskTimer); remaskTimer = null; }
      // doc 13: reveal auto re-masks after 30s unless opted out
      if (!masked && btn.dataset.autoRemask !== "off")
        remaskTimer = setTimeout(function () { setMasked(true); }, 30000);
    }
    btn.addEventListener("click", function () {
      setMasked(!target.classList.contains("bes-masked"));
    });
  }

  /* ---------- tabs ---------- */
  function bindTabs(list) {
    if (guard(list, "Tabs")) return;
    var tabs = Array.prototype.slice.call(list.querySelectorAll('[role="tab"]'));
    tabs.forEach(function (t) { // initialize roving tabindex + panel visibility defensively
      var on = t.getAttribute("aria-selected") === "true";
      t.tabIndex = on ? 0 : -1;
      var panel = document.getElementById(t.getAttribute("aria-controls") || "");
      if (panel) { panel.hidden = !on; if (!panel.hasAttribute("tabindex")) panel.tabIndex = 0; }
    });
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        var panel = document.getElementById(t.getAttribute("aria-controls") || "");
        if (panel) panel.hidden = !on;
      });
      tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var dirMod = document.documentElement.getAttribute("dir") === "rtl" ? -1 : 1;
        var j = null;
        if (e.key === "ArrowRight") j = (i + dirMod + tabs.length) % tabs.length;
        if (e.key === "ArrowLeft") j = (i - dirMod + tabs.length) % tabs.length;
        if (e.key === "Home") j = 0;
        if (e.key === "End") j = tabs.length - 1;
        if (j != null) { e.preventDefault(); select(tabs[j]); }
      });
    });
  }

  /* ---------- segmented ---------- */
  function bindSeg(seg) {
    if (guard(seg, "Seg")) return;
    var btns = seg.querySelectorAll("button");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (x) { x.setAttribute("aria-pressed", "false"); });
        b.setAttribute("aria-pressed", "true");
        seg.dispatchEvent(new CustomEvent("bes:change", { detail: b.dataset.value || b.textContent }));
      });
    });
  }

  /* ---------- switch (role + live state word) ---------- */
  function bindSwitch(label) {
    if (guard(label, "Switch")) return;
    var input = label.querySelector('input[type="checkbox"]');
    var word = label.querySelector(".state");
    if (!input) return;
    input.setAttribute("role", "switch");
    var onW = label.dataset.on || "On", offW = label.dataset.off || "Off";
    function sync() {
      if (word) { word.textContent = input.checked ? onW : offW; word.setAttribute("aria-hidden", "true"); }
    }
    input.addEventListener("change", sync);
    sync();
  }

  /* ---------- focus-trap dialogs (shared engine for modal / drawer / interrupt) ---------- */
  var FOCUSABLE = 'button:not([disabled]), a[href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), summary, [tabindex]:not([tabindex="-1"])';
  function visible(el) { return !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length); }
  function trapOpen(container, opts) {
    opts = opts || {};
    container._lastFocus = document.activeElement;
    container.classList.add("open");
    if (opts.scrim) opts.scrim.classList.add("open");
    var first = container.querySelector(FOCUSABLE);
    if (first) first.focus();
    function onKey(e) {
      if (e.key === "Escape" && opts.escapable !== false) { trapClose(container, opts); return; }
      if (e.key !== "Tab") return;
      var f = Array.prototype.filter.call(container.querySelectorAll(FOCUSABLE), visible);
      if (!f.length) return;
      var firstEl = f[0], lastEl = f[f.length - 1];
      if (!container.contains(document.activeElement)) { e.preventDefault(); firstEl.focus(); return; }
      if (e.shiftKey && document.activeElement === firstEl) { e.preventDefault(); lastEl.focus(); }
      else if (!e.shiftKey && document.activeElement === lastEl) { e.preventDefault(); firstEl.focus(); }
    }
    container._trapKey = onKey;
    document.addEventListener("keydown", onKey);
  }
  function trapClose(container, opts) {
    opts = opts || {};
    container.classList.remove("open");
    // A closed dialog must not keep claiming aria-modal: assistive tech treats the rest
    // of the page as inert while it is set, visible or not. Escape closes through here,
    // so removing it in BES.closeModal alone would miss the commonest path.
    if (container.getAttribute("aria-modal") === "true") container.removeAttribute("aria-modal");
    if (opts.scrim) opts.scrim.classList.remove("open");
    if (container._trapKey) { document.removeEventListener("keydown", container._trapKey); container._trapKey = null; }
    if (container._lastFocus && container._lastFocus.focus) container._lastFocus.focus();
  }

  BES.openModal = function (id) {
    var scrim = document.getElementById(id);
    if (!scrim) return;
    scrim.setAttribute("aria-modal", "true");
    if (!scrim._scrimBound) { // one scrim-click listener for the lifetime of the element
      scrim._scrimBound = true;
      scrim.addEventListener("click", function (e) { if (e.target === scrim) BES.closeModal(id); });
    }
    trapOpen(scrim, {});
  };
  BES.closeModal = function (id) {
    var scrim = document.getElementById(id);
    if (!scrim) return;
    // a closed dialog must not keep claiming aria-modal — assistive tech treats the
    // rest of the page as inert while it is set, whether or not the dialog is visible
    scrim.removeAttribute("aria-modal");
    trapClose(scrim, {});
  };
  BES.openDrawer = function (id) {
    var d = document.getElementById(id);
    if (!d) return;
    d.setAttribute("aria-modal", "true");
    var scrim = document.getElementById(id + "-scrim");
    if (scrim && !scrim._scrimBound) {
      scrim._scrimBound = true;
      scrim.addEventListener("click", function () { BES.closeDrawer(id); });
    }
    trapOpen(d, { scrim: scrim });
  };
  BES.closeDrawer = function (id) {
    var d = document.getElementById(id);
    if (d) trapClose(d, { scrim: document.getElementById(id + "-scrim") });
  };
  // Critical security surface: focus-managed, not Esc-dismissable by default
  BES.openInterrupt = function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    trapOpen(el, { escapable: false });
    BES.announce(el.dataset.announce || (el.querySelector("h2") || {}).textContent || "", true);
  };
  BES.closeInterrupt = function (id) {
    var el = document.getElementById(id);
    if (el) trapClose(el, {});
  };

  /* ---------- toast ---------- */
  var TOAST_MAX = 3;
  function toastHost() {
    var host = document.querySelector(".bes-toasts");
    if (!host) {
      host = document.createElement("div");
      host.className = "bes-toasts";
      document.body.appendChild(host);
    }
    return host;
  }
  BES.toast = function (msg, ms) {
    var host = toastHost();
    while (host.children.length >= TOAST_MAX) host.removeChild(host.firstChild);
    var t = document.createElement("div");
    t.className = "bes-toast";
    t.textContent = msg;
    host.appendChild(t);
    BES.announce(msg);
    setTimeout(function () { t.remove(); }, ms || 4500);
  };

  /* ---------- copy ---------- */
  function bindCopy(btn) {
    if (guard(btn, "Copy")) return;
    btn.addEventListener("click", function () {
      var text = btn.getAttribute("data-bes-copy");
      if (!text) return;
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(function () {
          BES.toast(btn.getAttribute("data-bes-copied") || "Copied");
        }).catch(function () {
          BES.toast(btn.getAttribute("data-bes-copy-failed") || "Couldn't copy — select and copy manually");
        });
      } else {
        BES.toast(btn.getAttribute("data-bes-copy-failed") || "Couldn't copy — select and copy manually");
      }
    });
  }

  /* ---------- combobox (APG-complete) ---------- */
  var comboSeq = 0;
  function bindCombo(root) {
    if (guard(root, "Combo")) return;
    var input = root.querySelector("input");
    var list = root.querySelector(".bes-combo-list");
    var status = root.querySelector(".bes-combo-count");
    if (!input || !list) return;
    var cid = "bes-combo-" + (++comboSeq);
    list.id = list.id || cid + "-list";
    list.setAttribute("role", "listbox");
    input.setAttribute("role", "combobox");
    input.setAttribute("aria-controls", list.id);
    input.setAttribute("aria-expanded", "false");
    var items = Array.prototype.slice.call(list.querySelectorAll("li[data-value]"));
    items.forEach(function (li, i) {
      li.setAttribute("role", "option");
      li.id = li.id || cid + "-opt-" + i;
      li.setAttribute("aria-selected", "false");
    });
    var emptyLi = list.querySelector(".empty");
    // A listbox may only own options. role="presentation" stripped the zero-results
    // message out of the accessibility tree entirely, so a screen-reader user heard
    // "0 results" and never the recovery instruction. aria-disabled keeps it valid as
    // an owned child while excluding it from selection (navigation reads [data-value]).
    if (emptyLi) {
      emptyLi.setAttribute("role", "option");
      emptyLi.setAttribute("aria-disabled", "true");
    }
    var active = -1;
    function vis() { return items.filter(function (li) { return !li.hidden; }); }
    function setActive(li) {
      items.forEach(function (x) { x.classList.remove("active"); x.removeAttribute("aria-selected"); });
      if (li) {
        li.classList.add("active");
        li.setAttribute("aria-selected", "true"); // active option per APG combobox w/ activedescendant
        input.setAttribute("aria-activedescendant", li.id);
        li.scrollIntoView({ block: "nearest" });
      } else input.removeAttribute("aria-activedescendant");
    }
    function filter() {
      var q = input.value.trim().toLowerCase();
      var n = 0;
      items.forEach(function (li) {
        var hit = !q || li.textContent.toLowerCase().indexOf(q) !== -1;
        li.hidden = !hit;
        if (hit) n++;
      });
      if (emptyLi) emptyLi.hidden = n !== 0;
      if (status) status.textContent = n + (input.dataset.resultsLabel || " results");
      list.hidden = false;
      input.setAttribute("aria-expanded", "true");
      setActive(null);
    }
    function close() { list.hidden = true; input.setAttribute("aria-expanded", "false"); setActive(null); }
    function commit(li) {
      input.value = li.getAttribute("data-label") || li.textContent.trim();
      root.dispatchEvent(new CustomEvent("bes:select", { detail: li.dataset.value }));
      close();
      input.focus();
    }
    input.addEventListener("input", filter);
    input.addEventListener("focus", filter);
    input.addEventListener("keydown", function (e) {
      var v = vis();
      var cur = v.findIndex(function (li) { return li.classList.contains("active"); });
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (list.hidden) filter();
        var next = e.key === "ArrowDown" ? Math.min(cur + 1, v.length - 1) : Math.max(cur - 1, 0);
        if (v[next]) setActive(v[next]);
      }
      if (e.key === "Enter" && cur >= 0 && v[cur]) { e.preventDefault(); commit(v[cur]); }
      if (e.key === "Escape") { if (!list.hidden) close(); else input.value = ""; }
    });
    list.addEventListener("mousedown", function (e) { e.preventDefault(); }); // keep input focus
    list.addEventListener("click", function (e) {
      var li = e.target.closest("li[data-value]");
      if (li) commit(li);
    });
    input.addEventListener("blur", function () { setTimeout(close, 120); });
  }

  /* ---------- date picker (roving tabindex, keyboard grid, announced) ---------- */
  var MONTHS = ["January","February","March","April","May","June","July","August","September","October","November","December"];
  var WDAYS_FULL = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
  var WDAYS = ["Mo","Tu","We","Th","Fr","Sa","Su"];
  function bindDatepicker(root) {
    if (guard(root, "Dp")) return;
    var y = +root.dataset.year || new Date().getFullYear();
    var m = root.dataset.month != null ? +root.dataset.month : new Date().getMonth();
    var selected = root.dataset.selected || "";
    var focusIso = null;
    var disabledDows = (root.dataset.disabledDays || "").split(",").filter(Boolean).map(Number);
    var note = root.dataset.disabledNote || "";
    var months = (root.dataset.months || "").split(",").filter(Boolean);
    if (months.length !== 12) months = MONTHS;
    var noteId = (root.id || "bes-dp") + "-note";
    root.setAttribute("role", "group");
    root.setAttribute("aria-label", root.dataset.label || "Choose a date");
    function iso(d) { return y + "-" + String(m + 1).padStart(2, "0") + "-" + String(d).padStart(2, "0"); }
    function render(announceMonth) {
      var first = new Date(y, m, 1);
      var startDow = (first.getDay() + 6) % 7;
      var days = new Date(y, m + 1, 0).getDate();
      var today = new Date();
      var html = '<div class="bes-dp-head">' +
        '<button type="button" class="bes-iconbtn" data-nav="-1" aria-label="Previous month">‹</button>' +
        '<span class="m" aria-live="polite">' + BES.esc(months[m]) + " " + y + "</span>" +
        '<button type="button" class="bes-iconbtn" data-nav="1" aria-label="Next month">›</button></div>' +
        '<div class="bes-dp-grid">';
      WDAYS.forEach(function (w) { html += '<span class="wd" aria-hidden="true">' + w + "</span>"; });
      for (var i = 0; i < startDow; i++) html += "<span></span>";
      var focusDay = focusIso && focusIso.slice(0, 7) === iso(1).slice(0, 7) ? +focusIso.slice(8) : null;
      var rovingSet = false;
      for (var d = 1; d <= days; d++) {
        var date = new Date(y, m, d);
        var dis = disabledDows.indexOf(date.getDay()) !== -1;
        var isToday = date.toDateString() === today.toDateString();
        var dIso = iso(d);
        var roving = focusDay ? d === focusDay : (dIso === selected || (!selected && isToday));
        if (roving) rovingSet = true;
        html += '<button type="button" data-iso="' + dIso + '" tabindex="' + (roving ? 0 : -1) + '"' +
          ' aria-label="' + d + " " + BES.esc(months[m]) + " " + y + ", " + WDAYS_FULL[(date.getDay() + 6) % 7] +
          (dis ? " — " + BES.esc(note) : "") + '"' +
          (dis ? ' aria-disabled="true" data-disabled="1"' : "") +
          (isToday ? ' aria-current="date"' : "") +
          (dIso === selected ? ' aria-selected="true"' : "") + ">" + d + "</button>";
      }
      html += "</div>";
      if (note) html += '<div class="bes-dp-note" id="' + noteId + '">' + BES.esc(note) + "</div>";
      root.innerHTML = html;
      if (!rovingSet) { var fb = root.querySelector("[data-iso]"); if (fb) fb.tabIndex = 0; }
      if (announceMonth) {
        var nav = root.querySelector('[data-nav="' + announceMonth + '"]');
        if (nav) nav.focus();
      }
    }
    function moveFocus(delta) {
      var current = root.querySelector('[data-iso][tabindex="0"]');
      var d = current ? +current.dataset.iso.slice(8) : 1;
      var target = new Date(y, m, d + delta);
      if (target.getMonth() !== m || target.getFullYear() !== y) {
        y = target.getFullYear(); m = target.getMonth();
        focusIso = BES.localISO(target);
        render();
      } else {
        focusIso = iso(target.getDate());
        root.querySelectorAll("[data-iso]").forEach(function (b) { b.tabIndex = -1; });
      }
      var btn = root.querySelector('[data-iso="' + focusIso + '"]');
      if (btn) { btn.tabIndex = 0; btn.focus(); }
    }
    root.addEventListener("click", function (e) {
      var nav = e.target.closest("[data-nav]");
      if (nav) {
        m += +nav.dataset.nav; if (m < 0) { m = 11; y--; } if (m > 11) { m = 0; y++; }
        focusIso = null; render(nav.dataset.nav); return;
      }
      var day = e.target.closest("[data-iso]");
      if (day && !day.dataset.disabled) {
        selected = day.dataset.iso;
        root.dispatchEvent(new CustomEvent("bes:date", { detail: selected }));
        focusIso = selected; render();
        var sel = root.querySelector('[aria-selected="true"]'); if (sel) sel.focus();
      }
    });
    root.addEventListener("keydown", function (e) {
      if (!e.target.closest("[data-iso]")) return;
      var rtl = document.documentElement.getAttribute("dir") === "rtl" ? -1 : 1;
      var map = { ArrowRight: 1 * rtl, ArrowLeft: -1 * rtl, ArrowDown: 7, ArrowUp: -7 };
      if (map[e.key] != null) { e.preventDefault(); moveFocus(map[e.key]); }
      if (e.key === "Home") { e.preventDefault(); moveFocus(-((+e.target.dataset.iso.slice(8)) - 1)); }
      if (e.key === "PageDown") { e.preventDefault(); m++; if (m > 11) { m = 0; y++; } focusIso = null; render(); var f = root.querySelector('[data-iso][tabindex="0"]'); if (f) f.focus(); }
      if (e.key === "PageUp") { e.preventDefault(); m--; if (m < 0) { m = 11; y--; } focusIso = null; render(); var f2 = root.querySelector('[data-iso][tabindex="0"]'); if (f2) f2.focus(); }
    });
    render();
  }

  /* ---------- sortable table (keyboard-operable, visible indicator) ---------- */
  function bindSortTable(table) {
    if (guard(table, "Sort")) return;
    table.querySelectorAll("th[data-sort]").forEach(function (th) {
      var colIdx = Array.prototype.indexOf.call(th.parentNode.children, th);
      // real button = keyboard + AT operable
      var btn = document.createElement("button");
      btn.type = "button";
      btn.className = "bes-sortbtn";
      while (th.firstChild) btn.appendChild(th.firstChild);
      th.appendChild(btn);
      btn.addEventListener("click", function () {
        var dir = th.getAttribute("aria-sort") === "ascending" ? -1 : 1;
        table.querySelectorAll("th[data-sort]").forEach(function (x) { x.removeAttribute("aria-sort"); });
        th.setAttribute("aria-sort", dir === 1 ? "ascending" : "descending");
        var tbody = table.querySelector("tbody");
        var rows = Array.prototype.slice.call(tbody.rows);
        var numeric = th.dataset.sort === "num";
        rows.sort(function (a, b) {
          var av = a.cells[colIdx].textContent.trim(), bv = b.cells[colIdx].textContent.trim();
          if (numeric) {
            // compare exact minor units; unparseable cells (—, blanks) sort as zero
            var am = Money.parse(av, th.dataset.currency || "AED");
            var bm = Money.parse(bv, th.dataset.currency || "AED");
            var an = am.isValid() ? am.minor : 0;
            var bn = bm.isValid() ? bm.minor : 0;
            return (an - bn) * dir;
          }
          return av.localeCompare(bv) * dir;
        });
        rows.forEach(function (r) { tbody.appendChild(r); });
        BES.announce((btn.textContent || "Column") + (dir === 1 ? " sorted ascending" : " sorted descending"));
      });
    });
  }

  /* ---------- rate-lock countdown (milestone announcements, cleanup) ---------- */
  function bindCountdown(el) {
    if (el._stop) el._stop(); // re-bind restarts cleanly
    var secs = +el.dataset.besCountdown || 300;
    var label = el.querySelector(".t") || el;
    var announced = {};
    function show() {
      var mm = Math.floor(secs / 60), ss = String(secs % 60).padStart(2, "0");
      label.textContent = (el.dataset.prefix || "locked ") + mm + ":" + ss;
    }
    show();
    var timer = setInterval(function () {
      secs--;
      if (secs <= 0) {
        clearInterval(timer);
        el.classList.remove("warn"); el.classList.add("expired");
        label.textContent = el.dataset.expiredText || "rate expired";
        BES.announce(el.dataset.expiredAnnounce || "Rate lock expired — get a new rate before sending.", true);
        el.dispatchEvent(new CustomEvent("bes:rate-expired", { bubbles: true }));
        return;
      }
      show();
      if (secs <= 60) {
        el.classList.add("warn");
        if (!announced.warn) {
          announced.warn = true;
          BES.announce(el.dataset.warnAnnounce || "Rate locked for one more minute.");
        }
      }
    }, 1000);
    el._stop = function () { clearInterval(timer); };
  }
  BES.stopCountdowns = function (root) {
    (root || document).querySelectorAll("[data-bes-countdown]").forEach(function (el) {
      if (el._stop) el._stop();
    });
  };

  /* ---------- PIN / code entry ---------- */
  function bindPin(root) {
    if (guard(root, "Pin")) return;
    var cells = Array.prototype.slice.call(root.querySelectorAll("input"));
    var isCode = root.classList.contains("bes-pin--code");
    if (!root.hasAttribute("role")) {
      root.setAttribute("role", "group");
      if (!root.getAttribute("aria-label") && !root.getAttribute("aria-labelledby"))
        root.setAttribute("aria-label", root.dataset.label || (isCode ? "Verification code" : "PIN"));
    }
    cells.forEach(function (c, i) {
      c.setAttribute("inputmode", "numeric");
      c.setAttribute("maxlength", "1");
      c.setAttribute("autocomplete", isCode ? (i === 0 ? "one-time-code" : "off") : "off");
      c.addEventListener("input", function () {
        c.value = c.value.replace(/[^0-9]/g, "");
        if (c.value && i < cells.length - 1) cells[i + 1].focus();
        if (cells.every(function (x) { return x.value; })) {
          root.dispatchEvent(new CustomEvent("bes:pin", { detail: cells.map(function (x) { return x.value; }).join("") }));
        }
      });
      c.addEventListener("keydown", function (e) {
        if (e.key === "Backspace" && !c.value && i > 0) cells[i - 1].focus();
      });
      // WCAG 2.2 3.3.8 Accessible Authentication: paste allowed on BOTH pin and code
      c.addEventListener("paste", function (e) {
        e.preventDefault();
        var digits = ((e.clipboardData || window.clipboardData).getData("text") || "")
          .replace(/[٠-٩]/g, function (d) { return "٠١٢٣٤٥٦٧٨٩".indexOf(d); })
          .replace(/[^0-9]/g, "").split("");
        cells.forEach(function (x, j) { x.value = digits[j] || ""; });
        var lastFilled = Math.min(digits.length, cells.length) - 1;
        if (lastFilled >= 0) cells[Math.min(lastFilled + 1, cells.length - 1)].focus();
        if (digits.length >= cells.length) {
          root.dispatchEvent(new CustomEvent("bes:pin", { detail: digits.slice(0, cells.length).join("") }));
        }
      });
    });
    root.setError = function (msg) {
      root.classList.add("error");
      cells.forEach(function (x) { x.value = ""; x.setAttribute("aria-invalid", "true"); });
      BES.announce(msg, true);
      cells[0].focus();
    };
    root.clearError = function () {
      root.classList.remove("error");
      cells.forEach(function (x) { x.removeAttribute("aria-invalid"); });
    };
  }

  /* ---------- character count ---------- */
  function bindCharcount(el) {
    if (guard(el, "Cc")) return;
    var input = document.getElementById(el.dataset.besCharcount);
    if (!input) return;
    var max = +input.getAttribute("maxlength") || +el.dataset.max || 140;
    var tplStr = el.dataset.msg || "{n} characters left";
    el.setAttribute("aria-live", "polite");
    function upd() {
      var left = max - input.value.length;
      el.textContent = BES.tpl(tplStr, { n: left });
      el.classList.toggle("over", left < 0);
    }
    input.addEventListener("input", upd);
    upd();
  }

  /* ---------- charts (escaped, guarded, labeled) ---------- */
  var CAT = ["var(--bes-chart-cat1)","var(--bes-chart-cat2)","var(--bes-chart-cat3)","var(--bes-chart-cat4)","var(--bes-chart-cat5)","var(--bes-chart-cat6)","var(--bes-chart-cat7)"];
  function chartGuard(el, data, opts) {
    if (!opts || !opts.label) {
      if (window.console) console.warn("BES chart: opts.label is required for accessibility");
    }
    if (!data || !data.length) {
      el.innerHTML = '<p class="bes-chart-empty">' + BES.esc((opts && opts.emptyText) || "No data to chart yet.") + "</p>";
      return false;
    }
    return true;
  }
  /* Axis labels are money, so they go through the one money formatter (doc 13).
     The old hand-rolled version rounded 1500 to "2K" and printed the wrong number
     next to the gridline it labelled; Intl compact notation gives "1.5K". The
     currency is dropped — the axis is labelled once, not per gridline. */
  function unitLabel(v, opts) {
    opts = opts || {};
    var m = Money.of(String(v), opts.currency || "AED", { rounding: "half-even" });
    if (!m.isValid()) return String(Math.round(v));
    return m.formatCompact({ currencyDisplay: "none", locale: opts.locale, numerals: opts.numerals });
  }
  function svgEl(w, h, label) {
    return '<svg viewBox="0 0 ' + w + " " + h + '" role="img" aria-label="' + BES.esc(label || "Chart") + '">';
  }
  BES.chartBar = function (el, data, opts) {
    opts = opts || {};
    if (!chartGuard(el, data, opts)) return;
    var W = 480, H = 220, padS = 56, padB = 28, padT = 12;
    var max = Math.max.apply(null, data.map(function (d) { return Math.max(0, d.value); })) || 1;
    var innerW = W - padS - 12, innerH = H - padB - padT;
    var bw = Math.min(48, innerW / data.length * 0.6);
    var html = svgEl(W, H, opts.label);
    [0, .5, 1].forEach(function (f) {
      var yy = padT + innerH - innerH * f;
      html += '<line class="gridline" x1="' + padS + '" y1="' + yy + '" x2="' + (W - 12) + '" y2="' + yy + '"/>';
      html += '<text x="' + (padS - 8) + '" y="' + (yy + 4) + '" text-anchor="end">' + unitLabel(max * f, opts) + "</text>";
    });
    data.forEach(function (d, i) {
      var x = padS + (innerW / data.length) * i + (innerW / data.length - bw) / 2;
      var bh = innerH * (Math.max(0, d.value) / max);
      html += '<rect x="' + x + '" y="' + (padT + innerH - bh) + '" width="' + bw + '" height="' + bh + '" rx="4" fill="' + (d.color || CAT[i % CAT.length]) + '"/>';
      html += '<text x="' + (x + bw / 2) + '" y="' + (H - 8) + '" text-anchor="middle">' + BES.esc(d.label) + "</text>";
    });
    el.innerHTML = html + "</svg>" + tableEquiv(data, opts);
  };
  BES.chartDonut = function (el, data, opts) {
    opts = opts || {};
    if (!chartGuard(el, data, opts)) return;
    var total = data.reduce(function (s, d) { return s + Math.max(0, d.value); }, 0) || 1;
    var W = 380, H = Math.max(200, 40 + data.length * 24), cx = 100, cy = H / 2, r = 72, sw = 30;
    var html = svgEl(W, H, opts.label);
    var a0 = -Math.PI / 2;
    data.forEach(function (d, i) {
      var frac = Math.max(0, d.value) / total, a1 = a0 + frac * Math.PI * 2;
      if (frac <= 0) return;
      var large = frac > .5 ? 1 : 0;
      var x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
      var x1 = cx + r * Math.cos(a1 - 0.02), y1 = cy + r * Math.sin(a1 - 0.02);
      html += '<path d="M' + x0.toFixed(1) + " " + y0.toFixed(1) + " A" + r + " " + r + " 0 " + large + " 1 " + x1.toFixed(1) + " " + y1.toFixed(1) + '" fill="none" stroke="' + (d.color || CAT[i % CAT.length]) + '" stroke-width="' + sw + '"/>';
      a0 = a1;
    });
    html += '<text x="' + cx + '" y="' + (cy - 2) + '" text-anchor="middle" class="lbl-strong" style="font-size:15px">' + BES.esc(opts.center || "") + "</text>";
    html += '<text x="' + cx + '" y="' + (cy + 16) + '" text-anchor="middle">' + BES.esc(opts.centerSub || "") + "</text>";
    data.forEach(function (d, i) {
      var ly = 24 + i * 24;
      html += '<rect x="212" y="' + (ly - 9) + '" width="10" height="10" rx="3" fill="' + (d.color || CAT[i % CAT.length]) + '"/>';
      html += '<text x="230" y="' + ly + '">' + BES.esc(d.label) + "</text>";
      html += '<text x="' + (W - 4) + '" y="' + ly + '" text-anchor="end">' + Math.round(Math.max(0, d.value) / total * 100) + "%</text>";
    });
    el.innerHTML = html + "</svg>" + tableEquiv(data, opts);
  };
  BES.chartLine = function (el, data, opts) {
    opts = opts || {};
    if (!chartGuard(el, data, opts)) return;
    if (data.length < 2) { // a line of one point misleads — degrade to the table
      el.innerHTML = tableEquiv(data, opts).replace("<details", "<details open");
      return;
    }
    var W = 480, H = 200, padS = 56, padB = 26, padT = 12;
    var vals = data.map(function (d) { return d.value; });
    var max = Math.max.apply(null, vals), min = opts.zeroBase === false ? Math.min.apply(null, vals) : 0;
    if (max === min) max = min + 1;
    var innerW = W - padS - 16, innerH = H - padB - padT;
    function X(i) { return padS + innerW * (i / (data.length - 1)); }
    function Y(v) { return padT + innerH - innerH * ((v - min) / (max - min)); }
    var html = svgEl(W, H, opts.label);
    [0, .5, 1].forEach(function (f) {
      var yy = padT + innerH - innerH * f;
      html += '<line class="gridline" x1="' + padS + '" y1="' + yy + '" x2="' + (W - 16) + '" y2="' + yy + '"/>';
      html += '<text x="' + (padS - 8) + '" y="' + (yy + 4) + '" text-anchor="end">' + unitLabel(min + (max - min) * f, opts) + "</text>";
    });
    var pts = data.map(function (d, i) { return X(i).toFixed(1) + "," + Y(d.value).toFixed(1); });
    html += '<polyline points="' + pts.join(" ") + '" fill="none" stroke="var(--bes-chart-cat1)" stroke-width="2.5" stroke-linejoin="round"/>';
    html += '<circle cx="' + X(data.length - 1) + '" cy="' + Y(data[data.length - 1].value) + '" r="4.5" fill="var(--bes-chart-cat1)"/>';
    data.forEach(function (d, i) {
      if (i % Math.ceil(data.length / 6) === 0 || i === data.length - 1)
        html += '<text x="' + X(i) + '" y="' + (H - 6) + '" text-anchor="middle">' + BES.esc(d.label) + "</text>";
    });
    el.innerHTML = html + "</svg>" + tableEquiv(data, opts);
  };
  var tableSeq = 0;
  function tableEquiv(data, opts) {
    var id = "bes-charttbl-" + (++tableSeq);
    var rows = data.map(function (d) {
      // the accessible table is the same money, formatted by the same code — it
      // used to use toLocaleString(), so it disagreed with the amounts beside it
      return "<tr><td>" + BES.esc(d.label) + '</td><td class="num">'
        + BES.esc(BES.formatAmount(d.value, { currency: opts.currency || "AED", locale: opts.locale }))
        + "</td></tr>";
    }).join("");
    var name = opts.label ? BES.esc("View “" + opts.label + "” as table") : "View as table";
    return '<details style="margin-top:6px"><summary class="bes-chart-table-link" style="cursor:pointer" aria-label="' + name + '">' +
      (opts.tableLabel || "View as table") + "</summary>" +
      '<div class="bes-table-wrap" style="margin-top:8px"><table class="bes-table" id="' + id + '" style="min-inline-size:0"><thead><tr><th>' +
      BES.esc(opts.colLabel || "Label") + '</th><th class="num">' + BES.esc(opts.colValue || "Value") + "</th></tr></thead><tbody>" + rows + "</tbody></table></div></details>";
  }

  /* ---------- init ---------- */
  function initAll(root) {
    root = root || document;
    root.querySelectorAll("[data-bes-currency]").forEach(bindCurrencyInput);
    root.querySelectorAll("[data-bes-mask]").forEach(bindMask);
    root.querySelectorAll("span[data-bes-state], .bes-badge[data-bes-state]").forEach(bindStateBadge);
    root.querySelectorAll(".bes-result[data-bes-state]").forEach(bindStateResult);
    root.querySelectorAll('[role="tablist"].bes-tabs').forEach(bindTabs);
    root.querySelectorAll(".bes-seg").forEach(bindSeg);
    root.querySelectorAll(".bes-switch").forEach(bindSwitch);
    root.querySelectorAll("[data-bes-copy]").forEach(bindCopy);
    root.querySelectorAll(".bes-combo").forEach(bindCombo);
    root.querySelectorAll(".bes-datepicker[data-bes-datepicker]").forEach(bindDatepicker);
    root.querySelectorAll("table[data-bes-sortable]").forEach(bindSortTable);
    root.querySelectorAll("[data-bes-countdown]").forEach(bindCountdown);
    root.querySelectorAll(".bes-pin").forEach(bindPin);
    root.querySelectorAll("[data-bes-charcount]").forEach(bindCharcount);
    root.querySelectorAll("[data-bes-open]").forEach(function (b) {
      if (guard(b, "Open")) return;
      b.addEventListener("click", function () { BES.openModal(b.getAttribute("data-bes-open")); });
    });
    root.querySelectorAll("[data-bes-close]").forEach(function (b) {
      if (guard(b, "Close")) return;
      b.addEventListener("click", function () { BES.closeModal(b.getAttribute("data-bes-close")); });
    });
    root.querySelectorAll("[data-bes-drawer-open]").forEach(function (b) {
      if (guard(b, "DOpen")) return;
      b.addEventListener("click", function () { BES.openDrawer(b.getAttribute("data-bes-drawer-open")); });
    });
    root.querySelectorAll("[data-bes-drawer-close]").forEach(function (b) {
      if (guard(b, "DClose")) return;
      b.addEventListener("click", function () { BES.closeDrawer(b.getAttribute("data-bes-drawer-close")); });
    });
    root.querySelectorAll("[data-bes-interrupt-open]").forEach(function (b) {
      if (guard(b, "IOpen")) return;
      b.addEventListener("click", function () { BES.openInterrupt(b.getAttribute("data-bes-interrupt-open")); });
    });
    root.querySelectorAll("[data-bes-interrupt-close]").forEach(function (b) {
      if (guard(b, "IClose")) return;
      b.addEventListener("click", function () { BES.closeInterrupt(b.getAttribute("data-bes-interrupt-close")); });
    });
    root.querySelectorAll("[data-bes-toast]").forEach(function (b) {
      if (guard(b, "Toast")) return;
      b.addEventListener("click", function () { BES.toast(b.getAttribute("data-bes-toast")); });
    });
  }
  BES.init = initAll;
  BES.init2 = initAll; // back-compat alias
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { initAll(); });
  else initAll();
})();
