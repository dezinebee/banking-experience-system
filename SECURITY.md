# Security Policy

BES ships a browser-side design system: `assets/tokens.css`, `assets/bes.css`, `assets/bes.js`, plus documentation and demo pages. It has no server, no network calls, no persistence, and no runtime dependencies. That shapes what counts as a vulnerability here — see **Scope** below.

## Supported versions

| Version | Supported |
|---|---|
| 2.0.x | ✅ Security fixes |
| 1.x | ❌ Superseded by 2.0.0 — see `docs/migrations/v1-to-v2.md` |

Security fixes ship as PATCH releases per GOVERNANCE.md, out of band if severity warrants it.

## Reporting a vulnerability

**Do not open a public issue for a security report.**

Use GitHub's private vulnerability reporting: repository → **Security** tab → **Report a vulnerability**. This opens a private advisory visible only to you and the maintainers.

> Maintainers: enable this at Settings → Code security → Private vulnerability reporting. Until it is on, the tab will not offer the option.

Please include: affected file and version, reproduction steps or a minimal page, the impact you believe it has, and whether it is already public.

**Response targets:** acknowledgement within 5 working days; an assessment with severity and a fix plan within 15 working days. You will be credited in the advisory and CHANGELOG unless you ask otherwise. Please allow a fix to ship before public disclosure.

## Scope

**In scope**

- XSS or markup injection through any BES component API — anything a component writes into the DOM from caller-supplied data (labels, payee names, amounts, error strings, toast content, combobox options, table cells)
- Incorrect output from the Money type that could mislead a user about a financial value: rounding, allocation, minor-unit handling, safe-integer boundaries, `Intl` rendering, Eastern Arabic numeral round-tripping
- Balance masking failing to mask, or masked values recoverable from the DOM
- A transaction state rendering a control it must not offer — most importantly a retry affordance on any state that is not a confirmed failure (doc 07). `UNKNOWN` offering retry is a security issue, not a UI bug: it can drive duplicate payments
- Focus-trap escapes in the modal, or authentication-adjacent surfaces (PIN entry, auth prompt, signing ceremony) leaking input through paste handling, autofill, or the accessibility tree
- Prototype pollution or unsafe dynamic evaluation anywhere in `bes.js`
- A build or audit script that executes untrusted input from a token file or document

**Out of scope**

- Vulnerabilities in an application that *consumes* BES — report those to that project
- Missing CSP, SRI, or frame protections on your own deployment. BES documents the recommended headers in README → *Hosting security notes*; applying them is the host's responsibility
- The demo pages (`showcase.html`, `brand-proof.html`, `journey-remittance.html`, `components/`, `pages/`) treated as a real banking endpoint. They are fictional-data illustrations and are not built to be exposed as a product surface
- Findings that require an attacker to already control the page embedding BES
- Accessibility or contrast failures — real defects and very welcome, but file them as bugs against the audit gates, not as security reports
- Automated scanner output with no demonstrated impact

## A note on the regulatory content

Compliance and regulatory material in this repository is UX translation, not legal advice. A claim that a pattern misstates a CBUAE requirement is a correctness issue — open a normal issue and flag it for the traceability matrix (`docs/compliance/traceability-matrix.md`), which is reviewed separately.

## Data in this repository

All examples use fictional AED scenarios. If you believe any file contains real customer data, credentials, or keys, report it privately through the channel above rather than opening an issue.
