# 07 — Experience Architecture

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

The structural model everything else hangs on: layers, cross-cutting concerns, the money-movement framework, the transaction state machine, the trust layer, and the core/brand split. Phase 02 details each; this document fixes the shape.

---

## 1. Layer model

```
FOUNDATIONS          color · type (AR+EN) · spacing · grid · iconography · motion · elevation
      ↓
DESIGN TOKENS        primitive → semantic → component → pattern → product
      ↓
CORE COMPONENTS      buttons · inputs · selects · tables · modals · navigation · feedback …
      ↓
FINANCIAL COMPONENTS money · account · transaction · payment · transfer · card · loan · investment · consent
      ↓
PATTERNS             disclosure · review-confirm · CoP · fraud response · KYC · consent · errors …
      ↓
FINANCIAL JOURNEYS   onboarding · transfer · remittance · card mgmt · financing · Open Finance · fraud · SME approval
      ↓
PRODUCT EXPERIENCES  retail app · SME portal · corporate treasury · wealth · kiosk
```

**Cross-cutting every layer** (not stages, but dimensions of every artifact): accessibility · Arabic/English · RTL/LTR · security · privacy · financial semantics · content · localization · responsive behavior.

Rule: **no artifact ships at layer N without its cross-cutting documentation.** A component without an RTL section, an a11y checklist and content guidance is incomplete, not "pending polish."

## 2. Token architecture (shape; detail in Phase 02)

- Five tiers: `blue.600` (primitive) → `action.primary` (semantic) → `button.primary.background` (component) → `transaction.primaryAction` (pattern) → Send Money CTA (product).
- Delivered as **CSS custom properties** (SLDS 2 mechanism) with the Carbon/Atlassian role-naming grammar; contrast ratios documented in the token contract.
- **Token dimensions** (Spectrum model): color theme (brand presets, light/dark), direction (LTR/RTL), density (comfortable/standard/compact), scale (platform), contrast (standard/high), terminology (conventional/Islamic — a content dimension resolved through the same configuration system).
- Financial semantic namespace reserved: `financial.*`, `balance.*`, `transaction.*`, `risk.*`, `verification.*`, `consent.*` — plus an **`ai.*` namespace reserved now** (Carbon precedent) for AI-generated content/agent-action surfaces.
- Color is never the only carrier of financial status (icon + label always accompany).

## 3. Money movement framework

One reusable spine for every transaction type (bank transfer, international remittance, bill payment, card payment, loan repayment, investment):

```
INTENT → SOURCE → DESTINATION → AMOUNT → FEES → FX → REVIEW → AUTHENTICATION → PROCESSING → RESULT → RECEIPT
```

Stages are **slots, not screens** — a domestic Aani P2P collapses FEES/FX and merges stages onto one screen; a first-time AED→INR remittance expands every stage. The framework guarantees that wherever a stage renders, it renders with the standard component and the nine questions answered:

**WHO** (payee, CoP-verified) · **WHAT** (transaction type) · **HOW MUCH** (Money component, sender + recipient amounts) · **FROM WHERE** (source account with available balance) · **TO WHERE** (destination, corridor, payout method) · **WHY** (purpose/reference where required) · **WHEN** (delivery time, honestly stated) · **WHAT FEES** (fee vs FX markup vs total — before review) · **WHAT NEXT** (consequence + recovery path).

UAE-specific bindings: CoP is mandatory at DESTINATION for instant payments (REG-05); AED 50,000 Aani limit surfaces at AMOUNT; estimated-vs-guaranteed rate with timestamp/expiry at FX; AUTHENTICATION uses post-OTP methods; RECEIPT is shareable (remittance proof is a real user job) and PDF-accessible.

## 4. Transaction state machine

```
DRAFT → REVIEW → AUTHENTICATION → PROCESSING → { SUCCESS | PENDING | FAILED | UNKNOWN }
SUCCESS → REFUNDED | REVERSED
PENDING → SUCCESS | FAILED | UNKNOWN
UNKNOWN → SUCCESS | FAILED   (resolution required; never terminal silently)
+ CANCELLED (from DRAFT/REVIEW), BLOCKED (compliance/fraud hold, from any pre-terminal state)
```

