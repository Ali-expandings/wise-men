# arm: lifeos-council (danielmiessler/lifeos 36c6f01e9c2c) | question: Q25 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# environment: voice-notification curl skipped; DEBATE workflow (3 rounds, 4 members)
# subagent tokens: 109037 | tool uses: 16 | duration: 227s

## Council Debate: Why Do Psychology Replication Studies Fail?

**Council Members:** Dr. Elena Voss (meta-science / replication researcher — multi-causal empiricist), Marcus Chen (statistician/methodologist — incentives-and-methods skeptic), Dr. Priya Nair (working social psychologist — context/moderator pragmatist), Dr. Sam Okafor (philosopher of science — theoretical-precision analyst)

### Round 1: Initial Positions

**Elena Voss (meta-science / replication researcher):**
Replication failures aren't one story—they're three or four converging. The base rate problem: original studies ran at 20-30% power chasing p<.05, so even real effects got wildly overestimated by winner's curse. Layer on publication bias filtering out the null results we never saw, plus researcher degrees of freedom—flexible exclusion criteria, outcome-switching, the garden of forking paths—and you inflate effect sizes before any replicator touches the data.

But OSC2015 and Many Labs also show something p-hacking alone doesn't explain: heterogeneity. Cognitive and perceptual effects replicate at much higher rates than social priming effects. That's not fraud, that's effects being genuinely context-dependent, sample-dependent, sometimes culture-dependent — moderators nobody was tracking because the original theory didn't specify boundary conditions.

Anyone who tells you it's "just p-hacking exposed" is retrofitting a tidy villain. Anyone who says it's "just how squishy social science is" is dodging the statistical incentive problem. It's both, plus power, plus genuine effect variability. Single-cause stories are why we're still having this argument a decade later.

**Marcus Chen (statistician/methodologist):**
Replication failures aren't mysterious — they're the predictable output of a broken statistical pipeline. Original studies ran with samples of 40, 60, 80 undergrads, tested five outcome measures, sliced by gender or mood or time-of-day, stopped collecting data when p crossed .05, and published the one comparison that worked. That's not fraud, that's just what unconstrained researcher degrees of freedom do to a significance threshold — you can hit p<.05 on pure noise most of the time if you give yourself enough flexible choices.

Then publication bias filters the record: null results die in the file drawer, "significant" ones survive. So the literature isn't a random sample of true effects, it's a curated sample of the luckiest noise plus whatever real signal exists. Combine that with underpowered designs and you get winner's curse — published effect sizes are systematically inflated, sometimes sign-flipped.

Preregister the hypothesis, fix the analysis plan, power the study properly, report everything — and most of this evaporates. I'm skeptical of framings that make this sound like some deep epistemological feature of social science. It's an incentive and methods problem, and it's fixable.

**Priya Nair (working social psychologist):**
Replication failures don't surprise me — they confirm something we should've taken seriously decades ago. A direct replication holds the surface procedure constant and assumes that's enough. It isn't. Social effects are transactions between a person and a context, and "context" includes things replication protocols routinely scrub out: population, historical moment, novelty, experimenter presence, cultural script for the task. Change the transaction, change the effect. That's not fraud exposed, that's a boundary condition discovered.

I'll grant p-hacking and researcher-degrees-of-freedom did real damage — I lived through discovering how much of my field's early canon was noise dressed as signal. But the response to that shouldn't be "therefore nothing generalizes." That's the mirror image of the original sin: overclaiming certainty in the other direction. WEIRD-sample fragility is itself a finding worth theorizing, not a reason to junk fifty years of work. The fix is moderator-aware theory — ask under what conditions an effect holds — not blanket dismissal.

**Sam Okafor (philosopher of science):**
The literature on this is unambiguous once you look past the p-hacking headlines: most psychological hypotheses are tested against a nil-null of "zero difference," which is almost never exactly true for anything correlated with anything else in a complex system. So a significant result confirms only that some difference exists — not that your specific causal story explains it. That's a weak test dressed up as a strong one.

Layer on weak construct validity — priming manipulations and self-report scales that only loosely index the theoretical construct — and you get the Duhem-Quine problem in full force. A failed replication could mean the theory's false, the manipulation didn't work, the measure was insensitive, or the population differed. You cannot tell which. Physics survives replication crises because its theories forbid specific numbers; ours mostly just predict "an effect," direction unspecified in advance, magnitude never specified at all.

Preregistration kills p-hacking. It does nothing for a field whose theories were never precise enough to risk falsification in the first place.

### Round 2: Responses & Challenges

**Elena Voss:**
Marcus, preregistration kills p-hacking — it does nothing about the heterogeneity OSC2015 and Many Labs actually found. If it were "just" flexible analysis, replication rates would be roughly uniform across domains once you adjust for power. They aren't: cognitive/perceptual effects clear 60-70%, social priming limps in under 25%. That gap is the signature of real moderator-dependence, not noise-mining.

