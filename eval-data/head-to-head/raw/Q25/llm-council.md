# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q25 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# subagent tokens: 113364 | tool uses: 12 | duration: 221s

## Council Verdict: Why Psychology Replications Fail

### Where the Council Agrees
All five advisors reject "it's just p-hacking." Even the most statistics-forward advisor treats forking-paths/p-hacking as the shallow layer and reaches for base rates and publication bias to do the real work. The others converge from different angles on the same deeper claim: the original studies never specified what population, context, or operationalization the effect held under, so "replication" was attempting to confirm a claim that was never precisely stated. Consensus diagnosis: underspecified scope conditions, not (just) bad statistics. There's also quiet agreement that multi-site, multi-context testing (Many Labs, registered replication reports, preregistration) is the right infrastructure response, whatever you think caused the crisis.

### Where the Council Clashes
**Good news or bad news?** One advisor reframes the crisis as the field finally building a real map of effect-size heterogeneity — useful, exportable to other fields before they have their own crisis. The rest treat this as a dodge: it answers "what do we do now" while substituting for "why did this happen."

**Bad science or bad ontology?** One advisor says scope conditions were simply unknown-but-discoverable — repairable with more data. Another goes further: constructs like "willpower" or "priming" may be folk-psychological bundles that don't carve reality at a joint at all — not repairable by more data, only by better theory or retiring the construct. This is a genuine, unresolved fork (ego depletion looks like the second case; loss aversion's cultural contingency looks more like the first).

**Is statistical hygiene the fix?** A practical checklist (preregistration, n>150/cell, direct vs. conceptual replication) is actionable but implicitly treats this as solvable by individual-study discipline. The theory-first view says even a perfectly preregistered study of an ill-specified construct still won't replicate across contexts — you'll just get a precise estimate of a context-bound regularity.

### Blind Spots the Council Caught
Every reviewer flagged the same gap independently, making it the single most important finding: **no advisor named the incentive structure** — tenure, grants, journal novelty bias, citation counts — as a causal layer. This is likely the upstream variable explaining both p-hacking (rewarded) and the failure to pin down boundary conditions before publishing (also rewarded, since specificity invites disconfirmation).

Second: nobody quantified anything. The right empirical question — do effects fail to zero, or shrink to something smaller but real — went unanswered. (For the record: OSC 2015 found ~36% of studies replicated by significance, with replication effect sizes roughly half the originals on average — meaning both things are happening at once, evidence multiple mechanisms operate simultaneously.)

Third: the council never localized the diagnosis. This isn't uniformly a "psychology" problem — psychophysics and tightly-measured cognitive subfields replicate reasonably well. It concentrates in social/personality psychology, where constructs are furthest from instrument-precision.

Fourth: fraud/fabrication (high-profile cases in recent years) is a distinct failure mode from both p-hacking and construct vagueness, and got no airtime despite driving some of the most visible failed replications.

### The Recommendation
"Is it p-hacking or something deeper" is a false binary — both are downstream of a third thing.

**Layer 1 (mechanical):** forking paths and publication bias mechanically inflate effect sizes even without misconduct. Basically solved as a technical matter by preregistration.

**Layer 2 (theoretical):** many social-psych constructs were never given scope conditions because nobody had incentive to stress-test them before publishing. Some effects turn out real-but-culturally-contingent; others may be constructs that don't carve reality at a joint and need retiring, not patching.

**Layer 3 (structural, the one the council missed on first pass):** both persist because tenure, novelty bias, and citation counts reward exactly the behavior that produces them and punish the behavior that would catch them. Fix the stats and the theory and you still haven't fixed what generates bad stats and bad theory in the first place.

So: not "just p-hacking retroactively exposed," and not purely a philosophy-of-science problem about natural kinds either. It's an incentive-driven epistemic culture that made sloppy stats and unspecified theory locally rational for individual researchers — and the replication crisis is what that culture looks like once external pressure (large-N collaborations, open data mandates) finally got strong enough to check it.

### The One Thing to Do First
Before accepting any specific effect as "robust," check whether it has been directly replicated by a lab with no stake in the original finding — if the answer is no, the effect's status is unknown regardless of its citation count, textbook presence, or original p-value.
