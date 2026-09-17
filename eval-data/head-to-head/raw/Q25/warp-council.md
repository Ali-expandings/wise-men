# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q25 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 119052 | tool uses: 4 | duration: 1215s

## Council

Three members, all Claude — this harness has no GPT or open-source models, so per the skill's own fallback rule (closest available model, note the substitution) all three seats are filled with distinct Claude tiers instead of the default Opus/GPT/OSS roster:

- **Opus** — Statistical & Methodological Rigor: p-hacking, power, publication bias, what OSC/Many Labs actually found
- **Sonnet** — Institutional Incentives & Sociology of Science: why questionable research practices became normal and stayed normal
- **Haiku** — Contrarian / Deeper Epistemology: construct validity, WEIRD samples, whether psychology can have physics-style "laws" at all

All three read-only, closed-book (own training knowledge, no file or web search — question is self-contained).

## Recommendation

Both, and they're not competing explanations — they stack. P-hacking, low power, and publication bias are real, large, and well-documented, and explain a lot of the headline replication numbers on their own. But that's not the whole story: one layer down is why those statistical habits became normal and stayed normal (career incentives), and one layer past that is why "replication" is a genuinely harder yardstick for psychology than for, say, chemistry (construct validity, WEIRD samples, reflexive subjects who change behavior when studied). Reducing it to "p-hacking, now fixed by preregistration" undersells all three.

## Why

- **The statistics alone do most of the visible damage.** Letting researchers make a few defensible-looking analysis choices after seeing the data can push false-positive rates from 5% toward 60%. Median statistical power in psychology has historically sat around 35%. Combine low power with publishing only significant results and you mathematically get inflated published effect sizes with zero fraud required — matching what large replication efforts found: the 2015 Reproducibility Project replicated roughly a third of classic findings, at roughly half the original effect size.
- **But "p-hacking" as a label implies cheating, and that's mostly wrong.** Surveys of researchers who admit to these practices show most didn't feel they were doing anything improper — it was mentor-taught craft, not misconduct. That's the institutional layer: journals reward novel/positive/surprising results, tenure and grants reward publication count in those journals, and direct replication earns almost no career credit. That reward structure is why the problem was field-wide and invisible from inside, and why fixing it needs more than better statistics — a preregistration can still hide a flexible-enough hypothesis, and replication work stays structurally underfunded relative to "discovery" work.
- **Even a clean, preregistered, adequately powered study can fail for reasons that are neither fraud nor incentives.** "Ego depletion" and similar constructs bundle several different things under one name. Samples are overwhelmingly WEIRD undergraduates. An effect can be genuinely real in one decade or culture and genuinely gone in the next as media environments and subject pools shift. And psychology studies people who read about psychology findings and adjust — a reflexivity problem physics doesn't have.
- **The council split on how much weight that third layer deserves, and the split is worth keeping rather than smoothing over.** The rigor member reads most of the remaining complexity as still fundamentally statistical — pointing to a large preregistered multi-lab test of ego depletion that landed near zero, and to Many Labs 2 finding little variation across sites — and treats that as evidence against "it's just hidden moderators." The epistemics member reads that same ego-depletion result as proof the original construct was never coherent, not proof there's simply no effect. Both agree the ~200-study original literature doesn't hold up; they disagree on the mechanism.

## Tradeoffs and risks

- "Just p-hacking, now fixed" undersells the problem: undisclosed deviations from preregistered plans are still common, and even a high-profile 2023 paper claiming strong post-reform replicability drew serious controversy over whether its own analysis matched what it preregistered.
- "Psychology can't produce stable laws" oversells the problem if used to wave away every failure as a hidden moderator — that move is unfalsifiable unless backed by actual evidence of context-dependence, not just asserted after the fact.
- "It's all incentives" correctly explains why bad practice persisted and spread, but doesn't tell you which specific surviving findings are true.
- Replicability isn't uniform across the field: cognitive-psychology effects hold up much better than social-psychology effects, and within-subject designs with many trials hold up better than one-shot between-subject designs. Treat this as a question about specific subfields and designs, not "is psychology broken" as one lump question.

## Final call

Treat "failed to replicate" as a diagnostic question, not a verdict: ask whether the original finding was underpowered or analysis-flexible (statistical), whether anyone was ever incentivized to check it (institutional), and whether the construct itself might be real but context-bound (epistemic) — usually more than one applies at once. Weight confidence by subfield and design rather than by one global prior about "the replication crisis." Confidence here: high that all three mechanisms are real and independently well-evidenced; moderate on their relative share of any given failure, which is itself an open dispute inside metascience.
