# Regulatory Traceability Matrix

**Purpose:** make the compliance review executable. Every BES pattern/component with a regulatory motivation is listed against its source, with a per-row review status a compliance officer or counsel can work through and sign.

> **Standing disclaimer:** the "BES implementation" column encodes *UX research interpretation* of UAE regulatory frameworks (as researched August 2026), **not legal advice**. No row is compliant until the Review status is set by qualified counsel against the current CBUAE Rulebook and related instruments. Regulations change; re-review on a 6-month cycle or on regulatory notice.

**Review status vocabulary:** `UNREVIEWED` (default) · `VERIFIED` (counsel sign-off, name + date) · `CHANGES-REQUIRED` (issue link) · `N/A` (institution out of scope, e.g., no Islamic window).

| # | Requirement (plain language) | Regulatory source* | BES implementation | Where to inspect | Review status |
|---|---|---|---|---|---|
| REG-01a | Key Facts Statement per product; rate-type prominent; all-fees-inclusive APR labeled | CBUAE Consumer Protection Regulation (Circ. 8/2020) + Standards — disclosure articles | KFS Product Summary component (fixed order, warnings block, fees enumerated) | Spec 18 · gallery patterns page · pages/lending.html demo | UNREVIEWED |
| REG-01b | 5-business-day cooling-off; waiver only with explicit warning | CPR/Standards — cooling-off | Cooling-off pattern P-25; post-signing notice + live cancellation entry; friction-full waiver, never pre-ticked | Spec 23 (P-25), Spec 18 KFS footer | UNREVIEWED |
| REG-01c | 60 days' notice of fee/T&C changes with plain summary | CPR/Standards — variation notice | Change-notice pattern P-29 (old→new comparison, effective date, disagree path) | Spec 23 (P-29) | UNREVIEWED |
| REG-01d | Complaints: published channels; written acknowledgment ≤2 business days | CPR/Standards — complaints | Complaint pattern P-68 with status tracking | Spec 25 (P-68) | UNREVIEWED |
| REG-01e | Bilingual (AR/EN) disclosures and advertising with warning statements | CPR/Standards — advertising & disclosure | Bilingual-parity architecture (doc 29); warning-statement component tiers; disclosure components render identically in both languages | Specs 12, 27, 29 · showcase AR toggle | UNREVIEWED |
| REG-02a | Open Finance consent: explicit, purpose-specific, standardized journey/format | Open Finance Regulation (2024); centralized consent framework | Consent Request renders the standardized format (data clusters, purpose, absolute expiry, revocation note); equal-weight Allow/Cancel | Spec 21 · gallery patterns page | UNREVIEWED |
| REG-02b | Consent management & revocation | Open Finance framework | Consent Dashboard + ≤2-tap Revocation flow; expiry countdowns; no auto-renew | Spec 21 | UNREVIEWED |
| REG-02c | Only verified/licensed TPPs presented as trusted | Trust framework / participant directory | TPP Identity Card: verified badge from directory; unverified = hard stop, no Allow button | Spec 21 | UNREVIEWED |
| REG-03 | National digital identity for onboarding/signing; legal equivalence messaging | UAE PASS framework | Identity sign-in + handoff patterns; signing ceremony; verified read-only fields | Spec 20 | UNREVIEWED |
| REG-04a | eKYC via approved channels; document verification flows | AML framework (Fed. Decree-Law 20/2018; CBUAE AML Rulebook) | Onboarding stepper, document capture with retry-strategy guard, verification status system, re-KYC ladder | Specs 20, 22 (P-04) | UNREVIEWED |
| REG-04b | No tipping-off in hold/review communications | AML framework | BLOCKED-state copy law: generic "additional checks required"; forbidden specificity documented | Specs 07 §4, 25 (P-73), 27 glossary | UNREVIEWED |
| REG-05a | SMS OTP/static passwords phased out (Mar 2026); app-based/biometric auth | CBUAE Notice 2025/3057 | Auth set = biometric/passkey/push/PIN; SMS OTP absent; Code Entry marked non-auth | Specs 09, 20 · journey auth step | UNREVIEWED |
| REG-05b | Confirmation of Payee before transfers | Notice 2025/3057 / instant-payments rails | Payee Verification component: match/close/no-match/unavailable; no-match proceed = explicit risk friction, escalates review warning tier | Spec 16 · journey step 2 · gallery | UNREVIEWED |
| REG-05c | Session suspension on screen-share/remote-access/active-call risk | Notice 2025/3057 | Session Pause Interruption at z.critical; scam-checkpoint variant | Spec 20 | UNREVIEWED |
| REG-05d | Consumer fraud education; anti-impersonation | Notice 2025/3057 + CBUAE campaigns | Verified-channel surfaces ("we never ask for your password"), tiered warnings, report-phishing entry | Specs 20, 25 (P-62, P-66) | UNREVIEWED |
| REG-06 | Consent-based data processing; rights (access/correct/delete/object); unbundled consent | PDPL (45/2021); DIFC/ADGM regimes where applicable | Granular unbundled consents (never pre-ticked), Privacy Center with rights flows, layered notices, strictest-regime default | Specs 21, 22 (P-10) | UNREVIEWED |
| REG-07 | Digital accessibility for People of Determination; WCAG AA expectations | National Policy for Digital Accessibility (2024); TDRA guidance | WCAG 2.2 AA floor engineered into tokens/components; automated audits + human protocols; PDF accessibility requirements | Spec 28 · docs/audits/ · docs/testing/ | UNREVIEWED |
| REG-08a | Islamic products: explain Shari'ah structure; disclose profit-sharing ratio/weightages/frequency | HSA framework; Consumer Protection Standards Islamic disclosures | Shari'ah Structure Explainer (disclosure-grade), Profit Rate Display distinct from APR, terminology dimension (profit rate/financing/takaful) | Specs 18, 27 §2 | UNREVIEWED |
| REG-08b | Services marketed as Islamic must be Shari'ah-compliant; no mis-selling | CPR Art. 11 | Conventional/Islamic differentiation system; certification trust mark | Specs 18, 30 | UNREVIEWED |
| REG-09 | Instant-payment rails conventions (proxy addressing, limits) | Aani scheme rules (Al Etihad Payments) | Proxy payee entry, QR patterns, AED 50,000 limit surfaced at amount entry | Specs 13 (Limit Indicator), 16 | UNREVIEWED |
| REG-10 | Ombudsman escalation disclosure in complaints | Sanadak framework | P-68 includes the 15-day → Sanadak escalation disclosure verbatim slot | Spec 25 (P-68) | UNREVIEWED |
| REG-11 | Per-license/jurisdiction disclosure variants | Licensing landscape (CBUAE/DIFC/ADGM) | Compliance-variant architecture: per-jurisdiction content sets, never hard-coded copy | Specs 30 §2, 06 §3 | UNREVIEWED |

\* Source names are working references from UX research; counsel should pin exact article/clause numbers during review — a column for that is intentionally left to the reviewer copy.

## How to run the review

1. Copy this file to `docs/compliance/reviews/YYYY-MM-DD-review.md`.
2. Reviewer works row by row against the current Rulebook text, setting status + initials + date + exact clause citations.
3. `CHANGES-REQUIRED` rows get a GitHub issue (label `compliance`) describing the gap; the linked pattern cannot reach **Stable** until resolved and re-reviewed.
4. Completed review is referenced from STATUS.md's verification ledger and the release notes of the next version.

## Reviewer guide (what BES needs from counsel)

- Judge the **experience contract**, not the pixels: does the pattern's structure/content order/timing satisfy the requirement in all mandated languages?
- Where regulation prescribes exact wording (e.g., KFS warning phrases), supply the canonical AR+EN strings — they'll be added to the glossary as locked entries.
- Flag requirements BES has *missed entirely* — absence rows are the most valuable finding and become proposals via the standard template.
