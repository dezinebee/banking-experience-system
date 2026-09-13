# 06 — Reference & Competitive Analysis

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

Two audits: (A) design systems studied for principles, (B) UAE banking experiences benchmarked. Per the brief: extract principles, never copy styling. Research: live, August 2026.

---

## Part A — Reference design systems

### A1. Visa Product Design System (design.visa.com) — *the payments-native reference*

- **Architecture:** Base elements → Design tokens (designer Figma variables + developer CSS variables/Flutter) → ~40 components → 13 patterns → content guidelines → chart components. Multi-framework (React, Angular, Flutter, plain CSS) plus "Abstracts" (behavioral primitives).
- **Financial domain lives in patterns + utilities:** Card input (IIN/BIN network detection, masking rules, format forgiveness), OTP, Wizard, Feedback & status, plus a `useCardNumberValidation` hook — financial logic as a system primitive.
- **Theming = guard-railed presets:** 10 pretested light/dark color themes (explicitly for white-labeling), shape/density/type modes, meta-tokens `--theme-scale-factor` and `--theme-responsive-factor`.
- **Accessibility:** VGAR — WCAG 2.2 AA distilled into per-platform checklists (**Web, Mobile, PDF**); components shipped accessibility-tested; focus-trap/ID utilities.
- **Forms:** validate onBlur; server-error scenario library including the security case where the failing field cannot be identified; don't disable submit; "Required" spelled out over asterisks.
- **Status:** component choice by placement × persistence × disruption; 4-tier attention scale; never stack alerts.
- **Gap:** no RTL guidance at all.
- **Take:** pattern template, financial primitives, guard-railed theming, VGAR model, status framework.

### A2. GOV.UK Design System — *the error-prevention and content-design reference*

- **Task-based pattern taxonomy:** "Ask users for…" (bank details, payment card details, addresses, dates…) and "Help users to…" (check answers, recover from errors, task lists, confirmations) — maps almost 1:1 to banking journeys.
- **Validation doctrine:** prevent first (accept all formats, ignore stray characters); on error re-show with input preserved, `Error:` in title, error summary with focus moved to it; **validate on submit** (explicitly opposite Visa — BES will resolve per-context, see below); always server-side; `novalidate`; never use validation for eligibility.
- **Bank details pattern:** per-state specified error copy; international variant = IBAN + BIC showing only country-relevant fields (UAE is an IBAN market — direct analogue).
- **Check answers → consequence statement → verb-labeled submit → confirmation page:** the canonical irreversible-transaction spine; documented rationale (raises confidence, cuts errors).
- **Docs:** live example → code tabs → when (not) to use → how it works → specified error messages → **"Research on this pattern"** (unique transparency) → backlog link. Component lifecycle statuses (Trial → Stable).
- **Gaps:** no tokens, no theming, no RTL — single-brand by design.
- **Take:** taxonomy, validation doctrine, check-answers spine, research transparency, lifecycle statuses.

### A3. Salesforce Lightning (SLDS 2) — *the runtime theming mechanism*

- Structure separated from theme; Sass tokens replaced by **CSS custom-property "styling hooks"** (pierce Shadow DOM): global `--slds-g-*` vs component `--slds-c-*`, with cross-version compatibility enabling incremental migration.
- **Take:** CSS custom properties as the multi-tenant theming contract; explicit global-vs-component hook taxonomy; the agentic-UI positioning as an early AI-surface signal.

### A4. Adobe Spectrum / Spectrum 2 — *the internationalization and token-dimension reference*

- Tokens as design data (public repo); global → system → component tiers; Spectrum 2's cascade-token format treats tokens as a queryable decision database; platform scale, density, contrast and color theme are **token dimensions, not variants** — including user personalization.
- **Best-in-class RTL:** dedicated bi-directionality foundation *plus per-component RTL sections* (Table: column order + alignment inversion; Meter: fill direction).
- **Take:** i18n documented per component; adaptive dimensions in tokens; component doc template (anatomy → options → behaviors → usage → content standards → i18n → keyboard).

### A5. IBM Carbon — *the token-rigor and ecosystem reference*

- Ecosystem layering: IBM Design Language → Carbon core → domain layers (Carbon for Products/Cloud/IBM.com), patterns harvested from products; honest tiered framework support.
- **Role-based tokens with contrast in the contract:** `$layer-01/02/03`, `$text-primary/secondary/helper/error`, `$support-error/success/warning/info` **plus graduated `$support-caution-minor/major/undefined`** (useful seed for risk severity); component tokens never reused outside their component; a dedicated **AI token suite**.
- Docs: Overview / Usage / Style / Code / Accessibility tabs.
- **Take:** token vocabulary (theme/token/role/value), layer model, caution gradation, core-vs-domain ecosystem, AI namespace reservation.

### A6. Briefly

- **Atlassian:** cleanest semantic naming grammar (`color.text`, `color.background.default`, chart token family); high-contrast + non-color themes (density, reduced motion) from one token layer.
- **USWDS:** constrained-token philosophy (tokens as limited "keys" consumed via functions, never raw values); banking-adjacent components (input mask, prefix/suffix, memorable date, step indicator, character count, language selector).
- **Finastra (design.fusionfabric.cloud):** the only fintech system with concrete Arabic/RTL rules — mirror layout but keep embedded LTR strings LTR; back button points right; don't mirror clocks/media; numbers read LTR, right-aligned; never mix numeral systems; no letter-spacing (cursive); +1–2px size, taller line-height; Arabic comma; weekday abbreviations fail.
- **Mastercard:** no public product system. **Capital One:** organizational lesson — parallel top-down (global library) + bottom-up (team consistency) rollout from written principles.

