# 02 — Design Principles

**Banking Experience System** · Phase 01 · v2.0.0-draft · August 2026

Ten principles, each with a decision test and the system mechanism that enforces it. Principles that cannot be enforced by the system itself (tokens, components, content rules, review checklists) are aspirations, not principles — so every principle names its enforcement.

---

## 01 — Clarity over cleverness

Financial information should be immediately understandable. Amounts, states and consequences are stated in plain language, in the user's language.

- **Test:** Can a first-time user, in Arabic or English, state what will happen after tapping the primary action?
- **Enforced by:** Content design system (doc 08 §6); verb-labeled confirmation buttons ("Send AED 5,000", not "Confirm"); readability standards; Shari'ah concept explainers on Islamic products.

## 02 — Transparency before conversion

Never optimize conversion at the expense of financial clarity. All fees, FX markups and totals appear before the review step — never revealed at the final screen. This is also a regulatory posture: CBUAE Consumer Protection Standards require all-fees-inclusive APR and prominent disclosure.

- **Test:** Could the user reconstruct the total cost of the product/transaction from screens seen *before* the confirm step?
- **Enforced by:** Fee-disclosure pattern is a required slot in the money-movement framework; KFS component; FX pattern distinguishes estimated vs guaranteed rate, fee vs markup.

## 03 — Prevent mistakes before explaining them

Good banking UX prevents errors rather than displaying error messages. Adopted from GOV.UK doctrine: accept all reasonable input formats, strip stray characters (spaces in IBANs, hyphens in phone numbers), preserve input on error, validate eligibility by routing — never by field validation.

- **Test:** For each error message in a flow, could the design have made the error impossible or irrelevant instead?
- **Enforced by:** Input components with format-forgiveness built in; Confirmation of Payee pattern (mandated by CBUAE Notice 2025/3057); check-answers pattern before submission; error summary + focus management as stock behavior.

## 04 — Money deserves hierarchy

Amounts, fees, balances and consequences get clear visual priority. The Money component family (tabular numerals, consistent decimal/sign/currency placement, size scale) is the most-used primitive in the system and is never approximated with a plain text style.

- **Test:** Is the most consequential number on the screen the most visually prominent, and is its status (estimated/final/pending) explicit?
- **Enforced by:** `financial.amount` type styles; Money component required wherever currency renders; lint rule against raw currency strings.

## 05 — Security should build confidence

Security UX reassures while communicating genuine risk. Calm, specific, actionable — never vague dread. Fraud interruptions explain what was noticed and give a safe next step; scam warnings are tiered (info → caution → hard stop) so the critical tier retains force.

- **Test:** After a security interruption, does the user know (a) what happened, (b) whether their money is safe, (c) exactly what to do next?
- **Enforced by:** Fraud pattern library with defined severity, messaging, CTA, escalation and recovery per scenario; content rules banning alarmist copy; "we will never ask for your password" verified-channel messaging.

## 06 — Accessibility is financial inclusion

Not an add-on. In the UAE this is literal inclusion: People of Determination policy, elderly users, ~1.7M under-banked blue-collar workers, and low-digital-literacy users. WCAG 2.2 AA is the floor; contrast ratios live inside token definitions; Arabic screen-reader behavior and bidi text (amounts, IBANs inside Arabic sentences) are first-class test cases.

- **Test:** Does the component pass its Web/Mobile/PDF accessibility checklist in *both* directions, and does the flow survive 200% text scaling?
- **Enforced by:** Per-platform requirement checklists (VGAR model); tokens carrying contrast contracts (Carbon model); accessible-authentication patterns (biometric/passkey with non-SMS fallbacks); reduced-motion alternatives mandatory.

## 07 — Localization is architecture

Arabic and RTL are designed from the beginning, not translated at the end. Direction is a token dimension; layouts use logical properties (start/end, never left/right); Arabic gets its own type metrics (+1–2px optical size, taller line-height, no letter-spacing, no caps-based emphasis); Eastern vs Western Arabic numerals is a declared policy, never mixed; every component documents its own RTL behavior (Spectrum model).

- **Test:** Was the Arabic layout reviewed as a design, not a translation? Do mixed-direction strings (Latin IBAN in Arabic sentence) render correctly?
- **Enforced by:** RTL section required in every component doc; bilingual terminology glossary; bidi test fixtures in the component library.

## 08 — Components encode behavior

A component is not a visual object; it carries interaction, states, accessibility, content rules and financial semantics. A Currency Input knows about precision and locale; a Transaction Item knows the full state vocabulary; a Consent Card knows expiry and revocation.

- **Test:** If the component were re-skinned beyond recognition, would its financial behavior survive intact?
- **Enforced by:** Core-vs-brand separation (doc 07 §5); behavior lives in core and cannot be overridden by themes; component tokens never leak outside their component.

## 09 — Design for uncertainty

Financial systems have pending, delayed, and unknown states. The UNKNOWN state is a designed state: never tell a user a transaction failed when the system doesn't know. "We're checking your transfer status" with a defined resolution path is stock behavior, not an edge case. Instant rails (Aani) make success feel instant — which makes honest handling of the exceptions matter more, not less.

- **Test:** For every async operation: what does the user see at 2 seconds, 30 seconds, 5 minutes, and next session? Is money-state ("no money has left your account" / "your money is safe, we're confirming") always stated?
- **Enforced by:** Transaction state machine (doc 07 §4) with mandatory UI/content per state; error taxonomy including UNKNOWN_TRANSACTION_STATE; payment-under-review patterns with tipping-off-safe copy.

## 10 — Consistency without rigidity

Banks express identity without breaking usability. Theming is guard-railed presets (Visa model): pretested color themes, shape scale, density modes, type stacks — not free overrides. A conventional brand, an Islamic brand and a youth brand share every behavior.

- **Test:** Can the brand change be described entirely in token values and content-vocabulary choices, with zero component forks?
- **Enforced by:** Layered token model (primitive → semantic → component); theme contract with contrast validation; terminology layer for conventional/Islamic vocabulary switching.

---

## Using the principles

- In critique: name the principle a design upholds or violates; the decision tests are the critique questions.
- In prioritization: principles 02, 03, 06, 07 and 09 are non-negotiable (regulatory or inclusion grounding); 01, 04, 05, 08, 10 are quality bars where trade-offs are argued explicitly.
- In contribution review: a new component/pattern PR must state how it satisfies principles 06, 07 and 08 before review begins.
