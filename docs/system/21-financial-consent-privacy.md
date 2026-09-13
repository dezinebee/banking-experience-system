# 21 — Financial Components: Consent, Privacy & Open Finance Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Consent doctrine (doc 07 §5): every permission is purpose-bound, time-bound, dashboard-listed, and revocable in ≤2 taps from that dashboard. A permission without a visible expiry is a design defect. Open Finance consent screens follow the centralized national consent format where mandated — the system renders the standard faithfully rather than inventing competing layouts.

Components: Consent Request · Data Cluster List · TPP Identity Card · Consent Summary · Consent Dashboard · Consent Card · Revocation Flow · Expiry & Renewal · Connected Institution Card · Payment Initiation Consent · Privacy Center · Data Request Tracker · Marketing Preferences · Just-in-Time Notice · Cookie/Tracking Consent.

---

## Consent Request (Open Finance / data sharing)

**Purpose:** the screen where a user grants a third party access to their financial data.

**Anatomy (fixed order):**
1. **TPP Identity Card** (who is asking — see below)
2. **Data Cluster List** (what they get)
3. Purpose statement ("Purpose: personal financial management")
4. Duration ("Access until: 30 September 2026" — absolute date, not "12 months")
5. Frequency/scope note where applicable ("They can refresh this data up to 4× per day")
6. Revocation promise ("Stop this anytime in Settings → Data sharing")
7. Actions: **[Allow access]** (primary) · **[Cancel]** (equal visual weight — consent screens never bias with a ghosted decline)

**Example:**
```
ABC Finance wants to access:
✓ Account information
✓ Balance
✓ Transaction history (last 12 months)

Purpose: Personal financial management
Access until: 30 September 2026
You can stop this anytime in Settings → Data sharing.

[Allow access]   [Cancel]
```

**States:** requesting · authenticating (step-up always required at grant) · granted (confirmation + where-to-manage) · declined ("Nothing was shared") · errored (nothing-shared assurance).

**Rules:** no pre-expanded bundles beyond the request; no "select all" defaults; partial grant supported where the standard allows (deselect clusters — the TPP sees a partial-grant result honestly).

**A11y:** clusters as a real list; Allow/Cancel equal reachability; the duration is part of the Allow button's described context.

**RTL:** full mirror; dates per locale; TPP names bilingual where registered.

---

## Data Cluster List

**Anatomy:** cluster rows: icon · plain name ("Transaction history") · expandable plain-language detail ("Merchant names, amounts and dates of your transactions — not your card numbers or passwords") · sensitive clusters flagged distinctly.

**Rule:** technical scope names never surface ("ReadAccountsDetail" → "Account information"); the *not-included* reassurance line is part of the pattern.

---

## TPP Identity Card

**Anatomy:** provider logo + registered name · **verified-participant badge** (sourced from the national directory — "Licensed provider · verified today") · regulator reference · "What is this company?" link (directory profile).

**States:** verified · unverified (**hard stop** — an unverified party's request never renders an Allow button; the screen becomes a warning) · suspended (historic consents flagged: "This provider's license was suspended — access has been paused").

---

## Consent Summary (post-grant confirmation)

Compact receipt of what was granted: clusters, purpose, expiry, manage-path. Delivered as screen + notification ("You gave ABC Finance access to your account information — manage in Settings").

---

## Consent Dashboard

**Purpose:** the single place a user sees and controls everything they've shared.

**Anatomy:** active consents (Consent Cards, soonest-expiry first) · expired/revoked history (collapsed) · per-card: provider, clusters (summary), granted date, **expiry countdown** ("Expires in 12 days") · empty state ("You're not sharing your data with anyone").

**Location rule:** reachable in ≤2 taps from settings and linked from every consent-related notification.

## Consent Card

Provider + scope summary + expiry + [View details] + **[Stop sharing]** (always visible, never buried in a menu).

**States:** active · expiring-soon (≤14 days: amber + renewal note) · expired · revoked · provider-suspended.

---

## Revocation Flow

**Anatomy:** one tap [Stop sharing] → consequence-honest confirm ("ABC Finance will lose access immediately. Your existing data with them isn't deleted — contact them for deletion.") → revoked confirmation + notification.

**Rules:** no retention friction (no "are you sure" chains, no guilt copy, no exit surveys before the act); revocation works even when the TPP is unreachable; the deletion-vs-access distinction is stated plainly (honesty about what revocation does and doesn't do).

---

## Expiry & Renewal

**Anatomy:** expiry notification at T-14/T-3 ("Your sharing with ABC Finance ends 30 Sep — renew or let it end") · renewal = full fresh Consent Request (never auto-renew, never one-tap re-grant without re-showing scope) · lapsed = quiet end + confirmation notice.

---

## Connected Institution Card (aggregation view — user's other banks in this app)

**Anatomy:** institution logo + name · linked accounts summary · data freshness ("Updated 14:32" / "Delayed — last updated yesterday") · connection health (healthy · needs-reauthentication ("Reconnect to keep seeing this account") · broken) · manage/unlink.

**Rule:** aggregated (external) balances are visually distinguished from the home institution's *actionable* balances — a stale external number must never read as spendable money; totals that mix home + external state it ("Total across 3 banks — includes external accounts updated today").

---

## Payment Initiation Consent

**Purpose:** a third party initiating a payment *from* the user's account.

**Anatomy:** TPP Identity Card · payment specifics rendered with the standard Payment Summary (payee, amount full-precision, date) — single vs recurring vs variable-recurring made explicit: variable mandates show **maximum per period** ("Up to AED 500.00 per month") · duration/expiry · then the normal review + step-up authentication contract.

**Rule:** a variable recurring authorization without a stated cap does not render — the cap is structurally required.

---

## Privacy Center

**Anatomy:** sections: what-we-hold (plain-language categories) · **your rights** actions: download my data (Data Request Tracker) · correct my data (routes: verified fields → re-verification; others → edit) · delete (scope honesty: "We must keep transaction records for N years by law — here's what deletion covers") · objection/automated-decisions info · policy documents (layered: summary first, full PDF second) · cross-border note where applicable.

**A11y/RTL:** fully bilingual; legal documents accessible PDFs.

---

## Data Request Tracker

Request rows (type, date, status: received → preparing → ready (download, expiring link) → completed) with SLA honesty ("Usually within 30 days"). Requests generate confirmations; identity re-verification precedes sensitive exports.

---

## Marketing Preferences

**Anatomy:** channel × category matrix (push/email/SMS × offers/product news/insights) · granular toggles (never one master-only) · master off-switch as well ("Stop all marketing") · service-message note ("You'll always receive security and transaction messages — they keep your account safe and can't be turned off") · effective-immediately confirmation.

**Rules:** marketing consent is opt-in at onboarding (unchecked); the marketing/service boundary is the notification-category taxonomy (doc 27) — fraud, security and transaction messages are never suppressible via this surface and never carry marketing content piggybacked.

---

## Just-in-Time Notice

**Anatomy:** inline one-liner at the point of collection ("We use your location to find nearby ATMs — it isn't stored") + "More" link into the relevant Privacy Center section.

**Rule:** any new data collection point ships with its notice; a permission dialog (OS-level) is always preceded by the in-context why.

---

## Cookie / Tracking Consent (web surfaces)

**Anatomy:** neutral banner: plain statement · [Accept all] · [Reject non-essential] (equal weight) · [Choose] (granular categories with purposes) · settings re-entry point persistent in footer.

**Rules:** no dark patterns (equal buttons, no color-biasing the accept, no repeat-nagging after rejection); essential-only operation is fully functional for banking tasks.
