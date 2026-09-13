# Banking Experience System (BES)

**A domain-specific design system for banking and fintech in the UAE** — foundations, tokens, components, patterns and cross-cutting architectures that encode financial behavior: money display, transaction states, disclosure, consent, fraud response, and bilingual Arabic/English RTL/LTR design.

Version 2.0.0-draft · August 2026 · Phase 02–03 deliverable (architecture + full component system)
Strategy phase: see `../01-system-strategy/`

---

## Structure

### Foundations
| Doc | Contents |
|---|---|
| [01 Color](01-foundations-color.md) | Primitive palette, semantic tokens, financial colors, dark scheme, contrast contract |
| [02 Typography](02-foundations-typography.md) | Latin+Arabic stacks, scale, Arabic metrics, financial amount styles, bidi text |
| [03 Spacing & Layout](03-foundations-spacing-layout.md) | Spacing scale, density modes, grid, breakpoints, elevation, shape, z-index |
| [04 Iconography](04-foundations-iconography.md) | Construction, financial glyph vocabulary, RTL mirroring policy |
| [05 Motion](05-foundations-motion.md) | Durations, easings, semantic motion patterns, reduced-motion rules |

### Architecture
| Doc | Contents |
|---|---|
| [06 Token Architecture](06-token-architecture.md) | Five tiers, naming grammar, six token dimensions, theming contract, delivery |
| [07 Financial Semantics](07-financial-semantics.md) | Money display system, FX rules, balance model, **transaction state machine**, risk/verification/consent vocabularies |

### Core components (~60)
| Doc | Components |
|---|---|
| [08 Actions](08-core-actions.md) | Button, Icon Button, Link, Menu, Button Group |
| [09 Inputs & Forms](09-core-inputs.md) | Text/Currency/Search inputs, Select, Combobox, Date pickers, Checkbox, Radio, Switch, PIN, Code Entry, Upload, form primitives + form doctrine |
| [10 Navigation](10-core-navigation.md) | App Bar, Bottom Nav, Side Nav, Tabs, Segmented Control, Breadcrumb, Pagination, Stepper, Language Switcher, Session Bar |
| [11 Containers](11-core-containers.md) | Card, List, Table, Accordion, Modal, Drawer, Bottom Sheet, Popover, Tooltip, Divider |
| [12 Feedback](12-core-feedback.md) | Alert, Banner, Toast, Status Badge, Progress, Skeleton, Spinner, Empty/Loading/Error states + the disruption model |

### Financial components (~50)
| Doc | Family |
|---|---|
| [13 Money](13-financial-money.md) | Amount, Amount Pair, Masked Balance, FX Rate, Rate Lock, Fee Line/Breakdown, Total Row, Delta, Limit Indicator |
| [14 Accounts](14-financial-accounts.md) | Account Card/Selector, Balance Display/Set, Details, IBAN Display, Status, Product Header, Spaces |
| [15 Transactions](15-financial-transactions.md) | Item, List, Table, Detail, Status, Timeline, Receipt, Search/Filters, Statements |
| [16 Payments & Transfers](16-financial-payments-transfers.md) | Payee, Beneficiary Manager, **Payee Verification**, Payment Summary, Method Selector, Transfer Review, Auth Prompt, Processing, Results, Scheduled, Request-to-Pay, QR, Split, Bills |
| [17 Cards](17-financial-cards.md) | Card Art, Overview, Controls, Freeze, Limits, PIN, Details Reveal, Replacement, Disputes, Carousel |
| [18 Lending & Financing](18-financial-lending.md) | **Key Facts Summary**, APR & Profit Rate displays, Structure Explainer, Calculator, Eligibility, Application, Offer, Schedule, Early Settlement, Overdue |
| [19 Investments](19-financial-investments.md) | Portfolio, Holdings, Allocation, Performance, Risk Indicator, Product Card, Order Ticket, Deposits, Disclosures |
| [20 Identity & Security](20-financial-identity-security.md) | National identity sign-in/handoff, Signing Ceremony, Document Capture, Liveness, Verified Fields, Auth Prompt set, Devices, **Session Pause**, Security Events, Warning Tiers |
| [21 Consent & Privacy](21-financial-consent-privacy.md) | Consent Request/Dashboard/Cards, TPP Identity, Revocation, Connected Institutions, Payment Initiation Consent, Privacy Center, Marketing Preferences |

### Patterns (~55)
| Doc | Patterns |
|---|---|
| [22 Asking Users For…](22-patterns-input.md) | P-01…P-14: amounts, payees (domestic/international), documents, addresses, card details, consent, credentials |
| [23 Review & Confirmation](23-patterns-confirmation.md) | P-20…P-33: check answers, payment confirmation, payee verification, step-up auth, signing, cooling-off, fee explanation, Islamic products, **approval workflow (maker–checker)** |
| [24 Status & Disclosure](24-patterns-status-disclosure.md) | P-40…P-52: transaction status, tracking, balances, rates, documents, holds, insights, budgets, degraded data |
| [25 Fraud, Errors & Recovery](25-patterns-safety.md) | P-60…P-75: suspicious activity, scam intervention, account takeover response, complaints & ombudsman escalation, session expiry, offline, restrictions, bereavement, account closure |

### Cross-cutting systems
| Doc | Contents |
|---|---|
| [26 Data Visualization](26-data-visualization.md) | 15 chart components, selection rules, categorical palette, accessibility, RTL behavior |
| [27 Content, Notifications & Errors](27-content-notifications-errors.md) | Voice, bilingual glossary, message frameworks, **error taxonomy**, notification categories & urgency |
| [28 Accessibility Architecture](28-accessibility-architecture.md) | WCAG 2.2 AA enforcement mechanisms, keyboard/reader/zoom rules, accessible auth, PDF a11y, testing matrix |
| [29 Localization & RTL](29-localization-rtl.md) | Direction architecture, numerals/dates/calendars, bidi rules, per-area direction table, extension path |
| [30 Multi-brand & Theming](30-multibrand-theming.md) | Core/brand split, theme anatomy, guard rails, brand scenarios, governance, quality bar |

---

## The system's non-negotiables

1. **Money is never a plain string** — the Amount component and financial type styles everywhere.
2. **Fees appear before review** — transparency is structural, not editorial.
3. **UNKNOWN is a designed state** — no false failures, ever; money-state is always stated.
4. **Color never carries meaning alone** — sign + icon + label always.
5. **Arabic is designed, not translated** — direction is a token dimension; every component documents RTL.
6. **Safety is one tap; risk requires proof** — freeze/revoke instant; loosening needs step-up.
7. **Consent is purpose-bound, time-bound, revocable in ≤2 taps.**
8. **Disclosure structure is brand-invariant** — themes skin it; nothing hides or reorders it.
9. **Accessibility is a build gate** — contrast in tokens, checklists per platform including PDF.
10. **Every error answers four questions** — what, why, what happened to the money, what next.

## Realistic data convention

All examples use realistic UAE scenarios (AED amounts, IBAN format AE.., Arabic/English pairs) and never represent actual customer data.

## Next phases

Phase 04: flagship journey blueprints (dashboard, transfer, remittance, cards, financing, consent, fraud response, SME approval) assembled from these patterns. Phase 05: full documentation site + design library builds + coded token package.
