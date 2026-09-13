# 29 — Localization & RTL Architecture

**Banking Experience System (BES)** · v2.0.0-draft

Arabic is a designed first-class language, not translated English. Direction is a token dimension; every component documents its own RTL behavior (the "RTL section" is mandatory in component docs); bidi correctness is tested with standing fixtures.

---

## 1. Architectural rules

- **Logical properties only** (`inline-start/end`, `block-start/end`) in all layout code; physical left/right is lint-banned.
- Direction set at the root (`dir="rtl"`/`ltr"` + `lang`); components inherit — no per-component direction hacks.
- Icons flip by **metadata flag** (doc 04 §3), not by blanket transform.
- Type metrics resolve per language (doc 02 §2: +1–2px, taller line-height, zero letter-spacing, no caps emphasis).
- Strings live in message catalogs with position-independent placeholders; **no string concatenation** (word order differs); pluralization via full Arabic plural categories. *(v1.0.1: catalogs are per-surface dictionaries + `data-*` overrides on library components; extraction to shared `assets/i18n/*.json` files is the next localization milestone.)*
- Language switching is live: swaps language + direction preserving screen, scroll and draft state (doc 10).

## 2. Numerals, dates, calendars

- **Numerals:** Western Arabic digits (0–9) default for all financial figures; Eastern Arabic digits (٠–٩) offered as an explicit locale preference applying to *display* only (entry accepts both, doc 07 §6). **Never mixed within one screen.** Amounts remain LTR runs in all cases.
- **Dates:** localized long forms ("٣٠ أغسطس ٢٠٢٦" / "30 August 2026"); numeric dates always labeled or unambiguous (DD/MM/YYYY is the UAE convention — never US order); weekday abbreviations avoided in Arabic (identical initials) — short names used instead.
- **Calendars:** Gregorian canonical for all processing and legal dates; **Hijri dual display** as a slot on relevant surfaces (Islamic products, cultural moments): "1 October 2026 · ١٩ ربيع الآخر ١٤٤٨". Hijri is never the sole date on an actionable element.
- **Week start:** locale-configurable; UAE default Monday (weekend Sat–Sun).

## 3. Bidirectional text rules (the defect factory — engineered away)

- Embedded LTR data in RTL sentences — IBANs, card numbers, amounts, emails, URLs, reference codes — always in isolation (`<bdi>`/`unicode-bidi: isolate`). Components that render these (IBAN Display, Amount, inputs) ship with isolation built in.
- Mixed-script names render per-run isolated; truncation direction-aware; never truncate inside an amount or identifier.
- Punctuation localizes: Arabic comma (،), Arabic question mark (؟); parentheses/brackets mirror automatically via bidi — components avoid ASCII-art constructions that break.
- Inputs holding LTR data (IBAN, email, card, reference) set `dir="ltr"` internally with start-anchored caret while labels/help remain RTL.

## 4. Component direction notes (system-wide summary)

| Area | RTL behavior |
|---|---|
| Layout/grid | Mirrors wholesale via logical properties |
| Navigation | Back points right; bottom-nav order mirrors; drawers dock inline-start |
| Steppers/progress | Advance inline (visual right→left); bars fill from inline-start |
| Tables | Column order mirrors; numeric columns end-aligned; sort arrows unmirrored |
| Charts | **Time axes stay LTR** (deliberate exception, doc 26 §5); category axes mirror |
| Amounts/identifiers | LTR isolated runs, positioned logically |
| Checkmarks/status | Unmirrored |
| Sliders | Min at inline-start (visual right in Arabic) |
| Phone/PIN pads | Digit layout unchanged (numeric convention) |

## 5. Content localization workflow

- EN + AR authored together at design time (bilingual content design); the glossary (doc 27 §2) is the single vocabulary authority; new strings without an AR pair fail the content gate.
- Legal/disclosure content: institution provides certified bilingual versions; layout renders either single-language-per-preference or dual-column (institution-configurable); the two versions are versioned together.
- Review process: native-speaker design review of Arabic *layouts* (not just strings) per release — screenshots of both directions are part of component PRs.

## 6. Beyond Arabic/English (extension readiness)

The architecture (catalogs, logical layout, isolation, plural rules, locale formatting) makes additional languages — Hindi, Urdu (RTL), Tagalog, Malayalam, Bengali — a content project, not re-engineering. Urdu inherits the full RTL machinery; Indic scripts get their own type-stack pairing entries and metric adjustments in the same mechanism Arabic uses. v1 ships AR/EN; the extension path is documented so product teams don't fork.

## 7. Testing

Standing fixtures: Arabic sentence containing an IBAN + amount + Latin brand name; mixed-script payee names; long-German-length strings; Eastern-numeral preference on every money surface; 200% scale AR; RTL screenshot diffs per component; live language-switch mid-flow (state preservation assert).
