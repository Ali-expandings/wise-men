# Q27 Arm C internals — 5 members + 5 reviewers
# salvaged_from_context: false
# regenerated: 2026-05-29 (fresh full pipeline)
# members: 5 sonnet-4.6 (Empiricist, Theorist, Methodologist, Integrator, Devil's Advocate)
# validator: all 5 passed (5-section contract present + non-empty + engaged)
# member outputs saved VERBATIM (no compression)
# reviewer framing: NEUTRAL grading frame (bug #6 fix — no anti-refusal / "real council" language)

==================================================================
## MEMBER: Empiricist (sonnet-4.6)
==================================================================

## Core judgment

This evidence is severely contaminated and should be treated as near-worthless for establishing genuine superiority. Benchmark selection by an interested party introduces profound degrees of freedom: the company can have iterated across dozens of candidate task sets, published only the one that favored their model, and framed this as a single clean test. Funding bias compounds the problem, since even without outright fraud, analytical choices — preprocessing, prompt formatting, metric selection, what counts as a "correct" answer — systematically drift toward the desired outcome when the people making those choices are the ones with money on the line. Fourteen tasks sounds specific and substantial, but without knowing the universe of tasks that were considered and rejected, the number is meaningless.

## Top risks

- **Cherry-picking the benchmark itself**: The 14 tasks were almost certainly selected from a larger candidate pool. Even without malicious intent, the tasks that happened to favor their model are the ones that made it into the paper.
- **Prompt and format advantages**: Benchmarks test prompts, not raw capability. The company likely tuned how they prompt their own model and may have used suboptimal prompting for GPT-4, artificially inflating the gap.
- **Training data contamination**: If the model was trained on data that overlaps with the benchmark, performance is measuring memorization rather than generalization. This is especially likely when a company designs the benchmark and trains the model.
- **Metric gaming**: The choice of what metric to report (accuracy, F1, BLEU, human preference rating, etc.) can swing results substantially. An interested party will naturally gravitate toward the metric where they look best.
- **No statistical rigor reported**: Confidence intervals and significance tests are routinely omitted in self-published benchmarks, masking whether the margin is real or noise.
- **Absence of failure disclosure**: Credible evaluations disclose where the model fails. A company benchmark has every incentive to omit or minimize those results.

## Recommended change

Commission an independent replication by a team with no financial relationship to the company: they re-run the same 14 tasks using standardized, pre-registered prompts for both models, then extend the evaluation to at least 3 external benchmark suites (e.g., MMLU, BIG-Bench Hard, HellaSwag) chosen before seeing any results, with the full evaluation plan pre-registered on OSF or a similar registry before a single inference call is made. The replication team should also run the company's original 14 tasks against a broader set of baseline models to check whether the advantage is model-specific or an artifact of the task set. Results should be reported with confidence intervals and the full distribution of per-task scores, not just aggregated wins.

## Confidence

**Medium** — the contamination risks are well-established in the benchmarking literature and the structural incentive problems are not in serious scientific dispute, but the severity of actual distortion in this specific case is unknown without access to the study materials; the model might genuinely be better on these tasks, and the honest contamination could be modest rather than decisive.

## Weakest assumption

My analysis assumes that the company actually had access to multiple candidate benchmarks and engaged in some form of selection, whether consciously or through iterative refinement — but it is at least conceivable that they designed a single benchmark de novo without cycling through alternatives, in which case the cherry-picking risk is lower than I imply, and the contamination would rest more narrowly on prompt optimization and metric choice rather than task-set selection.

==================================================================
## MEMBER: Theorist (sonnet-4.6)
==================================================================

## Core judgment

The evidence as described is severely contaminated and should be treated as near-worthless for third-party decision-making. When the entity designing the benchmark, selecting the tasks, funding the study, and reporting the results is the same entity with a commercial interest in the outcome, every layer of the research process is susceptible to Goodhart's Law: the benchmark stops measuring general capability and starts measuring whatever the company's model happens to do well. "Outperforms on 14 tasks" is a claim about a cherry-picked slice of possibility space, not a statement about the underlying construct of intelligence or usefulness the benchmark purports to represent. The number 14 sounds impressive only because we have no visibility into how many tasks were considered and discarded.

## Top risks

