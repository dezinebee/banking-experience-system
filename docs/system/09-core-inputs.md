# 09 — Core Components: Inputs & Forms

**Banking Experience System (BES)** · Core Components · v2.0.0-draft

Components: Text Input · Currency Input · Search · Select · Combobox · Date Picker · Date Range Picker · Checkbox · Radio Group · Switch · PIN Entry · Code Entry · File Upload · Character Count · Form primitives (Label, Help text, Error message, Fieldset).

**Form doctrine (applies to all):** prevent errors before validating (accept all reasonable formats, strip stray characters); validate on submit by default — inline on-blur validation permitted only for high-confidence format fields (IBAN, card number, Emirates ID, email); on error, preserve input, show an error summary at the top with focus moved to it, prefix page title with "Error:", and pair inline messages per field. Server-side validation always; never use validation to gate eligibility (route instead). "Required" is stated in words on the minority class — if most fields are required, mark only the optional ones ("(optional)").

---

## Text Input

**Anatomy:** label (always visible, above field — never placeholder-as-label) · field · optional prefix/suffix slots · help text · error message (icon + text, `border.error`) · optional character count.

**States:** default · hover · focus · filled · disabled · read-only (visually distinct from disabled; used for verified prefilled data) · error · ✦ verified (check + source note: "From UAE PASS") · ✦ masked (sensitive entries).

**Usage:** one thing per field; forgiving inputs (trim, collapse spaces); `inputmode`/`autocomplete` set per data type; paste never blocked — **especially** on IBANs, card numbers and passwords.

**Financial instances:** IBAN input (LTR always, even in RTL forms; groups display as `AE07 0331 2345 6789 0123 456`; strips spaces/hyphens on paste; validates checksum on blur with specific message: "This IBAN doesn't look right — UAE IBANs have 23 characters starting with AE"); reference/purpose field (character count, disallowed-character stripping for payment rails).

**A11y:** programmatic label association; error text linked via description; error icon not color-only; 16px+ font (prevents mobile zoom-jump).

**RTL:** label/help right-aligned; the field itself may hold an LTR run (IBAN, email) with `dir="ltr"` embedding and start-anchored caret behavior documented; prefix/suffix flip logically (a currency suffix in Arabic appears at the visual left).

---

## Currency Input

**Purpose:** the most consequential input in the system — amount entry.

**Anatomy:** label · currency indicator (fixed code or currency selector) · amount field (`type.amount.lg`, tnum) · optional quick-amount chips (AED 100 / 500 / 1,000 / Max) · context line (available balance and/or remaining preview) · help/error.

**Behavior:** locale-aware live grouping (10,000); precision clamp per `currency.precision`; forgiving paste ("AED 1,250.50" → 1250.50, "٥٬٠٠٠٫٥٠" → 5000.50); no spinner arrows; Backspace works on groups naturally; Eastern/Western digit entry both accepted, normalized (doc 07 §6). Paste is forgiving about *form*, never about *meaning*: input that could be read two ways ("1.234,56") is rejected rather than guessed, because a silently wrong amount is worse than a rejected one. An empty or half-typed field is **incomplete, not in error** — it carries no `aria-invalid`.

**States:** default · focus · error (over limit, over balance, below minimum — each with specific copy and the offending constraint shown: "The maximum for instant transfers is AED 50,000.00") · ✦ balance-exceeded (shows shortfall: "AED 1,200.00 more than your available balance") · disabled.

**Financial:** "Max" chip uses `balance.available` minus known fees, stated ("Max sends AED 24,985.00 after fees"); remaining-balance preview updates live: "Leaves AED 1,250.00". For FX flows, paired dual fields (you send / they get) with last-edited field as source of truth and the other marked ≈.

