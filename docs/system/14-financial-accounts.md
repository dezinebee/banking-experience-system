# 14 — Financial Components: Accounts Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Components: Account Card · Account Selector · Balance Display · Balance Set · Account Details · IBAN Display · Account Status · Product Header · Spaces/Goal Card.

---

## Account Card

**Purpose:** one account at a glance — the dashboard workhorse.

**Anatomy:** account name (user-renamable: "Rent account") · product type label ("Current account" / "حساب جاري") · masked number (••4521) · available balance (Amount `lg`, maskable) · optional pending indicator ("AED 500.00 pending") · optional status badge · primary quick actions (≤2: Send, Details).

**Variants:** full (dashboard) · compact (lists, pickers) · multi-currency (currency tabs or stacked balances per currency) · joint (co-holder indicator) · ✦ Islamic (product label carries structure: "Mudarabah savings"; profit-rate metadata instead of interest).

**States:** default · loading (skeleton — no zero flash) · stale (timestamp) · masked · restricted (`financial.blocked` treatment + "Why?" path) · dormant (reactivation path) · closed (read-only history access).

**Usage:** available balance is the headline number always (doc 07 §3); current balance relegated to Details. One tap → account home. Cards never show promotional content inside the account object.

**A11y:** single named control: "Current account ending 4521, AED 25,000.00 available"; quick actions as discrete stops.

**RTL:** name/labels mirror; number and balance LTR runs; actions at inline-end.

---

## Account Selector

**Purpose:** choose source/destination account in flows.

**Anatomy:** Select/Combobox specialization — trigger shows selected account (name + ••number + available balance); options show the same triple; groups: "Your accounts / Joint / Business".

**States:** default · open · insufficient (option visible but flagged: "AED 120.00 available — not enough for this transfer"; selectable only where partial funding is a real flow, otherwise disabled with reason) · single-account (renders as static confirmation line, not a dropdown).

**Financial:** in transfer flows, selecting a source re-validates amount + limits instantly; balance shown is *available*; hidden accounts (user preference) still listed under "More accounts".

**A11y:** option announced with full triple; insufficient state part of the announcement.

---

## Balance Display

**Purpose:** a single balance figure with its label and freshness.

**Anatomy:** label ("Available balance") · Amount · freshness/timestamp when not real-time · optional info affordance explaining the balance type.

**Rule:** never a bare number — the *type* of balance is always labeled, because "balance" is ambiguous by definition (doc 07 §3).

---

## Balance Set

**Purpose:** the full picture — available / current / pending / reserved in one structure.

**Anatomy:** primary row (available, `amount.lg`) · secondary rows (current, pending in/out, reserved) · "Why is my available balance different?" explainer link when current ≠ available · holds drill-down (list of reservations with merchant, amount, release date).

**Example:**
```
Available balance         AED 23,750.00
Current balance           AED 25,000.00
Pending out               −AED 750.00   (2 transactions)
Reserved (card holds)     −AED 500.00   → View holds
```

**A11y:** rendered as a definition list; explainer reachable by keyboard.

---

## Account Details

**Purpose:** the reference sheet — everything needed to *receive* money or verify the account.

**Anatomy:** rows for: holder name (legal, as registered) · IBAN Display · account number · branch/bank identifiers (SWIFT/BIC) · currency · product name & terms link · opened date. Each row: label + value + copy button. "Share details" action exports a clean payload (text/PDF) *excluding* anything not needed for receiving money.

**States:** default · restricted-view (joint/delegated users see per-permission subsets).

**Security:** details screens require an authenticated session but not step-up; screenshots allowed (users legitimately share IBANs) — but the share action is the promoted path.

---

## IBAN Display

**Purpose:** render the 23-character UAE IBAN (and foreign IBANs) reliably.

**Anatomy:** grouped display `AE07 0331 2345 6789 0123 456` · copy button (copies *unspaced* canonical form; toast confirms "IBAN copied") · always `dir="ltr"` in an isolated run.

**States:** default · verifying (payee-side lookups) · invalid (entry-side pairing with the IBAN input, doc 09).

**A11y:** announced in groups of four, not as one 23-character blur; copy announces success.

---

## Account Status

**Purpose:** account-level states surfaced honestly.

**Vocabulary:** active · restricted (with reason class: verification-needed / compliance-hold — tipping-off-safe copy) · dormant (with reactivation steps) · frozen (with support path) · pending-closure · closed.

**Anatomy:** Status Badge + explanation block + the recovery path (every non-active status names its exit).

**Rule:** a restricted account's *balance remains visible* — restriction of action never becomes concealment of the user's own money.

---

## Product Header

**Purpose:** top-of-screen identity for any financial product page (account, card, loan, deposit).

**Anatomy:** product name · identifying suffix (••4521) · status badge · headline figure (available balance / outstanding amount / card limit) · tab bar into sections (Transactions / Details / Statements).

**RTL:** headline figure LTR run; tabs mirror.

---

## Spaces / Goal Card

**Purpose:** sub-account earmarking (savings goals, VAT set-aside, rent).

**Anatomy:** goal name + icon/emoji slot · saved amount / target ("AED 6,500 of AED 20,000") · Progress bar · optional auto-rule summary ("Saves AED 500.00 every payday") · quick add/withdraw.

**States:** on-track · paused · reached (celebration allowed — savings context is the sanctioned celebratory surface, doc 05 §2) · behind (neutral framing: "AED 500 to stay on track" — never shame).

**Financial:** money in spaces is part of `balance.current` but excluded from spendable `balance.available` presentation — the set explains this ("AED 6,500.00 set aside in Spaces").
