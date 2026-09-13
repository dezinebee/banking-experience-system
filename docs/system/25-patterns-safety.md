# 25 — Patterns: Fraud, Errors, Recovery & System Pages

**Banking Experience System (BES)** · Patterns · v2.0.0-draft

The patterns for when things are risky, wrong, or broken — where trust is won or lost.

---

## P-60 · Suspicious transaction challenge

**Use:** risk engine flags an in-flight or recent transaction.
**Structure:** dedicated screen/notification (security category, `z.critical` when in-session):
```
We noticed unusual activity

AED 18,500.00 · International transfer
Dubai → India · today 15:47

Did you make this transfer?
[Yes, it was me]        [No, secure my account]
```
- **Yes:** release + thanks + "we check unusual patterns to protect you" (system credibility line) · false-positive friction tracked.
- **No:** immediate containment (card/credential freeze as applicable) → guided secure-account flow (P-63) → case creation with reference + what-happens-next.
**Rules:** the two buttons are outcome-explicit and equal weight; the challenge never reveals *why* the engine flagged (pattern secrecy) beyond the transaction facts; response deadline honesty ("We'll hold this transfer for up to 2 hours awaiting your reply, then it's cancelled for safety").

## P-61 · Suspicious login / new device event

**Structure:** Security Event Notice (doc 20) to all trusted devices: what/when/where + "Was this you?" fork → No: session-kill of the new device + credential rotation + review-recent-actions checklist.

## P-62 · Scam intervention (authorized-push-payment defense)

**Use:** high-risk payment signals (new payee + urgency + coached behavior; active call detected).
**Structure:** Warning Tier set (doc 20) escalation: caution interstitial → high-tier friction (re-auth + **the delay option**: "Wait 24 hours — genuine payees will understand. Scammers pressure you to act now.") → critical hard-stop (payment refused in-channel + education + support).
**Session pause variant:** active-call/screen-share detection → Session Pause Interruption (doc 20).
**Copy discipline:** describe the scam *pattern*, never accuse the named recipient; offer the human path ("Talk to us first — 800 XXXX, we're available now").

## P-63 · Account takeover response ("Secure my account")

**Use:** user-initiated ("No, that wasn't me") or bank-initiated.
**Structure (guided, one screen per step, no dead ends):**
1. Contain — freeze cards + block credentials + kill sessions (automatic, confirmed: "Done. No one can move money right now.")
2. Re-secure — identity re-verification (national identity where possible) → new credentials/passkeys
3. Review — recent transactions/payees/devices/consents checklist with dispute entry per item
4. Restore — unfreeze choices, restored access confirmation
5. Record — case reference, report copy (PDF), escalation path (police-report guidance where relevant, ombudsman disclosure)
**Tone:** calm competence; progress visible; the user is a victim, not a suspect.

## P-64 · Card fraud response

Dispute Entry fraud fork (doc 17): don't-recognize → immediate freeze offer → liability & provisional-credit honesty per policy → replacement flow → merchant-list review for compromised card.

## P-65 · Beneficiary fraud / impersonation warning

**Use:** payee-context risk (mule-flagged destination, impersonation patterns: "bank staff asked me to transfer").
**Structure:** critical-tier stop for known-bad; high-tier for patterns ("Banks never ask you to move money to a 'safe account'. This request is a known scam pattern.") · report-payee path feeding the ecosystem signal.

## P-66 · Phishing & impersonation education

**Structure:** verified-channel surfaces ("We'll never ask for your password, OTP or card PIN — anyone who does isn't us") · in-message authenticity markers for genuine bank messages (personalized salt the user set at onboarding, where deployed) · report-phishing entry (forward/upload → confirmation + takedown honesty).

## P-67 · Error recovery (universal)

**Structure (the four questions, always):** WHAT happened · WHY (plain class) · **what happened to the MONEY** (when money was in flight) · WHAT to do next (retry / alternative / support). Mapped from the error taxonomy (doc 27 §4): every error class has a defined message frame, recovery action, CTA and severity — screens compose, never invent.
**Retry safety:** retry buttons render only where idempotency is guaranteed; otherwise status-check paths ("See if it went through") replace retry.

## P-68 · Complaint & escalation

**Use:** "Report a problem" beyond disputes.
**Structure:** complaint entry (category + free text + attachments) → acknowledgment with reference + response-time commitment (written ack within 2 business days) → status tracking (received → investigating → resolved with outcome) → **escalation disclosure**: "Not resolved within 15 days, or unhappy with the outcome? You can escalate to Sanadak, the independent financial ombudsman — free of charge" + link. REG-anchored.
**Rule:** the complaint path is findable from every support surface and the app-level menu — never buried.

## P-69 · Session expiry & timeout

**Structure:** Session Bar warning at T-60s ("You'll be signed out in 0:59 — [Stay signed in]") → expired page: neutral ("You were signed out to protect your account") → re-auth → **draft restoration** with explicit confirm ("Continue your transfer to Priya Kumar? Amount: AED 10,000.00 [Continue] [Discard]"). Drafts of sensitive flows persist encrypted, payment-unauthorized, max 24h.

## P-70 · Offline & connectivity loss

**Structure:** offline banner + cached-data timestamps ("Showing balances from 14:32") · read surfaces stay useful · write actions queue *only* where safe (notes, categorization) — money movement never queues silently ("You're offline — we didn't send this. Try again when connected.") · reconnection re-sync quiet.

## P-71 · "There's a problem with the service" (full-page)

**Use:** unrecoverable screen-level failure. **Structure:** plain title · impact scope ("Your money and data are safe — we can't show this page right now") · reference code (short, for support) · retry + status-page link + support path · never a stack trace, never blame.

## P-72 · Service unavailable / maintenance page

P-52's blocking form: what's down, until when, what still works, alternatives (ATM/branch/phone for critical needs).

## P-73 · Account restriction & funds-hold communication

**Use:** compliance-driven restrictions. **Structure:** restriction surfaced at the point of blocked action + account-level status (doc 14): generic-safe reason class ("Additional checks required — we may need documents from you") · document-request flow where applicable (secure upload, checklist, SLA) · balance always visible · support path always present · resolution notification.
**Copy law:** no tipping-off; no fake specificity; no dead ends.

## P-74 · Deceased-customer & vulnerable-situation handling

**Use:** bereavement reporting, guardianship, power-of-attorney.
**Structure:** dedicated humane entry ("Report a bereavement") outside the complaint taxonomy · what-happens explanation (freezes, required documents, timelines) in plain, gentle language · document checklist + secure upload · named-contact continuity (one case, not repeated re-explanation) · marketing suppression immediate.

## P-75 · Account closure

**Use:** customer-initiated exit. **Structure:** closure is a *first-class journey*, not a support ticket: prerequisites checklist auto-checked (balance to zero — with transfer-out helper; no pending transactions; products to settle listed with paths) → consequence review (statements access post-closure, document downloads offered *before* closure) → typed confirmation → processing with SLA → written confirmation.
**Rules:** no retention dark patterns (one save-offer maximum, then respect); post-closure statement access guaranteed and stated ("Download your last 7 years of statements now — or request them later via support").