**A11y:** announces formatted value on blur ("Amount: 5,000 dirhams"); quick chips are buttons with full labels; error messages reference limits numerically. The context line is **structurally bound** to the field — it carries an `id`, the field references it via `aria-describedby`, and it is a polite live region — so `aria-invalid` is never set without a reachable reason (WCAG 3.3.1, 4.1.3). Setting a validation message without that binding is a build defect, not a content gap: the field goes invalid and the user is never told why.

**RTL:** amount remains LTR isolated run; currency indicator at logical start (visual right in Arabic); chips mirror order.

---

## Search

**Anatomy:** input with search icon · clear button (when filled) · optional scope selector · results behavior defined by consuming pattern.

**States:** default · focus · filled · loading (inline spinner) · no-results (with recovery: "No transactions matching 'Careem'. Try a shorter word or filter by date.").

**Financial:** transaction search matches merchant, amount ("89.50"), reference, and normalized Arabic/Latin merchant names; recent searches stored locally, excluded for shared/kiosk surfaces.

**RTL/A11y:** icon at inline-start; clear button ≥44px; results count announced.

---

## Select

**Anatomy:** label · trigger (value + chevron) · listbox surface · options (text + optional icon/description).

**States:** default · open · focus · disabled · error · option selected/disabled.

**Usage:** ≤ ~12 known options (account pickers, statement periods); more → Combobox. Never for binary choices (use Radio/Switch).

**Financial instance — Account Selector** is a specialized Select (doc 14) showing name, masked number, available balance per option.

**A11y:** native select on mobile web where feasible; otherwise full listbox keyboard pattern; selected option announced with its description ("Current account ••4521 — AED 25,000.00 available").

**RTL:** chevron mirrors; option icons inline-start.

---

## Combobox

**Purpose:** filterable long lists — beneficiary picker, bank picker (200+ institutions), country/currency picker.

**Anatomy:** input + listbox with type-ahead filtering · optional grouped sections (Recent / All) · empty state with add-new path ("No beneficiary found — Add new beneficiary").

**States:** as Select + filtering · loading async options.

**Financial:** bank picker matches English and Arabic names and SWIFT codes; country picker for remittance shows corridor availability and delivery methods inline.

**A11y:** combobox pattern with live results count ("6 banks found"); selection persists on blur; no keyboard traps.

---

## Date Picker / Date Range Picker

**Anatomy:** labeled input (typed entry always allowed — "31/08/2026") · calendar surface · month/year navigation · today marker · range: start/end fields + span highlight.

**States:** default · open · focus · error (invalid, out-of-window: "Statements are available for the last 7 years") · disabled dates (with reason on focus: settlement holidays).

**Usage:** memorable dates (DOB, expiry) use segmented fields (DD/MM/YYYY), never a calendar. Ranges offer presets first: This month · Last month · Last 90 days · Custom.

**Financial:** scheduled transfers block non-processing days with explanation ("Transfers don't process on Sunday. We'll send it Monday 1 Sep."); future-dating shows the effective debit date. Hijri display: secondary line where enabled ("1 Muharram 1449"), Gregorian remains canonical for processing.

**A11y:** full keyboard grid navigation; typed entry as first-class path; announced format hint.

**RTL:** calendar grid mirrors (week start per locale — Sat/Sun/Mon configurable, UAE default Monday); numerals per locale policy; chevrons mirror.

---

## Checkbox

**Anatomy:** box · label (tappable as one target) · optional description · optional indeterminate (bulk tables only).

**States:** unchecked · checked · indeterminate · focus · disabled · error.

**Usage:** independent opt-ins and multi-select. **Consent rules:** one checkbox per consent — never bundled ("I agree to terms *and* marketing" is banned); never pre-ticked; consent checkboxes carry the purpose inline, not only behind a link.

**A11y:** native input semantics; error at group level for "you must accept" cases with a specific message ("You need to accept the Key Facts Statement to continue").

**RTL:** box at inline-start (visual right in Arabic); check glyph unmirrored.

---

## Radio Group

**Anatomy:** group label (fieldset/legend) · options (radio + label + optional description + optional trailing content like a fee).

