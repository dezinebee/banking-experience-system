# 03 — Target Users

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

Two audiences: **end customers** of products built with the system, and **internal users** who build with it. Segment data from live research (Aug 2026); sources in doc 04/06.

---

## 1. The UAE population shape (why segmentation is extreme)

- ~10M residents; expatriates ≈ **88–89%** of population. Emiratis ~11.6%; South Asians ~60% (Indians ~38%); Egyptians ~10%; Filipinos ~6%.
- Blue-collar workers ≈ half the population; ~32% of the working population historically unbanked (~1.7M), gated out by minimum-salary thresholds.
- Smartphone penetration ~99%; >85% mobile banking penetration; 72% treat the app as their primary channel; ~half hold an account with a digital bank.
- World's #2–3 remittance sender (~$43B/yr): India ~28%, Pakistan ~13%, Philippines, Bangladesh, Egypt, Nepal, Sri Lanka.

Design consequence: the system must serve **one of the widest capability/language/wealth ranges of any banking market** — private-banking clients and first-time smartphone banking users are on the same rails.

## 2. End-customer segments

### R1 — Emirati nationals
Arabic-first (interface often Arabic, documents bilingual). High government-digital fluency (UAE PASS, government apps set expectations). Islamic products significant. Extended-family financial patterns; government-linked salary anchoring.
**System demands:** Arabic-first quality parity, Islamic terminology layer, UAE PASS-centric auth, familiarity with UAE Design System 2.0 conventions.

### R2 — Professional expatriates (Western, Arab, Asian)
English-dominant, high expectations set by home-market fintechs (Revolut, Monzo, Wise, Paytm, GCash). Transient: arrive, open account in minutes, leave in 2–8 years. Multi-currency needs, international investing, remittance to home country.
**System demands:** onboarding speed (UAE PASS 5-minute bar set by Wio/Hayyak/ruya), multi-currency Money display, transparent FX (mid-market comparison is unmet market need), account-closure journeys that work (notorious FAB failure), remittance corridor UX.

### R3 — Blue-collar / low-income workers
Hindi/Urdu/Tagalog/Malayalam/Bengali speakers beyond Arabic/English; variable literacy and digital literacy; WPS salary cards; exchange-house habits (cash, counters, trust in physical presence). Remittance is the primary financial job. Extremely low fault tolerance — an eKYC loop failure (Mbank pattern) leaves them with no fallback.
**System demands:** low-literacy patterns (icon+number redundancy, voice-friendly flows, simple mode), vernacular-extensible content architecture, cash-adjacent hybrid patterns, reliability as an inclusion issue, fee clarity in absolute AED (not percentages).

### R4 — Affluent / private banking
Hybrid behavior: ~70% prefer digital for routine tasks but want human advisory for high-value decisions. Data density tolerance high; portfolio, FX and wealth visualization needs.
**System demands:** compact density mode, financial data-viz system, human-escalation patterns embedded in digital journeys, document (PDF) accessibility for statements/agreements.

### R5 — SME owners and finance staff
Long underserved by incumbents; Wio Business set the bar (fast setup, virtual cards, VAT/rent earmarking spaces, invoicing). Mixed personal/business behavior; corporate tax + VAT deadlines drive calendar-based needs.
**System demands:** role/permission patterns, payroll (WPS) flows, invoice/receivables components, approval chains, business KYC (trade license, UBO) document journeys.

### R6 — Corporate treasury and finance teams
Multi-user, role-based access, maker-checker approval workflows, bulk payments, audit trails, delegation. Information density closer to enterprise software than consumer banking.
**System demands:** enterprise approval pattern (create → require approval → approve/reject with audit), data tables at compact density, bulk-operation states, exception queues.

### Cross-cutting: vulnerable and situational users
Elderly customers, People of Determination (explicit national policy focus), newly bereaved (inheritance/account transition), fraud victims mid-incident, users under coercion (scam-coaching — CBUAE mandates active-call session suspension). Each flagship journey names its vulnerable-user variant.

## 3. Internal users (who builds with the system)

| User | Needs from the system |
|---|---|
| Product designer | Figma library with variants/modes matching token dimensions (direction, density, brand, dark); journey blueprints; realistic AED sample data |
| Engineer | Token package (CSS custom properties contract), coded components, financial utilities (IBAN validation, amount formatting), state-machine references |
| Content designer | Bilingual terminology glossary, message frameworks, error-copy dictionary, Islamic/conventional vocabulary switch |
| Compliance/risk | Pattern-to-regulation traceability map (which pattern satisfies which CPR/Notice article), disclosure component inventory |
| Brand/marketing | Theme contract: what they may change (tokens, imagery, illustration, voice inflection) and what they may not (behavior, disclosure, a11y) |
| QA / accessibility | Per-platform checklists (Web/Mobile/PDF), bidi test fixtures, state matrices per component |

## 4. Priority persona set (for journey design in Phase 04)

1. **Amina** — 29, Emirati government employee, Abu Dhabi. Arabic-first interface. Salary account + Islamic auto financing + savings goal. Uses UAE PASS for everything.
2. **Rajesh** — 41, Indian project manager, Dubai, 11 years in UAE. Sends AED 8,000/month to Kochi. Tracks INR rate; uses rate alerts. Two banks + one exchange app.
3. **Maricel** — 34, Filipina retail supervisor, Sharjah. WPS salary card → wants full account. Sends to GCash weekly. English + Tagalog; moderate digital literacy; high fee sensitivity.
4. **Khalid** — 52, Emirati business owner (trading company, 30 staff). SME account, payroll, VAT payments, approves payments his accountant creates. Conventional + Islamic product mix.
5. **Sarah** — 38, British marketing director, Dubai. Multi-currency, invests globally, expects Monzo-grade UX, will leave UAE in ~3 years and needs clean account closure.
6. **Fatima** — 67, Emirati retiree. Larger type, Arabic, phone-first support expectations, fraud-target risk profile.

Each persona exercises different system stress points: Amina (Arabic parity + Islamic), Rajesh (remittance + FX), Maricel (inclusion + vernacular), Khalid (SME approvals), Sarah (multi-currency + lifecycle), Fatima (accessibility + fraud protection).

## 5. Jobs-to-be-done register (top-level)

Money in (salary, incoming transfer) · Money out (P2P Aani, bills, cards, remittance) · Money safe (fraud response, card controls, limits) · Money growing (savings, deposits, investments) · Money borrowed (personal financing, cards, mortgage, BNPL context) · Money shared (family, SME roles, corporate approvals) · Money proven (statements, certificates, tax) · Identity & consent (KYC, UAE PASS, Open Finance permissions) · Lifecycle (open, upgrade, complain → Sanadak, close).

These ten jobs are the parent categories for the journey taxonomy (doc 08).
