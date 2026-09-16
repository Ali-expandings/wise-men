# Q02 Arm C internals — members + peer reviews (pre-chairman)
# salvaged_from_context: false
# generated: 2026-05-31 (clean rerun — pilot Q02 was context-only)
# domain: engineering | composite: 2 | label: council-shaped | tier: standard | personas: Pragmatist / Skeptic / Architect / Maintainer / Devil's Advocate
# NOTE: frozen questions.yaml lists Q02 domain=ENGINEERING (the prior HISTORY next-phase note mislabeled it "product"). Engineering personas used to match the frozen domain.
# members: 5 × sonnet-4.6 | reviewers: 5 × haiku-4.5 (NEUTRAL grading frame) | chairman: sonnet-4.6 subagent (recorded in arm_c.md)
# validator: all 5 members returned the 5-section structure, none OUT OF DOMAIN. PASS.
# anonymization for reviewers: M1=Pragmatist, M2=Skeptic, M3=Architect, M4=Maintainer, M5=Devil's Advocate
# convergence: STRONG — all 5 converge on "thin component layer over Tailwind, NOT a full design system; tech lead is directionally right, 'design system' is the wrong/loose label." Genuine minority = premature-abstraction / extract-on-second-use / internal-tools-get-replaced caution + the "is 50 a stable number / who actually contributes UI" hidden assumption.

═══════════════════════════════════════════════════════════════════
## Member 1 — Pragmatist (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
At 50 internal users, a full design system (Storybook, versioned component library, design tokens, the whole apparatus) is almost certainly overkill. The ROI just isn't there. But "Tailwind utility classes directly everywhere" is also a false economy — it trades upfront design system cost for compounding maintenance debt. The right answer is the cheap middle path: a small, local component file (Button, Input, Badge, Card, maybe 8-12 components) that wraps Tailwind, lives in the same repo, and gets extended as needed. No separate package, no versioning, no Storybook. Just shared primitives. Your tech lead is right that raw utility sprawl creates problems. You're right that a formal design system is overkill. Neither of you is describing the cheap middle path.

## Top risks
1. Utility sprawl — `text-sm font-medium text-gray-700 px-3 py-1.5 rounded` independently in 40 places → 40 things to update when palette shifts. Happens fast on internal tools because nobody's watching.
2. Premature abstraction — building a DS before you know your UI patterns means abstracting the wrong things. Internal tools have weird specific UIs. Let patterns emerge 2-3 weeks first.
3. Opportunity cost — time on design infra for 50 engineers is time not on the features those 50 need. Internal tools live or die on utility, not polish.

## Recommended change
Week 1-2: raw Tailwind is fine, ship features. When you catch yourself copy-pasting the same utility string more than twice across files, extract it into a component in `/components/ui/` (same repo, no package, no versioning). You'll end up with ~10 components naturally. Total cost ~4-6 hours spread over a month. Beats both a formal DS (days-weeks) and utility chaos (hours of future pain per refactor).

## Confidence
7/10. Changes if the tool grows (100+ users, external stakeholders, or becomes a template for other tools) — then more structure earlier.

## Weakest assumption
That this stays internal and stays small. If there's any real chance it gets demoed to customers, open-sourced, or becomes a product foundation, the tech lead's instinct deserves more weight. "Internal tool for 50 engineers" is the framing doing a lot of work — verify that's actually the ceiling.

═══════════════════════════════════════════════════════════════════
## Member 2 — Skeptic (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
The framing is wrong. "Design system vs Tailwind" is a false dichotomy — Tailwind *is* a design system (a token-based one), and a "proper design system" could mean anything from a Figma file to a full component library with Storybook, versioned npm packages, and accessibility audits. Neither you nor your tech lead is actually disagreeing about a real thing yet, because the terms aren't defined. Before this debate goes further, specify: design system = what, exactly? The more honest question is: "Should we build a shared component abstraction layer on top of Tailwind, or should engineers write utility classes directly at every callsite?" That's a real tradeoff with real costs.

