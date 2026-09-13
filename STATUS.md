# Component & Pattern Status Registry

The single source of truth for what is actually ready. Statuses per GOVERNANCE.md:
**Specified** (docs only) → **Coded** (in bes.css/js, audits pass) → **Trial** (one human-protocol pass) → **Stable** (screen-reader + Arabic passes; usability evidence for money-moving patterns).

_Last updated: 2026-08-31 (post-1.0.1 independent review). Nothing is Trial/Stable yet — human
protocols are written and awaiting testers (docs/testing/). Five defects that all three automated
gates passed through are fixed in `[Unreleased]`, and the gates themselves now derive from the
artefacts rather than from hand-written lists (see CHANGELOG). **"Coded" still means the component
exists, the gates pass and its behaviour is exercised in jsdom — not that a human has used it.**
Trial and Stable remain gated on the human protocols in docs/testing/._

## Foundations

| Foundation | Spec | Status | Notes |
|---|---|---|---|
| Color · Typography · Spacing & layout · Motion | 01–03, 05 | **Coded** | Emitted as tokens; contrast gated per brand |
| **Icon set** | 04 | **Specified** | **No icon assets ship.** Doc 04 defines the 24px construction grid, ~20 required financial glyphs (transfer, remittance, FX, fee, hold, refund, reversal, split bill, request money, QR pay, instant…), the RTL mirroring policy and the accessible-name rules — but the repository contains **zero SVG assets**. Components inline the few glyphs they need or expect the consumer to supply them. Drawing the set is outstanding design work, not a build step. |
| Design-tool library (Figma) | — | **Specified** | Blueprint written (`docs/figma-build-spec.md`) — variables, styles, component pages. No library file has been built, so BES is currently adoptable by engineers but not by designers working in Figma. |

## Core components

| Component | Spec | Status | Notes |
|---|---|---|---|
| Button (all variants) | 08 | **Coded** | |
| Icon Button | 08 | **Coded** | |
| Link / Menu / Button Group | 08 | Specified | Menu styles coded; behavior partial |
| Text Input + form primitives | 09 | **Coded** | |
| Currency Input | 09 | **Coded** | Live validation, Arabic-digit parsing |
| Search | 09 | Specified | Compose from Text Input |
| Select | 09 | **Coded** | Styled native |
| Combobox | 09 | **Coded** | Filter + keyboard |
| Date Picker | 09 | **Coded** | Processing-day blocking; range variant Specified |
| Checkbox / Radio / Switch | 09 | **Coded** | |
| PIN Entry / Code Entry | 09 | **Coded** | |
| Character Count | 09 | **Coded** | |
| File Upload | 09 | **Coded** | UI states; transport is host-app concern |
| App Bar / Bottom Nav / Side Nav | 10 | Specified | Journey bar coded as instance |
| Tabs | 10 | **Coded** | RTL-aware keyboard |
| Segmented Control | 10 | **Coded** | |
| Breadcrumb / Pagination | 10 | **Coded** | |
| Stepper | 10 | **Coded** | Display + journey logic |
| Language Switcher / Session Bar | 10 | Specified | Language switch proven in showcase/journey |
| Card / List / List Item | 11 | **Coded** | |
| Table (+ sorting) | 11 | **Coded** | |
| Accordion | 11 | **Coded** | |
| Modal / Bottom Sheet | 11 | **Coded** | |
| Drawer | 11 | **Coded** | |
| Popover / Tooltip | 11 | **Coded** | |
| Alert / Banner / Toast | 12 | **Coded** | |
| Status Badge | 12 | **Coded** | 13 transaction states + generic UI status, glyph-paired |
| Progress / Skeleton / Spinner | 12 | **Coded** | |
| Empty / Loading / Error states | 12 | **Coded** | |

## Financial components

