# Figma Library Build Specification

**Banking Experience System (BES)** · Design Assets · v2.0.0-draft
The executable blueprint: how the BES token architecture (docs 01–07) maps to Figma variables, styles and components. This drives the automated library build once the Figma connector is authorized, and doubles as the source map for the code token package.

---

## 1. File structure

One **BES Foundations** library file + one **BES Components** library file (components subscribe to Foundations). Later: per-brand theme files overriding variable values only.

```
BES Foundations (library)
├─ Page: Cover & usage
├─ Page: Variables reference (rendered swatch/spec sheets)
├─ Page: Type & effect styles
└─ Page: Icons (mirroring flags in component descriptions)

BES Components (library)
├─ Page: 01 Actions        ├─ Page: 06 Money
├─ Page: 02 Inputs         ├─ Page: 07 Accounts & transactions
├─ Page: 03 Navigation     ├─ Page: 08 Payments & review
├─ Page: 04 Containers     ├─ Page: 09 Disclosure & consent
├─ Page: 05 Feedback       └─ Page: 10 Templates (mobile frames, RTL duplicates)
```

## 2. Variable collections & modes

Figma modes carry our token dimensions. Direction (RTL) is **not** a variable — it's handled by auto-layout mirroring and the icon-flip flags; density and terminology are component-property concerns where variables can't reach.

### Collection `01 Primitives` (no modes, hidden from publishing)
All raw scales as variables: `gray/0…900`, `blue/50…900`, `green/…`, `red/…`, `amber/…`, `teal/…`, `purple/…`, `gold/…` (hex values from doc 01); `space/2…80`; `radius/sm|md|lg|full`; `size/target-min: 44` etc.

### Collection `02 Color semantic` — modes: **Light / Dark**
| Variable | Light | Dark |
|---|---|---|
| `surface/primary` | gray/0 | #10141F |
| `surface/secondary` | gray/50 | #181D2B |
| `surface/tertiary` | gray/100 | #212739 |
| `surface/inverse` | gray/900 | #262D42 |
| `text/primary` | gray/900 | #F2F4F8 |
| `text/secondary` | gray/600 | #A8B1C2 |
| `text/disabled` | gray/400 | #71809A |
| `text/onAction` | gray/0 | #0C2140 |
| `border/default` | gray/200 | #2A324B |
| `border/strong` | gray/300 | #3D4763 |
| `border/focus` | blue/500 | blue/300 |
| `action/primary` + hover/pressed | blue/600·700·800 | blue/400·300·200 |
| `action/destructive` | red/600 | red/300 |
| `status/success·warning·error·info·pending` | green/600, amber/600, red/600, teal/600, teal/600 | 300-tier equivalents |
| `status/…-tint` (surfaces) | 50-tier | dark tints (doc 01 §5) |
| `financial/income·expense·negative·pending·reserved·blocked·available` | per doc 01 §3 | 300-tier equivalents |
| `chart/cat1…cat7` | doc 26 §3 | dark-verified equivalents |

### Collection `03 Dimension` — modes: **Comfortable / Standard / Compact**
`density/row-height: 64/56/44` · `density/cell-pad: 20/16/12` · `density/card-pad: 24/20/16` · `density/field-gap: 28/24/20`. Components bind padding/heights to these so one mode switch re-densifies a screen.

### Collection `04 Component` (aliases only, scoped per component set)
`button/primary/bg → action/primary`, `input/border/error → status/error`, `badge/pending/bg → status/pending-tint`, etc. Never referenced across components.

## 3. Text styles

Two parallel sets, per doc 02 (Arabic gets its own metrics — Figma has no per-lang resolution, so styles are explicit):

- `EN/display 40·48·700` … `EN/caption 12·16·400` (full scale, Inter)
- `AR/display 41·50·700` … `AR/caption 13·18·400` (Noto Sans Arabic, zero letter-spacing everywhere)
- `EN/amount/hero·lg·md·sm·meta` and `AR/amount/…` — **numeric styles stay Inter with tabular figures in both sets** (amounts are LTR Latin-digit runs)
- `EN/label`, `AR/label`; overline styles exist only in EN (Arabic equivalent = semibold sentence case, per doc 02 §2)

