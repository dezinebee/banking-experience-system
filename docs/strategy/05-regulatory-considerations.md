# 05 — Regulatory Considerations

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

> **Not legal advice.** This document translates UAE regulatory frameworks into UX design mandates for the system. Every adopting institution must verify against the CBUAE Rulebook (rulebook.centralbank.ae) and its own counsel before shipping compliance-critical flows or copy.

Format per area: regulation intent → what it requires → **BES mandates** (the patterns/components the system must therefore ship). The pattern-to-regulation traceability map in Phase 02 will reference the IDs used here (REG-01…).

---

## REG-01 · CBUAE Consumer Protection Regulation (Circular 8/2020) & Standards (2021)

**Intent:** fair treatment, transparency, informed consent across all Licensed Financial Institutions.

**Requirements found:** Key Facts Statement (KFS) per product with rate-type prominence (fixed/variable/hybrid) and all-fees-inclusive APR labelled "Annual Percentage Rate"; bilingual Arabic/English disclosures and advertising with warning statements; **5-business-day cooling-off** after signing (waivable only via explicit written warning, refunds net of direct costs); **60 calendar days' notice** of fee/T&C changes with plain-language summary; complaints published + acknowledged in writing within 2 business days, ~15 calendar days to respond before escalation.

**BES mandates:**
- **KFS component** — standardized, printable/downloadable pre-contract summary: product name, rate-type badge, APR (labelled, all-in), fees table, warnings block, cooling-off notice. Identical rendering AR (RTL) and EN. Reused across loans, financing, cards, savings, investments (brief §19).
- **Warning-statement component** — tiered visual treatment; non-dismissible inside contract flows; usable in ads/product pages.
- **Cooling-off pattern** — post-signing confirmation stating the right; friction-full waiver (never pre-ticked); visible cancellation entry point for 5 days.
- **Change-notice pattern** — "what's changing" plain-language summary + revised-terms presentation, timed 60 days ahead; includes disagree-path explanation.
- **Complaint pattern** — first-class navigation entry; channels, timelines, status tracking (acknowledged → responded → escalate), with **Sanadak** escalation disclosure (REG-10).
- **Fee-transparency doctrine** — principle 02's enforcement: totals before review, "why am I being charged?" pattern.

## REG-02 · Open Finance Regulation (2024) — Al Tareq / Nebras

**Intent:** licensed Open Finance ecosystem under the FIT programme; banks and insurers as mandated data holders; central API hub (Nebras), consumer-facing trust framework (Al Tareq); first OFP licenses issued 2026.

**Requirements found:** explicit, purpose-specific consent by affirmative action; **standardized consent journey and information format** regardless of TPP/bank; redirect model (TPP → bank Consent & Authentication App/Page with MFA → back), with app-not-installed fallbacks preserving consent state.

**BES mandates:**
- **Consent screens conform to the Al Tareq standard format** (data clusters, purpose, duration/expiry, TPP identity, revocation info) — the system provides compliant rendering, not invented layouts.
- **Consent dashboard pattern** — active consents list, per-consent detail, one-tap revoke, sharing history.
- **Redirect handoff pattern** — trust-preserving interstitials ("You're being taken to…"), state preservation, graceful fallbacks.
- **TPP trust signals** — verified-participant badge sourced from the Nebras directory; unverified never presented as trusted.
- **Expiring-permission primitives** — expiry countdowns, renewal prompts; consent tokens in the financial semantic model (consent.required/pending/granted/expired/revoked).

## REG-03 · UAE PASS

**Intent:** national digital identity/SSO/signature with legal equivalence to handwritten signatures; accepted KYC across 15+ banks.

**BES mandates:** official "Continue with UAE PASS" component; app-switch handoff with timeout handling and "why you're being redirected" messaging; signing ceremony (document review → UAE PASS handoff → signed receipt with legal-equivalence note); verified read-only prefilled fields with source indicator; SOP-level distinction and "upgrade your UAE PASS" interstitial; non-registered-user fallback paths.

## REG-04 · KYC / AML (Federal Decree-Law 20/2018; CBUAE AML Rulebook)

**Requirements found:** Emirates ID validation via ICP gateway / UAE PASS; individuals: EID/passport + address proof; corporates: trade license, incorporation, UBO; records ≥5 years; risk-based EDD; continuous monitoring (2026 guidance).

**BES mandates:**
- **Onboarding stepper** with document-capture components (EID front/back, NFC/OCR states, liveness selfie, uploads) — each with error/retry states and "why we ask" microcopy.
- **Verification status system** — pending / verified / needs-attention surfaced in-account; **re-KYC pattern** for EID expiry (reminder → deadline → restriction warning); tiered-KYC limit indicators and upgrade paths.
- **EDD interstitials** — "we need more information" flows (source-of-funds questionnaires, uploads) in a neutral, non-accusatory tone.
- **Payment-under-review states** — held/queried payments with expected timeframes and secure document requests; **copy stays generic to avoid tipping-off** ("additional checks required" — never the specific trigger).

## REG-05 · Fraud & Security — CBUAE Notice 2025/3057 (May 2025)

