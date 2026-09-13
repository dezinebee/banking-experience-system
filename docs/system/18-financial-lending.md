# 18 — Financial Components: Lending & Financing Family

**Banking Experience System (BES)** · Financial Components · v2.0.0-draft

One component set serves conventional credit and Islamic financing; the **terminology dimension** (doc 06 §3) resolves vocabulary and the rate components swap per product structure. Underlying behavior is shared — a repayment schedule is a repayment schedule.

Components: Product Summary (Key Facts) · Rate Display (APR) · Profit Rate Display (Islamic) · Shari'ah Structure Explainer · Payment Calculator · Eligibility Check · Application Progress · Offer Presentation · Approval / Rejection · Repayment Schedule · Outstanding Summary · Early Settlement · Payment Holiday · Overdue State.

---

## Product Summary (Key Facts)

**Purpose:** the standardized pre-contract summary — the single most regulated component in the system. Rendered identically in Arabic and English; printable/downloadable as an accessible PDF.

**Anatomy (fixed order):**
1. Product name + type badge (**Fixed / Variable / Hybrid** rate-type is prominent, first-glance)
2. Headline figures: amount · term · rate (Rate Display or Profit Rate Display per structure) · periodic payment · **total you will repay**
3. Fees table (processing, late payment, early settlement — every fee, no "other fees may apply" without enumeration link)
4. Warnings block (non-dismissible): consequences of missed payments, variable-rate risk where applicable
5. Cooling-off notice (the 5-business-day right, plainly stated)
6. Key Facts document link ("Key Facts Statement (PDF)")

**Example:**
```
PERSONAL FINANCING · Fixed rate
Amount                AED 100,000.00
Term                  48 months
Rate                  5.99% per year (reducing)
Monthly payment       AED 2,348.00
Total repayment       AED 112,704.00
Processing fee        AED 1,050.00 (incl. VAT)
Early settlement      1% of remaining balance, max AED 10,000
⚠ Missing payments can affect your credit record and future borrowing.
You can cancel within 5 business days of signing.
[Key Facts Statement (PDF)]
```

**States:** draft-quote (≈, inputs editable) · firm-offer (locked figures + validity: "This offer is valid until 6 Sep 2026") · contracted (immutable record).

**A11y:** definition-list semantics; the warnings block is a landmark; PDF tagged.

**RTL:** full mirror; figures LTR runs; the document renders bilingually per institution configuration.

---

## Rate Display (conventional)

**Anatomy:** headline rate + basis ("5.99% per year, reducing balance") · **APR line always present and labeled** ("Annual Percentage Rate: 6.54% — includes fees") · flat-vs-reducing clarifier where flat rates are quoted (with the reducing equivalent shown — quoting flat without equivalence is banned in-system) · variable-rate basis where applicable ("EIBOR 3M + 3.2%, revised quarterly" + rate-history link).

## Profit Rate Display (Islamic)

**Anatomy:** structure-appropriate presentation: financing (e.g. Murabaha) shows **profit rate + total profit amount in AED** ("Profit rate 5.99% — total profit AED 12,704.00 over 48 months"); deposits (e.g. Mudarabah) show **profit-sharing ratio + weightages + distribution frequency** ("You receive 70% of pool profit · distributed monthly · rates are indicative, not guaranteed" + historic distribution table) · expected vs guaranteed clearly separated — indicative profit is never typeset as a promise.

## Shari'ah Structure Explainer

