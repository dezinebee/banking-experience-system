# Changelog

All notable changes to the Banking Experience System. Format follows [Keep a Changelog](https://keepachangelog.com); versioning follows [Semantic Versioning](https://semver.org) as defined in GOVERNANCE.md.

## [Unreleased]

_Nothing yet._

## [2.0.0] — 2026-08-31

**Breaking release.** Migration guide: `docs/migrations/v1-to-v2.md`.

Post-1.0.1 independent review: five defects that every automated gate passed through. Four
were invisible to CI because they sat in the seam between CSS, JS and markup — the class of
defect a token audit, a static markup audit and a contrast audit all read past. The gates
have been widened so each one now fails on reintroduction (verified against negative controls).

> **Why MAJOR.** Per GOVERNANCE.md this release contains several MAJOR-class changes: a
> behaviour change (`parseAmount`), two markup contract changes (currency-input
> `aria-describedby`, `bes-result--success` → `--completed`), and token removals
> (`financial.pending` and the rest of the duplicated state colours). Several fail
> *silently* if a consumer skips them — which is precisely the failure mode this whole
> release is about — so the migration note is not optional reading.

### Fixed
- **Balance masking did not mask.** `.bes-masked > *:not(.cur)` matched element children,
  but amounts are authored with the digits as a bare text node inside `<bdi>` — so "Hide
  balance" rendered `AED 25,000.00•••••` while `aria-pressed` and the announcement both
  reported success, and the value stayed in the accessibility tree (`aria-label` on a
  `<bdi>` is ignored — a generic cannot carry a name). `bes.js` now wraps the value in
  `.bes-mask-val` on bind, the CSS hides it with `display:none`, and a visually-hidden
  `[data-mask-sr]` span carries the replacement text for assistive tech. A privacy control
  that silently did nothing is now the tested path.
- **`parseAmount` returned confident wrong numbers.** Negativity was detected by testing for
  a minus sign *anywhere* in the string and every non-digit was stripped and concatenated,
  so `"2026-08-31"` → `−20260831`, `"Ref-4471 AED 300"` → `−4471300`, `"AED 12 - fee"` →
  `−12`, `"1.234,56"` → `1.23456`. The documented "returns NaN for ambiguous input" contract
  was never true — nothing containing a digit ever returned NaN. Rewritten strict: leading
  sign only, comma grouping with a single dot decimal, currency affix at either end, Arabic
  separators and both Arabic-Indic digit ranges — everything else is NaN. **A wrong amount
  is worse than no amount, so it never guesses.** Numeric table sorting inherits the fix.
- **Toast and tooltip text was invisible in the default theme.** The system-preference branch
  `:root:not([data-theme="light"])` sat outside its `@media (prefers-color-scheme: dark)`
  query, so it also matched the un-stamped document every page ships — resolving toast text
  to `text.primary` on `surface.inverse`, contrast **1.00:1**.
- **Date picker lost keyboard focus at month boundaries in every UTC+ timezone**, including
  Asia/Dubai: arrow-key navigation derived the target day from a local `Date` and read it
  back through `toISOString()`, which converts to UTC — 1 August resolved to `2026-07-31`,
  the day button was not found, and focus fell to `<body>`. WCAG 2.1.1 / 2.4.3, failing in
  the primary market.
- **Currency-input errors were set but never communicated.** The control set
  `aria-invalid="true"` and wrote the reason into a context line with no `id`, no live region
  and no association from the field — in the gallery and the flagship journey alike (WCAG
  3.3.1 and 4.1.3). The context line is now given an `id`, linked via `aria-describedby`,
  and marked `role="status" aria-live="polite"` at bind time. Its original text is captured
  on bind so clearing the field restores it instead of leaving a stale, factually wrong
  message. An empty field is no longer marked invalid — incomplete is not an error.

### Gates now derive from the artefacts, not from lists

The five defects above shared one property: every automated gate passed them. Each gate
scored a *description* of the system — a hand-written pairing list, a grep for physical
properties, a set of pure functions — rather than the system. Three changes fix the class,
not the instances. All three were verified against negative controls: reintroduce the bug,
watch the gate go red.

- **Contrast audit is now computed from the artefacts.** Part A keeps the declared token
  pairings as a statement of intent (now 78, including all 13 state-on-tint pairs). Part B (new) parses `tokens.css`, `bes.css`, `site.css`
  and `gallery.css`, walks every element in every page, and resolves what each one *actually*
  renders — cascade order, specificity, scheme-scoped rules, `var()` chains, background
  inherited from the nearest ancestor that declares one. **60 hand-listed pairings → 1,582 computed element
  colourings, scored once per brand.** The v1.0.1 toast is caught by this at 1.00:1 with the
  offending selector named; the old audit could not see it because no line of the list
  described that combination. New helper: `tools/css_model.py`.
- **The audit also walks DOM snapshots**, because static files were never the whole system.
  The toast, the open combobox, its zero-results state, the date grid, the chart table
  equivalent — all are built by `bes.js` and exist in no HTML file, so no static gate had
  ever scored them. `tools/test-dom.mjs` now captures them to `docs/audits/dom-snapshots/`
  and the contrast audit reads that directory alongside `pages/` and `components/`. This is
  what actually closes the toast blind spot: deriving from the CSS was not enough while the
  element was never on disk to be scored.
- **Component DOM tests (`tools/test-dom.mjs`, 83 assertions in jsdom)** — the toast,
  combobox filtering and active-descendant, date-picker keyboard navigation across a month
  boundary, modal focus trap and focus return, PIN paste with Arabic-Indic digits, numeric
  table sorting with negatives, chart table equivalence, and tabs in both LTR and RTL.
  `jsdom` is a **test-time devDependency only**; `assets/` stays dependency-free.
- **Consistency audit C7** — fails any `:root:not([data-theme="light"])` rule outside a
  `prefers-color-scheme: dark` block, across all four stylesheets.
- **Consistency audit C8 — hardcoded-px ratchet.** Literal `font-size`, spacing and radius
  values in `bes.css` were counted against a committed baseline (93 / 136 / 5). Font-size and
  radius were subsequently retired to **zero** in this same release; spacing remains ratcheted. The count may
  fall and never rise: a new literal has to be paid for by removing an old one. It also names
  the 6 font sizes used in the CSS that are **absent from the type scale entirely** — those
  cannot be re-scaled by a brand theme and are not reached by the `:lang(ar)` optical metrics,
  which is why doc 30's multi-brand claim did not hold. Failing outright would have
  failed the build on day one and taught nobody anything; the ratchet keeps the real number
  visible in every report instead of buried in a review.
- **CI ordering is now load-bearing**: build → DOM tests (write snapshots) → audits (score
  them) → drift check. The drift check covers `docs/audits/` too, so a stale snapshot fails
  the build. `npm run gates` runs the same sequence locally.
- Added `package.json` (scripts + the one devDependency) — the repo had no manifest at all.

### Fixed by the new gates
Found by Part B and the DOM pass within minutes of them existing:
- **`text.disabled` was being used for live content in seven places** — struck amounts, list
  section headers, limit reset dates, timeline dots, paid schedule rows, notification
  timestamps and date-grid weekday headers — at **2.52:1** in light. None of it is disabled
  UI. Repointed to `text.secondary`. Worth stating plainly: there is no room in the palette
  for a third readable text tier — the gap between `text.secondary` and the 4.5:1 floor on
  tertiary surfaces is about 0.7 — so BES has two text tiers plus a disabled state, not three.
- **`action.primary` / `text.link` in dark mode sat at 4.49:1** on tertiary surfaces and
  **4.43:1** on the warning tint — both a hair under AA. Added primitive `blue.350` (#6B96F4)
  and repointed the two dark semantics; `text.onAction` on the new value is 5.58:1.
- **The combobox zero-results message was removed from the accessibility tree** by
  `role="presentation"` on a `listbox` child — a screen-reader user heard "0 results" and
  never "check the SWIFT code". Now `role="option" aria-disabled="true"`: valid as an owned
  child, still excluded from selection.
- **`aria-modal="true"` was never removed on close**, so a closed dialog kept telling
  assistive tech the rest of the page was inert. Removed in `trapClose`, which is the path
  Escape actually takes.
- **Disabled dates had no visual state**: the CSS styled `:disabled` while the JS emits
  `aria-disabled`, so non-processing days looked identical to selectable ones for sighted
  users. Selector now matches both.

### UNKNOWN, blocked and refunded ship as components, and one state namespace wins

The system's signature idea — that UNKNOWN is a designed state, because telling someone
their transfer failed when it may have succeeded is the most trust-destroying thing a
banking UI can do — existed as prose plus **one hand-built screen inside a single page**.
Meanwhile three artefacts disagreed about what the states even were: doc 07's contract
table defined 13, doc 06's prose listed 12, the tokens emitted 10, and **no component read
the state tokens at all**. So "Refunded" shipped styled as `--success`, pixel-identical to
"Completed", and UNKNOWN shipped as `--info`, identical to "Processing".

**One namespace.** `transaction.*` is now the only place a transaction state has a colour:
all 13 canonical states, each with a matching tint so a badge can be built from the state
alone. The duplicates are gone — `financial.*` keeps only value semantics (what an amount
*means*: income, expense, negative, reserved), `status.*` keeps generic UI status for form
validation and banners, and `status.pending` / `financial.pending` / `financial.completed`
and the rest are **removed**. Two namespaces for one concept is exactly why the state name
was not the stable API.

**One name per state.** Doc 07's diagram was the only artefact calling the terminal success
state `SUCCESS`; the token, the CSS class, doc 15's list and the customer-facing string all
said *completed*. Canonicalised on **`completed`**, and doc 07 updated.

**The components.**
- `.bes-badge--<state>` for all **13** states, each reading `transaction.<state>` and its tint.
- **A state registry, `BES.TRANSACTION_STATES`** — the colour, glyph, EN label, AR label and
  money statement for each state come from one table, so the product names only the state:
  `<span class="bes-badge" data-bes-state="unknown">`. Two screens cannot drift.
- `.bes-result[data-bes-state]` for the terminal screens, including **UNKNOWN, blocked and
  refunded** — previously only reachable by hand-writing the journey page.
- **Colour never carries a state alone.** `completed` and `refunded` share green;
  `processing`, `pending` and `unknown` share teal. That is deliberate — they are related —
  and it is why the glyph and label come from the registry rather than the caller. Each
  state carries a distinct glyph, so the two collisions above are now visually separable.

**Doc 07's prime directive is now behaviour, not prose.** A `.bes-result` whose state has
`allowsRetry: false` has any `[data-bes-retry]` control **removed at bind time**, with a
console warning citing the doc. A rail that has gone quiet may still be holding a successful
transfer; retry is a double-send, and a missing button is the smaller failure. Only a
confirmed `failed` keeps it.

**`tools/audit-states.py` (new) makes doc 06's claim falsifiable.** It takes doc 07 §4's
contract table as the single source of the state list and fails the build unless every state
has a colour token, a tint, a badge variant reading those tokens, a registry entry with a
glyph and both labels — and unless no state colour lives in a second namespace. It also
asserts the prime directive as a property of the data: UNKNOWN may not allow retry, only a
confirmed failure may, and something must enforce it at runtime. Six negative controls verify
each rule fails when broken. The audit found the `success`/`completed` collision within
seconds of existing.

Also: the contrast contract now asserts **all 13 state-on-tint pairings** rather than the
four someone happened to list — which is how "refunded" went unchecked while styled as
success. That found `authenticationTint` sitting at 4.49:1 in dark under a brand that shifts
the hue; the tint moved to one with headroom, because a tint that only works for one palette
is the system's problem, not each brand's. Consistency C5 also stopped miscounting
`classList.add("bes-badge--" + name)` as a class named `.bes-badge--`.

### The component token tier ships, and the multi-brand claim is finally tested

Doc 06 named a COMPONENT tier and marked it "reserved". Doc 30 stated the acceptance test —
*"a brand change is describable entirely as token values… if it requires touching component
internals, it's rejected"* — and nothing had ever tried. Meanwhile `bes.css` carried **93
hardcoded font sizes**, six of which were not in the type scale at all, so the `:lang(ar)`
optical metrics reached almost nothing and no brand could have retuned type without editing
component rules. The claim and the code disagreed.

**The tier is now emitted, and it is deliberately small: 30 tokens, not 93.** A token per
declaration would be a rename with extra steps. The rule is that a component token exists
where a brand needs to retune *one component* without moving a shared scale — a button's
silhouette, a card's corner, the card face's ink. Everything else reads the shared scales
directly. The test for adding one: *could a brand want this different from everything else
that currently matches it?* `--bes-alert-fontSize` fails that; `--bes-button-radius` passes.

- **93 → 0 font-size literals; 5 → 0 radius literals; all raw colour gone from `bes.css`.**
  The type scale gained three real steps (`bodyMd` 15, `bodyXs` 13, `micro` 11) and the
  half-pixel sizes collapsed onto it. **This changes rendering slightly** — 12.5/13.5/14.5px
  round down 0.5px, 17px → 16px, and the two 22px dialog headings become 20px (`h3`). That is
  the point: a scale with 13 distinct sizes across 93 declarations was not a scale.
- **`--bes-font-arabic` was emitted and consumed by nothing.** Arabic surfaces now lead with
  the Arabic face (`.bes:lang(ar)`), so a brand can change its Arabic type at all.
- **The card face was the last literal holdout** — gradient, ink, badge and frozen states are
  now `cardArt.*` tokens. The Latin tracking that broke Arabic cursive joining is a token too,
  set to `0` under `:lang(ar)`, so no rule has to win a specificity fight to undo it.
- Emission moved to `tokens/emit.py`, shared by the core and brand compilers — a brand can
  never be built by different rules than the core it overrides.

**One worked second brand, because until a theme exists the contract is untested.**
`Sadu` (`tokens/themes/sadu.json` → `assets/themes/sadu.css`) is a **fictional** Islamic-finance
neobank, built to sit as far from core as the contract allows: deep green not blue, squared not
rounded, serif Latin + Naskh Arabic, comfortable density as its standard, slower motion, gold on
green. Side by side with core at **`brand-proof.html`** — same markup, same `bes.css`, byte for
byte. **The cost in component CSS was zero lines.** The brand is **111 token values and no rules**,
5.2 KB.

**Three gates, each verified against a reintroduced failure:**
- `tools/audit-theme.py` (new) — T1–T6: a theme file may contain custom properties only, every
  selector must carry the brand scope, no `@font-face` or other machinery, no token core does not
  define, and the generated CSS must still match its JSON source.
- `tools/audit-contrast.py` now runs the full derived audit **once per brand** (3,092 element
  colourings). A brand that breaks AA fails the build — Sadu was caught doing exactly that during
  development, when a lighter, friendlier green dropped the pressed icon button to 2.11:1.
- Consistency **C8** holds `font-size` and `border-radius` at zero; **C4** dropped its card-art
  whitelist, so component CSS now carries no raw colour at all.

**The limit, stated rather than buried:** spacing is *not* tokenised. 135 padding, margin and gap
literals remain, because the space scale is a 4px grid while the CSS uses 6/10/14/18px throughout.
Closing it is a decision about the grid, not a substitution, and it would move every component's
rhythm. A brand can change colour, type, shape, density and motion; it cannot yet change spacing.
C8 keeps that number visible and only lets it fall.

### Money is now a value type, not a number

`BES.Money` holds an integer count of **minor units** plus a currency and its ISO precision.
`AED 1,250.50` is `{ currency: "AED", minor: 125050, precision: 2 }` — which is also the wire
form. Specified in `docs/system/13-financial-money.md`.

A balance is an exact quantity and IEEE-754 cannot hold one: `0.1 + 0.2` is
`0.30000000000000004`, and `8.165` rounded *down* because its nearest double is `8.164999…`.
The failure was silent, which is the problem — a total off by a fil looks exactly like a total
that is right, and it compounds through fee, FX and allocation arithmetic. Floats now appear at
one boundary only: a `number` handed in by a host app is read through its **shortest decimal
text** — the digits the author wrote — never its binary value.

- **Rounding is never implicit.** Any operation that could lose a fil needs a named mode:
  `half-even` · `half-up` · `half-down` · `up` · `down` · `ceil` · `floor`. Without one the
  result is an **invalid Money**, which renders `—` rather than a plausible wrong number.
  `multiply`/`divide` default to **half-even**, because rounding that runs over thousands of
  transactions must not be biased upward; `formatAmount` stays **half-up** for display, which
  is both the intuitive reading and its pre-existing contract.
- **Exact arithmetic**: `add` · `subtract` · `compare` · `multiply` (rate taken as decimal text,
  so 3.6730 is exactly 36730/10000) · `divide` · `negate` · `abs`.
- **`allocate(n | weights)`** — largest-remainder split whose parts sum to exactly the whole:
  AED 100.00 three ways is 33.34 / 33.33 / 33.33. Dividing and rounding each share invents or
  destroys fils, which in a split bill, a fee apportionment or a payroll batch is a
  reconciliation break.
- **Cross-currency arithmetic is invalid, not coerced.** AED + USD returns an invalid Money;
  conversion is an explicit `multiply` by a stated rate with a stated mode.
- **Ceiling is a wall, not a slope**: beyond `Number.MAX_SAFE_INTEGER` minor units (~90 trillion
  AED) a Money is invalid, never approximate. BigInt is the documented escape hatch if a
  treasury surface ever needs it.
- **Rendering through `Intl.NumberFormat`** — grouping, separators and numbering systems are
  locale data, not string manipulation. Sign and currency placement remain house rules: true
  minus `U+2212`, code before the amount, one bidi-isolated LTR run. Zero has no sign, so
  `−AED 0.00` can no longer appear.
- **Eastern Arabic numerals can finally be rendered.** BES has parsed ٠–٩ since v1.0.1 but had
  no way to produce them; `format({ locale: "ar-AE", numerals: "arab" })` gives `AED ٢٥٬٠٠٠٫٠٠`.
  Per doc 29 §2 this is a display-only preference requested per render — Western digits remain
  the default, and numerals are never mixed within a screen.
- **`toSpoken()`** — the accessible name doc 13 asks for ("minus 1,250.50 UAE dirhams"), from
  the same type rather than hand-written per component.
- **`formatCompact()`** for summaries and chart axes; doc 13 still bars abbreviation from
  authorize, review and receipt surfaces.

**Consumers routed through it, fixing three live defects:**
- The **currency input** did float subtraction on balances — "Leaves AED …" and "Exceeds by …"
  are now exact Money arithmetic, on the figure a user is about to authorise against.
- **Chart axis labels** used a hand-rolled abbreviator that printed `2K` next to the gridline
  for 1,500. Now `1.5K`, via the one money formatter.
- The **chart's own table equivalent** formatted with `toLocaleString()` — no currency, no
  precision — so it disagreed with the amounts beside it. Same formatter now.
- **Numeric table sorting** compares exact minor units instead of parsed floats.

`formatAmount` and `parseAmount` keep their signatures and route through Money, so there is one
implementation of money formatting in the system — which is what doc 13 says there must be.
`formatAmount` now also accepts a decimal string or a Money (it previously returned `AED —` for
`"1250.5"`, discarding exactly the representation a careful backend would send).

### Added
- `BES.localISO(date)` — derives a calendar date key from local fields. `toISOString()` must
  never be used for a calendar date.
- Primitive `blue.350` (#6B96F4) — the dark-scheme action/link value that clears AA on
  tertiary surfaces and tinted backgrounds.
- `tools/mini-dom.mjs` — a dependency-free DOM harness (~150 lines) so behaviors can be bound
  and driven in Node. Four of the five defects above were unreachable by a pure-function
  suite; masking and the currency input now have real DOM coverage.
- Consistency audit **C7**: fails any `:root:not([data-theme="light"])` rule outside a
  `prefers-color-scheme: dark` block, across all four stylesheets.
- CI runs the test suite a second time under `TZ=Asia/Dubai`; the date-picker regression is
  invisible in UTC.

### Changed
- Unit tests: **37 → 77 assertions**, now covering the reproduced defects and their DOM paths.
  Each new test was verified against a negative control — reverting the fix fails the test.
- Licensed the repository under **MIT** (was: all-rights-reserved placeholder).

### Known behavior change
- `parseAmount("1.234.567.89")` now returns `NaN` (was `1234567.89`). Multi-dot input is
  locale-ambiguous — `1.234,56` is one-thousand-two-hundred-and-thirty-four in most of
  Europe and one-point-two-three in the previous implementation. Callers that need European
  input must normalize before parsing; the currency input already normalizes keystrokes.

## [1.0.1] — 2026-08-31

Scrutiny release: three independent adversarial reviews (front-end code quality, ARIA/keyboard accessibility, architecture) produced 88 findings; every code-level CRITICAL/HIGH and the majority of MEDIUMs are fixed. Full report: `docs/audits/scrutiny-report.md`.

### Security
- **Fixed XSS in the remittance journey**: all user-derived values (payee name, account digits) now pass through `BES.esc()`; `$`-pattern-safe templating via `BES.tpl()`; chart labels escaped.
- Session-interrupt demo now uses the focus-managed `BES.openInterrupt` API (assertive announcement, focus trap, no swipe-dismiss).

### Fixed
- **Money correctness**: `parseAmount` now handles the true minus (U+2212), parenthesized negatives, Arabic decimal ٫ / thousands ٬ separators, and Extended Arabic-Indic digits — `parseAmount(formatAmount(x)) === x` is now a tested invariant; table sorting reuses it, so debits sort correctly. `formatAmount` rounds in minor units (no `2.675 → 2.67` float artifacts), guards NaN/Infinity, and resolves precision per ISO code (JPY 0, KWD/BHD 3).
- **Print no longer hijacked**: receipt print CSS is scoped to `body.bes-print-receipt`.
- **Leak-free dialogs**: shared focus-trap engine for modal/drawer/interrupt — per-element focus restore, live focusable computation, single scrim listener, drawer now traps and restores focus.
- Double-bind guards on every behavior (`BES.init` is safely re-runnable); countdown timers cleaned on re-render; toast stack capped with a persistent live-region host.
- Currency input: invalid input marks `aria-invalid` instead of leaving garbage; Eastern/Extended digits normalized live.
- Rate lock is now **enforced state**, not decoration: expiry blocks authentication, re-quote genuinely changes the rate, back-navigation can't renew a lock.
- Journey: step-0 amount gating; per-step focus + live announcements; hidden `h1`; CoP result live region; PIN errors announced (`role=alert` + `aria-invalid`); CSS spinner (reduced-motion safe); print via controller.

### Accessibility
- **Combobox**: full APG pattern — `listbox`/`option` roles, `aria-controls`, `aria-activedescendant`, click selection, Escape behavior.
- **Date picker**: roving tabindex with Arrow/Home/PageUp/PageDown navigation, full per-day accessible names, `aria-disabled` days keep their reason, month label announced, focus preserved across month changes.
- **Sortable tables**: real `<button>` headers (keyboard + AT operable) with visible sort indicators.
- **Switches**: `role="switch"` + live On/Off state word.
- PIN/code entry: paste allowed (WCAG 2.2 §3.3.8), `autocomplete="one-time-code"`, group labeling, `setError/clearError` API with assertive announcement.
- Shared polite/assertive live regions (`BES.announce`); mask toggle, sort, countdown milestones and step changes all announce.

### Added
- **CI** (`.github/workflows/ci.yml`): token build validation, docs build, generated-file drift check, all three audits, JS syntax, 37 unit tests, size budget.
- **Unit tests** `tools/test-js.mjs` (money round-trip, Arabic separators, escaping).
- Consistency audit `tools/audit-consistency.py` (undefined tokens, physical properties, raw hex, class drift).
- Token build hardening: unresolved references and missing light/dark values now **fail the build**; all primitive groups emitted; semantic values emit as `var()` chains so brand themes override primitives once and cascade.
- Emitted `transaction.*`, `verification.*`, `consent.*` state-color namespaces and `focus.width/offset` tokens; density now drives control/list padding.
- Fourth payee-verification state (`unavailable`) coded + demoed.
- Balance mask auto re-masks 30s after reveal (doc 13 contract).
- Versioned asset URLs (`?v=` stamped from `tokens.json`), build-time code-snippet fill (docs readable without JS), browser-support statement and hosting security notes.

### Changed
- Honest-tense pass over docs 06/09/29, README and STATUS: shipped vs reserved/planned is now explicit everywhere (component/pattern/product token tiers reserved; contrast & terminology dimensions planned; `data-theme` is the canonical attribute).

## [1.0.0] — 2026-08-31

First complete release of the system.

### Added
- **Strategy** (Phase 01): vision, principles, target users, UAE context, regulatory translation, reference analysis, experience architecture, taxonomy — 9 documents.
- **Specifications**: 31 documents — foundations (color, typography, spacing/layout, iconography, motion), token architecture, financial semantic layer (money display, FX, balance model, transaction state machine incl. UNKNOWN), ~60 core + ~50 financial components, 55 patterns (P-01…P-75), data visualization, content/notifications/error taxonomy, accessibility, localization/RTL, multi-brand theming.
- **Token package**: `tokens/tokens.json` source of truth → compiled `assets/tokens.css` (167 light tokens + dark scheme, 3 density modes, Arabic type metrics) via `tokens/build-tokens.py`.
- **Component library**: `assets/bes.css` + `assets/bes.js` — dependency-free; Waves 1–4 including Amount, Button, badges, alerts, form set, currency input with live validation, tabs, modal, toast, tables with sorting, combobox, date picker, drawer, accordion, popover/tooltip, breadcrumb, pagination, PIN/code entry, character count, upload, rate-lock countdown, amount delta, card art, risk indicator, SVG charts (bar/line/donut with table equivalents), timeline, receipt, session-pause interruption, journey shell.
- **Documentation site**: generated pages with embedded live examples (18 pages), unified sidebar, landing page; generator in `tools/build-docs.py` + `tools/demos.py`.
- **Component gallery**: 6 live-demo pages with theme/direction/density controls and auto-extracted code.
- **Showcase**: bilingual (EN ⇄ AR, full RTL) interactive specimen.
- **Proof-by-product**: `journey-remittance.html` — complete AED→INR journey (amount+FX → recipient + payee name-check → review + rate lock/expiry → PIN auth → processing → success/pending/unknown/failed results → printable receipt), fully bilingual.
- **Verification**: `tools/audit-contrast.py` (60 token pairings, light+dark — passing) and `tools/audit-a11y.py` (49 files — passing); reports in `docs/audits/`; human protocols (screen reader, Arabic/RTL review, usability) in `docs/testing/`.
- **Governance**: this changelog, CONTRIBUTING.md, GOVERNANCE.md, STATUS.md lifecycle registry, issue/PR templates.
- **Compliance**: traceability matrix mapping patterns to regulatory sources with review-status tracking (`docs/compliance/`).

### Changed
- `border.strong` demoted to decorative separators; new `border.input` token (≥3:1 both schemes) for functional control boundaries — found and fixed by the contrast audit.

### Security
- SMS OTP absent from the auth component set by design (regulatory sunset); Code Entry component documented as non-auth/legacy only.
