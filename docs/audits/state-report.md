# Transaction State Contract Audit

Doc 06 §6: *"The state names are the stable API: a 'pending' transaction is the same concept in the UI, the event stream and the copy deck."* This audit is that sentence, executable. The canonical list is doc 07 §4's normative contract table; every other artefact must agree with it.

**Result:** ✅ PASS · 13 canonical states

- ℹ️ S1 canonical states from doc 07 §4: 13 — draft, review, authentication, processing, completed, pending, failed, unknown, blocked, reversed, refunded, disputed, cancelled

## The contract, per state

| State | Colour token | Tint | Badge | Glyph | EN | AR | Retry |
|---|---|---|---|---|---|---|---|
| `draft` | ✅ | ✅ | `.bes-badge--draft` | `draft` | Not sent yet | لم تُرسل بعد | no |
| `review` | ✅ | ✅ | `.bes-badge--review` | `review` | In review | قيد المراجعة | no |
| `authentication` | ✅ | ✅ | `.bes-badge--authentication` | `hold` | Awaiting authentication | بانتظار المصادقة | no |
| `processing` | ✅ | ✅ | `.bes-badge--processing` | `inflight` | Processing | قيد التنفيذ | no |
| `completed` | ✅ | ✅ | `.bes-badge--completed` | `check` | Completed | تم التحويل | no |
| `pending` | ✅ | ✅ | `.bes-badge--pending` | `clock` | Pending | قيد المعالجة | no |
| `failed` | ✅ | ✅ | `.bes-badge--failed` | `cross` | Failed | فشلت | yes |
| `unknown` | ✅ | ✅ | `.bes-badge--unknown` | `query` | Checking status | نتحقق من الحالة | no |
| `blocked` | ✅ | ✅ | `.bes-badge--blocked` | `pause` | Additional checks required | مطلوب تحققات إضافية | no |
| `reversed` | ✅ | ✅ | `.bes-badge--reversed` | `ret` | Reversed | تم عكس العملية | no |
| `refunded` | ✅ | ✅ | `.bes-badge--refunded` | `refund` | Refunded | تم الاسترداد | no |
| `disputed` | ✅ | ✅ | `.bes-badge--disputed` | `flag` | Disputed | قيد الاعتراض | no |
| `cancelled` | ✅ | ✅ | `.bes-badge--cancelled` | `slash` | Cancelled | أُلغيت | no |

Arabic labels are machine-drafted and flagged unreviewed system-wide until the native review in `docs/testing/arabic-rtl-review.md` passes — see STATUS.md.

`completed` and `refunded` share green; `processing`, `pending` and `unknown` share teal. That is deliberate — they are related states — and it is exactly why the glyph and label come from the registry rather than from the caller.

## What is checked

| ID | Rule |
|---|---|
| S1 | Doc 07 §4's table parses and is the single source of the state list |
| S2 | Every state has a `transaction.*` colour **and** tint token |
| S3 | Every state has a badge variant reading those tokens |
| S4 | Every state has a registry entry with a glyph and EN + AR labels |
| S5 | No transaction state colour lives outside `transaction.*` |
| S6 | UNKNOWN never offers retry; only a confirmed failure does; a binder enforces it |
| S7 | The JS registry and doc 07's table contain exactly the same names |
| S8 | No two states share both a colour and a glyph — sharing a hue is fine, sharing both is not |
| S9 | No page labels a badge with a state name while styling it as generic status |