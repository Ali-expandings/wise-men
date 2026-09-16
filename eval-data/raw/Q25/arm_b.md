# Q25 Arm B raw output
# salvaged_from_context: false
# model: sonnet-4.6
# leakage_check: CLEAN — hardened anti-spawn wrapper held; 5 internal perspectives stayed inside <thinking>; visible output = exactly 3 sections. No retry, no contamination.
# note: <thinking> block preserved here in raw; stripped during blinding.
# generated: 2026-05-31 (clean rerun)

<thinking>
P1 Empiricist: OSC 2015 ~39% replicated, replication effect ~half original. SSRP ~62%. Many Labs: huge heterogeneity. ego depletion d≈0.6→0.04; power pose, stereotype threat, facial feedback failed. Perception/memory replicate better than social priming → inconsistent with single explanation.
P2 Theorist: construct validity + theory underdetermination. "ego depletion" not a natural kind, operationalized many ways. Duhem-Quine: failure refutes the conjunction not theory alone. Gergen 1973: social psych historically contingent, not invariant laws. Even perfect stats → "failures" because phenomena aren't stable kinds.
P3 Methodologist: Gelman-Loken garden of forking paths; Simmons/Nelson/Simonsohn researcher DOF → 60% FP; publication bias / p-curve; median power ~35% → winner's curse inflates published effects; Ioannidis. Broadly-construed p-hacking explains most failures.
P4 Integrator: both true, interact. Stats inflated literature; but which effects fail tracks theoretical solidity. Smaldino-McElreath natural selection of bad science. Pre-registered studies replicate better → implicates undisclosed flexibility.
P5 DA (against "psych is broken / it's all noise"): failures concentrated in social priming; cognitive/psychophysics replicate; OSC 39% challenged (Gilbert 2016); binary replicate y/n is itself questionable; medicine has similar problems; Bayesian: failure is rational updating not crisis.
Sharpest disagreement: Theorist (even perfect stats won't fix poorly-defined constructs in a non-invariant domain) vs Methodologist (fix stats, fix problem). Practical fork: pre-reg+N sufficient vs needs conceptual reform.
Synthesis: overdetermined — winner's curse + QRP + publication bias inflated; construct vagueness allows post-hoc escapes; genuine context-sensitivity; incentives selected for striking-but-fragile. Reform working.
</thinking>

## Answer

The failures are overdetermined — multiple mechanisms pile on, and disentangling them matters for what the fix actually is.

**The statistical story is real but incomplete.** Researcher degrees of freedom (Gelman & Loken's "garden of forking paths") mean that even without conscious fraud, the many implicit decisions during analysis — outlier handling, covariate selection, when to stop collecting data, which of several DVs to report — can push null effects past p<0.05. Add publication bias (p-curve analyses show suspicious clustering just below 0.05 across entire literatures), chronically underpowered studies (median power in social psychology for small effects ~35%), and you get Ioannidis's result: most single-study p-values in the literature are false positives by construction. Pre-registration of studies before data collection substantially increases replication rates — this directly implicates undisclosed flexibility.

**But the pattern of failure is not random, which points to something deeper.** Hard subfields — experimental cognitive psychology, psychophysics, developmental — replicate well. Social priming, ego depletion, power poses, and many social cognition effects fail badly. If the problem were purely statistical practice, you'd expect more uniform failure. The differential tracks theoretical solidity.

**The deeper issue is construct validity and the stability of the phenomenon itself.** "Ego depletion" is not a natural kind — it's operationalized in dozens of different ways. When a replication changes the manipulation, it's arguably measuring something different, and the theoretical framework offers no principled way to predict which operationalizations should work. More fundamentally, human behavior is constitutively social and contextual: effects can be genuine in the original lab, with that population, at that cultural moment, and genuinely absent elsewhere. This isn't measurement error — it's that many psychological phenomena don't have the kind of cross-contextual stability that physical constants do. Gergen made this argument in 1973 and the replication crisis is empirical confirmation.

**The sociology of science compounds both.** Smaldino & McElreath's "natural selection of bad science" model shows that academic incentives — novelty premium, publish-or-perish, career advancement through surprising findings — systematically select for studies that are striking but fragile. The institution was optimized for the wrong fitness function.

So the full explanation is layered: (1) researcher degrees of freedom + publication bias inflated the literature with false positives; (2) winner's curse / selection effects inflated effect sizes even for real findings — replications regress to the true (smaller) mean; (3) constructs are often too vague to predict which operationalizations will work — enabling infinite post-hoc boundary-condition explanations after failure; (4) some effects are genuinely context-sensitive and the original studies didn't recognize the specific conditions as boundary conditions. The good news is that pre-registration, registered reports, open data, and larger samples are measurably improving reproducibility.

## Dissent worth keeping

Gilbert et al.'s rebuttal to the OSC 2015 paper is underrated: treating "replication" as binary is itself methodologically wrong. Some "failures" are actually successful replications of a smaller, real effect. And some apparent failures may reflect genuine moderators rather than false positives. The 39% replication rate figure is probably too pessimistic for the field as a whole — it oversamples social priming and high-novelty findings. Dismissing whole research programs because a specific operationalization didn't generalize is itself a logical error. The theorist's point also cuts against easy fixes: if phenomena are inherently context-sensitive, pre-registration and larger N won't solve it — you need better theory first, which is harder than statistical reform.

## Confidence

Moderate-high on the multi-causal picture (statistical + construct + contextual); the evidence base is solid. Lower on relative weighting — whether statistical reform alone is sufficient vs. whether fundamental theoretical reconstruction is needed. The pre-registration evidence leans methodological, but the differential subfield failure rate leans theoretical. Genuinely unresolved.
