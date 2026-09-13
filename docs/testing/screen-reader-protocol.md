# Screen Reader Test Protocol

**Scope:** component gallery (`components/`) + remittance journey (`journey-remittance.html`)
**Readers:** VoiceOver (Safari, macOS or iOS) and NVDA (Firefox or Chrome, Windows) — one pass each
**Duration:** ~45 min per reader · **Recorder:** save results per TESTING.md

Setup: open the site (hosted URL or local files), screen reader on. For each item: perform the action, compare what you hear against "Expected", mark Pass / Fail / Partial with notes. "Expected" wording is indicative — equivalent phrasing passes; *missing information* fails.

## Part A — Components (components/forms.html, money.html, actions.html)

| # | Action | Expected announcement (gist) | Result |
|---|---|---|---|
| A1 | Tab to the "Send AED 5,000.00" button | "Send AED five thousand dirhams, button" — the amount is read, not spelled digit-by-digit | |
| A2 | Tab to the loading button | Conveys busy/disabled state; not just silence | |
| A3 | Tab into the IBAN field with error | Label "Recipient IBAN", "invalid", and the full error text including what to do | |
| A4 | Tab to currency input, type 30000 | Announces the field label; after typing, the context line change ("more than your available balance") is discoverable | |
| A5 | Tab to the Key Facts checkbox | Checkbox role, unchecked state, full label including "(PDF)" link presence | |
| A6 | Toggle the International payments switch | Switch/checkbox role + on/off state change announced | |
| A7 | Arrow through the Tabs (Transactions/Details/Statements) | Tab role, selected state, panel content reachable; arrows move selection | |
| A8 | Reach the account card balance, then activate the eye button | Balance read as an amount; after masking, "Balance hidden" — the masked value is NOT read as bullets | |
| A9 | Navigate the transaction list | Each row reads counterparty, context, amount with sign, and status badge text | |
| A10 | Open the confirm dialog (actions page) | Dialog role + title announced; focus lands inside; Escape closes; focus returns to trigger | |
| A11 | Trigger a toast ("Show a toast") | Announced politely without stealing focus | |
| A12 | Chart on any page with one (or journey review): find "View as table" | The table equivalent is reachable and reads label/value pairs | |

## Part B — Remittance journey (journey-remittance.html)

| # | Action | Expected | Result |
|---|---|---|---|
| B1 | Load page, browse by headings | "Send money to India" is the h2/main heading; step context present | |
| B2 | Change the amount to 12,000 | Total and recipient-gets updates are discoverable on revisit (values re-read correctly) | |
| B3 | Continue → payee list | Each saved payee reads name, bank, masked account, last-sent info as one coherent item | |
| B4 | Add new payee, enter "Priya K", continue | The name-check result is announced (close-match question) with both action options reachable | |
| B5 | Review screen: read top to bottom | Order: recipient → source → amount → rate + lock status → fees → total → consequence statement → send button with amount | |
| B6 | Let the rate timer run to zero (90s) | Expiry is announced or discoverable; send button becomes disabled; re-quote path reachable | |
| B7 | PIN entry | Each cell announces "PIN digit N"; wrong PIN (0000) error is announced; retry possible | |
| B8 | Result screen (success) | Heading announces the outcome; timeline stages readable in order | |
| B9 | Result screen (set demo outcome to Unknown, resend) | Hears "checking your transfer status" and the money-safety statement — never "failed" | |
| B10 | Receipt | All label/value pairs read as pairs; reference number read in groups, not as one blur | |

## Part C — Arabic pass (either reader with Arabic voice available)

| # | Action | Expected | Result |
|---|---|---|---|
| C1 | Switch the journey to العربية, browse headings | Reader switches to Arabic voice (lang attribute honored); headings read in Arabic | |
| C2 | Review screen in Arabic | Amounts still read as amounts (Latin digits within Arabic speech is acceptable); label/value pairing survives | |
| C3 | Name-check result in Arabic | Arabic announcement complete; action buttons distinguishable | |

## Failure triage

Fail on: missing labels/state, wrong reading order, focus lost, information visible but unreachable, masked values leaking. Partial on: awkward-but-complete phrasing. Log each as an issue tagged `verification` + `a11y` with the item number.
