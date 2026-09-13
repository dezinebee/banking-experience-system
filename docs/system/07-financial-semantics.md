# 07 — Financial Semantic Layer

**Banking Experience System (BES)** · Architecture · v2.0.0-draft

The layer that makes BES a financial system: how money is displayed, how balances are modeled, how transactions move through states, and how risk, verification and consent are represented. Everything here is brand-invariant.

---

## 1. Money display system

### 1.1 Anatomy of an amount
```
[sign] [currency] [integer].[decimals]   →   −AED 1,250.50
```
- Currency code at 0.75× size, weight 500; the number owns the hierarchy.
- True minus (U+2212); `+` only on credits in mixed lists.
- Whole block is a single bidi-isolated LTR run (doc 02 §5).

### 1.2 Formatting rules by context

| Context | Format | Example |
|---|---|---|
| Balance (actionable) | Full precision, tnum | AED 25,000.00 |
| Transaction list | Full precision, sign per direction | −AED 89.50 · +AED 12,500.00 |
| Review/confirm total | Full precision, `type.amount.lg` | AED 10,035.00 |
| Dashboard summary/charts | Abbreviation allowed | AED 25K · AED 1.25M |
| Approximate/converted | Tilde prefix + "approx." label | ≈ ₹250,800 |
| Masked | Currency + bullets, toggleable | AED ••••• |
| Zero | "AED 0.00" — never blank, never "--" | |
| FX rate | 4 significant decimals + timestamp | 1 AED = ₹25.0800 · rate at 14:32 |

Hard rules:
- **Abbreviation never appears on anything the user is about to authorize.** Review screens, confirmations and receipts always show full precision.
- Rounding is display-only and half-even; underlying values never mutate. Where a displayed sum could look inconsistent due to rounding, the display adds a footnote line ("Totals may differ by AED 0.01 due to rounding") — but prefer showing exact figures.
- **Estimated vs final is a labeled state**, not a typographic nuance: `≈` + "estimated" label + explanation of when it becomes final.
- Precision follows the currency: AED/INR/USD 2 decimals; JPY 0; KWD/BHD 3. `currency.precision` resolves per ISO code — never hardcode 2.
- Masked-by-default is a user setting honored everywhere balances render (glanceable privacy); reveal is per-tap or per-session, configurable.

### 1.3 Multi-currency
Primary amount in transaction currency; account currency as `type.amount.meta` beneath: "**USD 500.00** ≈ AED 1,836.50". The currency the user is *charged in* is always the primary. Supported display set at v1: AED, USD, EUR, GBP, INR, PKR, PHP, EGP, SAR, BDT, LKR, NPR + ISO-complete formatting fallback.

## 2. FX & conversion display

The FX block is one reusable component family used in remittance, card FX, and multi-currency transfers:

```
You send                      AED 10,000.00
Exchange rate                 1 AED = ₹25.0800   (guaranteed for 14:59 ⏱)
Transfer fee                  AED 15.00
FX margin                     AED 20.00          (i) why this fee?
─────────────────────────────────────────────
Total you pay                 AED 10,035.00
Recipient gets                ₹250,800.00        Delivery: within 1 hour
```

Rules:
- **Rate status is explicit:** `estimated` (≈, "rate may change") vs `guaranteed` (with lock icon + expiry countdown). Expired lock → re-quote step, never silent re-pricing.
- **Fee and FX margin are separate lines.** "Zero-fee" claims with margin priced into the rate are misrepresentation; the system's FX block structurally prevents it by always deriving and showing the margin against the mid-market reference where available, or labeling the rate "our rate" otherwise.
- Recipient amount states its own certainty (exact vs estimated) and delivery time honestly (range, not best case).
- Corridor context (payout method: bank / wallet / cash pickup) alters fees — the block re-renders on method change with a change highlight.

## 3. Balance model

| Token | Meaning | Display rule |
|---|---|---|
| `balance.current` | Ledger balance | Secondary |
| `balance.available` | What the user can spend **now** | Primary, `type.amount.lg`+; the default "balance" everywhere |
| `balance.pending` | Incoming/outgoing not settled | With clock icon + explainer |
| `balance.reserved` | Holds, pre-auth, blocked amounts | `financial.reserved` + "view holds" affordance |
| `balance.overdrawn` | Negative available | `financial.negative`, with recovery guidance |

