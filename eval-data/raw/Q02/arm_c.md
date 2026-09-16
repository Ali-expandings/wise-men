# Q02 Arm C — Chairman synthesis
# salvaged_from_context: false
# generated: 2026-05-31 (clean rerun — pilot Q02 was context-only)
# CHAIRMAN MODEL: sonnet-4.6 (spawned as sonnet subagent for model parity — main thread was opus-4-8)
# members: 5 × sonnet-4.6 | reviewers: 5 × haiku-4.5 (neutral grading frame, 0 refusals) | chairman: 1 × sonnet-4.6 subagent
# eval tier: standard | composite 2 | label: council-shaped | domain: engineering | Opus-DA rule SUSPENDED (model parity) | no flags
# engineering personas: Pragmatist / Skeptic / Architect / Maintainer / Devil's Advocate
# peer standing: Devil's Advocate 19.0 (TOP, unanimous top votes) / Skeptic 17.4 / Pragmatist 16.2 / Architect 16.2 / Maintainer 16.2. INVERTED-dissent (DA peer-STRONGEST).
# note: STRONG convergence (all 5 → thin component layer over Tailwind, not a full design system; tech lead directionally right). INVERTED-dissent (cf. Q38/Q47): the DA — arguing against the asker's "skip the design system" lean — produced the sharpest framing ("50 engineers CONTRIBUTING CODE not consuming is the axis") and was peer-strongest, so the contrarian-to-asker view IS the consensus. Chairman LED with it + preserved the asker's defer-abstraction instinct (4-5 real UI contributors / fast-shifting reqs / ~2yr-replace → duplication beats wrong abstraction) as a full dissent block.
# dissent precedence: dissent >3 sentences → full block.

## Council answer

The framing "50 users" is the wrong axis. The relevant number is 50 engineers contributing code — a component layer exists to coordinate contributors, not to impress end-users. At that contributor count, raw Tailwind utilities give each person maximum freedom to diverge independently. That divergence compounds silently: seven button variants emerge, a11y/focus states fall through the cracks on whoever's in a hurry, dark-mode becomes a sitewide search-and-replace, and PR diffs fill with color string debates. You end up with a shadow design system nobody owns. Your tech lead is directionally right. A *full* design system (Storybook, Figma handoff, versioned npm package, a11y audit pipeline) is overkill. But "just Tailwind everywhere" is not the safe default it appears to be.

The minimum non-negotiable — regardless of which side wins — is a token baseline in `tailwind.config`: your color palette, spacing scale, and type scale locked in one place. Without this, both approaches produce inconsistent UIs, and the "design system vs no design system" argument is moot. Do this first, today. It costs two hours.

The real deliverable is a thin `/components/ui` folder, not a package, not a library, not versioned — just local files in the same repo. Roughly 10-15 primitives: Button (with variants), Input, FormField, Badge, Card, Modal, Table, Alert, Spinner, Tooltip. These own their Tailwind classes internally. Feature code imports from `/ui` for structural elements and stays free to compose with Tailwind at the layout/feature level. The seam that matters: nobody writes raw `className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded"` for a button in a feature file — they write `<Button variant="primary">`. This is two to three days of work, saves weeks of drift cleanup, and the natural forcing function for extraction is second-use: write Tailwind inline the first time, extract on the second copy-paste. Use shadcn/ui as a starting scaffold if you want primitives you own rather than a black-box dependency.

One sharp caution from the Architect: the layer is only as good as its enforcement. Without a lint rule banning raw structural Tailwind in feature files, or consistent PR review culture that catches it, you will get both the overhead of maintaining `/ui` and the drift of people bypassing it under deadline. Either wire up an ESLint rule or make "did you use the ui component?" a standing PR checklist item. The component folder with no enforcement is worse than either pure alternative.

## Dissent worth keeping

The asker's instinct has legitimate force under specific conditions. If only four or five people realistically write frontend code — not 50 engineers occasionally touching a form — and they coordinate daily with organic shared taste, the cost of duplication is near zero and the cost of the wrong abstraction is real. Extracting a component before the usage pattern is stable means abstracting the wrong shape, then maintaining that abstraction through two rounds of requirement changes, then eventually deleting it. Duplication is cheaper than the wrong abstraction.

Additionally: if the tool is genuinely likely to be replaced, rewritten, or deprecated within two years (common for internal tooling), and if requirements are still shifting fast enough that the UI contract hasn't stabilized, deferring the component layer entirely is defensible. The calculus changes only when contributor count is real and the tool has proven longevity. Before committing, make the explicit bet: how many people have actually committed frontend changes in the last three months, and is this tool still going to be running in 2027? If the honest answer is "four people, probably gets rewritten," the asker is right and the tech lead is pattern-matching to a larger-scale problem that doesn't apply here.

## Confidence

High confidence on the structural answer (token baseline + thin local component layer + second-use extraction rule) — this is the convergence of four independent analyses with strong peer ratings. The dissent is also high confidence on its conditional: the asker needs to verify the real contributor count and trajectory before committing either way.
