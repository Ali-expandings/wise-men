# arm: direct (no skill) | question: Q25 | general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 69492 | tool uses: 0 | duration: 15s

Short answer: mostly not p-hacking retroactively exposed (though that's part of it) — replication failure exposes several compounding structural problems in how the field generated and validated knowledge in the first place.

**The main culprits, roughly in order of importance:**

1. **Flexible analysis, not fraud.** Researchers had many defensible choices — which covariates to include, how to exclude outliers, which subscale to use, when to stop collecting data — and tried combinations until something crossed p<.05. This is "p-hacking" but it's usually unconscious, not deliberate cheating. Simmons, Nelson & Simonsohn's "researcher degrees of freedom" paper showed you can get significant results supporting absurd hypotheses this way.

2. **Publication bias.** Journals published positive, surprising, clean results and buried null ones. So the literature is a filtered sample — even with zero p-hacking, if 20 labs run a weak-effect study, one gets p<.05 by chance and that's the one that gets published. The "very robust" feel came from seeing only the winners, not from the effect actually being robust.

3. **Low power, small samples.** Classic psych studies often ran n=20-40. Underpowered studies that do find significant effects tend to overestimate effect size (the "winner's curse") — so even a real effect gets reported inflated, and a properly powered replication attempt regresses to a smaller or null effect.

4. **Small effects, big theoretical claims.** Many original studies detected something real but tiny, then theory and popular science (and TED talks) inflated it into a large, general, robust phenomenon. Replications with honest power reveal the effect was always marginal.

5. **Hidden moderators / context-dependence.** Some effects (though fewer than originally claimed once you account for the above) genuinely depend on population, culture, or situational context not specified in the original theory. This is real but is probably a smaller share of the replication crisis than people now assume — it became a popular post-hoc excuse ("it just doesn't replicate in a different context") that's hard to falsify and sometimes used to avoid admitting the original was noise.

6. **Incentive structure.** Careers, tenure, and grants were built on novel significant findings, not on rigor or replication. Nobody was rewarded for running large, boring, pre-registered confirmations — so nobody did, until the crisis forced the issue.

**Deeper point about how the knowledge production worked:** the field's error wasn't lying, it was running many underpowered, flexible, unregistered studies and treating "p<.05, publishable" as the bar for truth. That's a systemic design flaw in the incentive and methodology pipeline, not primarily individual dishonesty. Since ~2011 (Bem's ESP paper, then the Open Science Collaboration's 2015 replication project putting the number around 36-40% of studies replicating) the field has moved toward preregistration, larger samples, and registered replication reports, which is why newer psych findings are generally more trustworthy than pre-2011 ones.

So: p-hacking is real and part of the story, but the bigger structural cause is publication bias plus underpowered studies plus researcher degrees of freedom compounding together — each individually defensible, collectively producing a literature full of noise dressed up as signal.
