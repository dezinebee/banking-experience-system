# Contributing to BES

Contributions welcome — components, patterns, content, Arabic corrections, audit findings. The bar is the system's own: behavior encoded, bilingual by design, accessibility structural.

## Before proposing

1. Check `STATUS.md` — it may already exist or be in flight.
2. Read the relevant spec in `docs/system/` and the [design principles](docs/strategy/02-design-principles.md). Proposals are evaluated against principles **06 (accessibility), 07 (localization), 08 (components encode behavior)** as a minimum bar.
3. One concept per proposal.

## Proposal flow

1. Open an issue with the **component/pattern proposal template**. It requires: the problem, why existing parts can't compose it, principle-compliance notes, and the financial states it must handle.
2. On acceptance (label `accepted`), spec first: a PR to `docs/system/` using the documentation template (doc 08 §7 of the taxonomy) — **the RTL section and per-platform a11y notes are not optional**.
3. Then code: `bes.css`/`bes.js` + a gallery demo + (if doc-relevant) a `tools/demos.py` entry.

## PR checklist (enforced by the PR template)

- [ ] Spec section exists/updated with RTL + accessibility + content guidance
- [ ] Tokens only — no raw color/size values; component tokens don't leak across components
- [ ] Logical properties only (no `left`/`right` in layout)
- [ ] Both schemes verified (light/dark screenshots)
- [ ] **Both directions verified (LTR/RTL screenshots)** — bidi fixtures for anything rendering amounts/identifiers
- [ ] `python3 tools/audit-contrast.py` and `python3 tools/audit-a11y.py` pass
- [ ] `python3 tools/build-docs.py` re-run if docs/demos changed
- [ ] CHANGELOG entry under Unreleased
- [ ] STATUS.md row added/updated
- [ ] Realistic AED example data; no real customer data; no reference-system names

## Content & Arabic contributions

Terminology fixes change the **glossary** (`docs/system/27-content-notifications-errors.md`) first, then propagate — never a one-screen fix. Arabic strings require a native-speaker reviewer on the PR.

## Verification contributions

Running a protocol from `docs/testing/` and filing results is a first-class contribution. File failures with the bug template, tag `verification`.

## Ground rules

Regulatory content is UX translation, not legal advice — flag anything compliance-adjacent for the traceability matrix. Be respectful; assume good faith; the maintainer call is final per GOVERNANCE.md.
