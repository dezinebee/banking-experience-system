# Migrating from BES 1.0.x to 2.0.0

Required reading if you consumed v1.0.1. Per `GOVERNANCE.md`, a MAJOR release ships a
migration note; this is it.

**Why it is a MAJOR.** v2.0.0 came out of an independent review that found five defects
every automated gate had passed through. Fixing them honestly meant changing behaviour
some consumers may have relied on — and the changes are the kind that fail *silently* if
you skip them, which is the whole reason this document is not optional.

Budget roughly **half a day** for a product of moderate size. Most of it is find-and-replace;
two items need a person to think.

---

## At a glance

| # | Change | Class | Silent if missed? |
|---|---|---|---|
| 1 | `parseAmount` rejects ambiguous input | Behaviour | **Yes** — returns `NaN` where it used to return a number |
| 2 | Money is a value type; `formatAmount` rounding differs | Behaviour | Partly — some amounts shift by one minor unit |
| 3 | Transaction state tokens consolidated to `transaction.*` | Token removal | No — CSS `var()` falls back to nothing, visibly |
| 4 | `bes-result--success` → `bes-result--completed` | Markup | No — the state loses its styling |
| 5 | Badges: use `data-bes-state`, not generic status classes | Markup | **Yes** — "Refunded" still renders, just wrong |
| 6 | Type scale rationalised; some sizes shift ≤1px | Visual | **Yes** — nothing breaks, things move slightly |
| 7 | Currency input requires an associated context line | Markup | **Yes** — accessibility regression, not a visual one |
| 8 | `financial.*` no longer carries state colours | Token removal | No |

---

## 1. `parseAmount` now rejects ambiguous input

**What changed.** v1 detected a minus sign *anywhere* in the string and stripped every
non-digit, so it returned confident, wrong numbers:

```js
BES.parseAmount("2026-08-31")        // v1: -20260831   v2: NaN
BES.parseAmount("Ref-4471 AED 300")  // v1: -4471300    v2: NaN
BES.parseAmount("AED 12 - fee")      // v1: -12         v2: NaN
BES.parseAmount("1.234,56")          // v1: 1.23456     v2: NaN
BES.parseAmount("1.234.567.89")      // v1: 1234567.89  v2: NaN
```

v1's own JSDoc promised "returns NaN for ambiguous input" and never delivered it. v2 does.

**What to do.** Anywhere you call `parseAmount`, handle `NaN` explicitly — it now means
*"this string is not unambiguously an amount"*, which is information you want. If you were
feeding it arbitrary text (table cells, pasted values, API strings), that path was returning
garbage before and is now returning a signal.

If you need to accept European separators, normalise before parsing — v2 will not guess
between `1.234,56` as one-thousand-two-hundred and as one-point-two-three.

---

## 2. Money is a value type

**What changed.** `BES.Money` stores an integer count of **minor units** plus a currency and
its ISO precision. `AED 1,250.50` is `{ currency: "AED", minor: 125050, precision: 2 }`.

`formatAmount` and `parseAmount` keep their signatures and route through it, so most calls
are unaffected. Two differences you will see:

```js
BES.formatAmount(8.165)     // v1: "AED 8.16"   v2: "AED 8.17"
BES.formatAmount(1.005)     // v1: "AED 1.00"   v2: "AED 1.01"
BES.formatAmount(-0.001)    // v1: "−AED 0.00"  v2: "AED 0.00"   (zero has no sign)
BES.formatAmount("1250.5")  // v1: "AED —"      v2: "AED 1,250.50"  (strings now accepted)
```

v1 rounded the *binary* value of the float; v2 reads the float's shortest decimal text — the
digits the author wrote — because the binary value was already not the amount they meant.

**What to do.** Nothing is required. But if you hold money in `number`, this is the release
to stop:

```js
// before
const total = amount + fee;
el.textContent = BES.formatAmount(total);

// after — exact, and cross-currency arithmetic is rejected rather than coerced
const total = BES.Money.parse(amount, "AED").add(BES.Money.parse(fee, "AED"));
el.textContent = total.format();
```

Use `allocate()` rather than dividing when splitting an amount — it distributes the remainder
so the parts sum to exactly the whole. Any operation that could lose a minor unit now needs an
explicit rounding mode (`half-even` for computation, `half-up` for display) or it returns an
invalid Money, which renders `—` rather than a plausible wrong number.

**New in v2 and worth adopting:** `format({ locale: "ar-AE", numerals: "arab" })` renders
Eastern Arabic numerals. v1 could parse them and had no way to produce them.

---

## 3–4. One state namespace, one name per state

**What changed.** Transaction lifecycle colours now live in `transaction.*` and nowhere else.
The duplicates are **removed**:

| Removed | Replace with |
|---|---|
| `--bes-status-pending` | `--bes-transaction-pending` |
| `--bes-financial-pending` | `--bes-transaction-pending` |
| `--bes-financial-completed` | `--bes-transaction-completed` |
| `--bes-financial-failed` | `--bes-transaction-failed` |
| `--bes-financial-refunded` | `--bes-transaction-refunded` |
| `--bes-financial-reversed` | `--bes-transaction-reversed` |
| `--bes-financial-reversedTint` | `--bes-transaction-reversedTint` |
| `--bes-financial-blocked` | `--bes-transaction-blocked` |

