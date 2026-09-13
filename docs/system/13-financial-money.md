# 13 — Financial Components: Money Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

The most-used primitives in the system. Rules inherit from doc 07 (Financial Semantic Layer); this file defines the components.

Components: Amount · Amount Pair (FX) · Masked Balance · FX Rate · Rate Lock Timer · Fee Line · Fee Breakdown · Total Row · Amount Delta · Limit Indicator.

---

## Money — the value type

**Purpose:** hold an amount exactly. Every component in this document renders a Money; nothing in the system holds an amount as a `number`.

**Representation:** an integer count of **minor units** (fils, cents, paise) plus an ISO currency code and its precision. `AED 1,250.50` is `{ currency: "AED", minor: 125050, precision: 2 }`, and that object is also the wire form — it is what a bank API should exchange and what `toJSON()` produces.

**Why not a float.** A balance is an exact quantity, and IEEE-754 cannot hold one: `0.1 + 0.2` is `0.30000000000000004`, and `8.165` rounds *down* because its nearest double is `8.164999…`. The failure is silent — a total that is off by a fil looks exactly like a total that is right — and it compounds across fee, FX and allocation arithmetic. Floats appear at one boundary only: when a host app hands over a `number`, it is read through its **shortest decimal text** (the digits the author wrote), never its binary value.

**Precision** comes from ISO 4217 per currency: AED/USD/EUR/GBP/INR/SAR/PHP 2 · JPY/KRW/VND 0 · KWD/BHD/OMR/TND/JOD 3. A product never hardcodes 2.

**Rounding is never implicit.** Any operation that could lose a fil requires a named mode; without one the result is an **invalid Money**, which renders as `—`, not as a plausible number. Modes: `half-even` · `half-up` · `half-down` · `up` · `down` · `ceil` · `floor`.

