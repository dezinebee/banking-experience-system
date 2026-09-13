# 08 — System Taxonomy

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

The shared vocabulary: what things are called, which layer they belong to, how they're categorized, and what documentation each kind requires. Phase 02 expands each taxonomy into full inventories; Phase 03 prioritizes them.

---

## 1. Artifact types (the nouns of the system)

| Type | Definition | Example | Lives in layer |
|---|---|---|---|
| **Token** | Named design decision, themeable value | `action.primary`, `financial.expense` | Tokens |
| **Foundation** | Non-token rule set | Arabic type metrics, icon mirroring rules | Foundations |
| **Component** | Reusable UI object encoding behavior + states | Currency Input, Transaction Item | Core / Financial |
| **Utility** | Non-visual logic primitive | IBAN validator, amount formatter | Core / Financial |
| **Pattern** | Named solution to a recurring task, composed of components | Confirmation of Payee, Check Answers | Patterns |
| **Journey** | End-to-end flow blueprint composed of patterns | International remittance | Journeys |
| **Experience** | Product-level assembly | Retail app, SME portal | Product |
| **Content standard** | Terminology, message frameworks, error dictionary | "Transfer completed" vocabulary | Cross-cutting |

## 2. Component taxonomy

### Core components (target ~50–70)
Categories: **Actions** (button, icon button, link, menu) · **Inputs** (text, currency, search, select, combobox, date/date-range, checkbox, radio, switch, upload, character count) · **Navigation** (nav bar, tabs, segmented control, breadcrumb, pagination, stepper) · **Containers** (card, table, list, accordion, drawer, modal, bottom sheet, popover, tooltip) · **Feedback** (alert, banner, toast, badge, progress, skeleton, empty/loading/error states) · **Media & data** (avatar, icon, chart primitives).

### Financial components (target ~30–50)
Categories: **Money** (amount display, currency input, masked balance, FX rate pair, fee line, total) · **Account** (account card, selector, balance set — current/available/pending/reserved, status) · **Transaction** (item, table, detail, status, timeline, receipt) · **Payment & transfer** (payee/beneficiary, source selector, CoP result, payment summary, method, result states) · **Card** (card art incl. Jaywan co-badge, controls, freeze, limits, PIN, dispute) · **Lending** (KFS, calculator, EMI/payment schedule, application progress, profit-rate display) · **Investment** (holding, portfolio, allocation, performance) · **Identity & consent** (UAE PASS button, document capture, verification status, consent card, consent dashboard entry, TPP badge) · **Security** (auth prompts, device list, warning tiers, session-pause screens).

Financial components carry extra states beyond core ones: pending · blocked · requires-verification · requires-consent · expired · reversed.

## 3. Pattern taxonomy (GOV.UK task-based model, target ~20–30)

- **Ask users for…** — amount · payee/IBAN · Emirates ID/documents · address (international) · purpose of payment · source of funds (EDD) · consent (data, marketing, Open Finance) · signature (UAE PASS)
- **Help users to…** — check answers before confirming · recover from errors · verify a payee (CoP) · understand fees ("why am I being charged?") · understand an Islamic product (Shari'ah explainer) · respond to suspected fraud · pause safely (scam interruption) · complain and escalate (→ Sanadak) · manage consents · re-verify identity (re-KYC) · close an account
- **Show users…** — transaction status (full state machine) · KFS/product summary · rate & fee breakdown (estimated vs guaranteed) · balance set · receipts/proof · changes to terms (60-day notice) · cooling-off rights · warnings (tiered)
- **System pages** — confirmation · service unavailable/maintenance · session expired · degraded data (partial third-party rails)

Every pattern that has a regulatory source carries its REG-ID (doc 05) in frontmatter.

## 4. Journey taxonomy

Parent jobs (doc 03 §5): money in · money out · money safe · money growing · money borrowed · money shared · money proven · identity & consent · lifecycle. Flagships (Phase 04): dashboard, transfer, remittance, cards, financing, Open Finance consent, fraud response, SME approval. Each journey is documented as: trigger → stages (money-movement slots where applicable) → patterns used → state coverage → vulnerable-user variant → bilingual notes → measurement.

## 5. Naming conventions

- **Tokens:** dot-namespaced roles, lowercase: `surface.primary`, `text.secondary`, `status.pending`, `financial.income`, `transaction.completed`, `consent.expired`. Prefix for code: `--bes-*` (working prefix until naming lands). Component tokens: `button.primary.background`. Never name by value (`blue.600` exists only at primitive tier).
- **Components:** singular nouns, plain English: Currency Input, Transaction Item, Consent Card. No brandable names for core parts.
- **Patterns:** verb-phrases matching taxonomy category ("Verify a payee", "Check answers").
- **States:** the fixed vocabulary of doc 07 §4 — new states require architecture review, not ad-hoc invention.
- **Bilingual naming:** every artifact has a canonical English name and a reviewed Arabic name; the Arabic name is a translation *decision*, recorded in the glossary, not an ad-hoc translation.

## 6. Content design system (structure)

- **Terminology glossary** — EN + AR columns, conventional + Islamic variants, preferred/avoid pairs ("Transfer completed" not "Transaction done"; "Your transfer is pending" not "Processing error").
- **Message framework** — every error answers: WHAT happened · WHY · WHAT happened to the money · WHAT to do next. Example: "We couldn't complete this transfer. Your bank declined the transaction. No money was deducted from your account. [Try again] [Contact support]".
- **Voice attributes** — calm, specific, respectful; no alarmism in security; no jargon leakage (no internal error codes).
- **Severity-matched tone** — informational/important/urgent/critical notification categories with distinct visual + verbal register; fraud/security messages visually and semantically distinct from marketing.

## 7. Documentation template (every component page)

Overview · Anatomy · Variants · States · Usage (when / when not) · Do & Don't · Accessibility (per-platform checklist refs) · Content (terminology + examples in AED, realistic, never implying real customer data) · Localization & **RTL** (required section) · Responsive behavior · **Financial considerations** · **Security considerations** · Code guidance · Figma guidance · Research & lifecycle status (Trial → Stable, GOV.UK model) · Regulatory references (REG-IDs) where applicable.

Component proposal format (from the brief §46): Purpose → Anatomy → Variants → States → Usage → Don't use when → Financial UX → Trust → Security → Accessibility → Arabic/RTL → Responsive → Content → Example (realistic AED).

## 8. Lifecycle & governance vocabulary

- **Statuses:** Proposed → Trial → Stable → Deprecated (with sunset date — e.g., SMS OTP components carry Deprecated + 31 Mar 2026 sunset from day one).
- **Change classes:** token-value change (theme-safe) · behavior change (major) · content change (glossary-versioned) · regulatory change (traceability-map update required).
- **Contribution:** proposals must state principle compliance (06, 07, 08 minimum), include both-direction designs, and name their pattern/journey consumers.

## 9. Prioritization formula (feeds Phase 03)

Score = **Frequency × Financial Risk × Reusability ÷ Complexity** (relative t-shirt scales). Predictably top of list: Money/amount display, Currency Input, Transaction Item + state system, review/check-answers pattern, CoP screen, KFS, consent card, auth prompts, error framework — these are the Phase 03 build-first candidates.
