# 17 — Financial Components: Cards Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Components: Card Art · Card Overview · Card Controls Panel · Freeze Control · Spending Limit Control · Channel Controls · PIN Management · Card Details Reveal · Replacement Flow entry · Card Transaction Item · Dispute entry · Travel Notice · Card Carousel.

---

## Card Art

**Purpose:** visual representation of a physical/virtual card.

**Anatomy:** brand card face (theme slot) · scheme mark(s) — **co-badged domestic+international schemes render both marks per scheme brand rules, never mirrored, never recolored** · masked PAN (•••• 4521) · cardholder name · virtual badge where applicable · frozen overlay state (frost treatment + "Frozen" label).

**Variants:** physical · virtual (distinct visual marker — users must never confuse which number they're sharing) · single-use virtual (countdown/remaining-uses) · supplementary (holder name highlighted).

**States:** active · frozen (visual + label, reversible affordance adjacent) · blocked (bank-initiated: distinct from frozen, with reason class + support) · expired (renewal state) · in-production ("Arriving in 3–5 days" + activate CTA when delivered) · closed.

**A11y:** decorative face; state carried by adjacent text ("Debit card ending 4521, frozen").

---

## Card Overview

**Purpose:** one card's home.

**Anatomy:** Card Art · status line · quick controls row (Freeze · Details · PIN · Settings) · spending summary (this month vs limit, Limit Indicator) · recent transactions (Transaction Items scoped to card) · linked account line.

**States:** inherits card states; every non-active state shows its recovery path here.

---

## Card Controls Panel

**Purpose:** all security/spend controls in one place, honest about what each does.

**Anatomy:** grouped Switches with per-control explanation:
- **Channels:** online payments · contactless · ATM withdrawals · international usage (geo-scope selector: "Everywhere / UAE + chosen countries")
- **Limits:** per-transaction cap · daily spend cap (Currency Inputs with policy bounds shown)
- **Merchant categories** (optional tier): gambling-block etc., with regulatory notes where locks apply (some blocks carry cooling-off periods before they can be disabled — stated at the moment of enabling: "If you turn this off later, it takes effect after 72 hours").

**States per control:** on · off · pending (async, doc 09 Switch) · locked-by-policy (with why) · locked-by-parent (supplementary cards: "Set by the primary cardholder").

**Security:** loosening controls (enabling international, raising limits) may require step-up auth; tightening never does — **safety is always one tap, risk requires proof.**

---

## Freeze Control

**Purpose:** instant reversible kill-switch.

**Anatomy:** prominent switch/button ("Freeze card") · effect summary ("Blocks new payments, ATM and online. Recurring payments you've approved may still go through — review them.") · unfreeze mirror.

**States:** active → freezing (pending) → frozen (confirmation + what still works) → unfreezing.

**Rules:** freeze requires **no** step-up (panic action); freeze is not loss-reporting — the panel links "Lost or stolen? Report it" into the replacement flow with card-block semantics explained (freeze = reversible; report = permanent block + replacement).

---

## Spending Limit Control

Currency Input + policy bounds + effect preview ("New daily limit: AED 3,000.00 — resets midnight"). Rises above bank thresholds require step-up + may carry cooling-in delay (stated). Lowering is instant.

---

## PIN Management

**Anatomy:** view-PIN (step-up auth → time-limited masked reveal with auto-hide, screenshot-blocked surface) · change-PIN (PIN Entry ×2 with weak-PIN rejection: sequences, birth year, repeats) · wrong-PIN counter state ("2 attempts left at ATMs — unblocks after successful app verification").

**A11y:** reveal announces countdown; keypad accessible; no haptic-only.

---

## Card Details Reveal (virtual card usage)

**Anatomy:** step-up auth → PAN/expiry/CVV revealed with per-field copy buttons · auto-mask after 60s · "who are you sharing this with" caution line for single-use cards.

**Security:** clipboard auto-clears after 90s where platform allows (stated); reveal events are notification-logged.

---

## Replacement Flow (entry component)

**Anatomy:** reason picker (lost / stolen / damaged / never-arrived) — reason drives consequence copy: lost/stolen = immediate permanent block + "your current card stops working now"; damaged = old card works until activation · delivery address confirmation (masked, change path re-verifies) · fee line where applicable · virtual-card-continuity note ("Your card number changes; update saved subscriptions — here are merchants that charged this card recently" → list).

**States:** reported → blocked → replacement-ordered → shipped → delivered → activated.

---

## Card Transaction Item

Transaction Item specialization: adds card ••suffix, channel icon (online/contactless/ATM), FX pair for foreign spend (Amount Pair), decline reason class on declined rows ("Declined — over daily limit" with the fix path: "Raise limit").

---

## Dispute Entry ("Report a problem")

**Anatomy:** launched from Transaction Detail · triage question set ("I don't recognize this" / "Charged twice" / "Wrong amount" / "Item not received" / "Subscription I cancelled") · route: recognition issues → fraud path (immediate freeze offer + secure contact); merchant issues → dispute case with evidence upload (File Upload) · expectation setting ("Provisional credit within X days where eligible; investigations take up to 90 days") · case tracker (Timeline: submitted → under review → resolved with outcome).

**Rules:** the fraud fork acts *first*, asks questions second; dispute status changes are notification events; outcomes state the money movement explicitly ("AED 89.50 returned to your account today").

---

## Travel Notice

Largely obsolete with smart authorization, but retained for institutions requiring it: date range + destinations → confirmation of coverage; the component self-documents when a bank should *not* deploy it.

---

## Card Carousel

Multi-card navigation: swipeable Card Art stack with dots, active card drives the overview beneath; order user-arrangeable; RTL swipe direction mirrors; a11y: cards as tabs with full names ("Card 2 of 3, virtual card ending 8834").
