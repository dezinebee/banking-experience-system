# 02 — Typography

**Banking Experience System (BES)** · Foundations · v2.0.0-draft

Typography must carry English, Arabic and mixed bidirectional content; large financial numbers; dense tables; and accessibility scaling — with equal quality in both languages. Arabic is designed, not translated.

---

## 1. Type stacks

| Token | Default value | Notes |
|---|---|---|
| `font.latin` | `"Inter", -apple-system, "Segoe UI", Roboto, sans-serif` | UI + content, variable weight |
| `font.arabic` | `"Noto Sans Arabic", "Segoe UI Arabic", "Geeza Pro", sans-serif` | Matched x-height/weight range to Latin stack |
| `font.numeric` | inherits, with `font-feature-settings: "tnum" 1` | Tabular numerals for all financial figures |
| `font.display` | brand-themeable (falls back to `font.latin`/`font.arabic`) | Marketing/display only, never for amounts or forms |

Rules: brands may substitute stacks from a **tested pair list** (Latin + Arabic verified together for x-height harmony, weight matching and numeral quality). A brand may never set an Arabic fallback chain that ends in a Latin-only face.

## 2. Arabic type metrics (mandatory adjustments)

Arabic script has no capitals, denser letterforms, and cursive joining. When `lang="ar"`:

- **Optical size:** +1px at body sizes, +2px at caption sizes (`caption` 12 → 13/14; `body` 16 → 17). Implemented via the size token resolving per-language, not via manual overrides.
- **Line-height:** +0.125 rem step at every level (Arabic ascenders/descenders and diacritics need air).
- **Letter-spacing: 0. Always.** Tracking breaks cursive joining. The `letterSpacing` axis is inert in Arabic contexts.
- **No uppercase emphasis.** `text-transform: uppercase` has no meaning; emphasis uses weight (600/700) or size instead. Any component style that uses caps in Latin (e.g. overline labels) defines its Arabic equivalent as semibold sentence case.
- **Underlines** sit lower (`text-underline-offset` increased) to clear descender loops.
- Truncation ellipsis follows text direction; never truncate mid-amount.

## 3. Scale

Rem-based (1rem = 16px), user scalable to 200% without loss of function. `lh` = line-height.

| Token | Size/lh (Latin) | Size/lh (Arabic) | Weight | Use |
|---|---|---|---|---|
| `type.display` | 40/48 | 41/50 | 700 | Marketing, hero balances on dashboards |
| `type.h1` | 32/40 | 33/42 | 700 | Screen titles |
| `type.h2` | 24/32 | 25/34 | 600 | Section titles |
| `type.h3` | 20/28 | 21/30 | 600 | Card titles, group headers |
| `type.bodyLg` | 18/28 | 19/30 | 400 | Lead paragraphs, review screens |
| `type.body` | 16/24 | 17/26 | 400 | Default |
| `type.bodySm` | 14/20 | 15/22 | 400 | Secondary text, table cells (compact) |
| `type.label` | 14/20 | 15/22 | 500 | Form labels, buttons |
| `type.caption` | 12/16 | 13/18 | 400 | Metadata, timestamps — never for amounts or legal text |

## 4. Financial type styles

Money gets its own styles; a raw text style on an amount is a defect.

| Token | Spec | Use |
|---|---|---|
| `type.amount.hero` | 40/48, 700, tnum | Dashboard balance |
| `type.amount.lg` | 28/36, 700, tnum | Transfer review total, account balance |
| `type.amount.md` | 20/28, 600, tnum | Transaction detail, card rows |
| `type.amount.sm` | 16/24, 600, tnum | Transaction list rows |
| `type.amount.meta` | 13/16, 500, tnum | Converted values, secondary currency |
| `type.financial.meta` | 13/18, 400 | Rate stamps, fee labels, IBAN display (with `dir="ltr"` embedding) |

Rules:
- **Tabular numerals everywhere money or columns of numbers appear** — amounts must align vertically in lists and tables.
- Currency code renders at 0.75× the amount size, weight 500 (e.g., **AED 25,000.00** with "AED" smaller): hierarchy belongs to the number.
- Decimals in hero/large amounts may render at 0.6× size, aligned to the cap height (25,000<sup>.00</sup>) — precision preserved, hierarchy improved. Never drop decimals to save space (see doc 07 for abbreviation rules).
- Sign (`+`/`−`) uses the true minus (U+2212), same size as the integer part, never separated from the number by wrapping.

## 5. Bidirectional (bidi) behavior

- Numbers are always Western-digit LTR runs by default (Eastern Arabic numerals available as an explicit locale preference — never mixed in one screen; see doc 29).
- Embedded LTR strings inside Arabic text — IBANs, card numbers, URLs, emails, reference codes — are wrapped in direction isolation (`<bdi>`/`unicode-bidi: isolate`) so punctuation doesn't scramble.
- Amounts in RTL context: the amount block (currency + number + sign) is a single isolated LTR run, positioned by the layout's logical alignment. `AED 5,000−` never happens; the sign stays attached: `−AED 5,000`, placed correctly in the RTL sentence.
- Mixed-language names (e.g., "شركة Al Noor Trading LLC") render with isolation per run; truncation tested in both directions.

## 6. Alignment

- Latin text: start-aligned (left in LTR). Arabic: start-aligned (right in RTL).
- **Numeric table columns: end-aligned in both directions** so magnitudes compare visually.
- Labels above inputs in both directions (never left-of-field, which breaks in RTL and at 200% zoom).
- No justified text (rivers harm dyslexic readers; Arabic justification via kashida is display-only and off by default).

## 7. Accessibility

- Text scales to 200% via OS/browser settings without truncating amounts, losing controls, or horizontal scrolling; critical flows tested at 200% in both languages.
- Minimum body text 16px (17 Arabic); minimum any text 12px (13 Arabic); disabled text never below 14px.
- Line length target 45–75 characters Latin, 35–60 Arabic.
- Weight is never the sole differentiator of meaning (pairs with size/position/label).
- Legal and disclosure text (KFS, terms) never renders below `type.bodySm`; "small print" is a banned pattern — disclosure uses standard body sizes with clear headings.
