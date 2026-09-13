# 03 — Spacing, Layout & Responsive System

**Banking Experience System (BES)** · Foundations · v2.0.0-draft

---

## 1. Spacing scale

4px base unit. Tokens are named by value for primitives, by role for semantics.

| Primitive | px | Common semantic roles |
|---|---|---|
| `space.2` | 2 | Icon-to-badge nudges |
| `space.4` | 4 | Inside compound controls |
| `space.8` | 8 | Icon-to-label, chip padding |
| `space.12` | 12 | Compact cell padding, stacked metadata |
| `space.16` | 16 | Default component padding, list row padding |
| `space.20` | 20 | Card padding (standard density) |
| `space.24` | 24 | Section separation within a card |
| `space.32` | 32 | Between cards/sections |
| `space.40` | 40 | Major section breaks |
| `space.48` | 48 | Screen-level top spacing (desktop) |
| `space.64` | 64 | Hero regions |
| `space.80` | 80 | Marketing/kiosk breathing room |

Semantic layer examples: `layout.gutter`, `layout.cardPadding`, `layout.sectionGap`, `form.fieldGap` (= `space.24`), `form.groupGap` (= `space.32`). Components consume semantics so density modes can remap them globally.

## 2. Density modes

A token dimension, not separate components.

| Mode | Multiplier | Row height (list/table) | Default for |
|---|---|---|---|
| `density.comfortable` | 1.25× padding | 64 / 56 | Consumer onboarding, elderly/large-type contexts |
| `density.standard` | 1× | 56 / 48 | Retail banking default |
| `density.compact` | 0.75× padding | 44 / 36 | SME dashboards, corporate treasury, data tables |

Rules: touch target minimum (44×44) is **never** reduced by density on touch surfaces — compact mode on mobile tightens visual padding but preserves hit areas. Density is user-adjustable on data-heavy surfaces (tables remember the choice).

## 3. Grid

- **Mobile:** 4-column, 16px gutters/margins.
- **Tablet:** 8-column, 24px gutters.
- **Desktop:** 12-column, 24px gutters, max content width 1200px (reading surfaces) / fluid to 1600px (data surfaces).
- **Large desktop:** 12-column, content max 1440px; extra width goes to data density or split panes, never to stretched line lengths.
- **Kiosk/ATM-like:** 8-column, enlarged type/targets (see §5).

Layout uses **logical properties exclusively**: `margin-inline-start`, `padding-inline-end`, `inset-inline` — never physical left/right. The grid mirrors automatically under `dir="rtl"` with zero layout overrides. Any physical property in a component stylesheet is a lint failure.

## 4. Breakpoints

| Token | Range | Class |
|---|---|---|
| `bp.mobile` | 320–599 | Primary design target |
| `bp.tablet` | 600–899 | |
| `bp.desktop` | 900–1279 | |
| `bp.desktopLg` | 1280–1919 | |
| `bp.kiosk` | 1920+ / device-class flag | Also set by deployment, not width alone |

## 5. Surface classes and adaptation rules

Do not scale desktop down. Each pattern declares its adaptation explicitly:

| Behavior | Mechanism |
|---|---|
| Stays visible | Core answer to the screen's primary question (e.g., available balance, total to pay) |
| Collapses | Secondary metadata into expandable rows/accordions |
| Progressive disclosure | Fee breakdowns, rate details behind an inline expander (content still one tap away, never hidden past review) |
| Moves to drawer | Desktop side-details (transaction detail) |
| Becomes bottom sheet | Mobile contextual actions, pickers, confirmations that don't warrant full screens |

Kiosk/ATM-like: minimum text 18px, touch targets 56px, no hover-dependent interactions, session-timeout patterns mandatory, privacy filters assumed (no sensitive data at glanceable size beyond the active user's need).

## 6. Elevation & shape

### Elevation
| Token | Use | Light treatment | Dark treatment |
|---|---|---|---|
| `elevation.0` | Flat, on-surface | none | none |
| `elevation.1` | Cards | y1 blur2 @8% | surface lightness step |
| `elevation.2` | Raised (menus, sheets) | y2 blur8 @10% | +1 lightness step |
| `elevation.3` | Modals, dialogs | y8 blur24 @14% | +2 steps + scrim |

Dark mode communicates elevation primarily by surface lightness, not shadow.

### Shape
| Token | Default | Range brands may choose |
|---|---|---|
| `radius.sm` | 6 | 2–8 (inputs, chips) |
| `radius.md` | 10 | 4–14 (cards, buttons) |
| `radius.lg` | 16 | 8–20 (sheets, modals) |
| `radius.full` | 999 | pills, avatars |

Shape is a themeable preset applied as a set (a brand picks "sharp / standard / soft", not per-component values). Financial document surfaces (receipts, KFS) always use `radius.sm` regardless of brand — they read as records, not marketing.

## 7. Z-index scale

`z.base 0` · `z.raised 10` · `z.sticky 100` (headers, table headers) · `z.drawer 800` · `z.modal 900` · `z.toast 950` · `z.critical 1000` (fraud interruptions, session pause — nothing may render above this layer).
