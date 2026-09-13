# 20 — Financial Components: Identity & Security Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

Components: National Identity Sign-in · Identity Handoff · Signing Ceremony · Document Capture · Liveness Check · Verified Field · Verification Status · Re-verification Prompt · Auth Prompt set (Biometric / Passkey / Push Approval / PIN) · Device List & Device Card · Trusted Device States · Session Pause Interruption · Security Checkup · Security Event Notice · Warning Tier set.

Security posture: reassure while communicating genuine risk; **safety actions are one tap, risk-increasing actions require proof** (doc 17 rule, generalized). SMS OTP is not an authentication method in this system (deprecated; regulatory sunset) — the auth set below is the canonical ladder.

---

## National Identity Sign-in ("Continue with UAE PASS")

**Anatomy:** official-branded button (brand rules of the national scheme respected verbatim; never restyled) · benefit line for first-timers ("Verifies your identity in minutes — no branch visit") · alternative path link ("Don't have UAE PASS?") · account-level note where the scheme account tier matters ("Requires a verified UAE PASS account" + upgrade interstitial when the user's tier is insufficient).

**States:** default · redirecting · returned-success (auto-continue) · returned-declined (respectful: "You didn't complete verification — nothing was shared" + retry/alternative) · timeout (safe return, state preserved) · identity-mismatch (the returned identity ≠ the applying identity: hard stop + support path — never silent merge).

---

## Identity Handoff (app-switch pattern)

**Anatomy:** pre-handoff interstitial ("You're being taken to UAE PASS to approve. We'll bring you back here.") · state preservation token · return handler (success/decline/timeout routes) · app-not-installed fallback (store link + web path + preserved state).

**Rule:** every external handoff — identity, third-party consent, wallet provisioning — uses this one pattern; the user always knows *why they're leaving* and *what returns them*.

---

## Signing Ceremony

**Purpose:** legally significant signatures (contracts, mandates).

**Anatomy:** document review surface (full document, accessible PDF, in-place — not a link the user can skip) · scroll-acknowledgment (bottom-reached before sign enables; time-based skip prevention off — reading isn't enforced, opportunity is) · key-terms recap card above the sign action (amount, term, rate, cooling-off) · sign action → Identity Handoff (digital signature) · signed confirmation (timestamped receipt + document copy delivered to the user's documents + email) · cooling-off notice with live cancellation entry.

**A11y:** document is real text (screen-reader readable); recap card is a summary landmark.

---

## Document Capture

**Anatomy:** document-type framing guide (EID front/back, passport MRZ) · live edge-detection frame · capture → review ("Readable? Glare?") → retake path · auto-extract preview (OCR fields shown for confirmation, editable where wrong: "Check your name matches your Emirates ID") · upload progress.

**States:** capturing · reviewing · extracting · confirmed · rejected-quality (specific: "Glare over the ID number — try tilting away from light") · rejected-mismatch (data conflicts with existing profile: routed to support, not a loop).

**Failure-loop guard:** after 3 quality rejections the component *changes strategy* (offers upload-from-files, alternative document, or human review) — repeated identical retries are a design defect (a known market failure this system explicitly designs against).

---

## Liveness Check

**Anatomy:** camera prompt with purpose ("A quick selfie confirms it's really you") · action instructions (accessible alternatives to motion gestures where available; audio guidance) · progress · result.

**States:** instructing · checking · passed · failed (specific, respectful: "We couldn't confirm — remove sunglasses and try brighter light") · escalated (after retries → alternative verification path).

**A11y:** never the *only* possible verification (accessible-authentication requirement); instructions not color/motion-only; extra time honored.

---

## Verified Field

**Purpose:** render identity data sourced from verified systems.

**Anatomy:** read-only field styling (distinct from disabled) · value · source note ("From your Emirates ID") · verified check · change path where legitimate ("Name changed? Update your Emirates ID first, then re-verify here").

**Rule:** verified data is never silently editable — corrections route through re-verification, and the *why* is stated.

---

## Verification Status

**Vocabulary (doc 07 §5):** unverified · pending · verified (with what+when: "Identity verified · 12 Mar 2026") · failed (with reason class + retry) · expired (→ Re-verification Prompt).

Rendered as Status Badge + explainer; appears on profile, payees, devices, documents.

---

## Re-verification Prompt (re-KYC)

**Anatomy:** advance notice ladder (T-30/T-14/T-3 days: banner → alert → blocking-at-deadline) · what's needed (usually renewed EID) · deadline + consequence honesty ("After 15 Sep we're required to restrict outgoing payments until you re-verify") · one-tap start (Document Capture) · post-restriction state (money visible, restricted actions labeled with the single fix).

**Tone:** procedural, not accusatory ("Your Emirates ID has expired" — a fact, not a fault).

---

## Auth Prompt Set

Shared contract (doc 16 Authentication Prompt): **context always shown** (what is being authorized), fallback path always present, lockout never a dead end.

- **Biometric Prompt:** platform-native face/fingerprint sheet + BES context header; fallback → device PIN → app PIN ladder.
- **Passkey Prompt:** platform ceremony + "What's a passkey?" first-use explainer; cross-device QR path.
- **Push Approval:** second-device approval card showing *the same context* (amount + payee + merchant) + approve/deny; deny asks "Was this you?" → secure-my-account path.
- **App PIN:** PIN Entry with attempt counter + recovery (re-verify identity, not "contact branch" dead ends).

**States (all):** awaiting · verifying · approved · failed (attempts + alternatives) · locked (recovery path) · unavailable (biometric hardware busy/absent → next rung auto-offered).

---

## Device List & Device Card

**Anatomy (card):** device name + platform icon · first-seen/last-active · location (city-level) · this-device marker · trust state · actions: rename · **sign out** · **remove & block**.

**Trust states:** trusted (established device) · new (first 72h: badge + tightened limits noted) · suspicious (unusual signals: prompted review) · revoked.

**Rules:** removing a device is one tap + confirm (safety action); *adding* trust (new device becoming trusted) is time + successful-auth based, never one-tap. New-device sign-ins always generate a Security Event Notice to all other devices.

---

## Session Pause Interruption (`z.critical`)

**Purpose:** in-session threat response — active call, screen-share/remote-access detection.

**Anatomy:** full-screen takeover, **no entrance animation** · calm headline ("We've paused your session") · specific reason in plain language ("We detected screen sharing. Banking with your screen visible to others isn't safe.") · scam-context education line ("If someone asked you to install an app or share your screen, it may be a scam — hang up.") · actions: end-the-risk-and-resume ("I've stopped sharing — continue") · emergency path ("I think I'm being scammed" → freeze + support) · high-risk payments during active calls get the checkpoint variant: "Are you on a call with someone guiding you through this payment?" [Yes → intervention] / [No, continue].

**Rules:** cannot be dismissed by swipe/tap-outside; screen readers announce assertively; the interruption *never* blames the user.

---

## Security Checkup

**Anatomy:** scored/checklist surface: auth methods active · devices reviewed · payee list reviewed · alerts enabled · scam-awareness moment (rotating single tip, not a wall) · each item one-tap fixable.

**Cadence:** quarterly prompt (dismissible), post-incident mandatory pass.

---

## Security Event Notice

**Purpose:** the notification content pattern for security events (new device, password change, payee added/removed, limit raised, details revealed).

**Anatomy:** what happened + when + where (city) · "Was this you?" fork: yes (dismiss) / **no ("Secure my account")** → guided response: freeze credentials → re-auth → review recent actions → support handoff.

**Rule:** security events are never batched/digested — each is immediate and individually actionable; they use the security notification category (visually + semantically distinct from all marketing, doc 27).

---

## Warning Tier Set (risk-severity rendering)

| Tier | Trigger examples | Form |
|---|---|---|
| `info` | first payment to a saved payee in months | inline Alert |
| `caution` | new payee <24h, CoP close-match | pre-review interstitial card, one acknowledgment |
| `high` | CoP no-match proceed, unusual amount/destination pattern | dedicated interstitial + re-auth + delay option ("Wait 24h — most scams pressure you to act now") |
| `critical` | known-mule destination, active-call + new payee + high value | hard stop: payment refused, education, support; no override in-channel |

Copy discipline: warnings describe the *pattern* ("Scammers often…"), never accuse the recipient; the delay option is framed as strength, not obstruction.
