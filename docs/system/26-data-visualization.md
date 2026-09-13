# 26 — Financial Data Visualization System

**Banking Experience System (BES)** · v2.0.0-draft

Charts in BES answer financial questions; they are information, not decoration. Every chart must remain understandable without color, and every chart has a text/table equivalent.

---

## 1. Chart components

| Component | Question it answers | Form |
|---|---|---|
| Balance Chart | "How has my balance moved?" | Line/area, time axis |
| Cash-flow Chart | "What came in vs went out?" | Paired columns (in/out) per period + net line |
| Spending Breakdown | "Where did it go?" | Donut (≤6 slices + Other) or horizontal bars (preferred ≥5 categories) |
| Category Trend | "Is dining growing?" | Small-multiple lines or bars per category |
| Budget Progress | "How much is left?" | Progress bar + remaining figure |
| Goal Progress | "How close am I?" | Progress + projection marker (est.) |
| Income vs Expenses | "Am I ahead?" | Grouped columns + net annotation |
| Portfolio Chart | "How is my portfolio doing?" | Line with period selector, basis toggle |
| Asset Allocation | "What am I holding?" | Donut/stacked bar + table legend |
| Loan Repayment | "How does my balance amortize?" | Stacked area (principal/profit split) + schedule table |
| Interest/Profit Breakdown | "What does this cost over time?" | Stacked columns per period |
| Credit Score Display | "Where do I stand?" | Sourced gauge + band label + factors list (real bureau data only) |
| Financial Health | "Am I okay?" | Composite indicators with plain-language basis (P-49) |
| Transaction Heatmap | "When do I spend?" | Calendar heat grid (with value labels on focus) |
| FX Rate History | "Is this a good rate?" | Line + current-rate marker + period high/low |

## 2. Chart selection rules

- Time → line/area. Composition → donut (≤6) or bars. Comparison → bars (never pie). Flow → paired columns. Single value vs target → progress.
- Sparklines (in cards/rows) show *shape only* — no axis implied precision; always paired with the actual current figure.
- 3D, gauges-as-decoration, dual-y-axes (except FX pair contexts with explicit labeling) are banned.

## 3. Color & accessibility

- **Categorical palette** (dedicated, ordered for adjacent distinguishability): `chart.cat1 #1F52C4` · `cat2 #0F6974` · `cat3 #8F5F0E` · `cat4 #5A3DA0` · `cat5 #0B7A45` · `cat6 #A82E1F` · `cat7 #55617A` — plus pattern fills (dots/hatch) engaged automatically in high-contrast mode and print.
- Status colors (success/error) are **not** chart categories; performance charts may use `financial.income`/`financial.negative` for gain/loss areas only.
- Every series distinguishable by ≥2 channels (color + marker shape/pattern/direct label). Direct labeling preferred over legends where space allows.
- **Text equivalent mandatory:** "View as table" on every chart; screen readers get a summary sentence ("Spending by category, August: Groceries AED 2,340 highest, seven categories, total AED 8,920") + the table.
- Interactive points keyboard-reachable; tooltips on focus; touch targets ≥44px via invisible hit areas.

## 4. Financial data rules

- **Axes honesty:** y-axis starts at zero for amounts; non-zero baselines (rate charts) show a break indicator + baseline label.
- Negative values plotted below a marked zero line, labeled with true minus; never clipped.
- Zero values render (a zero-spend month is data); missing data renders as a labeled gap ("No data") — never interpolated silently.
- Rounding: chart labels may abbreviate (AED 2.3K) but tooltips/tables carry full precision.
- Time periods labeled unambiguously ("Aug 2026", not "08/26"); comparison periods explicit ("vs Jul 2026").
- Projections/estimates: dashed + "estimated" label; never same treatment as actuals.
- Currency: single-currency per chart; multi-currency data converted with the conversion note ("All values in AED, converted at today's rate").

## 5. RTL behavior

- **Time axes stay LTR** (chronology reads left→right universally in charts; flipping time confuses more than it localizes) — documented as the deliberate exception; axis labels localize.
- Bar/column category axes mirror (first category at inline-start); donut rotation order mirrors; legends and labels mirror; numerals per locale policy.
- Heatmap weekday order follows locale week start.

## 6. Empty, loading, error

Loading: skeleton chart shape (no fake data motion). Empty: explanation + enablement ("Your spending breakdown appears after your first month of transactions"). Error: inline retry, cached-with-timestamp where available. Insufficient data (<3 points for a trend): show the table instead of a misleading line — the component downgrades itself.
