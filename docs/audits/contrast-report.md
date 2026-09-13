# Contrast Audit Report

**Generated:** 2026-09-13 by `tools/audit-contrast.py` (re-run on every token, CSS or markup change)
**Method:** WCAG 2.x relative-luminance contrast ratio.

| Part | Scope | Result |
|---|---|---|
| A — contract | 78 declared token pairings, both schemes | ✅ all pass |
| B — derived | 3136 element/state colourings across 65 pages × 2 schemes, resolved through 480 rules in bes.css, site.css, gallery.css | ✅ all pass |

Part B is the gate that matters: it computes what each element in the shipped HTML actually resolves to, so it catches combinations nobody listed. Part A remains as a statement of intent.

## Part A — declared token contract

| Mode | Foreground | Background | Values | Ratio | Min | Result | Context |
|---|---|---|---|---|---|---|---|
| light | `text.primary` | `surface.primary` | #161C2E / #FFFFFF | 16.94 | 4.5 | ✅ | Body text on base surface |
| light | `text.primary` | `surface.secondary` | #161C2E / #F7F8FA | 15.94 | 4.5 | ✅ | Body text on secondary surface |
| light | `text.primary` | `surface.tertiary` | #161C2E / #EEF0F4 | 14.85 | 4.5 | ✅ | Body text on tertiary fills |
| light | `text.secondary` | `surface.primary` | #55617A / #FFFFFF | 6.22 | 4.5 | ✅ | Secondary text on base |
| light | `text.secondary` | `surface.secondary` | #55617A / #F7F8FA | 5.85 | 4.5 | ✅ | Secondary text on secondary surface |
| light | `text.link` | `surface.primary` | #1F52C4 / #FFFFFF | 6.86 | 4.5 | ✅ | Links on base |
| light | `text.onAction` | `action.primary` | #FFFFFF / #1F52C4 | 6.86 | 4.5 | ✅ | Button label on primary action |
| light | `action.primary` | `surface.primary` | #1F52C4 / #FFFFFF | 6.86 | 3.0 | ✅ | Primary action vs base (non-text) |
| light | `action.destructive` | `surface.primary` | #A82E1F / #FFFFFF | 6.83 | 4.5 | ✅ | Destructive text/border on base |
| light | `border.focus` | `surface.primary` | #3168E8 / #FFFFFF | 4.91 | 3.0 | ✅ | Focus ring vs base |
| light | `border.input` | `surface.primary` | #717E92 / #FFFFFF | 4.12 | 3.0 | ✅ | Control boundaries (inputs, PIN, upload) |
| light | `status.success` | `status.successTint` | #0B7A45 / #EDFAF3 | 5.04 | 4.5 | ✅ | Success badge text on tint |
| light | `status.warning` | `status.warningTint` | #8F5F0E / #FDF6EC | 5.13 | 4.5 | ✅ | Warning badge text on tint |
| light | `status.error` | `status.errorTint` | #A82E1F / #FDF0EE | 6.14 | 4.5 | ✅ | Error badge text on tint |
| light | `status.info` | `status.infoTint` | #0F6974 / #EBF7F8 | 5.83 | 4.5 | ✅ | Info badge text on tint |
| light | `status.error` | `surface.primary` | #A82E1F / #FFFFFF | 6.83 | 4.5 | ✅ | Error text on base |
| light | `financial.income` | `surface.primary` | #0B7A45 / #FFFFFF | 5.41 | 4.5 | ✅ | Income amounts on base |
| light | `financial.negative` | `surface.primary` | #A82E1F / #FFFFFF | 6.83 | 4.5 | ✅ | Negative amounts on base |
| light | `financial.reserved` | `surface.primary` | #5A3DA0 / #FFFFFF | 8.05 | 4.5 | ✅ | Reserved amounts on base |
| light | `transaction.draft` | `transaction.draftTint` | #55617A / #EEF0F4 | 5.45 | 4.5 | ✅ | State badge: draft |
| light | `transaction.review` | `transaction.reviewTint` | #3D4763 / #EEF0F4 | 8.07 | 4.5 | ✅ | State badge: review |
| light | `transaction.authentication` | `transaction.authenticationTint` | #1F52C4 / #EFF4FF | 6.22 | 4.5 | ✅ | State badge: authentication |
| light | `transaction.processing` | `transaction.processingTint` | #0F6974 / #EBF7F8 | 5.83 | 4.5 | ✅ | State badge: processing |
| light | `transaction.pending` | `transaction.pendingTint` | #0F6974 / #EBF7F8 | 5.83 | 4.5 | ✅ | State badge: pending |
| light | `transaction.completed` | `transaction.completedTint` | #0B7A45 / #EDFAF3 | 5.04 | 4.5 | ✅ | State badge: completed |
| light | `transaction.failed` | `transaction.failedTint` | #A82E1F / #FDF0EE | 6.14 | 4.5 | ✅ | State badge: failed |
| light | `transaction.unknown` | `transaction.unknownTint` | #0F6974 / #EBF7F8 | 5.83 | 4.5 | ✅ | State badge: unknown |
| light | `transaction.blocked` | `transaction.blockedTint` | #8F5F0E / #FDF6EC | 5.13 | 4.5 | ✅ | State badge: blocked |
| light | `transaction.reversed` | `transaction.reversedTint` | #5A3DA0 / #F4F1FC | 7.22 | 4.5 | ✅ | State badge: reversed |
| light | `transaction.refunded` | `transaction.refundedTint` | #0B7A45 / #EDFAF3 | 5.04 | 4.5 | ✅ | State badge: refunded |
| light | `transaction.disputed` | `transaction.disputedTint` | #5A3DA0 / #F4F1FC | 7.22 | 4.5 | ✅ | State badge: disputed |
| light | `transaction.cancelled` | `transaction.cancelledTint` | #55617A / #EEF0F4 | 5.45 | 4.5 | ✅ | State badge: cancelled |
| light | `chart.cat1` | `surface.primary` | #1F52C4 / #FFFFFF | 6.86 | 3.0 | ✅ | Chart series 1 (non-text) |
| light | `chart.cat2` | `surface.primary` | #0F6974 / #FFFFFF | 6.38 | 3.0 | ✅ | Chart series 2 (non-text) |
| light | `chart.cat3` | `surface.primary` | #8F5F0E / #FFFFFF | 5.51 | 3.0 | ✅ | Chart series 3 (non-text) |
| light | `chart.cat4` | `surface.primary` | #5A3DA0 / #FFFFFF | 8.05 | 3.0 | ✅ | Chart series 4 (non-text) |
| light | `chart.cat5` | `surface.primary` | #0B7A45 / #FFFFFF | 5.41 | 3.0 | ✅ | Chart series 5 (non-text) |
| light | `chart.cat6` | `surface.primary` | #A82E1F / #FFFFFF | 6.83 | 3.0 | ✅ | Chart series 6 (non-text) |
| light | `chart.cat7` | `surface.primary` | #55617A / #FFFFFF | 6.22 | 3.0 | ✅ | Chart series 7 (non-text) |
| dark | `text.primary` | `surface.primary` | #F2F4F8 / #10141F | 16.70 | 4.5 | ✅ | Body text on base surface |
| dark | `text.primary` | `surface.secondary` | #F2F4F8 / #181D2B | 15.26 | 4.5 | ✅ | Body text on secondary surface |
| dark | `text.primary` | `surface.tertiary` | #F2F4F8 / #212739 | 13.49 | 4.5 | ✅ | Body text on tertiary fills |
| dark | `text.secondary` | `surface.primary` | #A8B1C2 / #10141F | 8.52 | 4.5 | ✅ | Secondary text on base |
| dark | `text.secondary` | `surface.secondary` | #A8B1C2 / #181D2B | 7.79 | 4.5 | ✅ | Secondary text on secondary surface |
| dark | `text.link` | `surface.primary` | #6B96F4 / #10141F | 6.39 | 4.5 | ✅ | Links on base |
| dark | `text.onAction` | `action.primary` | #0C2140 / #6B96F4 | 5.58 | 4.5 | ✅ | Button label on primary action |
| dark | `action.primary` | `surface.primary` | #6B96F4 / #10141F | 6.39 | 3.0 | ✅ | Primary action vs base (non-text) |
| dark | `action.destructive` | `surface.primary` | #EA8172 / #10141F | 6.90 | 4.5 | ✅ | Destructive text/border on base |
| dark | `border.focus` | `surface.primary` | #8AAEF9 / #10141F | 8.32 | 3.0 | ✅ | Focus ring vs base |
| dark | `border.input` | `surface.primary` | #8A94A8 / #10141F | 6.03 | 3.0 | ✅ | Control boundaries (inputs, PIN, upload) |
| dark | `status.success` | `status.successTint` | #6CCD9C / #0B2E1E | 7.62 | 4.5 | ✅ | Success badge text on tint |
| dark | `status.warning` | `status.warningTint` | #E8B054 / #33270A | 7.50 | 4.5 | ✅ | Warning badge text on tint |
| dark | `status.error` | `status.errorTint` | #EA8172 / #361410 | 6.23 | 4.5 | ✅ | Error badge text on tint |
| dark | `status.info` | `status.infoTint` | #63BFC8 / #0A2A2E | 7.10 | 4.5 | ✅ | Info badge text on tint |
| dark | `status.error` | `surface.primary` | #EA8172 / #10141F | 6.90 | 4.5 | ✅ | Error text on base |
| dark | `financial.income` | `surface.primary` | #6CCD9C / #10141F | 9.50 | 4.5 | ✅ | Income amounts on base |
| dark | `financial.negative` | `surface.primary` | #EA8172 / #10141F | 6.90 | 4.5 | ✅ | Negative amounts on base |
| dark | `financial.reserved` | `surface.primary` | #AA95E3 / #10141F | 7.11 | 4.5 | ✅ | Reserved amounts on base |
| dark | `transaction.draft` | `transaction.draftTint` | #A8B1C2 / #212739 | 6.88 | 4.5 | ✅ | State badge: draft |
| dark | `transaction.review` | `transaction.reviewTint` | #F2F4F8 / #212739 | 13.49 | 4.5 | ✅ | State badge: review |
| dark | `transaction.authentication` | `transaction.authenticationTint` | #6B96F4 / #181D2B | 5.84 | 4.5 | ✅ | State badge: authentication |
| dark | `transaction.processing` | `transaction.processingTint` | #63BFC8 / #0A2A2E | 7.10 | 4.5 | ✅ | State badge: processing |
| dark | `transaction.pending` | `transaction.pendingTint` | #63BFC8 / #0A2A2E | 7.10 | 4.5 | ✅ | State badge: pending |
| dark | `transaction.completed` | `transaction.completedTint` | #6CCD9C / #0B2E1E | 7.62 | 4.5 | ✅ | State badge: completed |
| dark | `transaction.failed` | `transaction.failedTint` | #EA8172 / #361410 | 6.23 | 4.5 | ✅ | State badge: failed |
| dark | `transaction.unknown` | `transaction.unknownTint` | #63BFC8 / #0A2A2E | 7.10 | 4.5 | ✅ | State badge: unknown |
| dark | `transaction.blocked` | `transaction.blockedTint` | #E8B054 / #33270A | 7.50 | 4.5 | ✅ | State badge: blocked |
| dark | `transaction.reversed` | `transaction.reversedTint` | #AA95E3 / #1F1638 | 6.60 | 4.5 | ✅ | State badge: reversed |
| dark | `transaction.refunded` | `transaction.refundedTint` | #6CCD9C / #0B2E1E | 7.62 | 4.5 | ✅ | State badge: refunded |
| dark | `transaction.disputed` | `transaction.disputedTint` | #AA95E3 / #1F1638 | 6.60 | 4.5 | ✅ | State badge: disputed |
| dark | `transaction.cancelled` | `transaction.cancelledTint` | #A8B1C2 / #212739 | 6.88 | 4.5 | ✅ | State badge: cancelled |
| dark | `chart.cat1` | `surface.primary` | #8AAEF9 / #10141F | 8.32 | 3.0 | ✅ | Chart series 1 (non-text) |
| dark | `chart.cat2` | `surface.primary` | #63BFC8 / #10141F | 8.60 | 3.0 | ✅ | Chart series 2 (non-text) |
| dark | `chart.cat3` | `surface.primary` | #E8B054 / #10141F | 9.43 | 3.0 | ✅ | Chart series 3 (non-text) |
| dark | `chart.cat4` | `surface.primary` | #AA95E3 / #10141F | 7.11 | 3.0 | ✅ | Chart series 4 (non-text) |
| dark | `chart.cat5` | `surface.primary` | #6CCD9C / #10141F | 9.50 | 3.0 | ✅ | Chart series 5 (non-text) |
| dark | `chart.cat6` | `surface.primary` | #EA8172 / #10141F | 6.90 | 3.0 | ✅ | Chart series 6 (non-text) |
| dark | `chart.cat7` | `surface.primary` | #9AA4B4 / #10141F | 7.31 | 3.0 | ✅ | Chart series 7 (non-text) |

