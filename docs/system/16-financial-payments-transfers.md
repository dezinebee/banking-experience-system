# 16 — Financial Components: Payments & Transfers Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

The components that implement the money-movement framework (INTENT → SOURCE → DESTINATION → AMOUNT → FEES → FX → REVIEW → AUTHENTICATION → PROCESSING → RESULT → RECEIPT). Stages are slots: simple domestic flows collapse stages; first-time international flows expand them.

Components: Payee Card · Beneficiary Manager · New Beneficiary Form · Payee Verification (name check) · Source Selector · Payment Summary · Payment Method Selector · Transfer Review · Authentication Prompt · Processing Screen · Result Screen · Scheduled/Recurring Setup · Request-to-Pay Card · QR Pay · Bill Split · Bill Payment Tile.

---

## Payee Card

**Purpose:** a person/business the user pays.

**Anatomy:** avatar/initials · display name (user's nickname) + registered name when different · identifier summary (bank + ••IBAN-last-4, or mobile proxy for instant rails) · trust metadata: verified badge (name-check passed) · "Added [date]" — **recency is risk signal**: payees added < 24h carry a "New" marker into every flow that uses them · last-paid summary ("Last sent AED 2,000.00 · 12 Aug").

**Variants:** personal · business · international (corridor flag + currency) · own-account (visually distinct — moving between own accounts skips warning tiers) · proxy-based (mobile/email for instant rails).

**States:** active · new (<24h) · unverified · verification-failed · dormant (>12 months: "You haven't paid this person in over a year") · blocked.

**A11y:** one summary name; trust metadata included ("Rajesh Kumar, Emirates NBD account ending 4102, verified, added 14 March 2025").

**RTL:** identifiers LTR runs; bilingual names displayed per registered script with the other available on detail.

---

## Beneficiary Manager

**Purpose:** list + lifecycle of payees.

**Anatomy:** search · grouped list (Recent / All, A–Z) · add action · item → detail (full identifiers masked-middle, payment history, edit nickname, delete).

**States:** list states + delete confirmation (names consequence: "You'll need to add them again — and new payees may have a holding period before large transfers").

**Security:** adding/editing beneficiaries is a step-up-auth event; deletions are notification events ("Beneficiary removed" push/email — account-takeover tripwire).

---

## New Beneficiary Form

**Anatomy:** country/corridor first (drives the rest of the form — only country-relevant fields render) · identifier entry: UAE IBAN input / mobile proxy / international (IBAN or account + SWIFT) · registered-name field · nickname (optional) · currency (corridor-driven).

**Behavior:** IBAN checksum on blur with specific errors; bank auto-derived from IBAN and shown for confirmation ("This IBAN belongs to Emirates NBD — correct?"); duplicate detection ("You already have this account saved as 'Priya ICICI'").

**States:** entering · validating · **name-check result** (see Payee Verification) · saved (with cooling-period notice where policy applies: "For your security, transfers to new payees are limited to AED 5,000 for 24 hours").

---

## Payee Verification (Confirmation of Payee)

**Purpose:** name-match check before money moves — mandatory on instant rails.

**Anatomy:** entered name vs registered name comparison · result state · action row.

**Result states:**
- **Match** — green check: "Name matches the account." → proceed enabled.
- **Close match** — amber: shows the registered name ("Did you mean **Rajesh Kumar Nair**?") → [Use this name] / [Check with the recipient].
- **No match** — red: "The name doesn't match this account. Sending money to the wrong account can be hard to recover." → proceed requires explicit friction: [I understand the risk — continue] (secondary style, never primary) / [Go back and check] (primary).
- **Unavailable** — neutral: "We couldn't check the name (recipient bank doesn't support it). Make sure the details are right." → proceed with caution tier.

**A11y:** result announced assertively; the risk copy is part of the continue button's described context.

**Rule:** no-match proceed events feed the risk tier of the subsequent review (escalated warning).

---

## Source Selector

Account Selector specialization (doc 14) scoped to eligible sources for the payment type, with live sufficiency validation and remainder preview.

---

## Payment Summary

**Purpose:** the compact who/what/how-much block reused across review, detail, approvals and receipts.

**Anatomy:** payee (name + identifier) · amount (full precision) · from-account · fees reference (link into Fee Breakdown) · date/schedule · reference/purpose.

**Rule:** the summary is *one component* everywhere — review, approval queues and receipts render the same structure so users learn one shape for "a payment".

---

## Payment Method Selector

**Purpose:** choose the rail/method where alternatives exist (instant vs standard; bank vs wallet vs cash-pickup payout; card vs account funding).

**Anatomy:** Radio option cards with per-method metadata: fee · speed ("Instant" only for genuinely instant rails; otherwise honest ranges) · limits ("Up to AED 50,000") · availability (cut-off times: "Before 22:00 for same-day").

**States:** available · selected · unavailable-now (with reason + next window) · corridor-unsupported.

**Rule:** switching method re-renders fees/FX with change highlight; the default preselects the *cheapest adequate* option, not the most profitable.

---

## Transfer Review

**Purpose:** the check-answers moment — the system's most important screen.

**Anatomy (ordered):**
1. Title: "Check and confirm"
2. Payment Summary with per-row Change links (each returns to its step, preserving state)
3. Fee Breakdown (expanded on first view) + Total Row
4. FX block with rate status (locked/estimated + timer) where applicable
5. Warning slot (risk-tiered: new payee, CoP mismatch escalation, high value, first international)
6. Consequence statement: "We'll send AED 10,036.75 from your Current account ••4521 now. Instant transfers can't be cancelled once sent."
7. Primary action naming the act: **"Send AED 10,036.75"** · secondary "Back"

**States:** ready · re-validating (upstream change) · rate-expired (re-quote inline) · blocked (limit/compliance with explanation).

**A11y:** summary as definition list; change links carry hidden context ("Change amount"); consequence statement programmatically associated with the confirm button.

**RTL:** rows mirror; amounts LTR; the confirm button's amount is an isolated run.

---

## Authentication Prompt (step-up)

**Purpose:** confirm identity proportionate to risk.

**Anatomy:** context line (**always** shows what is being authorized: "Confirm transfer of AED 10,036.75 to Priya Kumar") · method surface (biometric prompt / passkey / in-app push approval / national-identity app handoff) · fallback path (accessible, never SMS) · cancel.

**States:** awaiting · verifying · approved (auto-advance) · failed (attempts remaining, alternative method) · locked (support path — never a dead end) · timeout (safe return to review, nothing sent).

**Security:** the amount+payee in the prompt is the anti-tamper anchor — users are trained to read it; push-approval screens on a second device show the same context. Session-pause interruptions (active screen-share/call detection) override this surface at `z.critical`.

---

## Processing Screen

**Anatomy:** calm progress (determinate only if real) · "Sending your transfer" · safe-to-leave note ("You can close this — we'll notify you") · **no cancel** (post-authorization ambiguity is worse than waiting).

**States:** brief (<3s: minimal) · extended (>10s: expectation copy) · handoff-to-unknown (→ UNKNOWN state copy, doc 07 §4 — never a spinner that outlives trust).

---

## Result Screen

**Variants per terminal state:**
- **Success:** check-draw beat · "Transfer sent" · amount + payee + when it lands · actions: Download receipt · Share · Send again · Done.
- **Pending:** clock · "Your transfer is pending" + reason class + ETA + tracking (Timeline) · money statement ("The money has left your account").
- **Failed:** what + why-class + **money statement** ("No money was deducted") · Retry (idempotent-safe) · support.
- **Unknown:** "We're checking your transfer status" + money-safety line + notify-me commitment ("We'll tell you within 30 minutes") — *no retry button* (double-send risk); support path present.

**Rule:** result screens are screens — never toasts, never modals.

---

## Scheduled / Recurring Setup

**Anatomy:** frequency (once/weekly/monthly/payday-linked) · start date (Date Picker with processing-day awareness) · end condition (until date / N payments / until cancelled) · per-run summary ("AED 2,000.00 on the 25th of every month — next: 25 Sep") · skip/pause/edit affordances on the created object.

**States:** active · paused · insufficient-funds-retry policy stated ("If funds are short we'll retry once the next day and notify you") · ending-soon · completed.

---

## Request-to-Pay Card

**Purpose:** incoming/outgoing payment requests on instant rails.

**Anatomy:** requester identity (verified badge + registered name — impersonation-sensitive) · amount · note · expiry · actions: Pay (→ full review flow, never one-tap from the notification) · Decline · Report.

**States:** received · viewed · paid · declined · expired · reported.

**Security:** requester name always the registered name (nicknames can't mask identity); unusual-requester warnings tier in.

---

## QR Pay

**Anatomy:** scan surface (camera + gallery import) · parsed result → Payment Summary preview before any confirmation · own-QR generator (amount-embedded optional, share/save).

**States:** scanning · parsed (preview) · invalid/expired code · mismatched-scheme.

**Rule:** a scanned QR never leads directly to authentication — always through the review contract.

---

## Bill Split

**Anatomy:** total · participants (contacts/payees) · split method (equal/custom/percentage) · per-person share preview (rounding remainder assigned visibly: "You cover the extra AED 0.02") · request-all action → individual Request-to-Pay objects with per-person status tracking (paid/pending/declined).

---

## Bill Payment Tile

**Purpose:** utility/telecom/government billers.

**Anatomy:** biller logo + name · linked account/consumer number (nicknamed: "DEWA — Marina flat") · amount due + due date · autopay state ("Autopay on — pays in full on due date, cap AED 1,500.00") · pay action → standard flow.

**States:** due (amber ≤3 days) · overdue (red + late-consequence note where known) · paid · autopay-scheduled · fetch-failed (manual amount entry fallback) · biller-unavailable.

**Rule:** autopay always has a user-set cap and pre-debit notification ("We'll pay DEWA AED 843.50 tomorrow").
