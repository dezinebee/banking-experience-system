# 01 — Design System Vision

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

---

## 1. Proposition

> A scalable design language for building clear, trustworthy, accessible and intelligent financial experiences for the UAE market.

The Banking Experience System (BES) is not a UI kit. It is a **domain-specific financial experience system**: a set of foundations, tokens, components, patterns and journey blueprints that encode *financial behavior* — money movement, transaction states, disclosure, consent, fraud response, bilingual RTL/LTR — so that any UAE bank, neobank, fintech or payment provider can assemble the majority of its experience from tested, compliant, accessible parts.

## 2. Why this system needs to exist

Research (see doc 06) shows a specific whitespace:

1. **No public design system is Arabic/RTL-first.** Visa, GOV.UK, Carbon, Spectrum and SLDS 2 collectively solve tokens, error prevention, financial patterns and theming — but none ships Arabic type metrics, mirroring specs, dual numeral policy, or bilingual disclosure components. Only Finastra publishes partial RTL guidance.
2. **No system treats money as a first-class primitive.** None defines an Amount component, a transaction lifecycle vocabulary, fee-disclosure patterns, or Islamic finance semantics.
3. **No UAE bank publishes a design system.** Each mirrors RTL ad hoc, invents its own profit-rate display, and rebuilds consent, KYC and remittance flows from scratch. Digital quality varies wildly (ENBD X ~4.7★ vs DIB Trustpilot 1.6).
4. **Regulation is converging on standardizable UX.** CBUAE's Consumer Protection Standards (KFS, cooling-off, warnings), Open Finance / Al Tareq (standardized consent journeys), Fraud Notice 2025/3057 (Confirmation of Payee, OTP deprecation), and the national accessibility policy all *prescribe* experience behavior — a design system is the natural delivery vehicle.

**The synthesis is the product:** architect like Carbon/SLDS 2, document like GOV.UK, pattern like Visa, internationalize beyond Spectrum — for UAE banking specifically.

## 3. Design philosophy

- **Trust by design.** Every high-impact interaction answers: who, what, how much, from where, to where, at what cost, when, with what consequence, and what recovery exists.
- **Clarity by default.** Financial information is immediately understandable; transparency is never traded for conversion.
- **Confidence at every financial decision.** Review → correct → confirm before anything irreversible.
- **Accessibility as a foundation.** WCAG 2.2 AA is the floor, encoded in tokens and components, not audited at the end.
- **Consistency without removing product personality.** Core owns behavior; brands own expression.

Banking is not generic SaaS. The user may be moving money, borrowing, investing, verifying identity, responding to fraud, or reviewing a legally significant agreement. The system accounts for **financial consequence**, not just visual consistency.

## 4. What the system standardizes

Visual language · interaction behavior · financial UX · money movement · trust & transparency · security · fraud communication · accessibility · Arabic/English localization · RTL/LTR behavior · financial data visualization · regulatory-aware communication · Open Finance consent · multi-brand theming · retail, SME and corporate experiences.

## 5. Objectives and success criteria

| Objective | Success criterion |
|---|---|
| Reusable financial experience logic | A new UAE digital bank could build ~80% of its retail experience from BES journeys, patterns and components |
| Bilingual parity | Every component ships with documented Arabic/RTL behavior; no "translation pass" exists as a phase |
| Regulatory readiness | KFS, cooling-off, consent, CoP, warning and complaint patterns exist as named, versioned patterns mapped to their regulatory source |
| Accessibility | Components pass WCAG 2.2 AA by construction; contrast encoded in token definitions; Web/Mobile/PDF requirement checklists exist |
| Multi-brand | A conventional brand, an Islamic brand and a youth/neobank brand can be themed from the same core without touching behavior |
| Safe state handling | Every financial state — including UNKNOWN — has defined UI, content and recovery; no false failure messaging is possible using stock components |

## 6. Non-goals

- Not a generic cross-industry UI kit; financial semantics are load-bearing.
- Not a copy of Visa/Material/Stripe/GOV.UK — principles extracted, styling original.
- Not a component-count contest. The objective is the most reusable financial experience logic, prioritized by frequency × financial risk × reusability × complexity.
- Not legal advice. Regulatory patterns encode UX interpretations that each adopting institution must verify.

## 7. Audience for the system

- **Product designers** at banks/fintechs assembling journeys.
- **Engineers** consuming tokens and coded components (web first; token contract designed to extend to native mobile).
- **Content designers** using the bilingual terminology layer and message frameworks.
- **Compliance & risk teams** verifying that experience patterns map to regulatory requirements.
- **Brand teams** theming within guard-railed presets.

## 8. Naming

"Banking Experience System" is the working name. Naming criteria for the final identity: pronounceable in Arabic and English, no unintended meaning in Hindi/Urdu/Tagalog (major UAE languages), available as a namespace/token prefix (e.g. `bes-`), and distinct from existing UAE rails brands (Aani, Jaywan, Al Tareq, Sanadak). Candidate exploration is scheduled for end of Phase 02.