## Part B — derived from the artefacts

✅ **3136 element colourings computed and scored; none below threshold.**

## Scope notes
- Part B walked 65 HTML pages, matched 480 rules from `bes.css`, `site.css`, `gallery.css`, and scored 3136 element colourings per the cascade (specificity, then source order).
- Backgrounds are taken from the nearest ancestor that declares a resolvable one; where the whole chain declares none, the page ground is assumed and the row is marked.
- Unresolved and therefore unscored: 45100× literal:var, 1884× background, 16× var, 12× literal:transparent !imp. These are gradients, `rgba()`, `currentColor` and keywords — they need a rendering engine, and they are counted here rather than hidden.
- 13 selectors used syntax the matcher does not model and were skipped.
- `:disabled` rules are exempt per WCAG 1.4.3. Hover and focus states are scored — a state the user can reach is a state that has to be readable.
- Rules qualified `:root:not([data-theme="light"])` outside a `prefers-color-scheme: dark` block are scored in **both** schemes, because that is what they do — see consistency audit C7.
- Large-text threshold (3:1) applies at ≥24px, or ≥18.66px at weight ≥700, from the winning `font-size`/`font-weight`.
- Chart series are held to the 3:1 non-text minimum in Part A; data is never conveyed by colour alone.
- This audit covers colour contrast only. Focus visibility, target size and reflow are covered by the static audit, the DOM tests and the human protocols.