- **Task selection bias**: The company likely iterated on task selection — consciously or not — until the resulting benchmark favored their model's architecture, training data, or fine-tuning regime. Even without fraud, this is a structural inevitability when the selector benefits from a particular outcome.
- **Construct invalidity**: The benchmark may not measure what "outperforms" intuitively means to a user. A model can top a leaderboard on tasks that are poorly correlated with real-world utility, coherence, or safety.
- **Training data contamination**: If the company's model was trained or fine-tuned on data distributions similar to the benchmark tasks, the comparison is not between general capabilities but between memorization depth.
- **Reporting selective success**: There is no way to know whether 14 tasks represent a complete set or the winning subset of a larger, less flattering evaluation. Publication bias operates at the task level here, not just the study level.
- **Metric gaming**: The specific metrics used to score each task may have been chosen post-hoc to favor the company's model on tasks where it otherwise would have shown mixed results.

## Recommended change

Commission an independent replication using a held-out benchmark designed by a neutral third party — such as an academic lab or standards body with no equity stake — where task selection criteria are pre-registered before any model is evaluated, and where GPT-4 and the challenger model are submitted blind to the evaluators. The pre-registration requirement is the critical mechanism: it converts the evaluation from a retrospective narrative into a falsifiable prospective test, stripping away the post-hoc flexibility that makes self-published benchmarks epistemically hollow.

## Confidence

