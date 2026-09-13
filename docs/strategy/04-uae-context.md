# 04 — UAE Context

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

What is genuinely UAE-specific — the context that makes a generic global banking kit insufficient. Sources: live research Aug 2026 (key URLs at end).

---

## 1. Market shape

- Banking assets ~AED 5.3T, growing ~17% YoY. Top banks: FAB, Emirates NBD (9.8M+ customers), ADCB, DIB (largest Islamic bank), Mashreq, ADIB.
- 250+ active fintechs; ~half of customers hold a digital-bank account; licensed digital banks: Wio (profitable 2024, AED 50B+ deposits), Zand (corporate/digital assets), ruya (Islamic community), Mbank, Reem — plus incumbent digital brands Liv (ENBD) and Mashreq Neo.
- Smartphone ~99%; app is the primary channel for 72%.

## 2. National rails — the system must treat these as platform primitives

### UAE PASS (identity)
National digital identity + SSO + legally equivalent digital signature. The de-facto onboarding standard: 5-minute account opening at Mbank, ruya, DIB, ADCB Hayyak (58% of ADCB's new acquisition). Tourist Identity extends it to visitors.
**BES primitives:** "Continue with UAE PASS" component (official branding, primary path), app-switch handoff pattern with state preservation, verified read-only prefilled fields, signing ceremony pattern, SOP-level (basic vs verified) upgrade interstitial.

### Aani (instant payments — Al Etihad Payments)
Real-time transfers up to AED 50,000 via mobile number, email or QR; ~12.5M users, 74 FIs; request-to-pay, split payments; adopted for federal government fees. Confirmation of Payee rides on it (see doc 05).
**BES primitives:** proxy payee entry (contact picker), proxy registration management, QR generate/scan (P2P + merchant variants), instant-payment state model (success in seconds; distinct timeout/unknown handling), inline AED 50,000 limit surfacing.

### Jaywan (domestic card scheme)
Co-badged cards (Jaywan domestic + international scheme abroad) rolling out from H2 2025.
**BES primitives:** dual-scheme card art representation in card management/wallets, scheme-selection moments, Jaywan brand asset slots.

### Al Tareq / Nebras (Open Finance)
Centralized consent + authentication with standardized journeys (see doc 05 §2). Consent screens are substantially prescribed, not invented.

### Sanadak (ombudsman)
Complaint escalation disclosure ("unresolved after 15 days → Sanadak") is now standard consumer-rights content.

## 3. Remittance is core banking, not an add-on

~$43B/yr outbound; corridors India (~28%), Pakistan (~13%), Philippines, Bangladesh, Egypt, Nepal, Sri Lanka. Digital share 14% → 37% (2020→2025). Local inventions: 60-second DirectRemit (ENBD), Send-Now-Pay-Later remittance credit (Payit, Botim), corridor-specific payouts (bank / wallet — GCash, Vodafone Cash / cash pickup), chat-embedded remittance (Botim), rate alerts (Al Ansari). "Zero-fee" corridors recoup margin in FX spread — a transparency gap BES addresses head-on (estimated vs guaranteed rate, fee vs markup, always).
**BES consequence:** the FX/remittance pattern family (doc 07 §3) is a flagship, not an appendix; corridor-aware recipient components; payout-method selection; delivery-time honesty.

## 4. Language and direction

- Arabic + English bilingual is a launch requirement (also a regulatory one for disclosures/advertising). Arabic-first branding is a national identity signal (Aani, Jaywan, Mbank, ruya).
- Market failure mode: **translated-not-designed Arabic** — mirrored text but unmirrored icons/progress bars, bidi breakage in mixed Arabic + Latin IBANs/amounts, cramped adjacent tap targets.
- Arabic typography facts the system encodes: no capital letters (emphasis patterns must not rely on caps), cursive script (never letter-space), needs +1–2px optical size and taller line-height, Arabic comma (،), day-of-week abbreviations fail (identical first letters), truncation follows direction, embedded LTR strings (URLs, IBANs) stay LTR, numbers read LTR and right-align in RTL context.
- **Numeral policy:** Western Arabic numerals (0–9) as default for financial figures, Eastern (٠١٢٣) available as a locale preference — never mixed in one context.
- Beyond Ar/En: Hindi, Urdu, Tagalog, Malayalam, Bengali matter for inclusion. BES v1 ships Ar/En with a content architecture (message catalog, no hardcoded strings, direction-agnostic layouts) that makes vernacular expansion a content project, not a re-engineering project.
- Calendars: Gregorian primary; Hijri dual-display slot for relevant contexts (Islamic products, cultural moments).

## 5. Islamic finance is mainstream

- DIB is the world's largest Islamic bank; ruya and Emirates Islamic ("World's best Islamic digital bank 2025") prove Islamic + modern UX coexist; ADCB Hayyak offers a conventional/Sharia toggle at onboarding; Tamara markets Sharia-compliant BNPL.
- Higher Shari'ah Authority governs; Consumer Protection Standards contain Islamic-specific disclosure duties (explain the Shari'ah concept; disclose profit-sharing ratio, weightages, distribution method/frequency).
- **BES consequence:** a terminology layer (interest→profit rate, loan→financing, insurance→takaful, penalty→charity donation where applicable), Shari'ah concept explainer component (a disclosure requirement), profit-rate display distinct from APR display, Shari'ah-certification trust mark, dual conventional/Islamic differentiation system to prevent mis-selling. Terminology switches by product configuration without breaking underlying components.

