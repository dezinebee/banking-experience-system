# Banking Experience System (BES)

[![BES gates](https://github.com/dezinebee/banking-experience-system/actions/workflows/ci.yml/badge.svg)](https://github.com/dezinebee/banking-experience-system/actions/workflows/ci.yml)
[![Licence: MIT](https://img.shields.io/badge/licence-MIT-blue.svg)](LICENSE.md)
[![Status: draft](https://img.shields.io/badge/status-draft%20%C2%B7%20not%20human--verified-orange.svg)](STATUS.md)

A domain-specific design system for banking and fintech in the UAE — bilingual Arabic/English (RTL/LTR), regulatory-aware, accessibility-first.

**Trust by design. Clarity by default.** BES specifies the financial experience layer most design systems skip: money display, transaction states (including *unknown*), fee disclosure, payee verification, consent, fraud response, and Islamic/conventional terminology — as reusable foundations, tokens, components and patterns.

> **v2.0.0-draft — not yet human-verified.** Every gate this repository passes is automated. No screen-reader, Arabic native-speaker or usability testing has been carried out, and all Arabic UI copy is machine-drafted. See [Status & license](#status--license) before shipping it.

## Install

The library is **three files, no dependencies, no build step**. Pick whichever route suits you.

**A · Download the release zip** — simplest, no tooling required.

[Latest release](../../releases/latest) → `bes-<version>.zip` (≈40 KB). Contains the three files, the worked brand theme, LICENCE and a short usage README.

**B · Install from git** — versioned and updatable, no registry account needed:

```bash
npm install github:dezinebee/banking-experience-system
```

npm delivers only the library — `assets/tokens.css`, `assets/bes.css`, `assets/bes.js`, plus README and LICENCE. About 180 KB in `node_modules/`; the docs, specs and tooling are not installed. Reference the files from your build, or copy them out:

```html
<link rel="stylesheet" href="node_modules/banking-experience-system/assets/tokens.css">
<link rel="stylesheet" href="node_modules/banking-experience-system/assets/bes.css">
<script src="node_modules/banking-experience-system/assets/bes.js"></script>
```

Pin a release with `#v2.0.0-draft` on the end of the install spec. The package is not on the npm registry — `private: true` is deliberate while the system is a draft.

**C · Clone the whole repository** — if you also want the specifications and the audits:

```bash
git clone https://github.com/dezinebee/banking-experience-system.git
```

Then copy these three files out of `assets/`:

```
assets/tokens.css    design tokens — the theming contract
assets/bes.css       component library
assets/bes.js        behaviours (classic script, sets window.BES)
```

```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="bes.css">
<script src="bes.js"></script>

<div class="bes">
  <button class="bes-btn bes-btn--primary">Send AED 5,000.00</button>
</div>
```

Components live inside an element with `class="bes"`. `bes.js` initialises on `DOMContentLoaded` — load it with a plain `<script src>`, not `type="module"`.

Dimensions are attributes on `<html>`: `data-theme="dark"` (omit to follow the OS), `data-density="comfortable|compact"`, `dir="rtl" lang="ar"`. Tokens are the contract — theme by overriding `--bes-*` values, never by editing component CSS. `assets/themes/sadu.css` is a complete worked brand: 111 token values, zero rules.

**What is *not* part of the library:** `assets/site.css`, `assets/gallery.css` and `assets/gallery.js` are documentation-site chrome. `docs/`, `pages/`, `tools/` and `components/` are the specification, the rendered site and the verification apparatus — read them, but you don't ship them.

## Browse

- **Documentation site:** **[dezinebee.github.io/banking-experience-system](https://dezinebee.github.io/banking-experience-system/)** — or open `index.html` locally
- **Live showcase:** `showcase.html` — the design language rendered, with a working English ⇄ العربية RTL toggle and dark mode
- **Brand proof:** `brand-proof.html` — core and a second brand side by side, same markup and same `bes.css`; the brand is 111 token values and zero rules
- **Remittance journey:** `journey-remittance.html` — proof-by-product: the complete AED→INR flow (amount → payee verification → review with rate lock → auth → all result states → receipt), fully bilingual
- **Component gallery:** `components/` — 7 pages of live coded components with theme/RTL/density controls

## Verification & governance

| What | Where |
|---|---|
| Automated audits — contrast (78 declared pairings + 3,136 derived element colourings across brands, runtime surfaces included) · static a11y 53 files · consistency (drift · theme-guard · zero font-size/radius literals · **C9 version agreement**) · **brand-theme contract (doc 30)** · **transaction-state contract (doc 06 §6)** — all passing | `docs/audits/` · re-run via `tools/audit-*.py` |
| Money/text unit tests (147 assertions: the Money type — exactness, all seven rounding modes, allocation sums, safe-integer ceiling, Intl rendering, Eastern-numeral round-trip — plus masking and currency-input error association) | `node tools/test-js.mjs` |
| Component DOM tests in jsdom (83 assertions: all 13 transaction states, the UNKNOWN no-retry rule, toast, combobox, date picker, modal trap, PIN paste, sorting, charts, tabs LTR+RTL) — also captures the runtime-only surfaces the contrast audit scores | `node tools/test-dom.mjs` |
| Everything again in a UTC+ timezone | `npm run test:tz` |
| All gates in the order CI runs them | `npm run gates` |
| CI gates on every push/PR | `.github/workflows/ci.yml` |
| Adversarial scrutiny report (findings + fixes + residual risks) | `docs/audits/scrutiny-report.md` |
| Human test protocols (screen reader, Arabic review, usability) | `docs/testing/` |
| Component lifecycle registry | `STATUS.md` |
| Versioning, releases, change classes | `GOVERNANCE.md` · `CHANGELOG.md` |
| Contribution flow + PR gates | `CONTRIBUTING.md` · `.github/` |
| Regulatory traceability (counsel-review-ready) | `docs/compliance/traceability-matrix.md` |

## What's inside

Four things live here, for different readers. Only the first is something you ship.

| | Path | For |
|---|---|---|
| **The library** | `assets/tokens.css` · `assets/bes.css` · `assets/bes.js` · `assets/themes/` | Consumers — 148 KB, dependency-free. This is the release zip. |
| **The specification** | `docs/system/` · `docs/strategy/` | Anyone deciding whether the system is sound, or extending it. Markdown is the source of truth. |
| **The rendered site** | `index.html` · `pages/` · `components/` · `showcase.html` · `journey-remittance.html` · `brand-proof.html` · `assets/site.css` · `assets/gallery.*` | Readers of the docs site. Generated from `docs/` — not shipped. |
| **Build & verification** | `tokens/` · `tools/` · `docs/audits/` | Maintainers and reviewers. How every claim is checked. |

Detail:

| Path | Contents |
|---|---|
| `index.html` | Documentation site home |
| `pages/` | 40 generated HTML pages (one per specification) |
| `components/` | **Live component library gallery** — coded components with demos, controls (theme/RTL/density) and copy-paste code |
| `showcase.html` | Interactive visual specimen |
| `tokens/tokens.json` | **Token source of truth** (machine-readable) |
| `tokens/build-tokens.py` | Token compiler → `assets/tokens.css` (emission shared with the brand compiler via `tokens/emit.py`) |
| `tokens/themes/` · `tokens/build-theme.py` | Brand token sources → `assets/themes/<id>.css` — values only, no rules |
| `assets/tokens.css` | Generated CSS custom properties (light/dark, density, Arabic metrics) |
| `assets/bes.css` | Component library styles (logical properties, token-driven — zero font-size/radius/colour literals) |
| `assets/bes.js` | `BES.Money` (exact minor-unit value type) + behaviors: masking, tabs, modal, toast (dependency-free — jsdom is test-time only) |
| `docs/system/` | 31 markdown specifications (foundations → tokens → components → patterns → cross-cutting systems) |
| `docs/strategy/` | Phase 01 strategy: vision, principles, users, UAE context, regulatory translation, taxonomy |
| `tools/css_model.py` | Minimal CSS/HTML cascade model — how the contrast audit knows what each element actually renders |
| `tools/test-dom.mjs` | Component behaviour tests in jsdom; also writes `docs/audits/dom-snapshots/` |
| `docs/audits/dom-snapshots/` | **Generated** — the runtime-only surfaces (toast, open combobox, date grid, chart tables) so static audits can score them |

## Running the repository locally

Only needed if you are changing BES, not if you are using it — the library itself has no build step.

**Prerequisites**

| | Version | Used for |
|---|---|---|
| **Node** | 20 (see `.nvmrc`) | the test suites and `node --check` |
| **Python** | 3 (developed on 3.10) | the token build, the docs build, and all five audits |

Python is not optional: `npm run build` and `npm run audit` shell out to `python3`. It ships with macOS and most Linux distributions; on Windows use WSL or install Python 3 and make sure `python3` resolves.

```bash
git clone https://github.com/dezinebee/banking-experience-system.git
cd banking-experience-system
npm ci                 # installs jsdom — the only dependency, and test-time only
npm run gates          # every CI gate, in the order CI runs them
```

`npm run gates` should finish clean: 147 unit assertions, 83 DOM assertions run twice (once under `TZ=Asia/Dubai`), five audits, a generated-file drift check and the size budget. If it doesn't, that's a bug — please open an issue.

Then open `index.html` in a browser. The site is static, so no server is required; the pages under `pages/` are generated, so edit the markdown in `docs/` and re-run `npm run build` rather than editing HTML by hand.

## Cutting a release

```bash
npm run gates          # every CI gate, in the order CI runs them
npm run pack:release   # writes dist/bes-<version>.zip — the three library files,
                       # the themes, LICENSE and a consumer README
```

Tag `v<version>`, create the GitHub Release with the CHANGELOG entry as notes, and attach the zip. `dist/` is gitignored: the zip is a release artefact, not a committed file. The version comes from `tokens/tokens.json` `$meta.version` — consistency audit **C9** fails the build if `package.json`, any doc subtitle, any generated footer or any library file header disagrees with it.

## The system at a glance

- **110+ components** — ~60 core, ~50 financial (money, accounts, transactions, payments/transfers, cards, lending/financing, investments, identity/security, consent/privacy)
- **55 patterns** (P-01…P-75) — asking users for…, review & confirmation, status & disclosure, fraud/errors/recovery
- **Token architecture** — primitive + semantic + **component** tiers shipped (pattern/product reserved) × dimensions: brand, scheme, direction, density. `bes.css` carries **zero** font-size, radius or colour literals, so a brand retunes them all
- **Money is a type, not a number** — exact minor units, no implicit rounding, `allocate` for splits, `Intl` for rendering incl. Eastern Arabic numerals (doc 13)
- **UNKNOWN is a component, not a caveat** — all 13 transaction states ship as `data-bes-state`, colour never alone, and a retry control is *removed* from any state that isn't a confirmed failure (doc 07)
- **Non-negotiables** — fees before review; UNKNOWN is a designed state; color never carries meaning alone; Arabic designed, not translated; safety one tap, risk requires proof; WCAG 2.2 AA as a build gate

## Editing the docs

The markdown files in `docs/` are the source of truth. The HTML pages in `pages/` are generated from them — edit markdown, then regenerate the pages with `python3 tools/build-docs.py`, which wraps each doc in the site shell with navigation. CI fails if a regenerated page differs from what is committed, so run the build before pushing.

## Hosting the documentation site

The site is plain HTML with no build step at serve time, so GitHub Pages serves this repository as-is.

1. Repository → **Settings** → **Pages**
2. Build and deployment → Source = **Deploy from a branch**
3. Branch = **main**, folder = **/ (root)** → Save

The site appears at `https://dezinebee.github.io/banking-experience-system/` within about a minute, and redeploys on every push to `main`. A `.nojekyll` file is committed so Pages publishes the tree verbatim rather than running it through Jekyll.

Free-tier Pages requires a **public** repository; private-repo Pages needs a paid plan. For a custom domain, add it under Settings → Pages and point a CNAME at your DNS.

Before pointing real users at any deployment, read *Browser support* and *Hosting security notes* below.

## Status & license

**v2.0.0-draft · August 2026 — not yet human-verified.**

Every gate this repository passes is an automated one. None of the four human protocols in `docs/testing/` has been run: no screen-reader pass, no Arabic native-speaker review, no usability sessions, no compliance counsel review. Per `STATUS.md`, **nothing is Trial or Stable** — 52 components are Coded, meaning they exist, the gates pass and their behaviour is exercised in jsdom, not that a human has used them.

Concretely, that means:

- **All Arabic UI copy is machine-drafted** and unreviewed by a native speaker. It is flagged as such in-product.
- **Accessibility is a design target, not a verified outcome.** Contrast and structure are enforced by CI; assistive-technology behaviour is unproven.
- **Regulatory content is UX translation, not legal advice** — verify against current CBUAE requirements before shipping compliance-critical flows.

Treat this as a reference implementation and specification to learn from or build on, not as a system proven with users. `STATUS.md` is the authority on what is and isn't verified; marketing claims about this system defer to it. **Breaking release** — see `docs/migrations/v1-to-v2.md`.

License: **MIT** (`LICENSE.md`) — free to use, adapt and build on, attribution appreciated.

All examples use fictional data (realistic AED scenarios); nothing represents actual customer information.


## Browser support

The coded layer uses CSS custom properties, logical properties, `:focus-visible`, `unicode-bidi: isolate`, and `Intl.NumberFormat` (including compact notation and the `-u-nu-` numbering-system extension, which is how Eastern Arabic numerals are produced). Support floor: **Chrome/Edge 89+, Firefox 89+, Safari 15.4+** and equivalent WebViews. Older long-tail browsers receive readable content without density/theming refinements (custom-property fallbacks are present on control boundaries). Kiosk builds should pin an evergreen runtime.

## Hosting security notes

For production hosting of anything derived from this system: serve with a CSP (e.g. `default-src 'self'; style-src 'self' 'unsafe-inline' fonts.googleapis.com; font-src fonts.gstatic.com; img-src 'self' data:`), self-host fonts or add SRI where policy requires, and set `X-Frame-Options: DENY` on authenticated surfaces. The demo journey is fictional-data only and must not be presented as a real banking endpoint.