**States:** as checkbox minus indeterminate; exactly-one-selected model, no deselection.

**Financial instance — option cards:** payout method selection renders radios as cards with fee/time metadata ("Bank transfer — fee AED 15.00, within 1 hour" / "Cash pickup — fee AED 20.00, minutes"). Selection re-renders the FX block with change highlight.

**A11y:** arrow-key navigation within group; group label announced first; metadata part of the option's accessible description.

---

## Switch

**Purpose:** immediate-effect binary settings (card freeze, international payments on/off, balance privacy).

**Anatomy:** track+thumb · label · state word ("On"/"Off") adjacent — color alone never carries state.

**States:** on · off · focus · disabled · **pending** (async settings show an in-flight state; the switch does not lie by flipping before the backend confirms).

**Usage:** never inside forms that submit (use Checkbox); never for choices needing confirmation — freezing a card may flip instantly, but *unfreezing* into higher risk may route through confirmation (pattern decides).

**A11y:** switch role with state announced; pending announced ("Turning off international payments…").

**RTL:** thumb rests at inline-start when off; motion mirrors.

---

## PIN Entry

**Purpose:** local secrets — card PIN set/change, app PIN.

**Anatomy:** masked digit cells (4–6) · system or custom keypad · **paste allowed** (WCAG 2.2 §3.3.8 Accessible Authentication — password managers must work; velocity/fraud controls belong server-side) · shuffled-keypad option (high-security surfaces) · attempt counter messaging.

**States:** empty · filling · error (with remaining attempts: "Incorrect PIN. 2 attempts remaining.") · locked (with recovery path and support link — never a dead end).

**A11y:** cells announced as "PIN digit 1 of 4, filled"; timeout generous; no haptic-only feedback. Screen-capture blocked on this surface.

**RTL:** digits LTR always; cells fill left-to-right in both directions (numeric convention), documented so testers don't file it as a bug.

---

## Code Entry (one-time codes)

**Purpose:** verification codes from email/authenticator/push contexts. **Note:** SMS OTP is deprecated as an authentication method (sunset 31 Mar 2026 per regulator); this component ships for residual non-auth verifications and legacy migration only, and carries the deprecation notice in its doc.

**Anatomy:** 6 cells with auto-advance · paste-from-clipboard supported (unlike PIN) · resend with countdown · "didn't get it?" recovery.

**States:** empty · filling · verifying (spinner, cells locked) · error (specific: expired vs wrong) · resent confirmation.

**A11y:** single input semantically (one field, styled as cells) so screen readers treat it as one code; autocomplete="one-time-code".

---

## File Upload

**Purpose:** KYC documents, dispute evidence, address proof.

**Anatomy:** dropzone/button ("Upload trade license") · accepted formats + max size stated upfront · file rows (name, size, thumbnail for images, remove) · progress per file · camera-capture path on mobile.

**States:** idle · dragging-over · uploading (per-file progress, cancellable) · uploaded · error (too large / wrong format / failed — each with the fix: "Maximum size is 10 MB. Try a photo instead of a scan.") · ✦ verifying (document under review) · ✦ verified / rejected (with reason and re-upload path).

**A11y:** button path is primary (drag is enhancement); progress announced; errors focusable.

**RTL:** file rows mirror; filenames are LTR isolated runs.

---

## Form primitives

- **Label:** always visible, above the field, sentence case; optional-marker "(optional)".
- **Help text:** beneath label, before input; persistent (not tooltip-hidden); used for "why we ask" in KYC ("We're required to verify your address. A utility bill from the last 3 months works.").
- **Error message:** icon + specific text; says what to do, not just what's wrong ("Enter the IBAN without spaces — we'll format it for you" beats "Invalid IBAN").
- **Error summary:** top-of-form list of links to each error; receives focus on failed submit; title "There's a problem".
- **Fieldset/legend:** groups related inputs (address, card details) for screen-reader context.
