# Enterprise Scrutiny Report — Banking Experience System v1.0.1

**Date:** 31 August 2026 · **Method:** three independent adversarial reviews (front-end code quality · WAI-ARIA/keyboard accessibility · architecture & spec-code consistency) plus four automated audits, followed by a fix cycle and re-verification of every gate.

**Findings:** 88 total — 4 CRITICAL · 26 HIGH · 42 MEDIUM · 26 LOW (overlapping counts merged).
**Disposition:** every CRITICAL and every code-level HIGH fixed in v1.0.1; spec-claim HIGHs resolved by implementation or by explicit honest-tense relabeling; remaining items are logged below as residual risks with owners.

---

## 1. What the scrutiny caught (the headline defects — all fixed)

| # | Defect | Why it mattered | Fix |
|---|---|---|---|
| C1 | **Stored XSS** — payee name flowed unescaped into `innerHTML` across five journey screens | A reference implementation teaching banks an injection pattern | `BES.esc()` on every user-derived value; `BES.tpl()` immune to `$`-pattern semantics; chart labels escaped; regression test |
| C2 | **Sign-destroying money parse** — `parseAmount(formatAmount(-500)) === +500` (true-minus U+2212 stripped); debits sorted as credits | Money-corrupting invariant violation in a "trust by design" system | Parser handles U+2212, `(500)`, Arabic ٫/٬ separators, Extended Arabic digits; sorting reuses it; **round-trip is a tested invariant (37 unit tests)** |
| C3 | **Silent-to-AT components** — combobox choices, PIN failures, rate expiry, step changes produced zero screen-reader output | Blind users selecting money destinations blind; lockout without hearing errors | APG-complete combobox/date picker/sort; `BES.announce` live regions; PIN `setError` API; per-step focus + announcements in the journey |
| C4 | **Library-wide print hijack** — one `@media print` rule blanked printing for every consuming product | One line of CSS breaking every adopter | Scoped to `body.bes-print-receipt` |
| H | Arabic decimal `٥٫٥` parsed as `55` (10× error) | The bilingual system corrupting Arabic-locale amounts | Separator normalization + tests |
| H | Rate lock was decoration — expired silently off-screen, infinitely renewable, "re-quote" didn't change the rate | Fee-honesty theater | Lock is enforced state: blocks auth, survives navigation, re-quote mutates the rate |
| H | Listener/timer leaks (modal scrims, comboboxes, countdowns), double-binding on re-init | Degradation under real SPA usage | Shared trap engine, bind guards, `stopCountdowns`, capped toasts |
| H | Spec↔code drift — "five tiers shipped", phantom `data-scheme`, unimplemented "stable API" namespaces, STATUS overstatements | The governance layer itself was unverified prose | Implemented (`transaction/verification/consent` tokens, density wiring, 4th CoP state, var()-chain theming) or relabeled *reserved/planned*; STATUS corrected |
| H | **No CI, no tests** despite "non-negotiable gates" | Convention already failed on release one (version drift) | `.github/workflows/ci.yml` runs builds, drift check, 3 audits, syntax, 37 tests, size budget on every PR |

## 2. Per-dimension verdicts

| Dimension | Verdict | Basis |
|---|---|---|
| **Money correctness** | ✅ Strong | Round-trip invariant tested; minor-unit rounding; ISO precision map; Arabic numeral/separator coverage; sorted-by-value correctness |
| **Security (code)** | ✅ Strong for a reference implementation | XSS class eliminated with tested escaping; focus-managed critical interrupt; CSP/hosting guidance shipped. *Not a substitute for a product security review of any real deployment* |
| **Accessibility (machine-checkable)** | ✅ Strong | 60/60 contrast (both schemes), 0 static errors across 50 files, APG-correct composite widgets, live-region discipline, WCAG 2.2 §3.3.8 honored on auth entry |
| **Accessibility (human-verified)** | ⏳ Gated | Screen-reader, Arabic native review and usability protocols are written and executable — but unrun. Components stay below **Stable** until they pass (GOVERNANCE) |
| **Scalability** | 🟡 Adequate, with known ceilings | Token pipeline validated + theming cascade real; versioned assets; CI. Ceilings logged below: monolithic bes.css, per-surface i18n dictionaries, no npm artifact |
| **Consistency / drift control** | ✅ Strong | Consistency audit + generated-file drift check in CI; honest-tense docs; STATUS spot-check corrections applied |
| **Governance** | ✅ Operating | Gates enforced by CI, not convention; semver + changelog current (1.0.1 everywhere); templates live. LICENSE remains a deliberate owner decision |
| **Compliance** | ⏳ Review-ready | 22-row traceability matrix awaiting counsel; UNREVIEWED by design until signed |

## 3. Residual risks & deferred items (the honest list)

**Human-gated (cannot be closed by code):**
1. Screen-reader pass, Arabic native-speaker review, 5-session usability test — protocols in `docs/testing/`, awaiting people. Until then, no component may claim Trial/Stable.
2. Compliance counsel sign-off — matrix in `docs/compliance/`, all rows UNREVIEWED.
3. License decision (`LICENSE.md` placeholder) — blocks public reuse, owner's call.

**Engineering roadmap (logged, not blocking the reference-implementation claim):**
4. i18n extraction: journey/showcase dictionaries + library `data-*` string overrides → shared `assets/i18n/*.json` catalogs with plural rules (prerequisite for the Hindi/Urdu/Tagalog expansion claim in doc 29 §6).
5. `bes.css` monolith → per-component source files with a concat build, before the coded set grows past ~50 components.
6. Component-token tier emission + deprecation-alias mechanism (currently *reserved*, honestly labeled).
7. Typed-entry pairing for the date picker (spec requires it; calendar is now fully keyboard-operable, but the paired text input remains a consumer obligation documented in the spec).
8. `Intl.NumberFormat`-based localized display (Eastern-numeral *display* preference; current implementation normalizes input and renders Western digits per doc 29 default).
9. High-contrast dimension emission; terminology-resolver reference implementation.
10. npm/tagged-bundle distribution with checksums; theme-file input mode for the contrast audit (theming cascade is real; automated *theme* validation is manual today).

## 4. Re-verification (all gates, post-fix)

```
tokens build ........... validated OK (fails on unresolved refs / missing modes)
contrast audit ......... 60/60 pass, light + dark
static a11y audit ...... 0 errors, 0 warnings, 50 files
consistency audit ...... 0 errors
JS syntax .............. bes.js + gallery.js OK
unit tests ............. 37/37 (round-trip, Arabic separators, XSS escaping)
link check ............. all internal links resolve (50 files)
layout check ........... 49/49 pages share the identical shell
CI ..................... all of the above on every push/PR
```

## 5. The honest claim after scrutiny

BES v1.0.1 is a **rigorously self-verified reference implementation and specification** for UAE banking experiences: machine-checkable qualities are enforced by construction and by CI; every claim in the docs is either implemented or explicitly labeled reserved/planned; and the path from here to production-grade is written down as executable protocols and a numbered roadmap — not aspiration. "No flaws" is not a claim any honest system makes; **no known unfixed code-level flaws, and no unlabeled gaps** is the claim this report supports.
