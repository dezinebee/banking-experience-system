# 10 — Core Components: Navigation

**Banking Experience System (BES)** · Core Components · v2.0.0-draft

Components: App Bar (top) · Bottom Navigation · Side Navigation · Tabs · Segmented Control · Breadcrumb · Pagination · Stepper (Progress) · Language Switcher · Session Bar.

---

## App Bar (Top)

**Anatomy:** back/close at inline-start · title (screen question, e.g. "Send money") · contextual actions at inline-end (≤2 + overflow) · optional subtitle (account context: "From Current account ••4521").

**States:** default · scrolled (elevation on) · contextual (in-flow variant locks navigation to Back/Cancel only).

**Usage:** in money flows the bar shows **step context** ("Send money · Step 2 of 4") and Cancel behavior is explicit — cancelling a DRAFT asks nothing; cancelling past AUTHENTICATION confirms ("Your transfer hasn't been sent. Leave anyway?").

**A11y:** title is the page heading (h1); back has accessible name naming the destination ("Back to Payees").

**RTL:** back chevron mirrors and sits at inline-start (visual right in Arabic); title alignment start.

---

## Bottom Navigation (mobile)

**Anatomy:** 4–5 destinations: icon + label (labels always visible — icon-only bottom nav is banned) · badge slot (approvals count, unread).

**Default retail set:** Home · Payments · Cards · Hub (Products/More) · Profile. SME set: Home · Payments · Approvals · Accounts · More.

**States:** active (filled icon + `action.primary` tint) · inactive · badge (numeric ≤99, then "99+").

**Usage:** persistent across top-level destinations; hidden inside money flows (flows are modal journeys with the App Bar contract).

**A11y:** tab-bar semantics; active announced; badges included in name ("Approvals, 3 pending").

**RTL:** order mirrors (first destination at visual right).

---

## Side Navigation (desktop / SME / corporate)

**Anatomy:** product switcher region · sections with headers · items (icon + label + badge) · collapse toggle · footer (settings, language, session).

**States:** expanded · collapsed (icons + tooltips) · item active/hover/focus · section collapsed.

**Financial:** corporate surfaces pin **Approvals** with live count; entity/company switcher at top for multi-entity users, with the active entity always visible ("Al Noor Trading LLC — AED accounts").

**A11y:** landmark nav with label; collapse state persists; keyboard operable throughout.

**RTL:** docks at inline-start (visual right in Arabic); collapse chevrons mirror.

---

## Tabs

**Anatomy:** tab list · tabs (label + optional count) · active indicator · panels.

**States:** active · inactive · hover · focus · disabled (avoid; explain emptiness inside the panel instead).

**Usage:** peer views of one object (Account: Transactions / Details / Statements). Never for sequential steps (that's Stepper) and never nested two-deep.

**Financial:** counts on tabs reflect filtered results ("Pending (3)"); tab state preserved on back-navigation.

**A11y:** tablist pattern, arrow-key navigation, panel labeled by tab.

**RTL:** order and active-indicator animation mirror; horizontal scroll (if overflowing) starts from inline-start.

---

## Segmented Control

**Anatomy:** 2–4 segments, equal width, single selection.

**Usage:** view toggles within one dataset (AED / USD display; List / Chart; Monthly / Yearly). Not for navigation, not for actions.

**States:** selected · unselected · focus · disabled.

**A11y/RTL:** radiogroup semantics; order mirrors; selection thumb animation mirrors.

---

## Breadcrumb (desktop, deep hierarchies)

**Anatomy:** links + separator chevron · current page (non-link).

**Usage:** SME/corporate/back-office depth ("Payments › Bulk payments › July payroll › Payment 41 of 60"). Consumer mobile never shows breadcrumbs.

**A11y:** nav landmark "Breadcrumb"; current page marked.

**RTL:** chevrons mirror; order mirrors.

---

## Pagination

**Anatomy:** prev/next · page numbers or range readout ("41–60 of 214") · optional page-size select.

**Usage:** desktop tables. Mobile lists use progressive loading with an explicit "Load more" (auto-infinite scroll is banned on transaction lists — it breaks "find the receipt from March" tasks and footer reachability).

**Financial:** table pagination preserves filters/sort in URL/state; exports respect the *filtered* set, stated ("Export 214 filtered transactions").

**A11y:** current page announced; range readout is live text.

**RTL:** prev/next mirror.

---

## Stepper (Progress)

**Anatomy:** steps (number/check + label) · connectors · current highlight; horizontal (≤4 visible steps) or compact "Step 2 of 4" text form (mobile default).

**States per step:** complete (check) · current · upcoming · blocked (with reason) · error (needs revisit).

**Usage:** every multi-step financial journey ≥3 steps shows position; steps are nouns ("Amount", "Review") not verbs; completed steps are tappable to revisit **before** AUTHENTICATION, locked after.

**A11y:** list semantics with state per step ("Step 2 of 4, Amount, current step").

**RTL:** flows inline — visual right-to-left in Arabic; connector/animation mirror; checkmarks unmirrored.

---

## Language Switcher

**Anatomy:** globe icon + current language label ("العربية" shown *in Arabic* when the UI is English, and "English" *in English* when the UI is Arabic — each language named in itself, always).

**Usage:** available pre-login and in Profile; switching swaps language *and* direction live, preserving screen position and any draft state; never resets a flow.

**A11y:** announces the switch; `lang` attributes update so screen readers change voice.

---

## Session Bar (security navigation)

**Anatomy:** timeout countdown region (appears at T-60s: "You'll be signed out in 0:59 — Stay signed in") · sign-out control · last-login note on Home ("Last sign-in: yesterday 21:14, Dubai").

**States:** hidden · warning · expired (route to the Session Expired page, doc 25, preserving safe drafts).

**A11y:** countdown is a polite live region; "Stay signed in" is keyboard-first reachable; expiry never silently discards a payment draft (restored after re-auth with explicit confirmation).
