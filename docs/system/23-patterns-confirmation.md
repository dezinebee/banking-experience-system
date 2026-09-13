# 23 — Patterns: Review, Confirmation & Trust

**Banking Experience System (BES)** · Patterns · v2.0.0-draft

The patterns that implement "review → correct → confirm" before anything irreversible, and the trust contract (identity · intent · amount · destination · cost · timing · consequence · recovery) at every high-impact moment.

---

## P-20 · Check answers (universal review)

**Use:** before any submission with consequence — applications, profile changes, payments (specialized as P-21).
**Structure:** summary list of everything entered (label · value · Change link per row, returning to that step with state preserved) → consequence statement → verb-labeled submit ("Submit application", "Save changes").
**Rules:** optional skipped items show "Not provided" (still changeable); nothing the user entered is hidden from review; returning users see prior answers prefilled.
**A11y:** definition list; Change links carry hidden context ("Change monthly salary"); focus lands on the heading.

## P-21 · Confirm a payment (the money review)

**Use:** every money movement. **Structure:** Transfer Review contract (doc 16): Payment Summary + Change links → Fee Breakdown (expanded first view) + Total Row → FX block with rate status → warning slot (risk-tiered) → consequence statement (reversibility honesty: "Instant transfers can't be cancelled once sent") → **amount-bearing verb CTA** ("Send AED 10,036.75").
**Never:** fees introduced here for the first time (they appeared at the fee stage); a bare "Confirm" button; modal-based confirmation for significant amounts.
REG: fee disclosure; payee confirmation.

## P-22 · Verify a payee (name check moment)

**Use:** instant-rail transfers, new payees, edited payees. **Structure:** Payee Verification component (doc 16) with the four result states; no-match proceed escalates P-21's warning tier and is logged to the risk context.
REG: confirmation-of-payee mandate.

## P-23 · Step-up authentication

**Use:** risk-proportionate identity confirmation: money movement above thresholds, payee/limit/control changes, credential and detail reveals, consent grants, signing.
**Structure:** Auth Prompt set (doc 20) with **context always displayed** (what is being authorized, amount+payee for payments) · fallback ladder · lockout-with-recovery.
**Rules:** step-up protects *increases* of risk; safety actions (freeze, revoke, sign-out-device) never require it.

## P-24 · Signing ceremony (contracts)

**Use:** legally significant agreements. **Structure:** doc 20 Signing Ceremony: full in-place document → key-terms recap → national-identity signature handoff → signed receipt + document delivery → **cooling-off notice with live cancellation entry (5 business days)**.
REG: consumer protection cooling-off; digital-signature equivalence.

## P-25 · Cooling-off & cancellation window

**Use:** post-contract for applicable products. **Structure:** post-signing confirmation states the right; the product surface shows a "You can still cancel until 5 Sep" entry for the window; cancellation flow = consequence-honest confirm (refund treatment stated) → confirmation.
**Waiver variant:** explicit, friction-full, never pre-selected; warning of immediate commitment. REG-anchored.

## P-26 · Explain fees ("Why am I being charged?")

**Use:** every fee line's info affordance; fee-schedule surfaces. **Structure:** popover/sheet: this fee in plain language ("The transfer fee covers processing through the international payment network") · how it was calculated where formulaic · link to the full schedule of charges (accessible PDF) · dispute path for believed-wrong charges.

## P-27 · Explain an Islamic product

**Use:** every Islamic product surface. **Structure:** Shari'ah Structure Explainer (doc 18) + terminology-dimension enforcement + certification mark; comparison surfaces (conventional vs Islamic variants of a product) present both fairly with structure-appropriate rate components — never one framed as the "normal" one.

## P-28 · Present a Key Facts summary

**Use:** every product application entry (financing, cards, deposits, investments-adjacent). **Structure:** Product Summary component (doc 18) before application start; re-presented at offer; embedded in the signing recap. REG: KFS mandate.

## P-29 · Notify changes to terms

**Use:** fee/T&C changes. **Structure:** 60-day advance notice (notification + banner + document): plain-language "what's changing" summary (old → new comparison rows for fees) · effective date · what-you-can-do (including exit rights) · full revised terms link. Notice persists until acknowledged; acknowledgment ≠ consent (it records awareness). REG-anchored.

## P-30 · Handoff to an external service

**Use:** identity verification, third-party consent journeys, wallet provisioning, any redirect. **Structure:** Identity Handoff pattern (doc 20): why-interstitial → external ceremony → return handling (success/decline/timeout, state preserved) → confirmation in-context.
**Trust rule:** the user always sees who they're being sent to (named + logo) and what comes back.

## P-31 · Receipt & proof

**Use:** after every completed money movement; on demand from history. **Structure:** Receipt component (doc 15): immutable snapshot, accessible PDF, share-sheet summary, verification reference.
**Rule:** proof is a first-class user job — the receipt path is never more than one tap from a completed transaction.

## P-32 · Approval workflow (maker–checker)

**Use:** SME/corporate payment authorization; dual-control retail scenarios (joint accounts opt-in).
**Structure:**
- **Maker side:** create → standard review (P-21) → "Submit for approval" (not "Send") → pending-approval object with audit trail.
- **Checker side:** approval queue (Table/cards: payment summary + maker + created time + policy flags) → approval detail = **the same Payment Summary + Fee Breakdown the maker saw** (no information asymmetry) → risk flags (new payee, over-threshold, duplicate-suspect) → [Approve] (step-up auth) / [Reject with reason] (structured + free text, returned to maker) · batch approval only for same-class low-risk items with per-item visibility, never blind bulk.
- **States:** awaiting approval · approved-processing · rejected (reason to maker) · expired (approval SLA passed) · escalated (threshold chains: "Requires Finance Director above AED 100,000").
- **Audit:** every action timestamped + attributed; the trail is visible to both roles.

**Example:**
```
Payment for approval
AED 250,000.00 to Gulf Star Trading LLC
Created by Ahmed Al Mansoori · today 11:20
Requires: Finance Director approval (amounts above AED 100,000)
⚠ New beneficiary — added 2 days ago
[Review details]   [Approve]   [Reject]
```

## P-33 · Confirm a destructive action

**Use:** deletions, closures, revocations. **Structure:** confirm dialog naming object + consequence; buttons echo outcomes ("Remove beneficiary" / "Keep beneficiary"); typed-confirmation reserved for catastrophic irreversibles (account closure: type the account nickname) — used sparingly so it retains force.
**Safety-action exception:** freeze/revoke/sign-out execute immediately (one tap), offering undo where reversible instead of pre-confirmation.
