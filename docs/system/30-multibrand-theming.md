# 30 — Multi-Brand & Theming Architecture

**Banking Experience System (BES)** · v2.0.0-draft

One behavioral core, many brand expressions. A conventional bank, its Islamic window, a youth sub-brand and a white-label fintech run the same components, patterns, state machines and accessibility — differing only in themeable expression.

---

## 0. Status: tested, with one stated limit

This document used to describe a contract nothing had exercised. It now has a worked second brand.

**Sadu** (`tokens/themes/sadu.json` → `assets/themes/sadu.css`) is a fictional Islamic-finance neobank built to sit as far from BES core as the contract allows: deep green rather than blue, squared rather than rounded, a serif Latin stack and a Naskh Arabic stack, comfortable density as its standard, slower motion, and a gold-on-green card face. Side by side with core at `brand-proof.html` — same markup, same `bes.css`, byte for byte.

**The cost in component CSS was zero lines.** The brand is **111 token values and no rules at all**, 5.2 KB.

Three gates keep it honest, each verified by reintroducing the failure it exists to catch:

| Gate | Enforces |
|---|---|
| `tools/audit-theme.py` | A theme is token values only (T1–T6): no CSS properties, no selector outside the brand scope, no `@font-face`, no token core doesn't define, and the generated CSS must still match its JSON source. |
| `tools/audit-contrast.py` | The full derived audit runs **once per brand** — 1,502 element colourings each. A brand that breaks AA fails the build. Sadu was caught doing exactly that in development: a lighter, friendlier green dropped the pressed icon button to 2.11:1. |
| `tools/audit-consistency.py` C8 | `font-size` and `border-radius` literals in `bes.css` stay at zero. A literal is a hole in the theming contract, not a style choice. |

**The limit, stated plainly:** spacing is not tokenised. 135 padding, margin and gap literals remain in `bes.css`, because the space scale is a 4px grid while the component CSS uses 6/10/14/18px throughout. Closing that is a decision about the grid — widen the scale to 2px steps, or restyle onto 4px — not a mechanical substitution, and it would move every component's rhythm. **A brand can currently change colour, type, shape, density and motion. It cannot change spacing rhythm.** The consistency audit holds that number visible and lets it fall, never rise.

---

## 1. The split

```
BANKING CORE (locked)                      BRAND THEME (per institution)
──────────────────────                     ────────────────────────────
Behavior & interaction                     Color values (within contrast contract)
Financial semantics & state machines       Type stacks (from tested AR+EN pairs)
Component anatomy & states                 Shape preset (sharp / standard / soft)
Patterns & journey blueprints              Motion personality (calm / expressive)
Accessibility guarantees                   Logo, illustration, imagery slots
Disclosure structures (KFS, consent, CoP)  Iconography accent style (within grid)
Error taxonomy & content frames            Voice inflection (within content rules)
Status meanings & pairings                 Dashboard module arrangement (within IA rules)
```

The test: **a brand change is describable entirely as token values + content-vocabulary configuration + asset slots.** If a brand request requires touching component internals, it's either a core contribution (goes through system governance) or it's rejected.

## 2. Theme anatomy

A theme package contains:
1. **Primitive overrides** — brand palette mapped into the primitive scale slots
2. **Semantic map** — which primitives feed `action.primary`, surfaces, etc.
3. **Type pairing** — Latin + Arabic stacks from the certified pair list + `font.display`
4. **Preset selections** — shape, motion personality, density defaults per surface class
5. **Asset slots** — logo variants (light/dark/monochrome), card art faces, illustration set, empty-state art
6. **Content configuration** — terminology dimension (conventional/Islamic/dual), voice inflection parameters, institution names/legal footers, support channels
7. **Compliance variants** — jurisdiction/license-driven content sets (disclosures, regulatory footers)

## 3. Guard rails (what makes theming safe)

- **Contrast contract validation** (doc 01 §6): every themed pairing checked light+dark, LTR+RTL, standard+high-contrast — build-time rejection, not review-time debate.
- **Fixed financial semantics:** `financial.*` and `status.*` *meanings* and pairing rules are invariant; a brand may tune the exact hue within the semantic family's perceptual range (e.g., its green), never reassign meaning (no brand-purple "success").
- **Focus visibility, touch minima, type minima:** non-overridable floors.
- **Disclosure integrity:** KFS, consent screens, CoP, warnings render structurally identically across brands — brand affects their skin, never their content order or prominence rules.
- **Pretested presets over free values:** shape/motion/density are chosen from validated sets; arbitrary per-component overrides don't exist in the theme API.

## 4. Multi-brand scenarios supported

| Scenario | Mechanism |
|---|---|
| Bank + Islamic window | One theme, terminology dimension = dual; Islamic surfaces switch vocabulary + rate components; optional visual sub-cue (accent) within contract |
| Banking group, multiple brands | Theme per brand over one core; shared component updates propagate to all |
| Youth/neobank sub-brand | Distinct palette/type/motion personality; identical financial behavior |
| White-label fintech | Full theme package + compliance variant per license type |
| Co-branded products | Card art + partner logo slots; partner never enters the trust surfaces (payee verification, consent) except as disclosed data |

## 5. Dark scheme per brand

Every theme ships light + dark (dark is not optional and not auto-derived — derivation drafts it, designers verify it); financial/status colors re-verified on dark surfaces; brand marks swap to dark-appropriate variants via asset slots.

## 6. Governance

- Theme submissions run the automated gate (contrast, focus, minima, RTL render) + a design review against the quality bar (calm, precise, trustworthy — no gradient-noise, no decorative dashboards).
- Core changes version semantically; themes declare core-version compatibility; breaking core releases ship migration notes + codemods.
- Brand teams get the **theme sandbox**: the full component gallery rendered in their draft theme, both directions, both schemes, with the validation report inline — self-service iteration before submission.

## 7. The quality bar (restated as acceptance criteria)

Precise · calm · trustworthy · modern · accessible · information-rich · systematic. Rejected on sight: gradient-heavy surfaces competing with data, glassmorphism over financial figures, decorative dashboards, arbitrary accent colors on status meanings, animation that delays money tasks, illustration crowding decision screens. The system should feel like a serious financial institution that respects the user's attention — in every brand.