| Component | Spec | Status | Notes |
|---|---|---|---|
| **Money value type** | 13 | **Coded** | Exact minor units · 7 rounding modes · `allocate` · Intl rendering · Eastern numerals |
| **Component token tier** | 06/30 | **Coded** | 30 tokens · zero literals in bes.css · proven by the Sadu brand (`brand-proof.html`) |
| Amount (all variants) | 13 | **Coded** | Renders a Money; no component holds a float |
| Amount Pair (FX) / FX Rate | 13 | **Coded** | In journey + gallery |
| Rate Lock Timer | 13 | **Coded** | Expiry → re-quote proven in journey |
| Masked Balance | 13 | **Coded** | Class-based, 30s auto re-mask; cross-surface sync is host-app wiring |
| Fee Line / Breakdown / Total Row | 13 | **Coded** | |
| Amount Delta / Limit Indicator | 13 | **Coded** | |
| Account Card / Balance Set / Selector | 14 | **Coded** | Selector = Select instance |
| IBAN Display / Product Header / Spaces | 14 | Specified | IBAN input coded; display partial |
| **Transaction state (all 13, incl. UNKNOWN / blocked / refunded)** | 07/15 | **Coded** | `data-bes-state` reads one registry: colour, glyph, EN+AR label. UNKNOWN cannot render a retry control |
| Transaction Item / List / Table / Detail | 15 | **Coded** | Detail composed in journey/receipt |
| Transaction Timeline / Receipt | 15 | **Coded** | Receipt printable |
| Statement Row / Search & Filters | 15 | Specified | |
| Payee Card / Beneficiary Manager | 16 | **Coded** (journey) | Manager list = journey payee list |
| **Payee Verification (name check)** | 16 | **Coded** | All four states (match / close / no-match / unavailable) |
| Transfer Review / Auth Prompt / Results | 16 | **Coded** | Full contract in journey |
| Scheduled Setup / Request-to-Pay / QR / Split / Bills | 16 | Specified | |
| Card Art / Controls / Freeze / Limits | 17 | **Coded** | PIN mgmt / replacement / dispute Specified |
| KFS Product Summary | 18 | **Coded** | |
| Rate & Profit Rate Displays / Calculator / Schedule | 18 | Specified | Schedule table styles coded |
| Investments family | 19 | Specified | Charts coded (bar/line/donut) |
| Identity & Security family | 20 | Partial | Session-pause, device cards, warning tiers coded; document capture / liveness UI Specified |
| Consent & Privacy family | 21 | **Coded** (request card) | Dashboard/revocation Specified |

## Patterns (highlights)

| Pattern | Status | Evidence |
|---|---|---|
| P-01 Ask for an amount | **Coded** | Journey step 1 |
| P-02/03 Ask for a payee | **Coded** | Journey step 2 |
| P-21 Confirm a payment | **Coded** | Journey review |
| P-22 Verify a payee | **Coded** | Journey CoP |
| P-23 Step-up auth | **Coded** | Journey PIN (biometric/passkey host-app) |
| P-31 Receipt & proof | **Coded** | Journey receipt |
| P-40 Transaction status | **Coded** | All 13 states as components; UNKNOWN/blocked/refunded result screens in the gallery |
| P-60 Suspicious transaction challenge | **Coded** | Gallery patterns page |
| Remaining patterns (P-04…P-75) | Specified | |

## Verification ledger

| Gate | Status |
|---|---|
| Contrast audit — 78 declared pairings (incl. all 13 state-on-tint) **+ 1,582 derived per brand** (core + Sadu = 3,164) | ✅ Passing (docs/audits/contrast-report.md) |
| **Brand theme contract (doc 30, T1–T6)** — one worked brand, token values only | ✅ Passing (docs/audits/theme-report.md) |
| **Transaction state contract (doc 06 §6, S1–S7)** — 13 states agree across spec, tokens, CSS and JS | ✅ Passing (docs/audits/state-report.md) |
| Consistency audit (drift · C7 theme-guard · C8 font-size/radius at zero, spacing ratcheted) | ✅ Passing (docs/audits/consistency-report.md) |
| Money/text unit tests (147 assertions, incl. the Money value type) | ✅ Passing (`node tools/test-js.mjs`) |
| Component DOM tests in jsdom (83 assertions) | ✅ Passing (`node tools/test-dom.mjs`) — also generates the runtime snapshots the contrast audit scores |
| Whole suite re-run in a UTC+ timezone | ✅ Passing (`TZ=Asia/Dubai`) |
| CI gates (all of the above on every PR) | ✅ `.github/workflows/ci.yml` |
| Adversarial scrutiny (3 independent reviews, 88 findings triaged) | ✅ docs/audits/scrutiny-report.md |
| Static a11y audit (51 files) | ✅ Passing (docs/audits/a11y-report.md) |
| Screen-reader protocol | ⏳ Written, awaiting tester |
| Arabic/RTL native review | ⏳ Written, awaiting reviewer — **all Arabic UI copy (showcase, journey, glossary) is machine-drafted and flagged as unreviewed in-product until this passes** |
| Remittance usability test (5 sessions) | ⏳ Written, awaiting participants |
| Compliance counsel review | ⏳ Matrix ready (docs/compliance/) |