Every state defines: UI treatment (token-backed status style, icon + label — never color alone) · content (what happened, why, **what happened to the money**, what to do next) · allowed user actions · notification behavior · recovery path.

Hard rules:
- **Never report FAILED when the state is UNKNOWN.** Stock copy: "We're checking your transfer status." with explicit money-state ("No money has left your account" / "Your money is safe while we confirm").
- BLOCKED uses tipping-off-safe generic copy (REG-04).
- Instant rails: PROCESSING may be seconds — design the 2s/30s/5min/next-session sequence for when it isn't.
- Error taxonomy (USER_ERROR, SYSTEM_ERROR, BANK_ERROR, COMPLIANCE_ERROR, FRAUD_BLOCK, NETWORK_ERROR, TIMEOUT, UNKNOWN_TRANSACTION_STATE) maps each failure to message, recovery action, CTA, severity, a11y behavior and analytics event. Internal codes never surface unless genuinely useful.

## 5. Trust & transparency layer

Every high-impact interaction answers the eight trust questions: **Identity** (who am I dealing with — bank, TPP badge, verified payee) · **Intent** (what am I doing) · **Amount** · **Destination** · **Cost** · **Timing** · **Consequence** (what happens after confirm; reversibility stated) · **Recovery** (what if something goes wrong).

Delivery mechanisms: the review screen (GOV.UK check-answers spine: summary list → change links → consequence statement → verb-labeled submit), the KFS component (products), the consent card (Open Finance), CoP result states, and the receipt. The trust layer is a **review checklist applied to every journey**, not a component family alone.

## 6. Security architecture (experience level)

- **Auth ladder:** UAE PASS · passkeys · device biometrics · in-app push approval · PIN (device-local) — SMS OTP deprecated (REG-05 sunset 31 Mar 2026). Step-up model: risk-based escalation at high-value/high-risk moments, with accessible fallbacks that are not SMS.
- **Security states:** trusted device / new device / suspicious activity / session expired / account locked / verification required / auth failed — each with reassuring, actionable treatment.
- **Fraud UX:** tiered interruption library (info banner → caution interstitial → hard stop), scam-coaching defenses (active-call pause, "is someone guiding you?"), suspicious-transaction challenge ("Did you make this transfer?" [Yes, it was me] / [No, secure my account]) with defined severity, escalation and recovery per scenario.

## 7. Multi-brand architecture

```
BANKING CORE  — behavior · accessibility · financial semantics · components · patterns · interaction · state machines
   ├── Bank A theme (conventional)
   ├── Bank B theme (Islamic — terminology dimension: Islamic)
   ├── Bank C theme (youth/neobank)
   └── FinTech theme (white-label)
```

Brand owns: color values (within contrast contract), type stack (from tested AR+EN pairs), logo, illustration, imagery, radius/shape preset, motion personality (within reduced-motion rules), voice inflection.
Core owns everything else. Themes are **pretested presets** (Visa model) validated for contrast in both light/dark and both directions before release. Terminology (conventional/Islamic) is a configuration axis independent of visual brand, so an Islamic window of a conventional bank is one switch, not a fork.

## 8. Responsive & density model

Breakpoint classes: mobile (primary) · tablet · desktop · large desktop · kiosk/ATM-like. Not scaled-down desktop: each pattern declares what stays visible, what collapses, what becomes progressive disclosure, what moves to drawer/bottom sheet. Density modes comfortable/standard/compact map loosely to consumer/SME/treasury surfaces and are user-adjustable where appropriate. PDF is a first-class output surface (statements, KFS, receipts) with its own a11y checklist.

## 9. Journey inventory (Phase 04 flagship set)

1. Personal banking dashboard · 2. Money transfer (domestic/Aani) · 3. International remittance (AED→INR flagship corridor) · 4. Card management (incl. Jaywan co-badge) · 5. Loan/financing application (conventional + Islamic variants from one spine) · 6. Open Finance consent (Al Tareq) · 7. Fraud/security response · 8. SME payment approval (maker-checker).

Supporting journeys named now, designed later: onboarding (UAE PASS), re-KYC, complaint → Sanadak, account closure, statement/proof generation.
