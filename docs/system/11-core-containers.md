# 11 — Core Components: Containers & Surfaces

**Banking Experience System (BES)** · Core Components · v2.0.0-draft

Components: Card · List & List Item · Table · Accordion · Modal Dialog · Drawer · Bottom Sheet · Popover · Tooltip · Divider.

---

## Card

**Anatomy:** container (`surface.primary`, `elevation.1`, `radius.md`) · optional header (title + action) · body · optional footer.

**Variants:** static (grouping) · interactive (whole card tappable — one action only; internal buttons preclude whole-card tap) · summary (dashboard modules).

**States:** default · hover (interactive only) · focus · pressed · loading (skeleton body) · error (inline retry) · empty.

**Usage:** cards group one concept. **Anti-decoration rule:** no card-inside-card beyond two levels; if everything is a card, nothing is — dense data surfaces (tables, corporate) prefer flat sections with dividers.

**Financial:** money summary cards state their freshness when not real-time ("As of 14:32"); a card containing a balance respects the masked-balance setting.

**A11y:** interactive card is a single named control ("Current account, AED 25,000.00 available, view details"); internal structure headed properly.

**RTL:** header action at inline-end; content mirrors via logical properties.

---

## List & List Item

**Anatomy (item):** leading slot (icon/avatar/logo) · primary text · secondary text · trailing slot (amount/chevron/status/control) · optional third line (metadata).

**Variants:** navigation item · selection item (radio/checkbox embedded) · display item · **transaction item** (specialized, doc 15).

**States:** default · hover · focus · pressed · selected · disabled · swipe-actions (mobile: max 2 per side, destructive requires confirm — swipe never *completes* a destructive act alone).

**Usage:** height per density (64/56/44); dividers `border.default` inset from leading slot; grouped lists with sticky section headers (dates in transaction lists).

**A11y:** whole row is the target for navigation items; embedded controls get discrete focus stops; three-line max for readability.

**RTL:** leading/trailing swap visually; amounts in trailing slot remain LTR runs, end-aligned.

---

## Table

**Anatomy:** caption/title · column headers (sortable: label + direction arrow) · rows · numeric columns end-aligned tnum · optional row selection checkboxes · sticky header · footer (totals) · toolbar (search, filters, density toggle, export).

**Variants:** simple · data table (sort/filter/select/bulk) · comparison table (products; first column sticky).

**States:** default · loading (skeleton rows preserving column widths) · empty (with cause + action) · error (retry) · row hover/selected · sorted column · filtered (active-filter chips above, clearable).

**Usage:** desktop/SME/corporate density workhorse. On mobile, tables **transform** — defined per table: transaction tables become Lists; comparison tables become swipeable cards; approval tables become stacked cards with inline actions. A horizontally scrolling raw table on mobile is a last resort and must keep the identifying column sticky.

**Financial:** amount columns end-aligned with sign and color rules (doc 07); totals row uses `type.amount.md`; bulk selection surfaces a summary bar ("12 payments selected — total AED 84,300.00") before bulk actions; sort default is newest-first for time data.

**A11y:** real table semantics (th/scope); sort state announced; row actions reachable by keyboard; selection count live-announced.

**RTL:** column order mirrors; numeric columns stay end-aligned (visual left in Arabic); sort arrows unmirrored (vertical semantics).

---

## Accordion

**Anatomy:** header (label + optional metadata + chevron) · panel.

**Usage:** progressive disclosure of secondary detail (fee breakdowns, FAQ, transaction metadata). **Disclosure rule:** anything the user must see to decide (total fees, key risks) is *outside* accordions on review screens — accordions elaborate, they never hide obligations.

**States:** collapsed · expanded · focus · disabled.

**A11y:** button header with expanded state; panel labeled by header; multiple-open allowed (no auto-collapse on data surfaces).

**RTL:** chevron mirrors (points inline-start when open per convention chosen: chevron-down rotates — unmirrored vertical rotation, documented).

---

## Modal Dialog

**Anatomy:** scrim · surface (`elevation.3`) · title · body · action row (primary at inline-end, cancel at inline-start) · close (only when closing is safe).

**Variants:** confirmation (decision) · alert (acknowledge) · task (short embedded form) — anything longer is a screen, not a modal.

**States:** open · closing-guard (unsaved input → confirm discard).

**Usage:** modals interrupt; reserve for decisions that must block ("Remove beneficiary Rajesh Kumar? You'll need to add them again to send money."). Money-moving confirmation happens on **screens**, not modals — a modal confirm for AED 250,000 is too light. Destructive confirms name the object and consequence; buttons echo outcomes ("Remove beneficiary" / "Keep beneficiary").

**A11y:** focus trapped, initial focus on the least-destructive action, Esc closes (unless closing-guard), focus returns to trigger; title is the accessible name.

**RTL:** action order mirrors with logical placement; close at inline-end.

---

## Drawer (desktop side panel)

**Anatomy:** surface sliding from inline-end · header (title + close) · body · optional footer actions.

**Usage:** contextual detail beside data (transaction detail next to the table, approval detail in corporate queues) — preserves list context. Width 400–560px; push or overlay per surface density.

**States:** open · closed · stacked (max 2; breadcrumb within).

**A11y:** focus management as dialog when overlay, as region when push; close returns focus to the row.

**RTL:** slides from inline-end (visual left in Arabic).

---

## Bottom Sheet (mobile)

**Anatomy:** grabber · title · content · detents (medium/full) · scrim.

**Usage:** contextual actions, pickers, short confirmations, in-context explanations ("Why this fee?"). Full flows use screens. Critical warnings (fraud) never use sheets (dismissable-by-swipe is too weak).

**States:** medium · full · dragging · closing-guard for inputs.

**A11y:** dialog semantics; swipe-to-close paired with a visible close button; grabber not the only affordance.

---

## Popover

**Anatomy:** anchored surface (`elevation.2`) with arrow · content (rich: text, links, small forms) · close on outside-tap/Esc.

**Usage:** desktop contextual detail (rate breakdown hover-to-detail, calendar legends). On touch, popovers become bottom sheets automatically.

**A11y:** triggered by click/Enter (never hover-only for content that matters); focusable content reachable.

**RTL:** anchors and arrows flip logically.

---

## Tooltip

**Anatomy:** short text label on hover/focus.

**Usage:** names icon-only controls; ≤ 8 words; never contains information unavailable elsewhere; never on mobile as the sole explanation (use help text or an info popover→sheet).

**A11y:** appears on focus as well as hover; not the accessible-name mechanism itself (that's aria-label) but supplementary.

---

## Divider

`border.default`, 1px; section dividers full-bleed, item dividers inset from leading content; vertical dividers only in toolbars/dense headers. Semantic (hr) only when it separates true sections for assistive tech; otherwise decorative and hidden.
