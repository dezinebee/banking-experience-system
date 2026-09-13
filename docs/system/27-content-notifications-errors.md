# 27 — Content System, Notifications & Error Taxonomy

**Banking Experience System (BES)** · v2.0.0-draft

---

## 1. Voice

Calm · specific · respectful · bilingual by design. The product speaks like a competent banker who explains clearly and never panics: no exclamation marks in financial contexts, no "Oops!", no jargon leakage, no blame. Arabic register: formal-respectful (فصحى معاصرة), consistent across all surfaces — never machine-translated colloquialism.

## 2. Terminology glossary (structure + seed entries)

Every term: canonical EN · canonical AR · conventional/Islamic variant flags · avoid-list. One term per concept, everywhere.

| Concept | Use (EN) | Use (AR) | Avoid |
|---|---|---|---|
| Completed transfer | Transfer completed | تم التحويل | "Transaction done", "Success!" |
| In-flight | Your transfer is pending | حوالتك قيد المعالجة | "Processing error", "Wait" |
| Unknown state | We're checking your transfer status | نتحقق من حالة حوالتك | "Failed", "Error occurred" |
| Available money | Available balance | الرصيد المتاح | "Balance" (unqualified) |
| Money out | Sent / Paid | تم الإرسال / تم الدفع | "Debited" (in consumer UI) |
| Money in | Received | تم الاستلام | "Credited" |
| Cost of credit (conv.) | Interest rate / APR | معدل الفائدة / معدل النسبة السنوي | — |
| Cost of credit (Islamic) | Profit rate | معدل الربح | "Interest" (banned in Islamic dimension) |
| Credit product (conv.) | Loan | قرض | — |
| Credit product (Islamic) | Financing | تمويل | "Loan" (banned in Islamic dimension) |
| Insurance (Islamic) | Takaful | تكافل | "Insurance" (in Islamic products) |
| Beneficiary | Payee | المستفيد | mixing "beneficiary/payee/recipient" across screens |
| Verify identity | Verify your identity | التحقق من هويتك | "KYC", "CDD" |
| Security hold | Additional checks required | مطلوب تحققات إضافية | "AML hold", "Compliance block" |

The Islamic dimension (doc 06 §3) resolves flagged terms automatically; a conventional string appearing on an Islamic surface is a build-detectable defect.

## 3. Message frameworks

- **Errors (four questions):** WHAT happened · WHY (plain class) · what happened to the MONEY · WHAT to do next.
- **Confirmations:** what happened + the key facts (amount, destination, when) + where the record lives.
- **Warnings:** the risk pattern (not accusation) + the protective action + the escape ("If unsure, wait — genuine payees will understand").
- **Empty states:** explain + enable, never blame.
- **Buttons:** verb + consequence; money-moving CTAs carry the amount.

## 4. Error taxonomy (normative)

Every error in a BES product maps to exactly one class. Classes define: user message frame · technical state logged · recovery action · CTA · severity · a11y behavior · analytics event. Internal codes never surface (a short human reference code may, for support).

| Class | Meaning | Message frame | Recovery |
|---|---|---|---|
| `USER_ERROR` | Fixable input/choice | Specific fix at the field ("Enter the IBAN without spaces") | Inline correction |
| `LIMIT_ERROR` | Policy/limit boundary | Name the limit + alternatives | Adjust, schedule, or raise-limit path |
| `FUNDS_ERROR` | Insufficient funds | Shortfall named | Top-up path, lower amount |
| `SYSTEM_ERROR` | Our fault | Apology + money statement + retry/status | Retry (idempotent) or status-check |
| `BANK_ERROR` | Counterparty institution declined/failed | "The recipient's bank..." + money statement | Retry later, alternative rail |
| `COMPLIANCE_ERROR` | Regulatory block | Generic-safe ("Additional checks required") | Document flow / support (P-73) |
| `FRAUD_BLOCK` | Risk engine stop | Tiered per doc 20 (never "fraud" as accusation of the user) | Challenge / support |
| `NETWORK_ERROR` | Connectivity | Offline pattern (P-70), cached timestamps | Auto-retry on reconnect (reads only) |
| `TIMEOUT` | No confirmation received | **→ UNKNOWN handling, never "failed"** | Status-check, notify-me |
| `UNKNOWN_TRANSACTION_STATE` | Rail ambiguity | "We're checking..." + money-safety line | Resolution commitment + notification |
| `SESSION_ERROR` | Auth/session lapse | Neutral sign-out explanation | Re-auth + draft restore (P-69) |
| `PERMISSION_ERROR` | Role lacks rights (SME/corporate) | "You don't have permission — ask an administrator" | Request-access path |

## 5. Notification system

### Categories (semantic + visual separation)
| Category | Examples | Urgency ceiling | Suppressible? |
|---|---|---|---|
| `transaction` | Sent/received/settled, request-to-pay | important | Configurable granularity (e.g., "only above AED 100") |
| `security` | New device, credential change, detail reveal | critical | **Never** |
| `fraud` | Challenges, interventions | critical | **Never** |
| `payment` | Due dates, autopay pre-debits, standing-order results | urgent | Partially (timing, not existence, for committed payments) |
| `system` | Maintenance, degraded service, terms changes | important | No (regulatory notices), yes (minor) |
| `product` | Application progress, document ready, consent expiry | important | Partially |
| `marketing` | Offers, features | informational | **Fully; opt-in** |

### Urgency levels
`informational` (digestible, batchable) · `important` (timely, individual) · `urgent` (time-boxed action: pay-by, respond-by) · `critical` (immediate: fraud/security — full-screen-capable, bypass quiet hours per user's security setting).

### Rules
- Security/fraud notifications are visually + semantically distinct (dedicated styling, no brand-marketing dress) and never batched.
- Marketing never masquerades: no "security-style" urgency on offers; no piggybacking offers onto transaction notices.
- Every notification deep-links to its object (transaction detail, consent card, approval).
- Quiet hours honored except `critical`; digest option for `informational`.
- Notification center in-app mirrors push history (nothing exists only as an ephemeral push), filterable by category.

## 6. Writing for bilingual parity

Source strings are written EN + AR together at design time (content design is bilingual, not translate-later); placeholders are position-independent (`{amount}` orders differ per language); pluralization uses proper Arabic plural categories (zero/one/two/few/many/other); dates/numbers formatted by locale library, never string-built; text expansion budget: Arabic ±25% and German-length safety for future locales — layouts tested at both extremes.
