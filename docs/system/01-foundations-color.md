# 01 — Color

**Banking Experience System (BES)** · Foundations · v2.0.0-draft

Color in BES is functional first: it communicates state, hierarchy and financial meaning. It is never the *only* carrier of meaning — every status color is paired with an icon and a label. The palette is deliberately restrained: a calm neutral range, one action color, and a fixed set of status and financial colors that stay constant across all brand themes.

---

## 1. Primitive palette

Primitives are raw values. **Products never use primitives directly** — they exist only to be mapped into semantic tokens. Scales run 50 (lightest) → 900 (darkest). All 600-level colors pass 4.5:1 on white; all 200-level colors pass 4.5:1 against `gray.900`.

### Neutral (slightly cool, calm)

| Token | Value | Typical role (via semantic layer) |
|---|---|---|
| `gray.0` | `#FFFFFF` | Base surface (light) |
| `gray.50` | `#F7F8FA` | Secondary surface |
| `gray.100` | `#EEF0F4` | Tertiary surface, hover fills |
| `gray.200` | `#DDE1E8` | Default borders |
| `gray.300` | `#C2C9D4` | Strong borders, disabled fills |
| `gray.400` | `#9AA4B4` | Disabled text (large only), placeholder |
| `gray.500` | `#717E92` | Secondary icons |
| `gray.600` | `#55617A` | Secondary text |
| `gray.700` | `#3D4763` | — |
| `gray.800` | `#2A324B` | Primary text (soft contexts) |
| `gray.900` | `#161C2E` | Primary text, inverse surfaces |

### Blue (action)

`blue.50 #EFF4FF` · `blue.100 #DCE7FE` · `blue.200 #B9CFFD` · `blue.300 #8AAEF9` · `blue.400 #5A8AF2` · `blue.500 #3168E8` · **`blue.600 #1F52C4`** · `blue.700 #17408F` · `blue.800 #12305F` · `blue.900 #0C2140`

### Green (positive / income / success)

`green.50 #EDFAF3` · `green.100 #D3F2E0` · `green.200 #A5E4C2` · `green.300 #6CCD9C` · `green.400 #35B274` · `green.500 #149355` · **`green.600 #0B7A45`** · `green.700 #085F37` · `green.800 #06492B` · `green.900 #04331E`

### Red (negative / expense / error)

`red.50 #FDF0EE` · `red.100 #FADAD5` · `red.200 #F4B4AA` · `red.300 #EA8172` · `red.400 #DC5341` · `red.500 #C43A28` · **`red.600 #A82E1F`** · `red.700 #832317` · `red.800 #611A11` · `red.900 #43120C`

### Amber (warning / attention)

`amber.50 #FDF6EC` · `amber.100 #FAE8CC` · `amber.200 #F3D093` · `amber.300 #E8B054` · `amber.400 #D18F1F` · `amber.500 #B27612` · **`amber.600 #8F5F0E`** · `amber.700 #6F4A0B` · `amber.800 #523708` · `amber.900 #392605`

### Teal (informational / pending-neutral)

`teal.50 #EBF7F8` · `teal.100 #CFEDEF` · `teal.200 #9FDADF` · `teal.300 #63BFC8` · `teal.400 #2FA1AD` · `teal.500 #17838F` · **`teal.600 #0F6974`** · `teal.700 #0B525B` · `teal.800 #083E45` · `teal.900 #052B30`

### Purple (reserved / hold / scheduled)

`purple.50 #F4F1FC` · `purple.100 #E5DFF8` · `purple.200 #CBBFF0` · `purple.300 #AA95E3` · `purple.400 #8A6ED3` · `purple.500 #6F4FBF` · **`purple.600 #5A3DA0`** · `purple.700 #46307C` · `purple.800 #34245C` · `purple.900 #241940`

### Gold (premium / wealth accents — decorative tier only)

`gold.100 #F6EBD4` · `gold.300 #DDBE7F` · `gold.500 #B8933F` · `gold.700 #8A6B25`

## 2. Semantic tokens (light theme defaults)

Semantic tokens are the working vocabulary. Themes remap values; roles never change.

### Surfaces
| Token | Light value | Notes |
|---|---|---|
| `surface.primary` | `gray.0` | Page/card base |
| `surface.secondary` | `gray.50` | Grouped background |
| `surface.tertiary` | `gray.100` | Nested fills, table stripes |
| `surface.inverse` | `gray.900` | Inverse blocks, tooltips |
| `surface.raised` | `gray.0` + elevation.2 | Sheets, menus |
| `surface.overlay` | `gray.900` @ 48% | Scrims |

