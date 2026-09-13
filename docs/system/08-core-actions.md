# 08 — Core Components: Actions

**Banking Experience System (BES)** · Core Components · v2.0.0-draft

Components: Button · Icon Button · Link · Menu (Action Menu / Overflow) · Button Group.

Shared documentation contract (applies to every component in docs 08–21): anatomy, variants, states, usage, financial considerations, accessibility, Arabic/RTL, responsive, content — with realistic AED examples. States marked ✦ are financial-specific extensions.

---

## Button

**Purpose:** trigger an action. In banking, the primary button often moves money — it carries more responsibility than a generic CTA.

**Anatomy:** container · label (required) · leading/trailing icon (optional) · loading spinner slot · badge slot (rare, e.g. approvals count).

**Variants:**
- `primary` — one per screen region; the main action ("Send AED 5,000.00")
- `secondary` — bordered, neutral
- `tertiary/ghost` — low-emphasis, text-only with padding
- `destructive` — `action.destructive`; irreversible or negative actions ("Cancel transfer", "Remove beneficiary")
- Sizes: `lg` (56px — money-moving CTAs, mobile bottom-anchored) · `md` (48px default) · `sm` (36px — dense/inline; desktop tables)

**States:** default · hover · focus (2px ring, 2px offset) · pressed · disabled · loading (spinner replaces label? **No** — spinner + label persists: "Sending…" so context survives) · success beat (transient check for in-place completions) ✦ requires-authentication (lock glyph — pressing routes to step-up).

**Usage:** one primary per region; the primary label names the consequence, not the mechanism — "Send AED 5,000.00", "Confirm payment of AED 10,035.00", never bare "Submit"/"OK"/"Confirm" on money-moving steps. Don't disable the primary to signal invalid forms (blocks discovery of *why*); validate on activation and surface the error summary instead. Exception: structurally impossible actions (no account selected) may disable with adjacent explanation.

**Financial:** amount-bearing labels re-render live if the amount changes upstream; destructive + primary never stacked adjacent without `space.16`; double-tap protection (idempotency debounce) is built into loading state — a second tap while loading is a no-op.

**Accessibility:** target ≥ 44×44; label read as accessible name (icon-only forbidden for Button — that's Icon Button); loading announces politely ("Sending your transfer"); disabled buttons remain focusable with description of why (aria-disabled pattern) in forms context.

**RTL:** leading icon flips to inline-start; chevrons mirror; amount inside the label stays an LTR isolated run: زر: "إرسال AED 5,000.00".

**Responsive:** mobile money-flows use a bottom-anchored full-width `lg` primary above the home indicator, always visible (not below the fold of a scrolling form).

**Content:** verb-first, sentence case (Latin), no exclamation marks. AR labels verb-first equivalently. Pair Yes/No decisions as explicit outcomes: "Yes, it was me" / "No, secure my account".

---

## Icon Button

**Purpose:** compact action where the glyph is universally learned (close, search, more, copy, eye/mask-toggle).

**Anatomy:** container (transparent/subtle/bordered) · icon · required accessible name · optional tooltip (desktop).

**States:** default · hover · focus · pressed · disabled · **toggled** (filled icon variant, e.g. balance-mask eye) · loading.

**Usage:** only for learned glyphs; anything ambiguous gets a labeled Button. The copy-IBAN icon button announces "Copy IBAN" and confirms with toast "IBAN copied".

**Financial:** the **mask/reveal balance** icon button is a standard instance: toggling announces state to screen readers ("Balance hidden" / "Balance shown"), persists per user preference.

**A11y/RTL:** ≥44×44 target; mirrored per icon policy (doc 04 §3); tooltip appears on focus, not only hover.

---

## Link

**Purpose:** navigation or reference — never a money-moving action. "View Key Facts Statement", "Why am I being charged?", "Terms and conditions".

**Anatomy:** text · optional external-icon (opens outside app — mandatory marker) · optional download icon (PDF).

**Variants:** inline (underlined, `text.link`) · standalone (with chevron) · subtle (footers).

**States:** default · hover · focus · visited (content sites only; app suppresses) · disabled (avoid — hide instead).

**Usage:** links navigate; buttons act. A "link-styled" trigger that mutates state is banned — this distinction matters under screen readers, where role announces expectation.

**Financial:** disclosure links (KFS, terms, fee schedules) always state format and destination: "Key Facts Statement (PDF)". Legal links never open irreversibly modal-blocking flows.

**RTL:** chevrons mirror; external-link glyph does not; underline offset per Arabic metric (doc 02 §2).

---

## Menu (Action Menu / Overflow)

**Purpose:** secondary actions on an object (transaction row → "Download receipt / Report a problem / Repeat transfer").

**Anatomy:** trigger (icon button "⋯" or labeled) · surface (`elevation.2`) · items (icon + label) · optional destructive group separated at the end · optional section headers.

**States:** closed · open · item hover/focus/pressed · item disabled (with reason on focus).

**Usage:** max ~7 items; destructive items last, separated; never hide the *only* path to a critical action in an overflow (receipts, disputes must also exist on the detail screen).

**A11y:** full keyboard support (arrows, Home/End, Esc, typeahead); focus returns to trigger on close; items are real buttons/links with roles.

**RTL:** aligns to the trigger's inline-end; opens toward available space; item icons at inline-start.

---

## Button Group / Split Actions

**Purpose:** tightly related alternatives ("Approve" + "Reject" in approval rows; "Pay full amount" ▾ split with "Pay minimum").

**States:** as Button per segment; group manages single-primary rule.

**Financial:** approve/reject pairs use fixed order — affirmative at inline-start in both directions (order follows reading direction, so it mirrors); colors: approve = primary, reject = secondary-destructive (bordered red, filled red reserved for confirm step). Split buttons on payment amounts always show the *selected* amount on the main segment.

**A11y:** group labeled ("Approval actions for payment AED 250,000.00 to Gulf Star Trading"); each segment individually focusable.
