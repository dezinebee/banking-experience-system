# 22 — Patterns: Asking Users For…

**Banking Experience System (BES)** · Patterns · v2.0.0-draft

Task-based patterns for collecting information. Each pattern composes components (docs 08–21) and carries: when to use · structure · error prevention · specified error copy · accessibility · Arabic/RTL notes. Patterns with regulatory grounding carry their REG-ID (Phase 01 doc 05).

Global form doctrine applies (doc 09): prevent > validate; on-submit default; preserve input; error summary + focus; route eligibility, never validate it.

---

## P-01 · Ask for an amount

**Use:** any money entry. **Structure:** Currency Input + context line (available balance / limits surfaced *here*, not at failure) + quick chips where useful.
**Prevention:** precision clamp; paste forgiveness; limit discovery at entry (Limit Indicator).
**Errors:** below minimum ("The minimum transfer is AED 10.00") · above limit (names the limit and the alternative) · exceeds balance (names shortfall + top-up path).
**RTL:** amount LTR isolated; chips mirror.

## P-02 · Ask for a payee (domestic)

**Use:** transfers within UAE. **Structure:** choose-existing first (Beneficiary Manager picker with search) → add-new fork; add-new = IBAN input (checksum on blur, bank auto-derived and confirmed) or mobile-proxy for instant rails (contact picker with permission JIT-notice) → registered-name entry → **Payee Verification (name check)** before save/use. REG: payee confirmation mandate.
**Prevention:** duplicate detection; IBAN format forgiveness (spaces/hyphens stripped).
**Errors:** checksum fail ("This IBAN doesn't look right — UAE IBANs have 23 characters starting with AE") · proxy-not-registered ("This number isn't registered for instant transfers — send with their IBAN instead").

## P-03 · Ask for an international recipient

**Use:** remittance/international transfer. **Structure:** country first (drives everything) → corridor-relevant fields only (IBAN corridors: IBAN+name; account-number corridors: account+bank picker+branch code as required; wallet corridors: wallet ID+provider) → payout-method selection (Radio option cards with fee/speed) → name fields matching corridor requirements (full name as per ID — helper: "Enter their name exactly as on their ID; banks may reject mismatches").
**Prevention:** per-corridor validation rules; bank pickers searchable by English/Arabic/code; purpose-of-transfer selector where corridors require it (plain-language options).
**RTL:** recipient names may be non-Arabic/non-Latin — free-script field with isolation.

## P-04 · Ask for identity documents

**Use:** onboarding, re-KYC, EDD. **Structure:** stepper with requirements checklist upfront → per-document Document Capture → extracted-data confirmation (Verified Field preview) → Liveness where required → submission with review SLA stated. REG: KYC/AML.
**Prevention:** format/quality guidance before capture; strategy-change after 3 failures (doc 20).
**Tone:** "why we ask" on every step ("We're required to verify your address — a DEWA bill from the last 3 months works").

## P-05 · Ask for an address (international-aware)

**Use:** onboarding, delivery, beneficiary details. **Structure:** country selector first → country-appropriate fields (UAE: emirate + area + building/villa + optional PO Box — free-text-tolerant; no postal-code requirement where none exists) → maps-assist optional, manual always available.
**Prevention:** never require fields the country doesn't have; transliteration tolerance (Arabic or Latin entry accepted).

## P-06 · Ask for a phone number

**Structure:** country-code selector (default +971, full list) + national-number field (`inputmode="tel"`, forgiving of spaces/dashes/leading zero).
**Errors:** length-for-country specific ("UAE mobile numbers have 9 digits after +971").

## P-07 · Ask for personal details (names, DOB, nationality)

**Structure:** name fields matching ID documents (single full-name field preferred; "as shown on your Emirates ID") · DOB as segmented DD/MM/YYYY (no calendar) · nationality/dual-nationality per compliance need with JIT why-notice.
**Prevention:** diacritics/apostrophes/spaces accepted; Arabic and Latin scripts accepted with isolation.

## P-08 · Ask for employment & income (credit/EDD)

**Structure:** progressive: employment status → employer (searchable) → salary (Currency Input) → obligations; prefill from consented sources where available (Verified Field styling with source note).
**Tone:** neutral EDD framing; ranges accepted where exactness is unnecessary.

## P-09 · Ask for card details (funding/verification)

**Use:** funding from another bank's card, wallet top-up. **Structure:** PAN input (auto-format 4-4-4-4 or scheme-appropriate grouping, scheme auto-detected + shown, LTR always) · expiry (MM/YY, past-dates impossible) · CVV (masked, info affordance: "3 digits on the back") · no character limits that block typed spaces (stripped silently) · scan-card path.
**Errors:** scheme-specific copy ("Check the card number — it doesn't match a valid card") · expired card at entry.
**Security:** PCI-conscious surface (no clipboard broadcast, masked echo); never stored without explicit save-consent checkbox (unchecked).

## P-10 · Ask for consent (data / marketing / terms)

**Use:** every consent moment. **Structure:** one checkbox per consent, purpose inline, never pre-ticked, marketing separate from service, terms acceptance names the document version and links it ("I accept the Key Facts Statement (PDF, version 3.2)"). Open Finance consents use the dedicated Consent Request pattern (doc 21). REG: consumer protection + data protection.
**Errors:** "You need to accept the Key Facts Statement to continue" (specific, at the checkbox and in summary).

## P-11 · Ask for a purpose/reference

**Use:** transfer references, purpose-of-payment codes. **Structure:** free-text with rail-safe character stripping + counter, or corridor-mandated purpose selector (plain-language labels mapped to codes internally — codes never shown).

## P-12 · Ask for a date / schedule

**Structure:** Date Picker with processing-day awareness (non-processing days blocked with explanation + auto-suggested next day); recurring schedules via Scheduled Setup (doc 16).

## P-13 · Ask users to create credentials (app PIN / passkey enrollment)

**Structure:** benefit-first framing → passkey/biometric enrollment as primary → app PIN as fallback creation (weak-PIN rejection with reasons) → confirmation + where-to-manage. Never SMS-based factors. REG: authentication modernization.

## P-14 · Ask for feedback (post-task, optional)

**Structure:** single-tap score + optional comment, *after* the receipt, never blocking the result; fraud/complaint surfaces never carry feedback asks.