Rule: when current ≠ available, the UI must make the difference discoverable in one tap ("Why is my available balance different?"). Never show only `current` where spending decisions happen.

## 4. Transaction state machine (normative)

```
DRAFT → REVIEW → AUTHENTICATION → PROCESSING → COMPLETED | PENDING | FAILED | UNKNOWN
COMPLETED → REFUNDED | REVERSED | DISPUTED
PENDING → COMPLETED | FAILED | UNKNOWN
UNKNOWN → COMPLETED | FAILED          (must resolve; never silently terminal)
DRAFT|REVIEW → CANCELLED
any pre-terminal → BLOCKED            (compliance/fraud hold)
```

Per-state contract (every state defines all five):

| State | UI | Content core | Money statement | User actions |
|---|---|---|---|---|
| draft | neutral | "Not sent yet" | — | edit, delete |
| review | neutral emphasis | full trust block (doc 23) | "Nothing sent until you confirm" | change, confirm |
| authentication | secure styling | method prompt | — | authenticate, cancel |
| processing | progress | "Sending your transfer" | "Money is on its way" | none (safe-wait) |
| completed | `transaction.completed` beat | "Transfer completed" | amount + destination + time | receipt, repeat, share |
| pending | `transaction.pending` | "Your transfer is pending" + reason class + ETA | "Money has left your account" or "will leave when processed" — whichever is true | track, notify-me |
| failed | `transaction.failed` | what + why + **money state** + next step | "No money was deducted" / "will be returned by [date]" | retry, support |
| **unknown** | `transaction.unknown`, calm | **"We're checking your transfer status."** | "Your money is safe — we'll confirm within [X]" | notify-me, support |
| blocked | `transaction.blocked` | generic, tipping-off-safe: "Additional checks required" | held statement | provide docs (if flow exists), support |
| reversed | `transaction.reversed` | what was reversed + why + where money went | credited/debited statement | detail, support |
| refunded | `transaction.refunded` | original ref + refund date | "AED X returned to [account]" | detail |
| disputed | neutral + badge | dispute status timeline | provisional credit state if any | evidence, track |
| cancelled | neutral | who cancelled, when | "No money moved" | re-create |

> **One name per state.** These 13 names are the stable API — the same string in the UI, the tokens, the event stream and the copy deck. The terminal success state is **`completed`**, not `success`: that is what the token emits, what the badge class reads, and what the customer is shown ("Transfer completed"). Colour comes from `transaction.*` and from nowhere else; `status.*` is for generic UI status (form validation, banners) and `financial.*` is for what an amount *means*, not what stage it is at. `tools/audit-states.py` fails the build if any artefact disagrees.

**Prime directive: FAILED is only shown on confirmed failure.** Timeouts, opaque rail responses and lost callbacks map to UNKNOWN with its safe copy. Showing "failed" for an eventually-successful transfer is the most trust-destroying defect a banking UI can ship; the system makes it structurally hard by giving UNKNOWN first-class components.

## 5. Risk, verification, consent vocabularies

### Risk (`risk.*`) — drives fraud/warning tiers (doc 25)
low → inline info · medium → caution interstitial · high → friction + re-auth · critical → hard stop + support path. Severity mapping is a pattern decision, never ad-hoc per screen.

### Verification (`verification.*`)
unverified · pending · verified · failed · expired — applied to identity, documents, payees and devices. Verified states always show *what* was verified and *when*; expired states always pair with the renewal path (re-KYC pattern).

### Consent (`consent.*`)
required · pending · granted (with expiry) · expired · revoked. Consents are always: purpose-bound, time-bound, listed in the consent dashboard, revocable in ≤ 2 taps from that dashboard. A permission without visible expiry is a design defect.

## 6. Amount input semantics

Currency input (component detail in doc 09/13): locale-aware grouping while typing; forgiving paste (strips currency symbols, spaces, commas); precision clamp per currency; min/max validated against `balance.available` with inline remainder preview ("Leaves AED 1,250.00"); Arabic-locale entry accepts Eastern or Western digits, normalizes to canonical value, displays per locale preference.
