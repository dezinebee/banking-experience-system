# 24 — Patterns: Status, Tracking & Disclosure

**Banking Experience System (BES)** · Patterns · v2.0.0-draft

Showing users what is true: transaction states, balances, progress, documents, and the honest handling of uncertainty.

---

## P-40 · Show transaction status

**Use:** everywhere a transaction renders. **Structure:** canonical vocabulary only (doc 15 Transaction Status) at three zoom levels: badge (collections) → status line + money statement (detail header) → Timeline (multi-stage). State transitions notify per the category rules (doc 27).
**Prime rule restated:** UNKNOWN renders "We're checking your transfer status" + money-safety line — never a fabricated failure, never an eternal spinner.

## P-41 · Track a long-running process

**Use:** remittances, applications, disputes, card delivery, onboarding review. **Structure:** Timeline with per-stage expectations ("usually within 1 hour") · stalled-stage honesty (exceeded expectation → updated ETA + notify-me) · terminal resolution always announced (push + in-app) · reference number visible throughout.

## P-42 · Show a balance truthfully

**Use:** all balance surfaces. **Structure:** Balance Display/Set (doc 14): typed labels, available-first, current-vs-available explainer when they differ, holds drill-down, freshness timestamps on anything non-real-time, masked-mode support.
**Aggregation rule:** external-institution balances are visually distinct and freshness-labeled; mixed totals disclose composition.

## P-43 · Explain a rate honestly

**Use:** FX, deposits, financing. **Structure:** FX Rate + Rate Lock Timer (doc 13) for currency; Rate Display / Profit Rate Display (doc 18) for products. Invariants: estimated vs guaranteed always labeled; timestamps on quotes; expiry → explicit re-quote showing old→new; margin/fee split visible for FX; APR always accompanies headline rates; indicative profit never typeset as promise.

## P-44 · Progressive disclosure of financial detail

**Use:** dense objects (transactions, products, portfolios). **Structure:** three-layer rule — glance (list row: who/how much/state) → detail (facts block: everything relevant) → record (receipt/statement/contract PDF). Every fact reachable in ≤2 layers from glance.
**Boundary:** anything needed for a *decision* lives at or above the layer where the decision happens (fees never below the review layer; risk indicators never below the product card).

## P-45 · Present documents & statements

**Use:** statements, contracts, KFS, receipts, certificates (balance letters, IBAN letters, liability letters). **Structure:** Statement Access (doc 15) + document rows (type, period, format badges) · on-demand generation states · certificates request flow (purpose selector where fees vary, fee stated upfront, delivery: instant PDF vs processed) · all PDFs accessible (tagged, real text) · bilingual rendering per institution configuration.

## P-46 · Communicate holds & reservations

**Use:** card pre-auths, cheque holds, compliance holds. **Structure:** reserved amount in Balance Set + holds list (merchant/source, amount, placed date, **expected release date**) · plain explanations per hold type ("Hotels often hold more than the final bill — the difference releases automatically, usually within 10 days") · compliance holds use tipping-off-safe generic copy + support path.

## P-47 · Show spending insights (categorization)

**Use:** dashboards, monthly summaries. **Structure:** category breakdown (chart rules doc 26 + text equivalents) · month-over-month deltas in neutral tone (spend is not sin: "Dining AED 1,240.00 · AED 210.00 more than July" — no red shaming) · editable categorization (corrections train the view: "Move to Groceries") · insights are observations, not judgments; budgeting nudges only within user-created budgets.

## P-48 · Budget & goal progress

**Use:** budgets, savings goals (Spaces). **Structure:** Progress + remaining framing ("AED 460.00 left for Dining this month") · threshold notices at 80%/100% (informational tier, user-configurable) · goal projections labeled estimated ("On track for March 2027") · celebrations allowed at goal completion only.

## P-49 · Financial health snapshot

**Use:** opt-in wellness surfaces. **Structure:** composite view (spend vs income, buffer months, upcoming commitments) with plain-language basis for every signal ("Based on your last 3 months of salary and spending") · never scored publicly ("credit-score-like" gamification requires the real bureau product, clearly sourced: "Your Al Etihad Credit Bureau score, updated monthly") · improvement suggestions link to real actions, not products-in-disguise (product suggestions carry the marketing category, visually distinct).

## P-50 · Degraded & partial data

**Use:** rail outages, aggregation delays, market-data gaps. **Structure:** section-level honesty (the healthy sections stay fully functional) · stale data always timestamped, never silently old · unavailable actions disabled with reason + alternative ("Instant transfers are down — standard transfers still work, arriving next business day") · status-page link for prolonged incidents · recovery announced.

## P-51 · Empty & first-use states (financial)

**Use:** every collection (doc 12 Empty State variants). Financial specifics: zero-balance accounts render the number (AED 0.00) plus constructive next step; empty transaction history distinguishes "new account" from "no results in filter" from "period empty"; first-use states teach the one next action, not a feature tour.

## P-52 · Maintenance & service windows

**Use:** planned downtime. **Structure:** advance notice (banner, T-48h) with scope honesty ("Transfers unavailable Sat 02:00–04:00 — cards and balances keep working") · during: blocked actions carry the window end-time · after: quiet return (no fanfare needed).