## 6. Salary anchoring and WPS

Salary transfer is the switching moment: minimum-salary gates historically excluded ~1.7M workers; Wio's 6% salary-linked savings and Neo's salary cashback weaponize it. WPS (Wage Protection System) payroll shapes SME needs.
**BES consequence:** salary-account journey primitives, payroll patterns in SME suite, limit/eligibility communication patterns that route (never shame) users below thresholds.

## 7. Digital experience quality — market lessons

| Lesson | Evidence |
|---|---|
| Onboarding speed is a competitive stat | Hayyak = 58% of ADCB acquisition; 5-min bar everywhere |
| The support cliff destroys trust post-onboarding | FAB 1.1★ complaints, Mbank eKYC loops, Wio's thin human support |
| Redesigns must include wayfinding | ENBD X 2023 backlash despite eventual ~4.7★ |
| Fee opacity erodes trust measurably | surprise dormancy fees, FX-spread "zero fee" claims |
| Heritage brand ≠ digital trust | DIB Trustpilot 1.6 vs ruya's praised app |
| Lifestyle features ≠ banking depth | Liv's plateau vs Wio's profitable rise |
| Embedded finance gravity is real | Careem Pay, Botim, e& money meet users in daily-life apps |

**BES consequence:** journeys include the unglamorous lifecycle (support escalation, complaint → Sanadak, account closure, re-KYC) as first-class patterns; degraded/maintenance states are designed; "what changed" wayfinding pattern for releases.

## 8. Environment range

Mobile-first (majority), desktop dashboards (SME/corporate/wealth), tablet, kiosk/ATM-adjacent surfaces, and PDF (statements, KFS, contracts — with accessibility requirements). Density modes (comfortable/standard/compact) map to consumer → SME → treasury surfaces.

---

### Key sources
Alvarez & Marsal UAE Banking Pulse Q3 2025 · CBUAE FSR 2025 (Aani) · aep.ae (Aani/Jaywan) · PaymentsCMI UAE remittance data · Khaleej Times/ADL mobile-banking survey · The Asian Banker (ADCB Hayyak) · UXDA ENBD case study · masarif.ae & Trustpilot review corpora · Finastra RTL foundations (design.fusionfabric.cloud/foundations/rtl) · OMA UAE population statistics 2025 · NOW Money / UNCDF financial-inclusion studies · ruyabank.ae · Mambu Wio case study.
