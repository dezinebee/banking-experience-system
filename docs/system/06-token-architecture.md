# 06 — Token Architecture

**Banking Experience System (BES)** · Architecture · v2.0.0-draft

Tokens are the system's contract: behavior stays in components; every visual decision that may legitimately vary lives in a token. Brands theme by changing token values — never component internals.

---

## 1. Tiers

```
PRIMITIVE      blue.600, space.16, radius.md          — raw values, named by value
   ↓
SEMANTIC       action.primary, surface.secondary,      — named by role; the working vocabulary
               financial.income, status.pending
   ↓
COMPONENT      button.primary.background,              — scoped to one component;
               input.border.error, table.row.height      NEVER consumed outside it
   ↓
PATTERN        transaction.primaryAction,              — binds semantics to financial patterns
               review.total.emphasis, cop.mismatch.surface
   ↓
PRODUCT        sendMoney.cta, dashboard.heroBalance    — product-level aliases, optional tier
```

Resolution flows downward only. A component token may alias a semantic token; a semantic token may alias a primitive. Nothing references upward or sideways across component boundaries.

> **Implementation status:** PRIMITIVE, SEMANTIC and **COMPONENT** are shipped and build-validated (`tokens/tokens.json` → `tokens.css`, with each tier emitted as `var()` chains into the tier above, so a brand override at any level cascades). PATTERN and PRODUCT remain **reserved** — named here so consumers don't invent conflicting conventions, not yet emitted.

### What belongs in the component tier — and what does not

The component tier is small on purpose: **30 tokens**, not one per declaration. A token per declaration would be a rename with extra steps — it multiplies the surface a brand has to understand without giving it a decision it could not already make.

The rule is: **a component token exists where a brand needs to retune one component without moving a shared scale.** A button's silhouette, a card's corner, the card face's ink — those are decisions about that component. Everything else reads the shared scales directly:

```css
.bes-alert  { font-size: var(--bes-type-bodySm-size); }   /* shared scale — moves with the brand's type */
.bes-btn    { border-radius: var(--bes-button-radius); }  /* component tier — this button's silhouette */
```

The test for adding one: *could a brand want this different from everything else that currently matches it?* If not, it belongs on a scale. `--bes-alert-fontSize` fails that test; `--bes-button-radius` passes it.

**Component CSS carries no literals for any tokenised property.** `font-size` and `border-radius` literals in `bes.css` are held at **zero** by the consistency audit (C8): all 93 font sizes now read the type scale or a component token, and all raw colour is gone from the component layer. Spacing is the exception and is ratcheted rather than zeroed — see §5.

## 2. Naming grammar

`[namespace.]category.role[.variant][.state]` — lowercase, dot-delimited, camelCase for multiword roles.

- Categories: `surface` · `text` · `border` · `action` · `status` · `financial` · `balance` · `transaction` · `risk` · `verification` · `consent` · `space` · `type` · `radius` · `elevation` · `motion` · `z` · `chart` · `ai` (reserved)
- States: `.hover` `.pressed` `.disabled` `.focus` `.selected` `.error`
- Code delivery prefix: `--bes-` (CSS custom properties), e.g. `--bes-action-primary`, `--bes-financial-income`.

Prohibited: value-based names outside the primitive tier (`darkBlue`), physical-direction names anywhere (`marginLeft` → `marginInlineStart`), and component tokens leaking into other components.

## 3. Token dimensions (modes)

A resolved theme is the intersection of six dimensions. Components are written once; dimensions change values, not structure.

| Dimension | Values | Mechanism |
|---|---|---|
| **Brand** | default / bank-A / bank-B / white-label… | Theme package overriding semantic + primitive maps |
| **Scheme** | light / dark | `data-theme` attribute; respects OS preference; user override wins |
| **Direction** | ltr / rtl | `dir` attribute; logical properties + icon mirror flags; type metrics resolve per language |
| **Density** | comfortable / standard / compact | Spacing semantics remap; touch minima preserved |
| **Contrast** | standard / high *(planned)* | Text ≥7:1, thicker borders via `focus.width` token override; not yet emitted |
| **Terminology** | conventional / islamic *(specified; resolver planned)* | Content dimension: vocabulary keys (doc 27), profit-rate vs APR components |

Any dimension combination must be valid: an Islamic, dark, RTL, compact, high-contrast theme is a legitimate resolved state and part of the release test matrix (a sampled matrix, with the full matrix run on the money/transaction component families).

## 4. Theming contract

Brands receive a **theme manifest** listing exactly what they may set:

- Primitive palette substitutions (validated against the contrast contract, doc 01 §6, in light *and* dark, LTR *and* RTL)
- Type stacks (from the tested Latin+Arabic pair list) and `font.display`
- Shape preset (sharp/standard/soft), motion personality (calm/expressive — expressive still obeys doc 05 rules)
- Illustration/imagery slots, logo slots, voice inflection (content layer)

Locked (core-owned): all behavior; financial semantic colors' *meanings* and pairing rules; status shapes; focus visibility; spacing minima; touch targets; disclosure components' structure; state machines; error taxonomy.

Validation is automated: a theme that fails contrast, focus visibility, or touch minima is rejected at build, not review.

## 5. Delivery

- **Design:** variables organized by the same tiers and dimensions as code; modes for scheme/direction/density; library components consume variables only — no detached values.
- **Code:** a single token source of truth (JSON) compiles to CSS custom properties (web). Platform maps (iOS/Android) from the same source are on the roadmap. Semantic tokens are the public API; primitives are internal; component tokens are per-component files.
- **Versioning:** token changes classed as value-change (patch — theme-safe), addition (minor), rename/removal (major; deprecation aliases emitted for one major cycle — codemod tooling on the roadmap).
- Every token documents: role description, allowed surfaces/pairings, contrast contract, and which dimensions affect it.

## 6. Financial namespaces (summary — full definitions in doc 07)

```
currency.*        code · symbol · amount · precision · decimal · locale
balance.*         current · available · pending · reserved · overdrawn
transaction.*     draft · review · authentication · processing · pending ·
                  completed · failed · unknown · blocked · reversed · refunded ·
                  disputed · cancelled          (13 — doc 07 §4 is normative)
risk.*            low · medium · high · critical
verification.*    unverified · pending · verified · failed · expired
consent.*         required · pending · granted · expired · revoked
ai.*              (reserved) surface · badge · explanation — for AI-generated content marking
```

Status of each namespace in v1.0.1: `transaction.*`, `verification.*` and `consent.*` are **emitted as color tokens** (state → semantic color, both schemes). `risk.*` and `financial.*` are emitted. `currency.*` and `balance.*` are **data-model vocabularies**, not color tokens — they name concepts the components implement (precision maps, balance roles), and are not emitted as CSS. `ai.*` is reserved. The state *names* are the stable API: a "pending" transaction is the same concept in the UI, the event stream and the copy deck.

**This is now enforced, not asserted.** `tools/audit-states.py` takes doc 07 §4's contract table as the single source of the state list and fails the build unless every state has a `transaction.*` colour and tint, a `.bes-badge--<state>` variant reading those tokens, a registry entry in `BES.TRANSACTION_STATES` with a glyph and both EN and AR labels — and unless no transaction state colour lives in another namespace. It also enforces doc 07's prime directive as a property of the data: UNKNOWN may not offer retry, and only a confirmed failure may. Before that gate existed, three artefacts disagreed about what the states were (13 / 12 / 10) and no component read the state tokens at all.
