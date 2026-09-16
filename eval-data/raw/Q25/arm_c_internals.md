# Q25 Arm C internals — members + peer reviews (pre-chairman)
# salvaged_from_context: false
# generated: 2026-05-31 (clean rerun — pilot Q25 was context-only)
# domain: research | composite: 5 | label: single-prompt-shaped | tier: standard | personas: Empiricist / Theorist / Methodologist / Integrator / Devil's Advocate
# members: 5 × sonnet-4.6 | reviewers: 5 × haiku-4.5 (NEUTRAL grading frame) | chairman: sonnet-4.6 subagent (recorded in arm_c.md)
# validator: all 5 members returned the 5-section structure, none OUT OF DOMAIN. PASS.
# anonymization for reviewers: M1=Empiricist, M2=Theorist, M3=Methodologist, M4=Integrator, M5=Devil's Advocate
# note: composite-5 single-prompt-shaped research Q. Strong convergence on MULTI-CAUSAL/overdetermined answer (QRP+winner's-curse+publication-bias INTERACTING with genuine construct-invalidity + context-non-invariance). Sharpest split = Methodologist ("fix stats → fixed") vs Theorist/DA ("ontological: social objects don't sit still; stats reform necessary-not-sufficient").

═══════════════════════════════════════════════════════════════════
## Member 1 — Empiricist (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
The replication data points to a multi-causal failure, not a single villain. OSC 2015 found ~36% of 100 studies replicated at p<.05, median effect ~half the original. Many Labs 1: some effects replicate near-universally (anchoring, flag priming), others collapse by site. Many Labs 2: lab variation explains almost none of the variance — the effect itself is unstable. Registered Replication Reports on classics (ego depletion d ~0.62→~0; behavioral priming largely absent; facial feedback mixed) show the most "robust" effects failed hardest. Not random noise — systematic: large original effects from small samples in single labs fail most; small effects from large registered studies tend to survive. P-hacking/publication bias are real and measurable (p-curve, the spike just below .05, Ioannidis), but cannot explain ALL failures: for ego depletion and many priming effects, pre-registered N-in-thousands replications find effects indistinguishable from zero → those weren't attenuated, they were artifacts. Deeper structural issue: psychology studied context-dependent, population-sensitive, historically-contingent phenomena using methods built to detect universal laws; the WEIRD single-lab design can't distinguish "robust effect" from "local regularity in one context."

## Top risks
1. Survivor bias reading successes — surviving effects cluster in low-level cognition; the higher-order social effects that inform policy are disproportionately the failures.
2. Decline effect is documented (Schooler 2011; Jennions & Møller) and not fully explained by regression to the mean — some may be genuine historical contingency.
3. Replications can fail for legitimate reasons (population diffs) — weaponized defensively; Many Labs multi-site design controls for it and mostly confirms failure.
4. The "conceptual replication" norm created an unfalsifiability structure (failing the exact procedure = testing a "different" hypothesis).
5. N required for stable estimates in moderator-rich domains is orders of magnitude beyond standard lab budgets.

## Recommended change
Move from binary "did it replicate y/n" to estimating the posterior distribution of effect sizes across contexts/populations/operationalizations before claiming robustness. Require Bayesian or equivalence-testing pre-registration for any effect informing intervention/policy, minimum N set by the smallest effect size of interest (not convenience). The Many Labs model — simultaneous multi-site pre-registered replication as a condition of high-status publication — is the only design that has produced stable trustworthy estimates; it is expensive and rarely used, and the cost IS the answer to how robust the knowledge base is.

## Confidence
Moderate-high on multi-causality; high that the effect-size-halving pattern is real and not a replication-method artifact (consistent direction/magnitude across programs). Low-moderate on the relative weight of each cause — cannot tell from data alone what fraction of failures are pure artifacts vs genuinely context-dependent true effects, because that decomposition requires knowing the true effect size, which is what's in dispute.

## Weakest assumption
That "failed to replicate" and "original was wrong" are equivalent. The data consistently show originals were overestimates; not always that the true effect is zero. If ego depletion is a real-but-small effect (d~0.1) under specific motivational conditions, a replication not designed to optimize those conditions might correctly return ~zero while the original was a real phenomenon catastrophically mischaracterized in magnitude/generality. Data don't cleanly separate "never existed" from "much smaller + more conditional than claimed" — and that distinction decides whether the field needs rebuilding or recalibrating.