**Anatomy:** compact expandable card naming the structure ("This is Murabaha financing") · plain-language explanation (2–3 sentences: "The bank buys the item and sells it to you at a disclosed markup. You pay in fixed installments. The price never changes after signing.") · certification mark (internal Shari'ah committee approval) · link to the full structure document.

**Rule:** present on every Islamic product surface — it is disclosure, not education garnish.

---

## Payment Calculator

**Purpose:** explore amount/term/payment before applying.

**Anatomy:** amount (Currency Input + slider hybrid) · term (stepper/slider, months) · live outputs: periodic payment (`amount.lg`) · total repayment · total cost of credit (the honest number: "You pay AED 12,704.00 for this financing") · rate assumption line (≈, "your personal rate may differ — check eligibility") · apply CTA.

**States:** interactive · out-of-bounds (policy limits shown inline) · rate-personalized (post-eligibility: ≈ removed).

**Rules:** total cost is never hidden behind a tap; sliders always pair with typed inputs (a11y + precision); calculator outputs are estimated-labeled until a firm offer exists.

---

## Eligibility Check

**Purpose:** soft-check before full application.

**Anatomy:** minimal inputs (salary, obligations — prefilled where consented via open-data) · consent line for the check (bureau-impact honesty: "This soft check doesn't affect your credit record") · outcome: likely-eligible (range, not promise) / needs-full-application / not-eligible-now.

**Rule (routing, not rejection-by-validation):** not-eligible outcomes explain the *category* of reason where permitted (income threshold, existing obligations, tenure) and route constructively ("You may be eligible for AED 50,000 instead" / "Try again after 3 months of salary transfers") — never a bare dead end.

---

## Application Progress

Stepper + save-and-resume: stages (Details → Documents → Review → Decision) · per-stage document requirements upfront (checklist: EID, salary certificate, 3-month statement) · resume from any device · abandoned-application recovery notification.

**States:** in-progress · awaiting-documents (which, why, formats) · under-review (honest SLA: "Usually within 2 working days") · decision-ready.

---

## Offer Presentation

**Anatomy:** firm Product Summary (locked figures) · changes-from-request highlighted ("You asked for AED 100,000 — we can offer AED 80,000" with the difference explained) · validity countdown · accept path → contract review → **signing ceremony** (digital-identity signature handoff) · decline path (one tap, no retention traps).

**Rule:** accepting is a step-up event; the cooling-off notice renders again *after* signing with the cancellation entry point live for 5 business days.

---

## Approval / Rejection

- **Approved:** congratulation beat (restrained) · what happens next (disbursement timing, first payment date: "AED 100,000.00 arrives today. First payment AED 2,348.00 on 1 Oct.") · schedule preview.
- **Rejected:** respectful, plain ("We can't offer this financing right now") · reason category where permitted · what can change the outcome · alternatives · **no dark-pattern re-marketing on the rejection screen**.

---

## Repayment Schedule

**Anatomy:** table/list per installment: date · amount · principal/profit split (columns named per terminology dimension) · remaining balance · status per row (paid ✓ / upcoming / due / overdue / holiday) · progress header ("14 of 48 payments made · AED 79,832.00 remaining").

**States:** on-track · payment-due (≤5 days: prominence + pay-now) · overdue (see Overdue State) · restructured (old vs new schedule accessible).

**RTL:** table mirrors; numerics end-aligned LTR.

---

## Outstanding Summary

Product Header specialization: outstanding balance (`amount.lg`) · next payment (amount + date + auto-debit source: "Auto-pays from ••4521 on the 1st") · paid-so-far progress bar · quick actions (pay early, statement, settle).

---

## Early Settlement

**Anatomy:** settlement quote: remaining principal · settlement fee (per contract, with the fee-basis explained) · **total to settle today** · savings framing honesty ("Settling today costs AED 81,032.00. Continuing costs AED 84,528.00 over 34 months.") · quote validity · proceed → review contract.

**Rule:** both numbers (settle now vs continue) always shown — the component doesn't sell either path.

---

## Payment Holiday / Deferral

**Anatomy:** eligibility + terms ("Defer 1 payment · profit continues to accrue · term extends by 1 month") · **cost of deferral stated in AED** before confirmation · Ramadan/seasonal deferral programs as institution-configurable presets.

---

## Overdue State

**Anatomy:** amount overdue + days · consequence ladder stated factually (late fee applied → credit-record impact → escalation) · pay-now path (partial payment accepted where policy allows, stated) · **hardship path is always present** ("Struggling to pay? See your options" → restructure/contact) — collections pressure patterns (countdown timers, red full-screens) are banned.

**Tone:** factual, non-shaming; Arabic register matches (formal, respectful).