**Medium** — the contamination diagnosis is high-confidence given the structural incentives, but the actual degree of distortion could range from minor (if the company happened to be unusually rigorous) to total (if the benchmark was reverse-engineered from the model's strengths), and without seeing the methodology, precise placement on that spectrum is impossible.

## Weakest assumption

The analysis assumes that the company had meaningful control over task selection and metric design during the benchmark's development, but if the benchmark was adapted from a pre-existing, widely accepted framework with only minor modifications, the contamination is substantially lower than described — and my framing would be overstating the problem.

==================================================================
## MEMBER: Methodologist (sonnet-4.6)
==================================================================

## Core judgment

This evidence is severely contaminated and should be treated as near-worthless for the purpose of establishing genuine superiority. Benchmark selection, funding source, and the absence of any pre-registration create a near-perfect storm of motivated reasoning. The 14-task result is better understood as a marketing artifact than a scientific finding — the company almost certainly iterated on benchmark composition until it found a configuration that favored their model, whether consciously or through the ordinary human tendency to stop looking when the numbers look good.

## Top risks

- **Benchmark cherry-picking:** The company selected tasks post hoc, after knowing or estimating model performance profiles, choosing domains where their model is strong and GPT-4 is weak.
- **Training data contamination:** The evaluated model may have been trained on data that includes, or is statistically similar to, the benchmark test sets, inflating scores without reflecting genuine generalization.
- **Metric selection bias:** Within each task, choice of metric (e.g., BLEU vs. ROUGE vs. human preference) can dramatically shift relative rankings; the company chose the metrics.
- **Hyperparameter asymmetry:** The company's model was likely tuned against these specific tasks, while GPT-4 was evaluated off-the-shelf with no comparable optimization opportunity.
- **Publication bias / unreported comparisons:** We see 14 tasks where they won; we do not see the tasks where they ran evaluations and lost.
- **Absence of confidence intervals and significance testing:** Even if the setup were fair, without statistical rigor, small numerical advantages are noise, not signal.

## Recommended change

The single highest-leverage fix is **third-party pre-registered evaluation on a held-out benchmark the company did not select**. Concretely: an independent lab (no funding relationship with either company) should pre-register the full evaluation protocol — task selection criteria, metrics, prompt templates, model versions, and inference settings — before running any evaluations. The benchmark should either be one the company demonstrably had no access to during training, or should include a contamination audit (n-gram overlap analysis between training data and test sets). Results should be reported with confidence intervals across multiple runs, and the raw outputs should be released publicly so the community can re-evaluate. Funding should come from a neutral party, or at minimum the funder should have no stake in either model's commercial success.

## Confidence

**High** — the failure modes described are well-documented in the AI evaluation literature (see the consistent pattern of benchmark saturation once companies target specific leaderboards), and the structural conditions here (self-selected benchmark, self-funded study, no pre-registration) are precisely the conditions that reliably produce inflated, non-replicating results.

## Weakest assumption

The weakest assumption in my analysis is that the company actually had meaningful latitude to select the benchmark after observing performance — if the 14 tasks were chosen for domain-coverage reasons that were genuinely independent of model performance profiles, and if that selection process is documented and auditable, the cherry-picking concern weakens substantially. My framing assumes motivated selection, but it is logically possible (though empirically rare in commercial AI evaluation) that the benchmark composition was fixed on principled grounds before any model comparison was run.

==================================================================
## MEMBER: Integrator (sonnet-4.6)
==================================================================

## Core judgment

This evidence is heavily contaminated and should be treated as marketing material rather than scientific data. Self-selected benchmarks combined with self-funded studies create two compounding biases: the company almost certainly iterated on task selection until they found a favorable set, and the evaluation methodology faces no adversarial scrutiny. A calibrated reader should update only weakly toward "this model has some genuine strengths in some domains," while remaining agnostic about comparative general capability. The 14-task framing is particularly suspicious — it is specific enough to sound rigorous but small enough to be cherry-picked without difficulty.

## Top risks

- **Task selection bias**: The company chose which 14 tasks to publish, almost certainly after exploring a larger space. Tasks where GPT-4 won likely never made the report.
- **Metric gaming**: Benchmark metrics can be optimized directly during training if the company had access to the benchmark design during model development, which self-funded studies make structurally possible.
- **Evaluation leakage**: The model may have seen benchmark-adjacent data during training, inflating scores in ways a third-party auditor would catch.
- **Publication bias within the study**: Even within the 14 tasks, specific prompt formulations, shot counts, or temperature settings may have been tuned to favor the challenger.
- **No adversarial replication**: Without independent researchers attempting to break the results, failure modes remain invisible.

## Recommended change

Commission a replication using a benchmark suite selected *before* either model's scores are known, by an independent third party with no financial relationship to either company, using a pre-registered evaluation protocol published to arXiv before any inference is run. Specifically: require the evaluating team to sign a data-independence attestation confirming the challenger model's training data pipeline was not informed by the benchmark's task distribution. That single structural change — pre-registration by a disinterested party — converts the evidential weight from near-zero to genuinely informative.

## Confidence

Medium — the contamination diagnosis is high-confidence, but the magnitude of actual bias is uncertain, because some self-published benchmarks do reflect genuine capability gains even when selection pressure existed.

## Weakest assumption

The analysis assumes that independent replication would be feasible and that GPT-4's scores on the same tasks are themselves unbiased baselines — but if OpenAI's own benchmarking practices have similar selection or contamination problems, the comparison degrades into noise versus noise, which would make even a clean replication less meaningful than it appears.

==================================================================
## MEMBER: Devil's Advocate (sonnet-4.6)
==================================================================

## Core judgment

Self-chosen, self-funded benchmarks are not automatically near-worthless — they carry meaningful signal precisely because the company knows their model's failure modes better than any third party does. A benchmark designed by the people who built the system is more likely to probe the edges that matter operationally, not just the edges that are easy to measure. The contamination concern is real but overstated: the correct Bayesian update is not to zero, but to discount the claimed magnitude while still treating the directional claim as informative evidence worth investigating.

## Top risks

- Cherry-picking tasks where the model was already known to excel, suppressing results on tasks where it underperforms GPT-4
- Evaluation protocol ambiguity (prompt formatting, temperature, few-shot setup) that systematically advantages the home model
- Metric selection that captures the company's training objective rather than user-relevant outcomes
- Publication bias within the study itself — 14 tasks published, unknown number of tasks quietly dropped
- Conflating "outperforms on this benchmark" with "outperforms in deployment," which is a separate empirical question

## Recommended change

Require the company to release the full evaluation harness, all raw per-task scores including any tasks that were piloted and dropped, and the exact prompts used for both models. Then have a single independent replicator — not a rival lab, but a neutral academic group — run the identical harness unmodified. This is more useful than demanding a wholly new benchmark, because it tests whether the original results hold under controlled replication rather than replacing the question entirely. If the results replicate, the self-funded origin becomes substantially less damning.

## Confidence

Medium — because the core argument (that insider knowledge can improve benchmark quality) is empirically grounded, but the degree to which any specific company actually leverages that knowledge honestly versus strategically is unobservable from the outside.

## Weakest assumption

The analysis assumes that the company's superior knowledge of their model's failure modes was used to construct a more ecologically valid benchmark rather than to construct a more flattering one — and there is no structural mechanism in the described setup that forces those two motives apart.

==================================================================
## REVIEWERS (5 × haiku-4.5, neutral grading frame)
==================================================================
# 0 refusals (5/5 scored first pass) — neutral grading frame fixed bug #6 (Q23/Q24 had 7/10 refusals with aggressive framing).
# Unanimous: strongest=Methodologist (answer_3), weakest=Devil's Advocate (answer_5).

### Reviewer 1
```rubric
answer_1_empiricist: insight=4, rigor=5, usefulness=4, risk=5
answer_2_theorist: insight=4, rigor=4, usefulness=3, risk=4
answer_3_methodologist: insight=5, rigor=5, usefulness=5, risk=5
answer_4_integrator: insight=4, rigor=4, usefulness=4, risk=4
answer_5_devils_advocate: insight=3, rigor=3, usefulness=2, risk=2
strongest: answer_3
weakest: answer_5
```
Methodologist: highest rigor + most actionable (pre-registration = pivot to falsifiable). Empiricist close but dilutes usefulness with unrelated-benchmark extension. DA underestimates researcher degrees of freedom; insider-knowledge inversion contradicts motivated-reasoning literature.

### Reviewer 2
```rubric
answer_1_empiricist: insight=4, rigor=5, usefulness=4, risk=5
answer_2_theorist: insight=5, rigor=4, usefulness=3, risk=4
answer_3_methodologist: insight=5, rigor=5, usefulness=5, risk=5
answer_4_integrator: insight=4, rigor=4, usefulness=4, risk=4
answer_5_devils_advocate: insight=3, rigor=2, usefulness=2, risk=2
strongest: answer_3
weakest: answer_5
```
Methodologist best synthesis (precise failure modes → concrete fixes). DA miscalibrates the Bayesian update; conflates "insider knowledge of failure modes" with "incentive to hide them" — category error.

### Reviewer 3
```rubric
answer_1_empiricist: insight=4, rigor=5, usefulness=4, risk=5
answer_2_theorist: insight=4, rigor=4, usefulness=3, risk=4
answer_3_methodologist: insight=5, rigor=5, usefulness=5, risk=5
answer_4_integrator: insight=3, rigor=3, usefulness=3, risk=4
answer_5_devils_advocate: insight=3, rigor=2, usefulness=2, risk=2
strongest: answer_3
weakest: answer_5
```
Methodologist tightest diagnosis (post-hoc selection, metric bias, hyperparameter asymmetry) + HIGH confidence anchored to replication failures. DA treats insider knowledge as integrity-enhancing rather than capability-obscuring.

### Reviewer 4
```rubric
answer_1_empiricist: insight=4, rigor=5, usefulness=4, risk=5
answer_2_theorist: insight=5, rigor=4, usefulness=3, risk=4
answer_3_methodologist: insight=5, rigor=5, usefulness=5, risk=5
answer_4_integrator: insight=4, rigor=4, usefulness=4, risk=4
answer_5_devils_advocate: insight=3, rigor=3, usefulness=3, risk=2
strongest: answer_3
weakest: answer_5
```
Methodologist strongest (diagnosis→fixes, front-loads held-out benchmark selection). DA undersells contamination; conflates theoretical possibility with empirical likelihood.

### Reviewer 5
```rubric
answer_1_empiricist: insight=4, rigor=5, usefulness=4, risk=5
answer_2_theorist: insight=4, rigor=4, usefulness=3, risk=4
answer_3_methodologist: insight=5, rigor=5, usefulness=5, risk=5
answer_4_integrator: insight=4, rigor=4, usefulness=4, risk=4
answer_5_devils_advocate: insight=3, rigor=3, usefulness=2, risk=2
strongest: answer_3
weakest: answer_5
```
Methodologist strongest (perfect-storm framing + highest-leverage fix + appropriate high confidence). DA conflates "knowing failure modes" with "designing unbiased benchmarks"; release-and-replicate doesn't address post-hoc metric selection or task-universe opacity.

### Reviewer aggregate (mean composite /20)
- answer_3_methodologist: 20.0  ← strongest (unanimous, perfect)
- answer_1_empiricist: 18.0
- answer_2_theorist: 15.4
- answer_4_integrator: 15.4
- answer_5_devils_advocate: 9.8  ← weakest (unanimous; "insider knowledge" counter judged miscalibrated)
# Strong consensus answer: heavily contaminated → near-worthless → pre-registered independent replication on held-out benchmark + contamination audit.
# DA = genuine minority (update non-zero, not zero) but peer-judged weak. Chairman preserves it honestly as dissent; synthesis follows the consensus.
# No council-breaking flag.
