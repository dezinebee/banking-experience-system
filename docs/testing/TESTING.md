# BES Verification Program

Two layers of verification, honestly separated:

| Layer | Who runs it | Status |
|---|---|---|
| **Automated** — contrast math over the token contract; static HTML accessibility checks | `tools/audit-contrast.py`, `tools/audit-a11y.py` — re-run on every change, reports in `docs/audits/` | ✅ Running, passing |
| **Human protocols** — screen readers, Arabic native review, usability | The three protocols in this folder, each executable as written | ⏳ Awaiting testers |

The automated layer proves the *contract* (tokens, markup structure). The human layer proves the *experience*. A release is not "verified" until both columns are green — the status registry (`../../STATUS.md`) tracks this per component.

## The three protocols

1. **[screen-reader-protocol.md](screen-reader-protocol.md)** — a scripted pass over the component gallery and remittance journey with VoiceOver (macOS/iOS) and NVDA (Windows). ~45 minutes per reader. No accessibility expertise required to run; expected announcements are written out.
2. **[arabic-rtl-review.md](arabic-rtl-review.md)** — a structured checklist for a native Arabic speaker reviewing the RTL rendering as a *design*, not a translation. ~40 minutes.
3. **[usability-test-remittance.md](usability-test-remittance.md)** — a moderated test plan for the remittance journey (`journey-remittance.html`): 5 participants, 4 tasks, defined metrics. ~30 minutes per session.

## Recording results

Copy the relevant protocol, fill the result column per item, and save as
`docs/testing/results/YYYY-MM-DD-<protocol>-<initials>.md`. Open one issue per failure using the bug template, tagged `verification`. When a protocol passes with no open failures, update STATUS.md.

## Recruiting notes (UAE context)

- Screen reader pass: at minimum one VoiceOver + one NVDA session; ideally include a daily screen-reader user via an accessibility organization or People of Determination network.
- Arabic review: a native speaker who *reads Arabic interfaces daily* (banking app user), not just any Arabic speaker; Gulf dialect familiarity preferred for tone judgment, though the UI register is Modern Standard Arabic.
- Usability: recruit across the persona range — at least one participant matching the remittance-sender profile (monthly sender to India/Pakistan/Philippines) and one lower-digital-literacy participant. Sessions can run in English, Hindi/Urdu, or Arabic; the tasks are language-neutral.
