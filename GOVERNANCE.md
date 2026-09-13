# Governance

How the Banking Experience System is versioned, changed, and released.

## Versioning (SemVer)

`MAJOR.MINOR.PATCH` applies to the system as a whole (tokens + components + docs move together).

| Change class | Version bump | Examples |
|---|---|---|
| Token **value** change (theme-safe) | PATCH | Adjusting `border.input` dark value |
| Addition (new token, component, pattern, doc) | MINOR | Adding a Combobox |
| Behavior change, token rename/removal, markup contract change | MAJOR | Renaming `--bes-action-primary`; changing Currency Input events |
| Content/glossary change | PATCH (MINOR if terminology-dimension keys change) | Wording fixes |
| Regulatory-driven change | Per its technical class, **plus** a traceability-matrix update in the same release | CoP copy change |

Deprecations: marked in STATUS.md + docs with a sunset version; kept working for one MAJOR cycle with a console warning where feasible.

## Lifecycle statuses (per component/pattern — tracked in STATUS.md)

`Proposed → Specified → Coded → Trial → Stable → Deprecated`

- **Specified**: documented in `docs/system/` with all mandatory sections (incl. RTL + a11y).
- **Coded**: exists in `bes.css`/`bes.js` with a gallery demo; passes both automated audits.
- **Trial**: coded + at least one human-protocol pass touching it; consumers warned it may change.
- **Stable**: coded + screen-reader pass + Arabic review pass + (for money-moving patterns) usability evidence; breaking changes now require MAJOR.
- A component cannot claim Stable while any linked `verification` issue is open.

## Release process

1. All changes land via PR (see CONTRIBUTING.md) into `main`.
2. Release prep — the same gates CI enforces on every PR (`.github/workflows/ci.yml`): `python3 tokens/build-tokens.py` (validating build), `python3 tools/build-docs.py`, no generated-file drift, `python3 tools/audit-contrast.py`, `python3 tools/audit-a11y.py`, `python3 tools/audit-consistency.py`, `node --check` on both JS files, `node tools/test-js.mjs` (money/text unit tests), size budget. Then: update CHANGELOG (move Unreleased → new version), bump `$meta.version` in `tokens/tokens.json` (asset URLs re-stamp from it), update STATUS.md.
3. Tag `vX.Y.Z` on GitHub with the changelog entry as release notes. GitHub Pages redeploys automatically.
4. MAJOR releases additionally ship a migration note in `docs/migrations/`.

## Decision rights

- **Design authority** (currently: the system owner) accepts/rejects proposals against the ten principles and the quality bar (doc 30 §7).
- **The audits are non-negotiable gates** — no human override merges a failing contrast or a11y check; fix the tokens/markup instead.
- Regulatory-pattern changes additionally require the traceability matrix row to be updated and flagged for counsel re-review.

## Roadmap discipline

The gap between Specified and Stable **is** the roadmap. STATUS.md is therefore the single source of "what's actually ready" — marketing claims about the system defer to it.
