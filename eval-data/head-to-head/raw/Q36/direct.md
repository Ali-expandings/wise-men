# arm: direct (no skill) | question: Q36 | general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 69233 | tool uses: 0 | duration: 11s

Blameless and accountable aren't actually contradictory — they're solving different problems, and the tension you're feeling comes from mixing them up.

**Blameless** means: don't punish individuals for the failure. No firing, no public shaming, no "John pushed the bad config." Why: people who fear blame hide information, hedge, cover tracks. That kills your ability to learn what actually happened. Blameless is about *psychological safety during the investigation* so you get the truth.

**Accountability** means: the org owns fixing the systemic gaps that let this happen. Someone is responsible for each action item shipping. Processes that failed get changed. This is about *organizational ownership of the outcome*, not punishing a person.

So the split is: blameless toward individuals, accountable for the system.

How to actually write it:

1. **Timeline — facts only, no judgment language.** "At 14:32 the deploy script ran without the feature flag check" not "the engineer forgot to check the flag." Describe actions and system states, not people's competence or intent.

2. **Root cause — go past the human action to the systemic gap.** If someone pushed a bad config, the root cause isn't "human error," it's "no staging validation caught this" or "the config schema allowed this invalid state." Human error is where the 5-whys *starts*, not where it ends.

3. **Contributing factors, named plainly.** Include process gaps, missing alerts, unclear ownership, time pressure — whatever actually contributed. This is where accountability lives: not "who screwed up" but "what conditions made this possible."

4. **Action items — owned, dated, specific.** This is the accountability engine. Each item has a name, a deadline, and a concrete deliverable ("add config validation to CI by 9/30" not "improve testing culture"). Track these to completion publicly — that's the actual accountability mechanism, not language in the doc.

5. **Never write a name next to blame language.** It's fine to say "the on-call engineer" in the timeline as a factual actor. It's not fine to say "should have known better," "failed to," "didn't follow process" attached to a person. Attach those judgments to the process: "the runbook didn't cover this failure mode."

One-line way to tell your manager: blameless is about people, accountable is about the system — the doc doesn't blame individuals, but it damn well owns the fix.
