# Arabic / RTL Design Review Checklist

**Reviewer:** native Arabic speaker who uses Arabic banking/government apps regularly
**Scope:** `showcase.html` (العربية toggle) + `journey-remittance.html` (العربية toggle) + component gallery with the RTL direction control
**Duration:** ~40 min · **Stance:** you are reviewing a *design*, not checking a translation. If something reads like translated English, feels visually off, or you'd be embarrassed to ship it in your own bank's app — that's a finding.

Mark each item: ✅ correct · ⚠️ acceptable but improvable · ❌ wrong (with note).

## 1. Layout mirroring

| Item | Check | Result |
|---|---|---|
| 1.1 | Whole layout mirrors: navigation, cards, lists — nothing left anchored "left" | |
| 1.2 | Back control points right (direction of "back" in Arabic reading) | |
| 1.3 | Stepper/progress advances right-to-left; checkmarks NOT mirrored | |
| 1.4 | List rows: icon at right, amount at left, correctly aligned | |
| 1.5 | Toggles/switches: on-position reads naturally; state word visible | |

## 2. Numbers, amounts, identifiers (the defect factory)

| Item | Check | Result |
|---|---|---|
| 2.1 | Amounts (AED 10,036.75) hold together as one unscrambled unit inside Arabic sentences — sign attached, currency code placed correctly | |
| 2.2 | The IBAN/account strings don't scramble punctuation or reverse groups | |
| 2.3 | Rate expression "1 AED = ₹25.0800" reads intact in the Arabic review screen | |
| 2.4 | Mixed names (Latin payee name in Arabic UI) don't break line flow | |
| 2.5 | Reference codes (BES-XXXXXX) render left-to-right, unbroken | |

## 3. Typography

| Item | Check | Result |
|---|---|---|
| 3.1 | Arabic text is comfortably readable — not cramped (line-height feels right, size not smaller than the English felt) | |
| 3.2 | No letter-spacing artifacts breaking cursive joining anywhere | |
| 3.3 | Emphasis works without caps (bold/size does the job); nothing renders in "fake caps" | |
| 3.4 | Font renders properly (no fallback tofu, correct ligatures, ة/ه and ي/ى render correctly) | |

## 4. Language quality (register and correctness)

| Item | Check | Result |
|---|---|---|
| 4.1 | Register is consistent Modern Standard Arabic, respectful banking tone — not colloquial, not stiff machine translation | |
| 4.2 | Financial terms match UAE banking convention: حوالة (transfer), الرصيد المتاح (available balance), مستفيد (payee), رسوم (fees), سعر الصرف (rate) | |
| 4.3 | The critical safety strings read natural and calm: "نتحقق من حالة حوالتك", "لم يُخصم أي مبلغ من حسابك", "أموالك آمنة" | |
| 4.4 | Button labels are verb-first and idiomatic ("إرسال AED …", "متابعة", "رجوع") | |
| 4.5 | The name-check question "هل تقصد «…»؟" reads naturally with the quoted Latin name | |
| 4.6 | Nothing reads as word-for-word English structure; sentence order feels Arabic-native | |
| 4.7 | Punctuation: Arabic comma (،), question mark (؟), quotes «» used where appropriate | |

## 5. Journey feel (the real test)

Run the full remittance flow in Arabic, start to receipt.

| Item | Check | Result |
|---|---|---|
| 5.1 | At no point did you have to mentally "translate back to English" to understand a step | |
| 5.2 | The review screen would give an Arabic-first user full confidence about cost and consequence | |
| 5.3 | Error and warning moments (wrong PIN, rate expiry, name mismatch) remain clear and non-alarming in Arabic | |
| 5.4 | The receipt is something you would accept as proof-of-payment in Arabic | |
| 5.5 | Overall verdict: ship / fix-first / redesign — one sentence why | |

## Reporting

File each ❌ (and important ⚠️) as an issue tagged `verification` + `rtl`, quoting the current Arabic string and your proposed correction. Terminology corrections also update the glossary (`docs/system/27-content-notifications-errors.md`) so the fix propagates system-wide, not per-screen.