## 4. Effect & layout styles

Effects: `elevation/1·2·3` (light values; dark handled by surface variables, shadows off) · `focus/ring` (2px border/focus + 2px offset, as a style guide component since Figma can't token focus).
Layout grids: `grid/mobile-4col-16`, `grid/tablet-8col-24`, `grid/desktop-12col-24-max1200`.

## 5. Component build order

Priority = frequency × financial risk × reusability ÷ complexity (doc 08 taxonomy). Variant properties listed = the Figma component properties to generate.

### Wave 1 — primitives everything consumes (build first)
| Component | Variants/properties |
|---|---|
| **Amount** | size(hero/lg/md/sm/meta) × semantic(neutral/credit/negative/estimated/masked) × currency(text prop) |
| **Button** | variant(primary/secondary/ghost/destructive) × size(lg/md/sm) × state(default/hover/focus/pressed/disabled/loading) × icon(boolean, start/end) |
| **Status Badge** | status(completed/pending/checking/failed/blocked/reversed/refunded/draft/disputed) × form(pill/dot/count) — icon+label locked pairs |
| **Icon Button** | style(subtle/bordered) × state × toggled(boolean) |
| **Text Input** | state(default/focus/filled/disabled/read-only/error/verified) × slots(prefix/suffix booleans) + Label/Help/Error as nested components |
| **Currency Input** | state(default/focus/error/exceeded/disabled) × chips(boolean) × context-line(boolean) |
| **Checkbox / Radio / Switch** | state × checked/selected/on × pending(switch) |
| **List Item** | leading(icon/avatar/logo/none) × lines(2/3) × trailing(amount/chevron/badge/control) |
| **Alert** | severity(info/success/warning/error/hold) × dismissible × actions(0/1/2) |

### Wave 2 — financial molecules
Fee Line + Fee Breakdown + Total Row · FX Rate (+ lock timer states) · Balance Display + Balance Set · Account Card (full/compact × states) · Transaction Item (variant × all 8 render states) · Payee Card (+ New/verified marks) · Payee Verification result (match/close/no-match/unavailable) · Limit Indicator (normal/approaching/reached) · Tabs, Segmented, Stepper, App Bar, Bottom Nav · Modal, Bottom Sheet, Toast, Banner, Skeleton, Empty State.

### Wave 3 — composed organisms
Transfer Review (assembled) · Result screens (success/pending/failed/unknown) · KFS Product Summary · Consent Request + Consent Card · Auth Prompt set · Warning tier interstitials · Card Art + Controls panel · Transaction Detail + Timeline · Repayment Schedule row · Data-viz frames (chart styling references).

### Wave 4 — templates
Mobile flow templates (amount → review → auth → result) in EN-LTR and **AR-RTL duplicates** (constraints + mirrored auto-layout verified by eye, per doc 29 rules), dashboard template, SME approval queue template.

## 6. RTL strategy in Figma

- All components built with auto-layout so direction flips cleanly; icons carrying the mirror flag (doc 04 §3) get an `RTL` boolean variant that swaps the glyph.
- Amount/IBAN layers marked "do not mirror" in descriptions; numerals always LTR.
- Wave 4 ships side-by-side EN/AR template frames as the visual regression reference.

## 7. Component documentation in Figma

Every component's description field carries: one-line purpose · doc link (GitHub Pages URL + page slug) · a11y note (target size, focus, name) · RTL note. The site remains the source of truth; Figma descriptions point to it.

## 8. Definition of done (per component)

Bound to variables only (no detached fills) · all listed variants/states present · light+dark verified · AR text style twin exists where text renders · description filled · published without overrides in the demo frame.

---

## Execution plan (once Figma is connected)

1. Create **BES Foundations** file → generate collections 01–04 with modes and all values (§2) → type/effect/grid styles (§3–4) → publish.
2. Create **BES Components** file, subscribe to Foundations → build Wave 1 (9 component sets) → review checkpoint with you → Waves 2–4 in order.
3. Each wave ends with the EN/AR + light/dark verification pass before the next begins.