═══════════════════════════════════════════════════════════════════
## Member 2 — Theorist (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
The crisis is not primarily fraud/p-hacking (those exist) — it is construct under-determination colliding with sampling from a non-ergodic social world. Most social-science effects are not natural kinds; they are constructs stabilized within a particular measurement apparatus, population slice, and historical moment. Replicating "the same study" is not re-sampling the same generative process — it draws from a different node in a causally heterogeneous system while assuming the node is interchangeable. The effect was real the first time; it is also real the second time; they are just not the same effect. Duhem-Quine is central: (Theory ∧ Aux₁…Auxₙ) → Observation; failure licenses rejecting the conjunction, not theory alone. "Ego depletion fails to replicate" may mean the glucose-candy operationalization was load-bearing auxiliary content that stopped being true, or the 2016 subject pool differs from the 2000 pool in construct-relevant ways. Stability-of-kinds problem physics escapes: the electron does not read papers about itself; human subjects do — effects built on participants' implicit theories are partly constituted by the cultural scaffolding that produces them.

## Top risks
1. Conflating measurement failure with theoretical failure ("power poses don't raise testosterone" could be wrong-pathway OR bad-proxy OR construct-not-indexed-by-testosterone-in-all-populations) — investigators/journalists collapse these.
2. Over-weighting the file-drawer/p-hacking story produces bad epistemics: if all failures = "original false positive," you'd predict large-N pre-registered effects replicate ~100%; they don't.
3. Treating heterogeneity of effect sizes as noise when it may be signal (a moderator) — meta-analytic averaging to zero destroys the information that the effect is real under some conditions.
4. Assuming ergodicity: between-subjects variance applied as if it describes within-person dynamics — non-ergodic systems don't replicate in the standard sense even when the theory is correct.

## Recommended change
Formally separate four kinds of replication failure and report which occurred: MEASUREMENT (operational def no longer tracks construct), POPULATION (sample-equivalence auxiliary violated), TEMPORAL (the phenomenon itself changed), THEORETICAL (the mechanism never existed — the p-hacking/false-positive case). Pre-registration helps only the last; the first three require construct-validity audits, explicit sampling theory, and longitudinal tracking of construct stability. Without this taxonomy the field is stuck in all-or-nothing epistemics, the wrong frame for a science of historically situated, self-interpreting agents.

## Confidence
Moderate-high that construct under-determination + auxiliary fragility do more explanatory work than p-hacking alone. Moderate that this specific taxonomy is the right decomposition. Low that the field adopts the distinction (incentives reward clean replicate/not-replicate headlines).

## Weakest assumption
That "the effect was real the first time" in any theory-laden sense — that a stable underlying process existed that the original tracked. The alternative: many originals are genuine false positives from underpowered + flexible-analysis regimes, and the construct-validity framing is a sophisticated post-hoc rationalization that lets original researchers off the hook. I lean against (heterogeneity patterns look like moderated effects, not pure noise) but can't rule it out, and the p-hacking account is simpler. Occam cuts both ways.

═══════════════════════════════════════════════════════════════════
## Member 3 — Methodologist (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
Failures are overdetermined — multiple independent mechanisms all push the same way, so "robust" published effects were structurally guaranteed to be inflated even without misconduct. Correct framing: not "fraud exposed" but "the epistemic infrastructure was misconfigured from the start." Published effects are a censored sample (only p<.05 passes). Given most tested hypotheses are false (base-rate problem) and typical social-psych N≈50-100/cell, the PPV of a single significant finding is shockingly low. Ioannidis (2005): prior ~10%, α=.05, 80% power → PPV ~64% — and social-psych power was rarely 80%. Button et al. (2013): median power ~8-31%. At 30% power + 10% base rate, PPV ~41% → majority of published positives false. Winner's curse compounds: conditional on a true effect surviving the filter at low power, observed effect size is inflated by ~1/power — at 25% power, published estimates average ~4× the true effect. This is not p-hacking; it is a mathematical consequence of selection on noisy estimates. Replications with better power estimate closer to truth → looks like "failure," is actually regression to a less-biased estimate.