### A7. Synthesis — the buildable core

| Layer | Standard | Model |
|---|---|---|
| Tokens | 3 tiers (primitive → semantic role → component) as CSS custom properties; contrast in token contract; direction/density/scale as token dimensions | Carbon + Atlassian naming, SLDS 2 mechanism, Spectrum dimensions |
| Theming | Pretested brand presets; light/dark via attribute + `prefers-color-scheme`; RTL as first-class mode with Arabic type metrics | Visa + Finastra |
| Components | Generic set with per-platform a11y checklists (Web/Mobile/PDF) | Visa VGAR + Carbon doc tabs |
| Financial patterns | Card input, IBAN entry (UAE 23-char), auth (post-OTP), amount entry, payee mgmt, check-answers→confirm→receipt, transaction status, consent | Visa + GOV.UK |
| Errors | Prevention rules, submit-time summary + inline, focus mgmt, error-copy dictionary, server-error scenarios | GOV.UK + Visa |
| Docs | Example → anatomy → when(-not) → behaviors → content → **RTL section** → a11y → research/lifecycle | GOV.UK + Spectrum + Visa hybrid |
| Governance | Trial/Stable lifecycle, contribution criteria, research loop, core + domain layers | GOV.UK + Carbon |

**Open decision carried to Phase 02:** validation timing. GOV.UK says on-submit; Visa says onBlur. BES direction: on-submit as default (inclusion-safe), onBlur permitted for high-confidence format fields (IBAN, card number, EID) where research shows net benefit — decided per pattern, documented per component.

---

## Part B — UAE banking landscape audit

### B1. Score summary (digital experience reputation, Aug 2026)

| Player | Standout | Weakness |
|---|---|---|
| ENBD X | ~4.7★; 150+ instant services; DirectRemit 60s; in-app investing | 2023 redesign buried features initially |
| ADCB Hayyak | Onboarding machine — 58% of new acquisition, NPS 60 | Onboarding-app split from main app |
| Mashreq / Neo | >50% fully-digital customers; corporate persona dashboards | Usability edge cases, support |
| FAB | Scale; Payit innovation (SNPL remittance) | Worst support reputation of tier-1; account closure dead-ends |
| DIB | "Banking in Minutes" UAE PASS onboarding | Trustpilot 1.6; maintenance windows; digital lag |
| Emirates Islamic | World's best Islamic digital bank 2025; in-app gold | — |
| Wio | Profitable; Spaces; multi-currency; 6% salary savings; clean app | Thin human support |
| Liv / Liv X | Lifestyle acquisition engine; 2025 relaunch | Depth plateau vs Wio |
| Mbank | Inclusion positioning (no minimums, 5-min open) | eKYC loops, crashes — reliability failure at the inclusion end |
| ruya | Modern Islamic UX; values-led voice; Sharia-compliant BTC | Young, thin product set |
| Zand | Corporate/digital-asset frontier (AED stablecoin) | Not a consumer UX reference |
| Careem Pay / Botim / e& money | Embedded remittance where users already live | Not full banking |
| LuLu / Al Ansari | Blue-collar trust, hybrid digital+branch, corridor breadth | FX-spread opacity behind "zero fee" |

### B2. What works (adopt as system patterns)
UAE PASS 5-minute onboarding · instant virtual cards · remittance as first-class flow (corridor payouts, rate alerts, SNPL) · salary-anchored switching · Spaces/goal sub-accounts · multi-currency accounts · Aani P2P (phone-number addressing, QR, request/split) · modern Islamic UX (ruya/EI).

### B3. What doesn't (design against)
Support cliff after onboarding · account-closure dead-ends · redesigns without wayfinding · reliability failures for inclusion segments · fee/FX-spread opacity · translated-not-designed Arabic · legacy Islamic digital lag.

### B4. What's missing (whitespace BES occupies)
Published design-system-level RTL/bilingual standards · blue-collar-grade UX (low literacy, vernacular, voice) · cross-bank financial-health layer (Open Finance-ready) · transparent total-cost remittance (mid-market-rate disclosure) · unified conventional/Islamic presentation patterns · WCAG maturity · SME depth beyond Wio.

### B5. What is UAE-specific (the system's reason to exist locally)
Identity rails making instant KYC real · remittance as a core banking job · 88% expat transience (open-fast, multi-currency, close-cleanly) · bilingual RTL parity as launch requirement · Islamic banking as mainstream with dual taxonomy · salary/WPS anchoring · fast-standardizing state rails (Aani/Jaywan/Al Tareq) · super-app gravity (banking as a feature inside Botim/Careem).

---

### Key sources
design.visa.com (patterns: card-input, forms, feedback-and-status; tokens) · design-system.service.gov.uk (validation, bank-details, check-answers) · carbondesignsystem.com (themes, color tokens) · salesforce.com/blog/what-is-slds-2 + developer.salesforce.com LWC styling hooks · spectrum.adobe.com/page/bi-directionality + adobe/spectrum-design-data · designsystem.digital.gov · atlassian.design/foundations/tokens · design.fusionfabric.cloud/foundations/rtl · UXDA ENBD case study · theasianbanker.com (Hayyak) · Trustpilot/ComplaintsBoard/masarif.ae corpora · fintechnews.ae · Mambu (Wio) · ruyabank.ae.
