# Usability Test Plan — Remittance Journey

**Product under test:** `journey-remittance.html` (hosted URL preferred over local file)
**Method:** moderated, think-aloud, in person or video call with screen share
**Participants:** 5 (see recruiting in TESTING.md — include ≥1 regular remittance sender and ≥1 lower-digital-literacy participant)
**Session length:** ~30 min · **Facilitator note:** the page is a demo — no real money; say so upfront, then ask participants to behave as if it were real.

## Research questions

1. Do users understand the **total cost** (fee vs FX margin vs total) before confirming?
2. Does the **name-check** (close match / no match) change behavior — do users pause and verify, or click through?
3. Is the **rate lock + expiry** understood, or does re-quoting feel like a bait-and-switch?
4. Do the **result states** (especially UNKNOWN) leave users calm and correctly informed about where their money is?
5. (Arabic-speaking participants) Does the Arabic journey feel first-class?

## Tasks

Give tasks verbally, one at a time. Don't guide. Note paths, hesitations, and quotes.

**T1 — Send with a saved payee.**
"You want to send AED 10,000 to Priya Kumar, who you've paid before. Go ahead and send it. PIN is any 4 digits."
*Success:* completes without help. *Probe after:* "Before you confirmed — how much was this costing you in fees? How many rupees does Priya get? When does she get them?"

**T2 — Cost comprehension (no UI).**
After T1, hand them paper/chat: "Write down: total you paid, and what part of that was fees."
*Success criterion:* states AED 10,036.75 total and ~AED 36.75 fees (or equivalent understanding). This is the transparency-before-conversion principle, measured.

**T3 — New payee with a name mismatch.**
"Now send AED 2,000 to a new recipient. Their name is **Priya K** — enter exactly that, account number 12345678, IFSC ICIC0001234."
*Watch:* the close-match screen. Do they read it? Choose "Use this name" vs "Check with recipient"? *Probe:* "What was that screen telling you? What would you do in real life?"

**T4 — The uncertain outcome.**
Set demo outcome to **Unknown** (facilitator does this). "Send AED 5,000 to Anil Sharma."
*Probe at the result screen:* "What just happened? Where is your money right now? What do you need to do?"
*Success:* participant says the bank is confirming / money is safe / nothing to do — **fail** if they believe it failed or money is lost.

**T5 (Arabic speakers) — repeat T1 in Arabic** via the العربية toggle. *Probe:* anything that felt translated rather than designed?

## Metrics

| Metric | Target |
|---|---|
| T1 completion without facilitator help | 5/5 |
| T2 cost comprehension | ≥4/5 state total AND fees correctly |
| T3: pauses and engages with name-check (reads/considers, regardless of choice) | ≥4/5 |
| T4: correctly states money-state at UNKNOWN | 5/5 — this one is non-negotiable |
| Post-task confidence "I knew what was happening at every step" (1–7) | median ≥6 |
| SEQ (single ease question) per task (1–7) | median ≥6 |

## Debrief questions

1. "If this were your bank, would you use this instead of your current way of sending money? Why/why not?"
2. "Was anything hidden from you, or did anything appear at the last moment?" (fee-surprise check)
3. "What would you tell the person who designed this to fix first?"

## Outputs

Per session: task results + quotes + SEQ scores → `docs/testing/results/`. Across sessions: findings ranked by frequency × severity; each actionable finding becomes an issue tagged `verification` + `usability`; T4 or T2 failures block the Stable status of the affected patterns in STATUS.md.