Sam, I'll take the Duhem-Quine point seriously, but "theories were never precise enough" proves too much — it can't explain why some subfields replicate fine with equally vague theories and others don't. Something domain-specific is failing, not epistemology-of-social-science-in-general.

Priya, I'm with you on moderator-aware theory as the fix, but I'd push back on tone: WEIRD-fragility isn't just "a finding to theorize," it's diagnostic evidence for genuinely narrow effects, and pretending every failure is a hidden boundary condition risks becoming unfalsifiable — always available as an excuse, never checked before publication.

**Marcus Chen:**
Preregistration's success rate isn't a footnote — it's the headline. RRRs and Many Labs preregistered designs hit success rates far above the original literature's baseline; that gap is the causal effect of fixing the pipeline, measured, not asserted. Sam, "does nothing" can't survive that number.

Priya, I'll take heterogeneity where it's specified — Elena's cognitive-vs-social-priming split is a real, predicted-in-advance moderator. What I won't take is heterogeneity invoked post hoc, per failure, with no advance prediction of which populations or conditions should flip the sign. That's not a boundary condition, that's an epicycle.

Elena — multi-cause, agreed, but weighted unevenly. Power and forking paths explain most of the inflation and most of the failures; genuine moderation explains the residual, not the median case. Fix the methods first, then go hunting for real heterogeneity in what's left.

**Priya Nair:**
Elena, "heterogeneity" isn't item four on your list — it's the finding. You're bundling it with power and p-hacking like they're the same kind of problem, but they're not: one is measurement error, the other is the effect actually being a different quantity in a different population. Collapse them and you'll keep treating a moderator as noise to average out instead of a variable to model.

Sam — yes, and that's exactly what I mean by context: priming manipulations and vague self-report scales aren't measuring "the construct," they're measuring the construct-as-instantiated-in-this-specific-transaction. Construct validity failure and context-dependence are the same problem wearing different disciplinary clothes.

To Marcus's charge before he makes it: this is falsifiable. A legitimate moderator claim is pre-specified or theoretically derived before you see the failed replication, predicts *which* populations diverge and in what direction, and converges across independent studies. "It didn't work because context" is an excuse. "It didn't work because urban samples lack the scarcity cue's ecological validity, and three other studies confirm that split" is a theory.

**Sam Okafor:**
Marcus—preregistration disciplines the statistical test, but it doesn't touch what the test is *testing*. A preregistered nil-null hypothesis with a loosely-validated manipulation is still only licensed to say "some nonzero difference exists," not "my causal story is right." You can hit every open-science checkbox—locked analysis plan, full reporting, adequate power—and still not know whether a failed replication means the theory's false, the prime didn't land, or the scale didn't track the construct. That's not incentive contamination; it's the theory never risking a specific number.

Which is why Priya's fix *is* my argument, not a rebuttal to it. "Moderator-aware theory" means specifying in advance which populations, contexts, and magnitudes the effect should and shouldn't survive—exactly the precise, falsifiable structure nil-null testing let the field skip. And Elena's cognitive/social gap isn't a fourth independent cause sitting beside ours—cognitive psychology has tighter construct validity and more formal models, so it inherits less of this looseness. The gap traces the theoretical precision gradient.

### Round 3: Synthesis

**Elena Voss:**
Convergence first: nobody at this table defends pure p-hacking-and-done. We all now treat heterogeneity as real, not noise — that's the actual movement since Round 1. And we agree preregistration is necessary but insufficient; it disciplines the test, not the theory behind it.

Where I still push back: Sam's precision-gradient story is elegant but risks explaining everything after the fact — "tighter constructs replicate better" is itself underspecified until someone states in advance how tight is tight enough. Priya's falsifiability criterion is the fix I'll adopt.

What I underweighted: I listed heterogeneity as one factor among four. It's not a factor — it's the lens the other three get filtered through. Power and p-hacking explain why weak effects looked strong; they don't explain why real effects vanish in new contexts.

Recommendation: preregister the test, but also preregister the boundary conditions. A theory that can't say where it stops isn't ready for confirmation.

**Marcus Chen:**
The agreement across the table is broader than round two let on: everyone accepts heterogeneity is real, everyone accepts nil-null testing and weak theory inflate false-positive rates, everyone accepts preregistration disciplines but doesn't complete the fix. Where I still push back on Sam and Priya is sequencing. Construct precision matters, but you can't even see the heterogeneity signal clearly until you've cleared the statistical noise floor — that's not a footnote, it's a prerequisite.