## Top risks
1. Winner's-curse inflation is quantitatively large and invisible pre-replication (median power ~0.35 → boundary inflation ~1.25×, worse deep in the tail).
2. Conceptual vs direct replication conflation — conceptual-replication failure is epistemically ambiguous; Many Labs (direct, multisite) is more informative and shows lower failure for well-powered originals (~60-70%), suggesting some failures are construct-boundary, not pure false positives.
3. Measurement reliability ceiling: r=.60 reliability caps true-score correlation at √.60≈.77, attenuating further in independent samples; many social-psych scales sit α≈.65-.75.
4. Contextual sensitivity is a genuine scientific property, not an excuse (priming/ego-depletion may be real-in-context but not generalizable — a scope-condition finding invisible when single-lab WEIRD studies were treated as universal laws).
5. File drawer inflates literature-level effect sizes (ego depletion: Hagger et al. 2016 pre-reg d≈0.04 vs original d≈0.62 → file drawer can account for nearly all of a cited effect).

## Recommended change
Highest-leverage change: pre-registration with POWERED designs — forces a-priori effect-size specification → honest confrontation with N. For α=.05, power=.90, realistic d=.30 → N≈234/group; legacy studies used ~30-40/group (powered only for d≈.65) → the inflation correction alone predicts the ~50% effect-size shrinkage observed. Secondary: distinguish direct vs conceptual replication in reporting; specify scope conditions before data collection. Third: Bayesian/equivalence testing so "small but real" and "negligible" are distinguishable, collapsing the binary pass/fail frame.

## Confidence
Moderate-high on the structural diagnosis (winner's curse + low power + publication bias as primary drivers — math uncontested, Many Labs/OSC fit quantitative predictions). Lower on the proportion attributable to p-hacking vs structural inflation vs genuine context-specificity (best rough estimate: ~40% winner's-curse/low-power, ~30% publication bias, ~20% genuine context-specificity, ~10% outright p-hacking — mechanisms interact). Lowest on whether pre-registration alone suffices (multi-site pre-registered designs more powerful but face coordination costs).

## Weakest assumption
That the base rate of true hypotheses in social psych is low enough to make the PPV math alarming (prior ~10-20%). Hard to verify directly; strongest evidence it's low comes from the replication data itself (circular but informative) + that the worst-failing literatures (social priming, ego depletion) were theory-driven loosely enough to motivate almost any directional prediction — a low effective prior, exactly the condition that makes the winner's curse catastrophic.

═══════════════════════════════════════════════════════════════════
## Member 4 — Integrator (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
Both mechanisms are real, both large, and they MULTIPLY rather than add. Not primarily bad actors — a measurement paradigm brittle by design, applied to genuinely context-sensitive phenomena, inside an incentive structure that punished honesty. Strip out every QRP and you still have a replication problem, because social phenomena lack the invariant causal structure the NHST + small-N + single-lab paradigm assumed. Rough decomposition: QRP artifacts explain most of the MAGNITUDE INFLATION (d=0.5+ → ~zero); genuine context-sensitivity/construct non-invariance explains most DIRECTIONAL REVERSALS and moderator explosions. They compound: inflated effect sizes created false confidence the effect was large enough to detect anywhere, which suppressed curiosity about boundary conditions; when replications finally ran, investigators discovered simultaneously that the true effect is much smaller AND highly localized — and you can't cleanly separate these post-hoc.

## Top risks
1. Over-attributing to QRPs exonerates the deeper epistemology → field generates well-powered pre-registered studies of locally-real-but-globally-non-invariant effects and replication stays disappointing, just more expensively.
2. Over-attributing to context-sensitivity becomes a shield for weak findings ("real, just context-dependent" is unfalsifiable if boundary conditions are post-hoc — HARKing with extra steps).
3. The interaction term is underappreciated (small true effect × high context-sensitivity × publication bias compounds worse than any single component).
4. Construct validity is the neglected pillar (most debate is statistical validity; many famous effects have logically-prior construct-validity problems).
5. Theory impoverishment sustains the cycle (findings accumulated faster than theories specifying when effects should hold → every replication is a random draw from an underspecified distribution).