**Requirements found:** SMS/email OTPs and static passwords **phased out by 31 March 2026** (app-based/biometric/passkey replaces them; 3DS-SMS fraud refundable from July 2025); **Confirmation of Payee mandatory for instant payments** (display payee name, account, bank, account type before confirm); apps must **suspend sessions** on screen-share/malware/remote-access detection **or when the consumer is on an active phone call**; mule/dormant monitoring; anti-impersonation programs; consumer education expected.

**BES mandates:**
- **Auth pattern set post-OTP:** device biometrics, in-app approval push, passkeys, UAE PASS — with accessible non-SMS fallbacks. SMS-OTP components exist only as deprecated/legacy with sunset guidance.
- **Confirmation-of-Payee screen** — match / close match / no match states; payee details block; proceed-at-own-risk friction on mismatch.
- **Scam-interruption patterns** — full-screen "we paused this session" (active call, screen share) with calm copy and safe-resume; "is someone guiding you?" checkpoint on high-risk payments.
- **Tiered fraud-warning library** (info → caution → hard stop) triggered by new payee, first payment, high value, risky categories.
- **Verified-channel education surfaces** — "we will never ask for your OTP/password" cards/banners fed by campaign content.

## REG-06 · Data Protection — PDPL (45/2021), DIFC, ADGM

**Requirements found:** consent-default legal basis, clear/specific/revocable; sensitive data needs explicit consent; rights: access, correction, erasure, portability, objection to automated processing. Banking/credit data also sits under CBUAE confidentiality rules; DIFC (GDPR-like) and ADGM have their own regimes.

**BES mandates:** granular unbundled consent (never pre-ticked; marketing separate from service); withdrawal path mirrors grant path; **privacy center pattern** (rights-exercise flows + request tracking); layered just-in-time privacy notices, bilingual; cross-border transfer disclosure line; **build to the strictest regime (DIFC/GDPR-like)** so one component set serves all three jurisdictions.

## REG-07 · Accessibility — National Policy for Digital Accessibility (2024)

**Requirements found:** WCAG 2.1 AA benchmark for government digital services; TDRA platforms and UAE Design System 2.0 built to **WCAG 2.2 AA**; People of Determination and senior citizens explicitly targeted; financial services import the expectation via UAE PASS/Aani adjacency and CBUAE fair-access posture.

**BES mandates:** WCAG 2.2 AA floor system-wide; Arabic screen-reader and bidi-text test coverage (amounts, IBANs, names in mixed strings); elderly/low-literacy patterns (large-type mode, simplified flows, human escape hatches); accessibility statement pattern; benchmark conventions against UAE Design System 2.0; Web/Mobile/**PDF** requirement checklists (statements and KFS are documents).

## REG-08 · Islamic Banking — Higher Shari'ah Authority; CPS Islamic disclosures

**Requirements found:** HSA rules binding; Internal Shari'ah Supervision Committees; CPS requires explaining the applicable Shari'ah concept per product and disclosing profit-sharing ratio, weightages, distribution method and frequency (deposits) and structure + takaful requirements (financing); Article 11 CPR: services marketed as Islamic must be Shari'ah-compliant.

**BES mandates:** terminology layer (interest→profit rate, loan→financing, insurance→takaful…), ideally content-linted; **Shari'ah concept explainer component** (disclosure, not decoration); **profit-rate display** (ratio, weightages table, frequency) distinct from APR display — while KFS still carries all-in cost; Shari'ah-certification trust mark (ISSC/HSA); conventional-vs-Islamic differentiation system for dual-product banks.

## REG-09 · Aani & Jaywan (Al Etihad Payments)

See doc 04 §2. Regulatory intersection: CoP (REG-05) rides on Aani; AED 50,000 limit surfaced inline; federal-government adoption makes these rails' conventions familiar defaults.

## REG-10 · Sanadak (Ombudsman, 2024)

**Requirements found:** complain to FI first (≤15 calendar days) → escalate to Sanadak (free; ~15 working days resolution; 3-year/2-year time limits).
**BES mandate:** complaint pattern includes the standard escalation disclosure with link.

## REG-11 · Licensing landscape (context)

Full digital banks, incumbent digital brands, payments licenses (SVF), DIFC/ADGM entities, Oct 2025 digital-asset licensing integration. **BES mandate:** compliance-variant architecture — per-jurisdiction/per-license content and component variants, never hard-coded copy.

---

## The regulation-as-pattern thesis

GOV.UK's core move — turning policy into named, researched patterns — is directly transferable: CBUAE prescriptions (KFS, cooling-off, CoP, consent format, session suspension) are *experience specifications*. BES ships them as versioned patterns with a traceability table (pattern ID ↔ REG ID ↔ source article), so a compliance team can audit the experience by auditing the pattern inventory.

### Key sources
rulebook.centralbank.ae (Consumer Protection Regulation & Standards; Open Finance Regulation; AML rulebook; Shari'ah governance) · Pinsent Masons & Clifford Chance Open Finance briefings · openfinanceuae.atlassian.net (Al Tareq consent guides) · sardine.ai / descope.com / onespan.com analyses of Notice 2025/3057 · securiti.ai & Gowling WLG on PDPL · TDRA national digital accessibility policy · centralbank.ae Islamic finance/HSA pages · sanadak.gov.ae · aep.ae.
