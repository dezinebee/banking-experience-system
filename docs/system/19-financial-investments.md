# 19 — Financial Components: Investments & Wealth Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Components: Portfolio Summary · Holding Item · Holdings List · Allocation Display · Performance Display · Risk Indicator · Investment Product Card · Order Ticket · Investment Transaction Item · Deposit/Term Product Card · Watchlist Item · Disclosure Footer.

Cross-cutting rule: **investment surfaces are the only place gain/loss red-green is fully in force** (doc 13, Amount Delta) — and every performance figure carries its timeframe and basis. Nothing here constitutes advice UI: the system renders information and execution, and its content patterns avoid advisory framing unless the institution's licensed advisory layer supplies it.

---

## Portfolio Summary

**Anatomy:** total value (`amount.hero`, maskable) · invested vs cash split · Amount Delta (period selector-linked: 1D · 1M · YTD · 1Y · All) · unrealized P&L (labeled "unrealized") · currency note (portfolio base currency; holdings in other currencies marked converted).

**States:** market-open (live-ish, refresh cadence stated) · market-closed ("As of close, 29 Aug") · stale/degraded (timestamped) · loading (skeleton, no zero-flash).

**Rule:** delta defaults to a *longer* timeframe (1M) rather than 1D — the system does not manufacture daily anxiety; 1D remains one tap away.

---

## Holding Item

**Anatomy:** instrument (symbol + name + logo slot) · quantity + avg cost · current value (Amount) · Amount Delta (period-linked) · weight in portfolio (%).

**Variants:** equity/ETF · fund (NAV-dated: "NAV as of 28 Aug") · sukuk/bond (yield + maturity) · gold/commodity (units + karat where physical) · crypto (where licensed; volatility banner tier applies).

**States:** default · price-stale · suspended (trading halted, explained) · corporate-action pending (badge + notice).

**A11y:** row summary: "Emaar Properties, 200 shares, value 1,840 dirhams, up 2.1 percent this month".

**RTL:** numerics LTR end-aligned; symbol stays Latin; name localized where listed bilingually.

---

## Holdings List

Grouped by asset class with class subtotals · sort (value/performance/weight) · Table transform on desktop · export.

---

## Allocation Display

**Anatomy:** proportional visualization (donut/stacked bar — chart rules doc 26) · legend with **values and percentages as text** (the chart is never the only representation) · drill per class · target-vs-actual overlay where a plan exists ("Equities 68% — target 60%", drift flagged neutrally).

**A11y:** data table equivalent behind "View as table"; patterns/labels not color-only.

---

## Performance Display

**Anatomy:** line/area chart with period selector · basis toggle where relevant (value vs % · with/without contributions — "time-weighted" labeled in plain language: "Performance excluding your deposits") · benchmark comparison optional (named, dated) · summary stats (best/worst period honest pairing).

**Rules:** y-axis never truncated to exaggerate movement without a zero-baseline indicator; past-performance disclaimer in Disclosure Footer, not fine print.

---

## Risk Indicator

**Anatomy:** scale position (1–7 or Low/Medium/High per product regime) · plain meaning ("Medium risk: value moves noticeably; you could get back less than you invest") · basis link ("How we rate risk").

**Variants:** product-level (on Product Cards, mandatory before order) · portfolio-level (aggregate) · profile-match (product risk vs the user's assessed profile: mismatch triggers the caution tier — "This is riskier than your profile" with the assessment path).

**Rule:** never color-only; the meaning sentence always renders.

---

## Investment Product Card

**Anatomy:** name + type · Risk Indicator · headline figures per type (fund: NAV, TER, 5y performance; sukuk: profit rate, maturity; deposit: rate, term) · minimum investment · fees line ("Total annual cost ~1.2%") · **Shari'ah-compliant badge** where certified (with certifier) · Key Information document link (PDF).

**States:** open · closed-to-new · coming-soon · restricted (eligibility: professional-investor gates explained, not hidden).

---

## Order Ticket (buy/sell)

**Purpose:** money-movement contract applied to investing.

**Anatomy:** instrument + live/indicative price (stamped: "Indicative — final price at execution") · order type (market/limit with plain explanations: "Market: executes now at the best price, which may differ from what you see") · quantity or amount entry (either-driven, other derived) · estimated cost/proceeds + fees (Fee Breakdown: commission, spread note, FX line for foreign instruments) · settlement date · review → consequence statement ("Market orders can't be cancelled once executed") → verb CTA ("Buy ~AED 5,000.00 of Emaar") → step-up auth per policy → Result states (filled / partial-fill explained / pending / rejected with reason).

**States:** market-open · market-closed (queued-order explanation: "Executes when the market opens Sunday 10:00") · price-moved-since-review (re-confirm threshold: reprice + highlight) · insufficient-funds (fund-first path).

---

## Investment Transaction Item

Transaction Item specialization: adds instrument, quantity @ price, fees, settlement status (executed → settled), corporate-action rows (dividend/profit distribution credited, splits) with plain descriptions.

---

## Deposit / Term Product Card (savings side)

**Anatomy:** rate presentation per structure (conventional APY / Mudarabah expected-profit with ratio + "indicative" honesty) · term + maturity date · early-withdrawal consequence stated upfront ("Withdraw early: you receive the base rate of 0.5% instead") · maturity instruction selector (renew / pay out — default *pay out*, never silent auto-renewal without notice; renewal notice event at T-7 days).

---

## Watchlist Item

Instrument + price + delta + add-to-portfolio path; alerts (price above/below — Currency Input) with notification-category routing (product, not marketing).

---

## Disclosure Footer

**Anatomy:** standard block on all investment surfaces: capital-at-risk statement ("Investments can fall as well as rise; you may get back less than you invest") · past-performance line where charts exist · licensing line (institution-configurable) · **not** collapsed on first view, standard body size (no fine print).