- **`half-even` (banker's) is the default for computation** — `multiply`, `divide`. Rounding that runs over thousands of transactions must not be biased in one direction; half-up is.
- **`half-up` is the default for display** — the intuitive reading of a printed figure.
- Anything that *moves* money states its mode explicitly and records it. "Which way did we round?" is an audit question.

**Splitting money uses `allocate`, never division.** Largest-remainder distribution, so the parts sum to exactly the whole: AED 100.00 three ways is 33.34 / 33.33 / 33.33. Dividing and rounding each share loses or invents fils — in a split bill, a fee apportionment or a payroll batch, that is a reconciliation break.

**Ceiling:** `Number.MAX_SAFE_INTEGER` minor units — about 90 trillion AED, comfortably above any UAE balance. Beyond it a Money is **invalid, never approximate**. A treasury surface that needs more moves the representation to BigInt; it does not widen the tolerance.

**Cross-currency arithmetic is invalid, not coerced.** Adding AED to USD returns an invalid Money. Conversion is an explicit `multiply` by a stated rate with a stated rounding mode — never an implicit unit change.

**Rendering** goes through `Intl.NumberFormat`. Grouping, decimal separators and numbering systems are locale data, not string manipulation. Sign and currency placement stay house rules: true minus `U+2212` (never a hyphen), currency code before the amount, the whole amount one bidi-isolated LTR run in both directions. Zero has no sign — a rounded-away negative renders `AED 0.00`, never `−AED 0.00`.

**Numerals (doc 29 §2):** Western digits are the default for all financial figures. Eastern Arabic digits (٠–٩) are an explicit **display-only** preference, requested per render, never mixed within a screen — entry accepts both (doc 07 §6). Both directions now work: the system parses Eastern digits *and* renders them.

**Accessible name:** the spoken form, from the same type — "minus 1,250.50 UAE dirhams", not the glyph sequence.

**Abbreviation** (`25K`, `1.25M`) is a separate render mode, permitted in summaries and chart axes and **forbidden on authorize, review and receipt surfaces**. It reports the real number: an axis gridline at 1,500 reads `1.5K`, never `2K`.

---

## Amount

**Purpose:** render money. The single source of money formatting — raw text amounts anywhere in a product are lint failures. Its input is a Money.

**Anatomy:** optional sign · currency code (0.75×, weight 500) · integer (tnum) · decimals (optionally 0.6× top-aligned at lg/hero) · optional certainty marker (≈) · optional status pairing (icon+label via Status Badge).

**Variants (size):** `hero` 40 · `lg` 28 · `md` 20 · `sm` 16 · `meta` 13. **Variants (semantic):** neutral (default/expense) · credit (`financial.income`, `+`) · negative (`financial.negative`) · estimated (≈ + label) · masked.

**States:** resolved · loading (skeleton block, never 0.00) · stale (timestamped: "as of 14:32") · masked · error ("—" + "Couldn't load" + retry).

**Usage:** full precision on anything actionable; abbreviation (25K, 1.25M) only in summaries/charts and never on authorize/review/receipt surfaces. Sign always attached; color never alone (sign carries meaning for color-blind users).

**A11y:** accessible text is the *spoken* form ("minus 1,250 dirhams and 50 fils" locale-aware), not character-by-character; masked announces "balance hidden".

**RTL:** the whole amount is one LTR bidi-isolated run; placement follows logical alignment. Eastern Arabic digits render per locale preference, never mixed per screen.

**Example:** list row `−AED 89.50` · dashboard `AED 25,000.00` · converted `≈ ₹250,800.00`.

---

## Amount Pair (FX)

**Purpose:** dual-currency display — send/receive, charge/settle.

**Anatomy:** primary amount (what the user pays/receives in *their* decision currency) · secondary converted amount (`meta` size, ≈ when estimated) · rate reference line.

**Usage:** the charged currency is always primary (card FX: "**USD 500.00** ≈ AED 1,836.50 at 1 USD = 3.6730"). Order never swaps between screens of one flow.

**States:** estimated · locked (rate guaranteed, shows lock + expiry) · settled (final, no ≈).

---

## Masked Balance

**Purpose:** glanceable privacy — balances hidden by default per user preference across dashboard, lists, widgets.

**Anatomy:** currency code + bullet group (`AED •••••`) · reveal toggle (eye icon button).

**Behavior:** reveal per-tap (auto re-mask after 30s) or per-session, configurable; masking state syncs across surfaces; amounts under masking still expose *no* value to screen readers ("balance hidden — double tap to reveal"); kiosk surfaces force masked-by-default.

---

## FX Rate

**Purpose:** display an exchange rate with honest status.

**Anatomy:** rate expression ("1 AED = ₹25.0800", 4 significant decimals) · status: `estimated` ("rate may change") or `guaranteed` (lock icon) · timestamp ("rate at 14:32") · optional mid-market comparison line where available ("mid-market: ₹25.2100 — our rate includes a 0.5% margin").

**States:** live (auto-refresh with change flash — increase/decrease flash uses motion, then settles neutral) · locked · expired (struck through + re-quote prompt) · unavailable ("We can't quote this rate right now").

**Rule:** a rate presented as "our rate" without margin disclosure must at least link "How we set this rate". The structural fee/margin split lives in Fee Breakdown.

---

## Rate Lock Timer

**Purpose:** countdown for guaranteed rates.

**Anatomy:** lock icon · countdown ("Rate held for 4:59") · expiry behavior note.

**States:** active · warning (<60s: amber; screen readers get one polite announcement, not per-second) · expired (→ re-quote step; **never silent re-pricing**; the new rate is shown against the old: "Rate updated: ₹25.08 → ₹24.99").

**A11y:** timer is not the only mechanism — expiry always produces an explicit re-confirmation step, so slow users are never penalized by surprise.

---

## Fee Line

**Purpose:** one fee, named honestly.

**Anatomy:** label ("Transfer fee") · amount · optional info affordance ("why this fee?" → popover/sheet with plain-language explanation and the fee schedule link).

**Variants:** fee · FX margin · VAT line (5% where applicable, always broken out) · waived (struck amount + "Waived — Premium account") · third-party ("Correspondent bank fee — deducted from recipient amount, up to USD 15").

**Rule:** fees deducted from the *recipient* side are never hidden inside "recipient gets" — they are a labeled line with the uncertainty stated.

---

## Fee Breakdown

**Purpose:** the complete cost stack of a transaction or product. Mandatory before REVIEW in every money-movement flow (transparency-before-conversion is structural).

**Anatomy:** ordered Fee Lines · subtotal · Total Row · certainty markers per line · collapse behavior: **collapsed only after first full view** — first exposure is expanded.

**Example:**
```
You send                    AED 10,000.00
Transfer fee                AED 15.00
FX margin                   AED 20.00        (i)
VAT on fees (5%)            AED 1.75
────────────────────────────────────────
Total you pay               AED 10,036.75
Recipient gets              ₹250,800.00  (exact)
```

---

## Total Row

**Purpose:** the number the user commits to. `type.amount.lg`, separated by strong rule, labeled by consequence ("Total you pay today" / "Total repayment over 48 months") — never bare "Total" where the basis is ambiguous.

**States:** final · estimated (≈ + when it becomes final) · updating (brief highlight when upstream values change — users must *see* the total move).

---

## Amount Delta

**Purpose:** change indication (portfolio moves, balance vs last month, rate changes).

**Anatomy:** direction arrow + signed value + optional % ("▲ +AED 1,200.00 (4.8%)") · timeframe label ("vs July").

**Rules:** arrows + sign + color together (green up/red down for *investment performance only* — spend deltas stay neutral: spending more isn't morally red); zero delta renders "No change", not "+AED 0.00".

**RTL:** arrow glyphs unmirrored (up/down semantics); the block is an LTR run.

---

## Limit Indicator

**Purpose:** show limits before they bite: daily transfer limits, card spending limits, instant-rail caps (AED 50,000).

**Anatomy:** label ("Daily transfer limit") · progress bar (used/remaining) · figures ("AED 32,000.00 used of AED 50,000.00") · reset note ("Resets at midnight") · optional raise-limit path.

**States:** normal · approaching (≥80%, amber) · reached (input-blocking with explanation and alternatives: "You've reached today's limit. Schedule for tomorrow, or use a standard transfer.") · lowered-by-bank (with reason class + support path).

**Rule:** the user discovers a limit **at amount entry**, never at the review or failure step.