## Top risks
If raw Tailwind everywhere: 50 engineers writing `flex items-center justify-between gap-4` 200 times → 200 slightly different versions; no semantic abstraction (rebrand = grep-and-pray); "internal tool" scope creep calcifies "temporary" decisions. If a "proper design system": "proper" can mean a 6-month investment before anyone ships; premature abstraction (you don't know what components you need until 3 features in); maintenance burden (an unkept component library is worse than none — a graveyard engineers route around). Shared hidden risk BOTH sides: without an agreed design-token baseline (colors/spacing/type), both approaches produce inconsistent UIs. That's the actual minimum.

## Recommended change
Stop debating the label and align on scope: (1) Define a token file (colors, spacing, type scale) — 2 hours, one place, imported by Tailwind config; non-negotiable regardless of which side wins. (2) Build components only when you have 3+ callsites for the same pattern — just-in-time extraction, not upfront design. (3) No Storybook / npm package / versioning — a `/components` folder in the same repo suffices. ~80% of the consistency benefit at ~10% of the cost.

## Confidence
Low-medium on the specific recommendation, because the right answer is highly sensitive to one unknown: how homogeneous is the UI? 90% tables+forms → ~5 components + tokens, done. Complex many-pattern product → abstraction pays off sooner. Neither framing reveals which.

## Weakest assumption
That 50 engineers is a stable, fixed number. "Internal tool for 50 engineers" is the story at the start of every internal tool that later became a platform bolted onto a product. Real question: what's the tool's expected trajectory in 18 months? "Core product surface" → undervaluing consistency; "gets replaced" → keep it cheap.

═══════════════════════════════════════════════════════════════════
## Member 3 — Architect (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
Your tech lead is right, but probably for the wrong reasons — and "design system" is the wrong frame. At 50 engineers the problem isn't visual consistency or brand; it's decision fatigue and drift. Without shared primitives, every engineer writes their own `flex items-center gap-2` button, shadow variant, spacing rhythm, focus ring. Six months in: 12 button variations, inconsistent disabled states, changing "the primary color" = full-text grep. The answer is not a design system (Storybook, tokens, visual-regression, a team — overkill). It's a thin component layer over Tailwind: Button, Input, Card, Badge, a layout primitive or two. ~20 components, ~800 lines. Each accepts explicit variant props and owns its Tailwind classes internally. Consumers write `<Button variant="destructive">`, never raw Tailwind for these. That seam is what matters.

## Top risks
1. Variant proliferation — without a component contract, every engineer adds their one inline tweak; no single place for cross-cutting changes (focus rings, radius, contrast).
2. No accessibility baseline — internal tools skip a11y; a component layer encodes keyboard nav/aria/focus once.
3. Over-engineering the counter-reaction — treating this as "build a real DS" → tokens pipeline, Figma sync, Storybook, changelog → kills momentum and validates the "overkill" instinct.
4. Coupling to Tailwind string literals — raw Tailwind in feature code makes global changes (dark mode, rebrand, density) require grepping class strings.

## Recommended change
Build a `src/components/ui/` directory (shadcn/ui is an excellent start — "Tailwind components you own, not a library you import"). 2-3 days to wrap the 10-15 elements the app uses: Button, Input, Select, Textarea, Badge, Card, Modal/Dialog, Tooltip, Table. Minimal variant-driven API. Rule: feature code writes ZERO Tailwind for structural UI elements; only imports from `/ui`. Feature-level layout (grid, page structure) can stay raw Tailwind. That's the seam: primitives owned by `/ui`, composition free-form.

## Confidence
7/10. High for a 50-engineer internal tool with a multi-year horizon. Drops to 5/10 if hard 12-month sunset, single maintainer, or strong existing informal conventions + review. Rises to 9/10 if cross-functional, grows beyond 50, or frequent turnover.

## Weakest assumption
That the 50 engineers actually follow the component boundary. The recommendation is only as good as enforcement — without a lint rule (eslint-plugin-tailwindcss / a no-raw-classname-on-native-element rule) or PR-review culture, the layer gets ignored under deadline and you get BOTH the overhead of components AND the drift of raw Tailwind. Architecture sound; weak link is the social contract.

═══════════════════════════════════════════════════════════════════
## Member 4 — Maintainer (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
For 50 engineers with rotating contributors, your tech lead is right — but "design system" is being used too loosely. You don't need a full Figma token pipeline, a Storybook instance, and a dedicated design-systems team. You need a thin constraint layer on Tailwind: a small set of shared components (Button, Input, Badge, Modal, Alert) and a tailwind.config that encodes your actual palette and spacing scale. ~2 days, not a quarter. The real question is not "design system vs utilities" — it's "how much uncoordinated copy-paste can you absorb before cleanup costs more than prevention." 50 engineers writing raw utilities → the tenth writes a different hover state, the twentieth adds an off-palette color; in two years, 40 variants of 3 button styles, none accessible, each owned by no one.

## Top risks
1. Consistency drift compounds silently — no one breaks it; it degrades incrementally until refactoring is a multi-week project with no owner and no business justification.
2. Dark mode / theming retrofits are brutal on raw utilities — scattered `bg-gray-800 text-white` → touch hundreds of files; CSS vars via Tailwind config = one-line change.
3. Accessibility debt accumulates fast — focus rings, contrast, ARIA handled differently or not at all; a shared Button enforces once.
4. Onboarding cost — utility-only codebase has no map; a thin component library is documentation that runs.
5. Copy-paste divergence creates fake DRY — engineers copy a card/modal, tweak it; two slightly different versions neither gets cleaned up.

## Recommended change
Don't build a design system. Build a component kit: `components/ui/` with 8-12 shared primitives, Tailwind config that pins color/spacing tokens, and a one-page doc ("use these, not raw utilities for interactive elements"). 2-3 days. Enforce via code-review norms, not tooling. Revisit scope at 6 months. Extract Button, Input, Select, Badge, Alert, Card, Modal, a typography scale. Everything else stays utility-first. Goal isn't perfect abstraction — it's a shared vocabulary for the 10 patterns all 50 reach for independently.

## Confidence
Medium-high. The failure mode (utility drift at team scale) is well-documented and plays out predictably. Uncertainty is this team's review discipline — strong reviewers survive utility-only longer.

## Weakest assumption
That the tool will actually have rotating contributors and not effectively be owned by 3-4 people who develop shared taste organically. If 4 engineers write 90% of the UI and communicate daily, the coordination problem shrinks and raw utilities become much more defensible. Check who actually contributed to the last 3 frontend features before deciding.

═══════════════════════════════════════════════════════════════════
## Member 5 — Devil's Advocate (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
Your tech lead is right, and the "50 users" framing is the wrong axis. The relevant number is 50 engineers *contributing code*, not 50 users consuming the product. A design system exists primarily to coordinate contributors, not to impress end-users. At 50 contributing engineers — even part-time — you'll have dozens independently solving identical UI problems, and Tailwind utilities give each maximum freedom to diverge. That divergence is the cost, and it compounds silently until it becomes a refactor.

## Top risks
- Consistency erosion through copy-paste amplification — utilities look readable so engineers copy snippets rather than reference an abstraction; six months → seven button variants, nobody made a wrong decision, they each made *a* decision; reconciling is harder than one `<Button>` upfront.
- The "just Tailwind" rule gets violated unevenly — engineers who care build components anyway, locally, with their own conventions → a shadow incoherent design system nobody owns, instead of a real one someone does.
- Accessibility/interaction states fall through the cracks — shared component enforces aria/keyboard/focus once; raw utilities require every engineer to remember every time.
- Tailwind verbosity makes diffs/reviews noisy — 14 inlined classes vs `<FormField>`; for a tool 50 engineers will modify, review quality matters.
- Dark mode / theming → sitewide search-and-replace; CSS custom properties in a token layer are trivially updated.

## Recommended change
Don't build a full Storybook-backed design system. Build a thin component layer over Tailwind — 10-15 primitives (Button, Input, Badge, Card, Modal, Table, FormField, Alert, Spinner, Tooltip). They use Tailwind internally (keep velocity) but encapsulate the decisions otherwise made 50 different ways. ~2-3 days to scaffold, saves weeks of drift cleanup. You're not building a design system; you're building a vocabulary for your specific app.

## Confidence
High (8/10). The argument against a full Figma-specced, versioned, multi-package design system at this scale is valid. The argument against *any* abstraction on top of raw utilities at 50-engineer contributor scale is not. The tech lead draws the right line, even if "design system" is doing too much work.

## Weakest assumption
That 50 engineers will actually contribute meaningfully to this tool's UI. If it's realistically 4-5 frontend-aware engineers and the rest only touch backend services, the drift risk drops sharply and the asker's lean becomes more defensible. The case for a component layer scales with the number of people who write JSX, not the number who click buttons.

═══════════════════════════════════════════════════════════════════
## PEER REVIEW SCORES — 5 haiku-4.5 reviewers, NEUTRAL grading frame
═══════════════════════════════════════════════════════════════════
# reviewer_event: 5/5 reviewers returned, 0 REFUSALS (neutral frame; cumulative 0/65 across Q27–Q59 + Q02).
# anonymization: Answer1=M1 Pragmatist, Answer2=M2 Skeptic, Answer3=M3 Architect, Answer4=M4 Maintainer, Answer5=M5 Devil's Advocate.
# per-reviewer 4-axis totals (max 20):
#            R1   R2   R3   R4   R5    SUM   AVG
# M1 (A1)    17   19   15   15   15     81   16.2
# M2 (A2)    17   19   17   17   17     87   17.4
# M3 (A3)    16   17   16   16   16     81   16.2
# M4 (A4)    18   18   15   15   15     81   16.2
# M5 (A5)    19   20   19   18   19     95   19.0
# top-votes:    M5 ×5 (UNANIMOUS). bottom-votes: M1 ×3, M2 ×1, M3 ×1.

peer_standing:
  M5_Devils_Advocate: 19.0   # TOP, unanimous 5/5 top votes — "50 engineers CONTRIBUTING CODE, not consuming, is the axis; a design system coordinates contributors" + thin-component-layer-as-vocabulary
  M2_Skeptic: 17.4           # "false dichotomy / define design system = what / token baseline is the actual minimum / build at 3+ callsites"
  M1_Pragmatist: 16.2        # cheap middle path + extract-on-second-use; carries the strongest form of the asker's caution (premature abstraction, opportunity cost, "is 50 the ceiling")
  M3_Architect: 16.2         # thin layer over Tailwind, shadcn/ui, the /ui-owns-primitives seam
  M4_Maintainer: 16.2        # component kit + tailwind.config tokens + review-norm enforcement; drift compounds silently

convergence_note: |
  STRONG convergence — all 5 land on the SAME answer: a thin shared component layer over Tailwind (8-15 primitives +
  pinned design tokens), NOT a full design system, and the tech lead is directionally right while "design system" is the
  wrong/loose label. INVERTED-DISSENT setup (cf. Q38/Q47/Q32): the Devil's Advocate — tasked with arguing AGAINST the
  asker's "skip the design system" lean — produced the council's SHARPEST framing ("the relevant number is 50 engineers
  CONTRIBUTING CODE, not 50 users consuming; a design system coordinates contributors") and was peer-rated STRONGEST
  (19.0, unanimous top). So the contrarian-to-the-asker view IS the consensus. Chairman → LEAD with the DA reframe + the
  thin-layer recommendation (+ M2's token-baseline-is-the-minimum + M1/M4's extract-on-2nd-use + M3's /ui seam), and
  preserve the GENUINE MINORITY = the asker's original lean defended at full strength (the conditions under which deferring
  abstraction / staying utility-first actually wins: only 4-5 people really write UI, requirements still shifting fast,
  tool likely replaced in ~2yr → premature/ wrong abstraction costs more than duplication). Pragmatist (M1) carries that
  caution most explicitly.