What I underweighted: I treated moderator-hunting as cleanup work after the "real" fix. It's not cleanup, it's the next research program, and it needs the same rigor as the original claim — preregistered, not retrofitted. So: keep the methods-first triage, but stop calling what's left "residual." It's the actual object of study now, and skipping it because the pipeline's cleaner is its own failure mode.

**Priya Nair:**
Marcus and I aren't saying the same thing, and Sam's merge flattens something practitioners can't afford to lose. Theoretical precision tells you an effect should vary by population; it doesn't tell you which clinician, in which intake room, with which client in front of them, gets to trust the finding today. That's a different question—applied, not philosophical—and it's where I actually live.

So: we agree p-hacking was real but overstated as the whole story, and that preregistration fixes the test without fixing the theory behind it. We still split on how much explanatory work "heterogeneity" can do after the fact versus in advance. My recommendation: treat every original effect as a conditional claim, not a null hypothesis to bury or a law to defend—build the boundary conditions into the design next time, and until then, ask "under what conditions was this shown," not "is this true."

**Sam Okafor:**
We've converged more than round one suggested. Marcus's incentive fixes, Priya's moderator-aware theory, Elena's heterogeneity — these aren't rivals, they're symptoms of one root: theories underspecified relative to the tests run on them. My "not precise enough" claim isn't refuted by variable replication rates, Elena — it predicts them. It's a gradient, not a binary: cognitive psychology, behavioral economics, parts of developmental psych have tighter formal models and inherit less looseness; social priming inherited the most.

Where I'll concede: precision alone doesn't explain everything — Priya's right that measurement-as-transaction adds noise even to reasonably precise constructs. So: preregistration for honesty, moderator-mapping for scope, but the actual fix is unglamorous — force theories to predict effect sizes and boundary conditions before they're allowed a "robust" reputation.

### Council Synthesis

**Areas of Convergence:**
- Nobody defends a pure "it's just p-hacking, case closed" account. All four agree p-hacking / researcher degrees of freedom / publication bias / low power are real and did substantial damage — but insufficient as the whole story.
- All four agree the empirical gradient (cognitive/perceptual effects replicating far more than social priming) is a real, load-bearing pattern, not noise — they just disagree on what it's evidence *for*.
- All four converge on preregistration as necessary-but-not-sufficient: it disciplines the statistical test but doesn't validate the theory or the construct the test is standing in for.
- All four land on some version of "specify boundary conditions in advance" as the actual fix, whether framed as Priya's moderator-aware theory, Sam's risky/precise predictions, or Marcus's "next research program done with the same rigor as the first."

**Remaining Disagreements:**
- **Sequencing/weighting:** Marcus holds that statistical/incentive fixes are the prerequisite and explain the median failure, with heterogeneity as the (real but secondary) residual once the noise floor is cleared. Elena and Sam hold heterogeneity/theoretical looseness is the primary lens, not a residual category.
- **What's doing the explanatory work:** Sam frames the whole picture as one root cause (theoretical/construct-validity looseness, on a precision gradient across subfields); Elena resists collapsing it to one root, insisting power, publication bias, and genuine effect variability are distinct mechanisms that happen to co-occur.
- **Level of analysis:** Priya maintains that even a fully precise, falsifiable theory doesn't answer the practitioner's question — under what conditions can *this* finding be trusted *right now, in this context* — and thinks Sam's philosophy-of-science framing, however correct, absorbs but doesn't replace that applied layer.
- **Falsifiability risk:** Marcus remains wary that "heterogeneity"/moderator talk can silently become an unfalsifiable excuse-generator unless the field enforces Priya's and Sam's discipline (pre-specified, convergent, theoretically derived) rather than invoking it ad hoc after each failure.

**Recommended Path:**
The honest answer to the original question is "both, but not as equal partners, and not a mystery." A large chunk of famous "robust" effects were artifacts of small samples, flexible analysis, and a publication filter that only let winners through — that part is p-hacking retroactively exposed, is well-documented (OSC2015, Many Labs, RRR success rates), and is substantially fixable with preregistration, adequate power, and full reporting. But that alone doesn't explain the replication-rate gradient across subfields (cognitive/perceptual holding up far better than social priming), and this is where something deeper about social-science knowledge shows up: most psychological theories have historically licensed only a nil-null test ("there is some effect") rather than a precise, risky prediction ("this effect, this size, in these populations, not others") — combined with loose construct validity, that means a "confirmed" hypothesis was never pinned down as tightly as it looked, and a "failed" replication often can't even tell you which link in the chain broke. The fix isn't choosing between "it's p-hacking" and "it's deep" — it's treating both as real and sequential: clean the statistics first so you can actually see the signal, then do the harder, historically avoided work of building theories that specify in advance where and for whom an effect should and shouldn't hold. A finding survives being called "robust" only once it has cleared both bars, not one.
