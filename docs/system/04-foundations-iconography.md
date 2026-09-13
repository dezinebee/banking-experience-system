# 04 — Iconography

**Banking Experience System (BES)** · Foundations · v2.0.0-draft

Icons in BES are functional signage: simple, recognizable, consistent, and safe in both reading directions. Decorative illustration is a brand-layer concern; this foundation governs the functional icon set.

> **Status: Specified — no icon assets ship yet.** This document defines the construction grid, the required financial glyph vocabulary, the RTL mirroring policy and the accessibility rules. It does **not** come with drawn icons: the repository contains no SVG icon assets, and components that need a glyph either inline their own or expect the consumer to supply one. Treat §2's glyph list as the specification a set must satisfy, not as an inventory of what you get. See `STATUS.md`.

---

## 1. Construction

- **Grid:** 24×24 with 2px padding safe area; key shapes on a 20×20 live area. Secondary size 20×20 (dense tables), large 32×32 (empty states, feature intros).
- **Stroke:** 1.75px, rounded caps and joins; filled variants exist for *selected/active* states only — outline is default.
- **Corner language** follows the shape preset direction (sharp brands get squarer joins) within legibility limits.
- **Color:** icons inherit text color tokens (`text.primary`, `text.secondary`, status colors). Multicolor icons are banned in the functional set.
- Every icon ships with a required accessible name; decorative uses must be explicitly marked hidden from assistive tech.

## 2. Core functional vocabulary (baseline set, ~120)

Categories: navigation (home, back, forward, close, menu, search, filter, sort) · accounts & money (bank, wallet, coins, transfer arrows, exchange, receipt, statement, safe) · cards (card, freeze/snowflake, lock, PIN pad, contactless) · status (check-circle, warning-triangle, error-octagon, info-circle, clock/pending, hold/lock, reversed) · security (shield, fingerprint, face-ID, key/passkey, device, eye/eye-off) · identity & consent (ID card, passport, document-scan, signature, consent-check, link/unlink institution) · people (person, people, beneficiary-add) · communication (bell, mail, chat, phone, headset) · documents (download, upload, share, print, PDF) · charts (trend-up, trend-down, pie, bars) · misc (calendar, location, globe/language, settings, help).

Financial-specific glyphs that must exist and be unambiguous: **transfer** (two horizontal arrows), **remittance/international** (globe + arrow), **exchange/FX** (circular double arrow), **fee** (price tag), **hold/reserved** (dashed circle + lock), **refund** (arrow returning), **reversal** (arrow undo), **split bill** (divide), **request money** (hand + arrow in), **QR pay**, **instant** (bolt — used only for genuinely instant rails).

## 3. RTL mirroring policy

**Never mirror everything.** Each icon carries a `mirror` flag in its metadata; the build flips flagged icons automatically under `dir="rtl"`.

### Mirror (directional semantics follow reading order)
- Back / forward chevrons and arrows
- Progress/continuation arrows ("next step")
- List indent/outdent, breadcrumb separators
- Send arrow (points in reading direction of "away")
- Undo/redo pair (swap)
- Speech/chat bubble tails

### Never mirror
- **Numbers, currency symbols, and the dirham symbol** — numerals are LTR in Arabic
- Clock, watch, hourglass (time reads clockwise universally)
- Media controls (play points right by convention)
- Checkmarks, warning, error, info glyphs
- Brand and scheme marks (card networks, national rails logos, bank logos)
- Fingerprint, face, shield, lock, eye
- Charts/trends (trend-up rises to the end of the reading direction? **No** — trend direction is data semantics, axis mirrors but the up/down meaning holds; chart icons stay unmirrored)
- QR, barcode
- Globe, documents, download/upload (vertical semantics)

### Case-by-case (documented per icon)
- Transfer between two accounts: mirrors (A→B order follows reading direction)
- Refund/reversal arrows: mirror with their flow context
- Phone/headset: unmirrored by default

## 4. Usage rules

- Icon + label is the default; icon-only requires an accessible name and is reserved for universally learned glyphs (search, close, settings) or space-critical toolbars with tooltips.
- Status icons are mandatory companions to status colors (doc 01 §2) — shape carries the meaning for color-blind users: circle=info/success context, triangle=warning, octagon=error.
- One metaphor per concept system-wide: "freeze card" is always the snowflake; never alternate metaphors between surfaces.
- Icons never substitute for amount signs — `+`/`−` on amounts are typographic, not iconographic.
- Minimum tap target around interactive icons: 44×44 regardless of visual size.
