# 15 — Financial Components: Transactions Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Components: Transaction Item · Transaction List · Transaction Table · Transaction Detail · Transaction Status · Transaction Timeline · Receipt · Search & Filters · Statement Row.

State vocabulary and money-statements are normative from doc 07 §4.

---

## Transaction Item

**Purpose:** one transaction in a list — the most-rendered financial component in any banking product.

**Anatomy:** leading: merchant/counterparty logo or category icon (fallback: initial avatar) · primary: counterparty/merchant display name (cleaned, not raw acquirer strings — "Carrefour MOE", not "CARREFOUR4901 DXB AE") · secondary: category + time (or account context in multi-account lists) · trailing: Amount (`sm`, signed) + Status Badge when non-settled · optional third line: note/reference.

**Variants:** card transaction (shows card ••suffix) · transfer (shows direction + counterparty bank) · remittance (corridor flag + delivery status) · recurring marker (↻) · split/shared marker · declined (struck amount + reason class).

**States (rendering the machine):** settled (neutral, no badge — settled is the default and stays quiet) · pending (badge + clock) · processing · failed/declined (struck amount, `status.error` label, **money statement on the detail**) · blocked/under-review (generic-safe label "Checking this payment") · refunded (link chip to original) · reversed · disputed (badge + dispute stage).

**Usage:** grouped by day with sticky date headers ("Today", "Yesterday", "28 August"); running daily totals optional per surface. Tap → Transaction Detail. Swipe actions (mobile): receipt, note — never dispute/report via swipe alone.

**A11y:** one summary name per row: "Carrefour, groceries, yesterday 19:42, minus 89 dirhams 50 fils, settled"; badges included; logo decorative.

**RTL:** leading/trailing swap; amount stays LTR end-aligned; cleaned merchant names may be bilingual — display per UI language with the counterparty's registered name on detail.

---

## Transaction List

**Purpose:** the scrollable history surface (mobile default).

**Anatomy:** search trigger · filter chips row (Date · Type · Amount range · Card/Account · Status) · grouped Transaction Items · "Load more" (explicit, no infinite auto-scroll) · export action.

**States:** loading (skeleton rows) · incremental loading · filtered (active chips + result count + clear-all) · empty variants (first-use / filtered-empty / period-empty: "No transactions in July") · offline (cached + timestamp banner) · partial (some rails degraded: "Card transactions may be delayed").

**Financial:** pending transactions float in a distinct "Pending" section above settled history (they re-sort into date order on settlement); search matches amount, merchant, note, reference, in Arabic and Latin.

---

## Transaction Table (desktop / SME / corporate)

**Purpose:** dense operational view.

**Anatomy:** Data Table specialization — columns: date+time · counterparty · reference · category/type · debit · credit · balance-after (optional, statement mode) · status · row menu. Numeric columns end-aligned tnum; debit/credit split *or* signed single column (per surface convention, never mixed).

**States:** table states (doc 11) + bulk selection with money-aware summary bar ("14 transactions — total −AED 23,410.00") · reconciliation mode (SME: matched/unmatched markers).

**Financial:** default sort newest-first; export respects filters and states the scope; column set configurable and persistent per user.

---

## Transaction Detail

**Purpose:** the full record — the screen users screenshot for proof, check when worried, and start disputes from.

**Anatomy (ordered):**
1. Header: counterparty (logo + name) · Amount (`lg`, signed) · Status Badge
2. **Money statement line** for any non-settled state ("No money has left your account")
3. Timeline (see below) for multi-stage transactions
4. Facts block (label/value rows): date & time · account/card used · category (editable) · reference number (copyable) · FX facts where applicable (original amount, rate, fees — full Fee Breakdown reproduced, exactly as at authorization) · counterparty details (IBAN masked middle)
5. Note field (user memo)
6. Actions: Download receipt (PDF) · Share · Repeat/Send again · Report a problem → dispute flow · Refund status link where applicable

**States:** per machine — the detail is the canonical surface where every state explains itself fully.

**A11y:** facts as definition list; headline is a proper heading; actions in a labeled group.

**RTL:** label/value rows mirror (labels inline-start); values that are codes/IBANs/amounts stay LTR runs.

---

## Transaction Status

**Purpose:** the state, rendered consistently (badge + optional line).

Uses the canonical vocabulary only: Draft · In review · Awaiting authentication · Processing · Pending · Completed · Failed · Checking status (UNKNOWN) · Additional checks (BLOCKED) · Reversed · Refunded · Disputed · Cancelled. Each maps to `financial.*` colors + shape-coded icons. Localized pairs are fixed in the glossary (doc 27) — one Arabic term per state, everywhere.

---

## Transaction Timeline

**Purpose:** multi-stage progress for transfers/remittances/disputes.

**Anatomy:** vertical steps: done (check + timestamp) · current (pulse + expected time: "Processing — usually within 1 hour") · upcoming (grey) · terminal. Failure/hold renders the stage where it happened with its explanation and recovery inline.

**Example (remittance):**
```
✓ Sent from your account          14:32
✓ Converted AED → INR             14:32
● With recipient bank             expected by 15:30
○ Delivered to Priya Kumar
```

**States:** advancing · stalled (current stage exceeds expectation → honest note + notify-me) · unknown (dedicated stage copy: "We're confirming this stage with the partner bank — your money is safe") · complete.

**A11y:** ordered list semantics; current stage announced with expectation.

**RTL:** timeline rail at inline-start; checkmarks unmirrored.

---

## Receipt

**Purpose:** shareable, durable proof — a first-class artifact (remittance proof is a real household job).

**Anatomy:** issuer identity (bank name + logo slot) · "Payment receipt" title · status (completed only — pending payments export a "payment instruction" doc, clearly different) · amount block (full precision) · parties (sender/recipient with masked identifiers) · facts (date, reference, rate & fees for FX) · verification element (reference + QR against issuer verification endpoint) · regulatory footer slot.

**Formats:** in-app view · PDF (accessible: tagged, selectable text, logical reading order — a screenshot is not a receipt) · share-sheet text summary.

**Rules:** receipts are immutable snapshots — they render the fees *as charged*, not the current schedule; bilingual layout (AR/EN dual-column or per-preference single language, institution-configurable).

---

## Search & Filters (transactions)

**Anatomy:** Search (doc 09) + filter sheet/panel: date presets + custom range · type checkboxes · amount range (Currency Inputs) · account/card scope · status. Applied filters render as removable chips with a stated result count.

**Rule:** filters are additive-transparent — the user can always see *why* the list looks the way it does.

---

## Statement Row / Statement Access

**Anatomy:** period label ("July 2026") · format actions (PDF · CSV/Excel) · generated-on-demand states (generating → ready → download) · older-statement request path where archives require retrieval.

**Financial:** statements are the audit-grade export: balance-after per line, official formatting, accessible PDF. The e-statement consent state (paper vs digital) surfaces here with its own toggle + confirmation.