## Recommended change
Stop treating "does it replicate" as binary; replace with a structured per-effect decomposition: (a) effect-size deflation audit (original N, pre-reg?, PET-PEESE bias-corrected true effect); (b) construct-invariance check (does the IV/DV operationalization hold meaning across the replication's population/context?); (c) boundary-condition mapping via registered replication reports with systematic moderator variation (not single-lab exact replication); (d) theory accountability (any published effect must come with a theoretical account making ≥1 novel moderator prediction, tested in original or registered follow-up). Goal: distinguish "false positive produced by QRPs" from "real but mischaracterized as a main effect when it's actually a substantial interaction" — different failures, different fixes.

## Confidence
Medium-high on the compound diagnosis (60-70%); almost certainly closer than either monocausal story. Lower on proportional attribution (QRP-inflation vs genuine context-sensitivity are confounded in the historical record; no clean natural experiment). Dampened further because meta-science itself has replication issues + incentive distortions toward dramatic failure findings.

## Weakest assumption
That context-sensitivity and QRP artifacts are independent inputs that multiply. They may be endogenous: labs that used QRPs may have done so precisely BECAUSE they worked with highly context-sensitive phenomena where true effects were small and hard to detect — making QRP behavior a rational response to phenomenon fragility, not purely bad incentives. If so, cleaning up statistics without improving theoretical specification of boundary conditions reduces QRP-driven false positives but won't substantially raise replication rates for context-sensitive constructs — the epistemological reform must accompany the statistical reform, not follow it.

═══════════════════════════════════════════════════════════════════
## Member 5 — Devil's Advocate (sonnet-4.6)
═══════════════════════════════════════════════════════════════════

## Core judgment
The statistics-cleaning narrative is seductive and partially correct but ultimately insufficient. The crisis reveals what the p-hacking story cannot account for: even pre-registered, adequately powered replications of theoretically coherent effects fail — not because originals cheated, but because the effects genuinely behave differently across populations, historical moments, and cultural contexts. The deeper problem: psychology has been selling universal laws about objects that are moving targets. Priming, ego depletion, stereotype threat, social comparison are not broken clocks awaiting better measurement — they are real phenomena whose magnitude, direction, and even existence is constitutively shaped by the context studied. The failure is a category mistake baked into the program: assuming human psychological responses admit context-independent regularities like physical constants. Henrich/Heine/Norenzayan's WEIRD critique (2010) was understated — the undergraduate sample wasn't merely narrow, it was drawn from a historically anomalous, high-individualism, post-industrial population during a specific window. Replicating a 1980s conformity study on a 2023 Prolific cohort is a different experiment on a different population in a different historical context; the null is not a refutation, it is a datum about context-dependence.

## Top risks
1. The argument gets weaponized as a get-out-of-jail-free card — if every failure is "context changed," nothing is ever falsified; the ontological argument collapses into post-hoc rationalization (the stats reformers are right to be suspicious).
2. Confusing "context-dependent" with "not real" — context-dependence ≠ non-existence; failing to replicate a specific effect size doesn't make the phenomenon zero; a science that only produces context-free findings misses most of what matters about human behavior.
3. The "moving target" problem means current reforms are necessary but not sufficient — pre-reg + larger N detect whether an effect is present in your sample at your moment, not whether it generalizes or how to map boundary conditions; better microscopes for continuously-evolving specimens.
4. Journals/funders haven't updated incentives to reward boundary-condition cartography (boring, expensive, hard to publish, no clean narrative).

## Recommended change
Adopt an explicitly population- and time-indexed approach: report findings not as "effect X exists" but as "effect X, magnitude Y, observed in population Z during period T under conditions C" — as epidemiology treats risk factors and ecology treats population dynamics. Abandon universal-law rhetoric for a CARTOGRAPHY of effects (systematically map where/when phenomena obtain). Practically: fund multi-site, multi-cohort replications DESIGNED to measure heterogeneity (not just "does it replicate"); the Many Labs projects began this but were still framed around the binary. And require theoretical frameworks that make context-dependence a first-class prediction, not a post-hoc escape hatch — if your theory can't predict boundary conditions in advance, it isn't a good theory regardless of your statistics.

## Confidence
Moderately high that context-dependence is a genuine, underappreciated structural feature (not just noise). Moderate that it's THE primary driver (vs a major co-contributor alongside QRPs). Low on what institutional solutions would actually work (universal-law storytelling is deeply embedded in careers/grants/journalism).

## Weakest assumption
That "context-dependence" is a coherent explanation rather than a label for our ignorance. If effects can shift sign or vanish across populations/time, it's hard to distinguish "real but context-bound" from "never real, original was noise" — exactly where the stats reformers press hardest. For context-dependence to be scientific not rhetorical, the field must specify IN ADVANCE which contexts activate the effect; as long as that's post-hoc, the ontological argument is indistinguishable from motivated reasoning. This is the knife edge the position sits on.

═══════════════════════════════════════════════════════════════════
## PEER REVIEW SCORES — 5 haiku-4.5 reviewers, NEUTRAL grading frame
═══════════════════════════════════════════════════════════════════
# reviewer_event: 5/5 reviewers returned, 0 REFUSALS (neutral frame; cumulative 0/70 across Q27–Q59 + Q02 + Q25).
# anonymization: Answer1=M1 Empiricist, Answer2=M2 Theorist, Answer3=M3 Methodologist, Answer4=M4 Integrator, Answer5=M5 Devil's Advocate.
# per-reviewer 4-axis totals (max 20):
#            R1   R2   R3   R4   R5    SUM   AVG
# M1 (A1)    18   18   18   18   18     90   18.0
# M2 (A2)    17   17   17   16   17     84   16.8
# M3 (A3)    17   17   18   18   17     87   17.4
# M4 (A4)    18   18   19   19   17     91   18.2
# M5 (A5)    15   17   17   17   17     83   16.6
# top-votes:    M1 ×5 (UNANIMOUS). bottom-votes: M2 ×4, M5 ×1.

peer_standing:
  M4_Integrator: 18.2        # TOP composite — "both mechanisms MULTIPLY not add; QRP→magnitude inflation, context-sensitivity→directional reversals; they compound"; per-effect decomposition (deflation audit / construct-invariance / boundary mapping / theory accountability)
  M1_Empiricist: 18.0        # 5/5 TOP votes (most resonant) — the data (OSC 36%, ego depletion 0.62→~0, Many Labs instability); "the most robust failed hardest"; posterior-distribution-not-binary
  M3_Methodologist: 17.4     # the quantitative WHY (winner's curse ~1/power, PPV math, median power ~35%, the ~50% shrinkage prediction); powered pre-registration
  M2_Theorist: 16.8          # 4 bottom votes — Duhem-Quine / non-ergodic / four-failure-type taxonomy; dinged practical 3 (most abstract)
  M5_Devils_Advocate: 16.6   # peer-WEAKEST — the ontological "moving target / social objects are non-stationary / stats reform necessary-not-sufficient" + WEIRD critique + population-time-indexed reporting; dinged practical 2-3 (light on actionable levers)

convergence_note: |
  STRONG convergence on a MULTI-CAUSAL / overdetermined answer: QRP (researcher DOF + publication bias + winner's-curse
  at low power) INTERACTING/COMPOUNDING with genuine construct under-determination and context-non-invariance — directly
  answering the user's two-part question ("just p-hacking, or something deeper?") with "both, and they multiply." NORMAL
  DA pattern: the Devil's Advocate (pure ontological "moving target" view) was peer-WEAKEST (16.6, dinged hard on practical
  for offering little actionable beyond cartography), in a tight 16.6-18.2 pack. NOT inverted. Member order: Integrator 18.2
  (top composite, the compound framing) / Empiricist 18.0 (5/5 top votes, the data) / Methodologist 17.4 (the winner's-curse
  math) / Theorist 16.8 / DA 16.6. Chairman → lead with the compound diagnosis (Integrator) anchored in the data (Empiricist:
  OSC 36%, ego depletion 0.62→~0, differential subfield pattern) + the mechanistic why (Methodologist: winner's curse,
  low power → the ~50% effect-size shrinkage) + the Theorist's four-failure-type taxonomy as the operational lever; preserve
  the DA's strongest ontological claim (many social-science objects are genuinely non-stationary / context-constituted, so
  statistical reform is necessary-but-not-sufficient and the field needs population-×-time-indexed "cartography of effects")
  as the dissent — it is the substantive "something deeper" the question asks about, even though peer-rated weakest on
  actionability.
