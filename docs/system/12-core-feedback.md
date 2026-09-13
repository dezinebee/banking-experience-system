# 12 — Core Components: Feedback & Status

**Banking Experience System (BES)** · Core Components · v2.0.0-draft

Components: Alert (inline/section) · Banner (page-level) · Toast · Status Badge · Progress (bar/circular) · Skeleton · Spinner · Empty State · Loading State · Error State.

**Choosing the component — the disruption model.** Pick by *where it belongs* × *how long it persists* × *how much attention it may demand*:

| Level | Attention | Component | Example |
|---|---|---|---|
| 1 · Passive | Ambient | Status Badge | "Pending" on a transaction row |
| 2 · Notice | Read when reached | Inline Alert | "This beneficiary was added today" on review |
| 3 · Prominent | See before acting | Section Alert / Banner | "International payments are unavailable until 02:00" |
| 4 · Transient confirm | Momentary | Toast | "IBAN copied" |
| 5 · Blocking | Must respond | Dialog / Interruption pattern (doc 25) | Fraud stop, session pause |

One rule above all: **never stack multiple alerts of the same level in one region** — consolidate or escalate.

---

## Alert (inline / section)

**Anatomy:** container tinted per status (`status.*` 50-tint surface + 600 border-start bar) · status icon (shape-coded) · title (optional) · body · optional actions (≤2, link-style or small buttons) · optional dismiss (only if the information is elsewhere recoverable).

**Variants:** info (teal) · success (green) · warning (amber) · error (red) — plus ✦ **financial-hold** (purple, for reserved/held explanations).

**States:** static · dismissible · with-actions · live-updating (polite announcement).

**Usage:** contextual, adjacent to what it describes. Error alerts follow the message framework: WHAT happened · WHY · what happened to the MONEY · what to DO. Warnings before actions ("Sending to a new beneficiary — added 2 minutes ago") sit directly above the action row.

**A11y:** role=status (info/success) vs role=alert (warning/error); icon + color + title redundancy; focus moved only by the error-summary pattern, not by every alert.

**RTL:** border-start bar flips to visual right; icon at inline-start.

**Content example:**
> ⚠ **We couldn't complete this transfer.** Your bank declined the transaction. No money was deducted from your account. [Try again] [Contact support]

---

## Banner (page/app-level)

**Anatomy:** full-width strip above content · icon · single line + optional link · dismiss per policy.

**Variants:** system (maintenance: "Scheduled maintenance Fri 02:00–04:00 — cards keep working") · security campaign ("We'll never ask for your password — how to spot scams") · regulatory notice (fee changes effective date + "See what's changing") · degraded service (partial data: "Balances from other banks are delayed").

**Usage:** max one banner visible; priority order security > degraded > regulatory > system > campaign. Marketing content is **never** a Banner (marketing uses dashboard content slots) — the banner channel stays trustworthy.

**A11y:** landmark-region labeled; re-announced only on content change.

---

## Toast

**Anatomy:** compact surface, bottom (mobile) / top-inline-end (desktop) · icon + ≤ 2 lines · optional single action ("Undo") · auto-dismiss 4–6s, pausable on hover/focus.

**Usage:** confirmations of small, completed, *recoverable* acts (copied, saved, preference changed). **Never for money movement results** — a transfer outcome is a screen, not a toast. Never for errors that need action.

**A11y:** polite live region; persists longer at high text-scaling; actions also achievable elsewhere (toast-only actions banned).

---

## Status Badge

**Anatomy:** dot or pill · icon (shape-coded, doc 04) + label · tint per `status.*` / `financial.*`.

**Variants:** dot+label (tables, compact) · pill (cards, headers) · count (numeric, navigation).

**Usage:** the passive tier of the state machine everywhere a transaction/verification/consent state appears in collections. Labels come from the canonical state vocabulary — never invent per-screen synonyms ("Pending", not "In progress" here and "Processing" there).

**A11y:** label text always present (icon+color never alone); included in row's accessible name.

---

## Progress (bar / circular)

**Anatomy:** track + indicator · label (what's progressing) · value text (% or step) when determinate.

**Variants:** determinate (uploads, application completeness "Profile 80% complete") · indeterminate (short unknown waits) · step progress (see Stepper, doc 10).

**Usage rules:** determinate only with a real basis — **fake progress percentages on opaque payment rails are banned**; use the processing state's calm pulse + honest copy instead. Indeterminate > 10s escalates to a status message with expectation ("This is taking longer than usual — we'll notify you when it's done").

**A11y:** progressbar semantics with value; updates announced at sensible intervals (25/50/75/100), not continuously.

**RTL:** bar fills from inline-start (visual right in Arabic); circular rotation unmirrored.

---

## Skeleton

**Anatomy:** grey shapes matching the real layout (text lines, amount block, avatar) with subtle shimmer (reduced-motion: static).

**Usage:** structure-known loads ≥ 300ms: dashboards, lists, detail screens. Skeletons for amounts use the amount block shape but **never** placeholder digits (no "0.00 flash" — a wrong number seen for 200ms is still a wrong number seen).

**A11y:** container announced busy; real content announced on arrival.

---

## Spinner

Small inline waits ≤ ~3s inside components (button loading, search). Appears only after a 400ms delay to avoid flicker. Always with text for waits users notice ("Checking payee name…").

---

## Empty State

**Anatomy:** illustration slot (brand-tier, optional) · headline · explanation · primary action · optional secondary link.

**Variants:** first-use ("No beneficiaries yet — add someone to send money to") · filtered-empty ("No transactions match your filters" + Clear filters) · permission-empty (SME: "You don't have access to approvals — ask an administrator") · ✦ zero-balance treatments (an empty savings goal encourages; an empty account does not shame).

**Usage:** every collection defines all its empty variants at design time; a blank region shipped without one is a defect.

**Content:** explain + enable, never blame; no "Oops".

---

## Loading State (screen-level)

Composition rules: skeleton for structure + staged reveal (balance may resolve before transactions — render independently, no all-or-nothing gate); slow-path messaging at 5s; timeout at 15s → inline Error State, not an infinite shimmer.

---

## Error State (screen/section-level)

**Anatomy:** icon (octagon) · headline (what failed) · body (why, if known + money reassurance where relevant) · retry action · support path · reference code (short, human-readable, for support — internal codes stay internal).

**Variants:** connection ("You're offline — showing balances from 14:32" with cached-data timestamping) · service ("We can't load transactions right now") · partial (section-level failure inside an otherwise healthy screen — prefer partial over full-page).

**Usage:** cached financial data shown during errors is always timestamped; never silently stale. Retry is idempotent-safe (a retry never risks double-sending — the money-movement patterns own that guarantee).

**A11y:** focus moves to the error headline on full-screen errors; retry reachable first.
