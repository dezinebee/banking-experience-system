# 05 — Motion

**Banking Experience System (BES)** · Foundations · v2.0.0-draft

Motion communicates progress, state change, confirmation, error, loading, navigation and hierarchy. It never decorates a financial decision. If an animation does not answer "what just happened / what is happening / where am I", it does not ship.

---

## 1. Tokens

### Durations
| Token | ms | Use |
|---|---|---|
| `motion.instant` | 80 | State ticks (checkbox, toggle) |
| `motion.fast` | 140 | Hover/pressed feedback, chip changes |
| `motion.standard` | 220 | Component enter/exit (menus, tooltips, accordions) |
| `motion.gentle` | 320 | Sheets, drawers, page transitions |
| `motion.deliberate` | 480 | Success confirmations, progress completions |

### Easings
`ease.standard` = cubic-bezier(0.2, 0, 0, 1) — most transitions ·
`ease.enter` = (0, 0, 0, 1) — decelerate in ·
`ease.exit` = (0.3, 0, 1, 1) — accelerate out ·
`ease.spring` — reserved for celebratory success only (see §3)

Directional motion uses **logical direction**: "forward" slides from the inline-end. In RTL, forward comes from the left automatically. Never hardcode translate-x signs.

## 2. Semantic motion patterns

| Event | Motion | Rationale |
|---|---|---|
| Navigation forward/back | Slide inline-direction + fade, `gentle` | Spatial model of the journey |
| Sheet/drawer | Slide from block-end/inline-end, scrim fade | Physical origin |
| State change (pending→success) | Cross-fade + icon draw-in, `deliberate` | The moment of financial certainty deserves a beat |
| Error appearance | No shake. Fade-in error summary + focus move | Shake reads as blame and harms motion-sensitive users |
| Loading | Skeletons for structure, spinner ≤ after 400ms delay | Avoid flash-of-spinner |
| Processing money | Determinate progress where the rail allows; calm indeterminate pulse otherwise | Never fake progress percentages for opaque rails |
| Balance/amount changes | Count-up animation **banned** for real balances; permitted only in calculators/projections | A real balance ticking implies the money is moving *now* |
| Success (transfer sent) | Single check-draw + subtle scale, `deliberate`, once | Confidence, not confetti; celebratory effects allowed only in savings-goal contexts, brand-tier opt-in |

## 3. Rules

- **Reduced motion:** every pattern defines its `prefers-reduced-motion` alternative — cross-fades replace slides, draws become instant appears, progress remains (it's information). Reduced-motion is a tested state, not a fallback.
- Nothing critical is *only* communicated by motion; state changes always pair with text/icon change.
- No looping ambient animation on financial task screens (dashboards may use one calm hero treatment at brand tier, off by default).
- No parallax; no motion during input focus (keyboard jumps + animation = missed taps).
- Fraud/security interruptions appear with **no entrance animation** — instant, full attention.
- Timing budget: any interaction's total animated latency ≤ 500ms before the user can act again.
