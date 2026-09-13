# 28 — Accessibility Architecture

**Banking Experience System (BES)** · v2.0.0-draft

Accessibility is financial inclusion, engineered into tokens and components — not audited at the end. Floor: **WCAG 2.2 AA** across web, native mobile, and PDF outputs, in **both languages and both directions**.

---

## 1. How accessibility is enforced structurally

| Mechanism | What it guarantees |
|---|---|
| Contrast in token contracts (doc 01 §6) | No theme can ship failing text/icon/focus contrast; validated at build |
| Component-encoded semantics | Roles, states, names, focus order ship inside components — products can't forget them |
| Per-platform checklists | Every component carries Web / Mobile / **PDF** requirement checklists; "accessibility-tested" is a release gate, not a claim |
| Content rules | Message frames produce specific, actionable errors; reading-level targets; no color-only meaning (paired icon+label mandated by the status system) |
| Bidi test fixtures | Mixed AR/EN strings (amounts, IBANs, names) are standing test cases per component |
| Reduced-motion alternatives | Defined per motion pattern (doc 05), tested state |

## 2. Keyboard & focus

Full keyboard operability for every interactive component (documented per component: keys, order, escape routes); visible focus ≥3:1 contrast, 2px + offset, never suppressed; focus management owned by patterns (error summary focus, dialog traps + return, drawer/sheet handling); no keyboard traps; skip-links on web; roving tabindex where composite widgets need it (tables, menus, tab lists).

## 3. Screen readers

- Names describe the financial object fully ("Current account ending 4521, 25,000 dirhams available").
- Amounts announced as spoken currency (doc 13), not digit strings; IBANs in groups.
- Live regions: polite for status/progress; assertive only for security interruptions and payee-verification results.
- Arabic surfaces carry correct `lang` so voices switch; mixed-language rows isolate runs for pronunciation.
- Charts expose summary + table (doc 26 §3); decorative imagery hidden.

## 4. Touch, pointer, zoom

Targets ≥44×44 (56 kiosk) with ≥8px spacing between destructive/affirmative pairs; density modes never shrink touch targets on touch surfaces; drag/swipe always has a tap alternative; text scaling to 200% without loss (tested in AR+EN — Arabic's larger metrics stress-test first); page reflow at 320px width without horizontal scroll; pinch-zoom never disabled.

## 5. Accessible authentication (WCAG 2.2 conscious)

No cognitive-function-only tests (no memorized transcription; code entry supports paste/autofill); biometric always paired with non-biometric fallback; liveness offers accessible alternatives + human path (doc 20); re-auth timeouts generous and extendable; no SMS-dependency (deprecated anyway) — fallbacks work for users without a second device via identity re-verification.

## 6. Cognitive accessibility & vulnerable users

Plain language (target ~grade 8 reading level EN; equivalent clarity AR); one primary question per screen in flows; progress visibility; no countdown pressure on decisions (rate-lock timers pair with re-quote safety, doc 13); **simplified mode** (institution-optional): larger type preset + comfortable density + reduced feature surface for elderly/low-digital-literacy users — same components, token-level switch; consistent placement (actions, navigation never move between screens of a flow); error tolerance (drafts, undo where reversible, review-before-commit everywhere).

## 7. PDF & document accessibility

Statements, receipts, KFS, contracts: tagged PDFs, logical reading order, real text (never image-of-text), document language set (AR/EN), tables tagged, headings navigable — the PDF checklist is part of the component definition for every document-producing component (docs 15, 18, 21).

## 8. Assistive-context specifics for finance

- Masked balances: reveal state announced; masked value never leaked to accessibility tree.
- Security surfaces (PIN, card reveal) block screen capture but **never** block screen readers.
- Fraud interruptions: assertive announcement, focus moved, simple binary actions, no timeout on the decision.
- Approval flows (SME): the checker's screen reader gets the same complete payment facts as the visual layer (no summary-only shortcuts).

## 9. Testing matrix (release gate)

Per component: keyboard-only pass · screen reader pass (one desktop + one mobile reader) · 200% text scale AR+EN · high-contrast dimension · reduced-motion · RTL visual review · bidi fixtures. Flagship journeys additionally: cognitive walkthrough with the vulnerable-user variant (doc Phase 01/03 personas) and document-output (PDF) audit.