`financial.*` now carries value semantics only — what an amount *means* (`income`, `expense`,
`negative`, `reserved`) — and `status.*` is for generic UI status: form validation, banners,
alerts. Not transactions.

The terminal success state is **`completed`**, not `success`. Doc 07's diagram was the only
artefact that said otherwise; the token, the class, doc 15 and the customer-facing string all
said *completed*.

```html
<!-- v1 --> <div class="bes-result bes-result--success">
<!-- v2 --> <div class="bes-result bes-result--completed">
```

```bash
# find every affected reference in your product
grep -rn "financial-pending\|financial-completed\|financial-failed\|financial-refunded\|\
financial-reversed\|financial-blocked\|status-pending\|bes-result--success" src/
```

---

## 5. Render states with `data-bes-state`

**What changed.** All 13 canonical states ship as components. Colour, glyph and label come
from one registry (`BES.TRANSACTION_STATES`).

```html
<!-- v1: hand-rolled, and this is the bug — "Refunded" rendered identically to "Completed" -->
<span class="bes-badge bes-badge--success">Refunded</span>

<!-- v2: name the state, get the rest -->
<span class="bes-badge" data-bes-state="refunded"></span>
```

**This one is silent.** Your old markup still renders — with the wrong colour and no glyph,
and in a hue that collides with a different state. `tools/audit-states.py` check **S9** finds
these: it flags any badge whose visible label is a canonical state name but whose class is a
generic status variant.

Result screens work the same way, and encode doc 07's prime directive:

```html
<div class="bes-result" data-bes-state="unknown">
  <div class="ic"></div><h3></h3><p class="money-state"></p>
  <button data-bes-retry>Try again</button>   <!-- REMOVED at bind time -->
</div>
```

A `[data-bes-retry]` control is stripped from any state that is not a confirmed failure. A rail
that has gone quiet may still be holding a successful transfer; retry is a double-send. If your
product renders its own retry affordance on an UNKNOWN result, **remove it** — the binder only
sees controls carrying that attribute.

---

## 6. The type scale was rationalised

**What changed.** `bes.css` carried 93 hardcoded font sizes across 13 distinct values, six of
which were not in the type scale at all. All 93 now read the scale or a component token, which
is what makes a brand able to retune type. Three real steps were added (`bodyMd` 15, `bodyXs`
13, `micro` 11) and the half-pixel sizes collapsed onto them.

**Sizes that moved:** 12.5 → 12 · 13.5 → 13 · 14.5 → 14 · 17 → 16 · 22 → 20 · 10 → 11.

Nothing breaks; some text is up to 2px different. If you have pixel-comparison screenshot tests,
expect to re-baseline. If you overrode BES type sizes in your own CSS, check those overrides are
still doing what you intended.

**New:** `border-radius` and all raw colour are also fully tokenised, and the component tier
(`--bes-button-radius`, `--bes-cardArt-ink`, and 28 others) is emitted. See
`docs/system/06-token-architecture.md` §3 and the worked brand at `brand-proof.html`.

---

## 7. The currency input needs its context line

**What changed.** v1 set `aria-invalid="true"` and wrote the reason into an element with no
`id`, no live region and no association — so a screen-reader user heard the field become
invalid and never learned why (WCAG 3.3.1 and 4.1.3, both failing).

v2 wires it at bind time. Your markup needs the context line present inside the field:

```html
<div class="bes-field">
  <input class="bes-input" data-bes-currency data-max="25000" data-currency="AED">
  <div class="bes-context-line">Available AED 25,000.00</div>   <!-- required -->
</div>
```

BES adds the `id`, the `aria-describedby` and `role="status" aria-live="polite"`. If the context
line is missing, validation messages have nowhere to go. Also: an empty field is no longer marked
`aria-invalid` — incomplete is not an error.

---

## 8. Balance masking changed shape

`bes.js` now wraps the masked value in `.bes-mask-val` at bind time and hides it with
`display:none`, plus a visually-hidden `[data-mask-sr]` span for assistive tech. In v1 the CSS
targeted element children while amounts are authored as bare text nodes, so **"Hide balance"
displayed the balance in full** while reporting success.

No markup change is needed — the JS adapts your existing `<bdi id="…"><span class="cur">AED</span>
25,000.00</bdi>`. But if you styled `.bes-masked > *` yourself, that selector no longer matches.

---

## Verifying your migration

```bash
npm ci
npm run gates      # build → tests → DOM tests → audits, in the order CI runs them
```

The gates that will catch a partial migration:

- **`tools/audit-consistency.py` C1** — any `var(--bes-…)` you reference that no longer exists.
- **`tools/audit-states.py` S9** — any badge still labelled with a state but styled generically.
- **`tools/audit-contrast.py`** — 78 declared pairings plus every element colouring in your
  pages, scored per brand.

If you maintain a fork of `bes.css`, note that font-size and radius literals are now held at
**zero** by C8; a new literal fails the build rather than warning.

---

## What did not change

- Every component class name except `bes-result--success`.
- `BES.init()` and the `data-bes-*` binding model.
- The density, scheme and direction attributes on `<html>`.
- The accessibility contract — it got stricter, not different.