### Text
`text.primary` = `gray.900` · `text.secondary` = `gray.600` · `text.disabled` = `gray.400` (min 14px, never for amounts) · `text.inverse` = `gray.0` · `text.link` = `blue.600` · `text.onAction` = `gray.0`

### Borders
`border.default` = `gray.200` · `border.strong` = `gray.300` · `border.focus` = `blue.500`, 2px, always paired with 2px offset ring · `border.error` = `red.600`

### Actions
`action.primary` = `blue.600` (hover `blue.700`, pressed `blue.800`, disabled `gray.300`) · `action.secondary` = transparent + `border.strong` + `text.primary` · `action.destructive` = `red.600` · `action.ghost` = transparent, `text.link`

### Status (always icon + label + color)
| Token | Color | Icon shape |
|---|---|---|
| `status.success` | `green.600` | check circle |
| `status.warning` | `amber.600` | triangle |
| `status.error` | `red.600` | octagon |
| `status.info` | `teal.600` | circle-i |
| `status.pending` | `teal.600` on `teal.50` | clock |
| `status.neutral` | `gray.600` | dash circle |

## 3. Financial semantic colors

Fixed across all brands — a customer moving between two BES-based banks reads money the same way.

| Token | Value (light) | Pairing rule |
|---|---|---|
| `financial.income` | `green.600` | Always with `+` sign and label |
| `financial.expense` | `text.primary` (NOT red) | Default spend is neutral; red is reserved for problems |
| `financial.negative` | `red.600` | Overdrawn, failed, shortfall |
| `financial.pending` | `teal.600` | With clock icon |
| `financial.completed` | `green.600` | Confirmation moments only; settled items relax to neutral |
| `financial.failed` | `red.600` | With octagon icon |
| `financial.refunded` | `green.600` on `green.50` | With return icon |
| `financial.reversed` | `purple.600` | With reverse icon |
| `financial.blocked` | `amber.600` | With lock icon; tipping-off-safe copy |
| `financial.available` | `text.primary` | The number users act on — highest weight |
| `financial.reserved` | `purple.600` | Holds, pre-auth |

**Design rationale — expense is not red.** In transaction lists, most rows are expenses; painting them red makes the list read as a wall of alarm and blunts red's error meaning. Debits render in neutral primary text with a `−` sign; red is kept for genuinely negative states.

## 4. Risk severity ramp

`risk.low` = `green.600` · `risk.medium` = `amber.600` · `risk.high` = `red.600` · `risk.critical` = `red.700` on `red.50`, paired with hard-stop pattern. A graduated caution pair `caution.minor` (`amber.500`) / `caution.major` (`amber.700`) supports fraud-warning tiering.

## 5. Dark theme

Dark theme is a first-class theme, not an inversion filter. Surfaces step *up* in lightness as elevation rises: `surface.primary` = `#10141F` · `secondary` = `#181D2B` · `tertiary` = `#212739` · raised = `#262D42`. Text: `text.primary` = `#F2F4F8`, `secondary` = `#A8B1C2`. Status/financial colors shift to their 300–400 primitives to hold 4.5:1 on dark surfaces (e.g. `financial.income` → `green.300`). Amounts and status pairs are re-verified for contrast in dark independently — never assume symmetry.

## 6. Contrast contract

Every semantic token documents its minimum contrast against its permitted surfaces: text tokens ≥ 4.5:1 (≥ 3:1 for ≥ 24px/700), interactive and status icons ≥ 3:1, focus indicator ≥ 3:1 against adjacent colors. Theme submissions (multi-brand) are validated against this contract automatically before acceptance — a brand cannot ship a palette that breaks it.

## 7. Usage rules

- Never use color alone to distinguish income/expense, gain/loss, or any status — sign, icon and label are mandatory companions.
- One primary action color per screen region; destructive and primary never adjacent without spacing ≥ `space.16`.
- Gold accents are decorative-tier only (wealth surfaces); never used for status or action.
- Charts draw from the dedicated categorical chart palette (doc 26), not from status colors, so a chart never accidentally says "error".
- High-contrast mode: an alternate token set raises text tokens to ≥ 7:1 and thickens borders; delivered as a token dimension, not a separate stylesheet.
