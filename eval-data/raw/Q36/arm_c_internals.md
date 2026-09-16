# Q36 Arm C internals — 5 members + 5 reviewers
# salvaged_from_context: false
# regenerated: 2026-05-29 (fresh full pipeline)
# members: 5 sonnet-4.6 (Editor, Audience Advocate, Rhetorician, Strategist, Devil's Advocate) — writing-domain personas
# validator: all 5 passed (5-section contract present + non-empty + engaged)
# member outputs saved VERBATIM (no compression)
# reviewer framing: NEUTRAL grading frame (bug #6 fix)
# note: 4-member consensus = resolvable via levels (blameless past/systemic + accountable future/named-DRIs + local-rationality); 3 flag "clarify manager's real ask". DA = genuine split (contradiction is real political cover → decision-quality review + force the conversation).

==================================================================
## MEMBER: Editor (sonnet-4.6)
==================================================================

## Core judgment

"Blameless" and "accountable" are not contradictory — they operate at different grammatical levels. Blameless means the *sentence subject* is a system, a process, or a condition, never a person. Accountable means the *action item* has a named owner and a due date. You resolve the tension by keeping those two things in separate structural zones of the document: the narrative section uses agentless or system-subject constructions, while the action-items section uses direct ownership language. The document as a whole can be both simultaneously because no single sentence has to carry both burdens.

## Top risks

- Passive voice masquerading as blamelessness: "The deployment was approved without review" sounds neutral but still implies someone failed to review, which readers will map onto a person. The system was never named as the subject.
- Over-correction into vagueness: scrubbing all agency from the narrative produces a document that reads like the outage caused itself, which erodes trust and teaches nothing.
- Action items without owners: writing "the alerting pipeline should be improved" instead of "Alice owns a proposal by June 14" is accountability theater — it looks responsible but produces no actual follow-through.
- Conflating cause with fault: "the engineer pushed the config change at 14:32" is a factual statement of causation, but placed in the wrong section it reads as a finger-pointing exhibit. Location and framing determine whether a fact is neutral or accusatory.
- Timeline that narrows onto one person: if every entry in your incident timeline is an action taken by a single engineer, the structure itself creates blame regardless of word choice.

## Recommended change

Separate your document into three structurally distinct zones, and write each zone with a different grammatical contract. In the **narrative / timeline** zone, make systems and processes the subjects of sentences: "The config validation step did not catch the malformed value" rather than "X did not validate the config." In the **contributing factors** zone, name conditions and gaps, not decisions: "The team lacked a documented rollback procedure" rather than "The team did not roll back promptly." In the **action items** zone, flip completely — name a specific person, a specific deliverable, and a specific date: "Maria will add config schema validation to the deploy pipeline by June 6." This zoning approach means a reader cannot find a sentence that simultaneously names a person and attributes failure to them, which is the structural definition of blameless, while the action section provides the concrete accountability your manager needs.

## Confidence

High — because this is a question of document architecture and sentence grammar, both of which have well-established craft answers that do not depend on the specifics of the outage.

## Weakest assumption

The analysis assumes that your organization's postmortem readers are operating in good faith and will read the document as a whole — but in a highly political environment, action-item ownership ("Maria owns X") can itself become blame-by-association if the culture is dysfunctional enough to weaponize it, which would require a different strategy than the one recommended here.

==================================================================
## MEMBER: Audience Advocate (sonnet-4.6)
==================================================================

## Core judgment

"Blameless" and "accountable" are not opposites — they operate at different levels of analysis. Blameless means you do not attribute the outage to individual moral failure or incompetence; accountable means the organization owns the outcome and commits to specific remediation. The tension your manager feels is real but resolvable: you write about systems, processes, and decisions (fully accountable) while framing individual actions as reasonable responses to the conditions those people faced (psychologically safe). The document can be simultaneously honest, fair, and action-oriented.

## Top risks

- **The blameless frame becomes a cover for vagueness.** Engineers read "blameless" as permission to omit specifics; the resulting document is so sanitized it teaches nothing and leadership loses confidence in the process.
- **Accountability lands on individuals anyway, just implicitly.** Passive voice ("a misconfiguration was pushed") still points at someone, and everyone in the room knows who. It provides the appearance of blamelessness while delivering the psychological harm of blame.
- **The document serves the manager, not the engineers.** If the team senses the postmortem is a performance for leadership rather than a genuine learning exercise, future incident honesty collapses — which is the single most valuable thing the process produces.
- **Remediation items are too vague to satisfy any audience.** "Improve monitoring" satisfies no one: engineers don't know what to build, the manager can't track it, and leadership can't point to it as assurance.
- **Different audiences read the same sentence differently.** A statement meant to be neutral reads as accusatory to the engineer involved and as a whitewash to a skeptical customer or executive.

## Recommended change

Separate the structural narrative from the action register, and write each for its actual audience. The narrative section uses the "reasonable person" frame: describe each decision as what a competent person would do given the information available at that moment — because that is almost always true, and it is both accurate and psychologically safe. The action register is where accountability lives: every contributing factor in the timeline must produce at least one named, dated, owner-assigned action item. The combination lets you say honestly, "No one acted wrongly given what they knew, and here are the twelve specific things we are changing so that no one ever faces those conditions again." That sentence satisfies the engineer (fair), the manager (accountable), and leadership (assured) simultaneously. Write a one-paragraph executive summary last, after the full document is stable, tuned specifically for the leadership/customer audience — it can reference the action register without re-litigating the technical timeline.

## Confidence

**High** — this is a well-established pattern in incident culture (Google SRE, Etsy, Allspaw's work) and the core insight that blame vs. accountability operates at different analytical levels is not controversial among practitioners who run mature postmortem programs.

## Weakest assumption

The analysis assumes that your manager, when they said "blameless but accountable," actually wants the system-level accountability described here — but there is a real possibility they want visible individual accountability (i.e., a paper trail that shows a specific person was responsible) and are using "blameless" as a softer label for the same thing. If that is the true ask, the tension is not resolvable within a single document, and the right move is to clarify with your manager before writing a word.

==================================================================
## MEMBER: Rhetorician (sonnet-4.6)
==================================================================

## Core judgment

The contradiction dissolves once you recognize that "blameless" is a claim about persons, while "accountability" is a claim about systems and future obligations. Blaming a person means treating their individual choice as the root cause and directing moral censure at them; accountability means identifying what commitments were not met and who holds the authority — and therefore the responsibility — to fix the conditions that allowed the failure. These operate at different levels of analysis. The framing trap is treating "blameless" as "consequence-free" and "accountability" as "someone must be punished," when the actually productive version of each is: no person is condemned for being human in a flawed system, and specific roles own specific remediation work going forward.

## Top risks

- **Blame laundering**: Nominally blameless language ("the deployment process failed") that everyone in the room understands as pointing at one engineer — the emotional truth contradicts the stated framing and destroys trust in the exercise.
- **Accountability vacuum**: Overcorrecting into pure systemic abstraction means every action item is owned by "the team," which in practice means no one. Diffusion of responsibility is the enemy of remediation.
- **Retrospective collapse into prospective theater**: The postmortem becomes a list of action items nobody follows up on because the accountability mechanism (who owns this, by when, reviewed by whom) was never specified.
- **Local rationality elided**: If you don't explicitly state that each decision made by each person was rational given the information they had at the time, people will read between the lines and still feel blamed, even if you used blameless language.
- **Systemic causes used to protect institutional inertia**: "It's a system problem" can be weaponized to avoid changing anything, particularly when the system problem implicates leadership decisions or resourcing.

## Recommended change

Write the postmortem in two structurally distinct movements. The first is a backward-looking factual narrative that invokes the "local rationality" principle explicitly — for each decision node, state what information was available and why the choice made was reasonable given that information. Name people only to establish context, not to assign fault. The second movement is forward-looking and role-explicit: for every contributing factor identified, name the role (not the person) responsible for owning the fix, set a deadline, and define a review mechanism. If a specific person currently holds that role, they appear in the accountability column not because they caused the outage but because their role carries the authority to prevent the next one. The document's moral logic should be: *we are not blaming the past you for being human; we are asking the present you to own the future fix because you are the person with the power to make it.*

## Confidence

High — because this framework is not theoretical; it is the model that Google's SRE practice, Etsy's engineering culture, and John Allspaw's foundational work on blameless postmortems converged on independently, and it has been validated at scale across organizations with very different cultures.

## Weakest assumption

The analysis assumes that your organization's leadership will genuinely honor the blameless frame — that if the postmortem correctly identifies a systemic cause rooted in a resourcing or architectural decision made by management, no informal blame will flow downward anyway. If the psychological safety does not actually exist above the level of the postmortem document, the framework becomes a performance, and no amount of careful prose engineering will protect the people in the room.

==================================================================
## MEMBER: Strategist (sonnet-4.6)
==================================================================

## Core judgment

"Blameless" and "accountable" are not actually contradictory — they operate at different levels of abstraction. Blameless means you do not attribute the outage to a person's character, carelessness, or moral failure; accountable means specific humans own the action items that prevent recurrence. The confusion usually comes from conflating "who caused this" (backward-looking, blame-adjacent) with "who owns the fix" (forward-looking, accountability). Your postmortem should do exactly one thing with people's names: attach them to future action items with due dates, not to past mistakes.

## Top risks

- **Manager's real ask is opaque.** "Blameless but accountable" is sometimes a coded request to name the engineer who made the bad deploy without appearing to name them. If you write a genuinely blameless document, you may satisfy the stated ask while missing the actual one.
- **Accountability without authority.** If you assign DRIs to action items but those people lack the authority or resources to actually close the items, the postmortem becomes theatrical. The accountability looks real on paper and evaporates in practice.
- **Root cause stops too early.** Most outages have a proximate human action AND a systemic reason that made the action possible — a missing safeguard, a broken alert, a deployment process with no circuit breaker. Stopping at "engineer X ran the wrong command" is blame dressed up as root cause analysis.
- **No follow-through mechanism.** Postmortems that do not get reviewed in a recurring forum (e.g., weekly ops review) produce action items that quietly expire. The document feels complete the day it is written and becomes forgotten within two weeks.
- **Audience mismatch.** The document that satisfies your manager, the one that reassures leadership, and the one that actually prevents the next outage are often three different documents with different levels of technical detail and different framings. Trying to write one document that serves all three audiences usually produces a document that serves none well.

## Recommended change

Write the postmortem in two parts. Part one is the technical narrative: a timeline, a clear multi-level root cause (proximate cause, contributing factors, systemic gaps), and an impact statement with numbers. No names appear here except in the timeline where needed for chronological clarity. Part two is the action-item registry: each item has an owner (a name), a due date, a definition of done, and a designated reviewer. This structure makes "blameless" the default reading of part one (systems failed, not people) while making "accountable" unambiguous in part two (this person owns this item by this date). Before you publish, have a five-minute conversation with your manager to confirm that what they want is the structure above — not a document that implicitly points at someone. That conversation will tell you whether you are solving a writing problem or a political one.

## Confidence

Medium — the structural advice is sound and well-established in SRE practice, but the confidence is limited because the manager's actual intent is unknown, and the right document depends heavily on that intent.

## Weakest assumption

The weakest assumption in this analysis is that your manager's stated goal ("blameless but accountable") reflects their genuine intent rather than a socially acceptable way of asking you to document someone's responsibility for the failure — if the latter is true, the structural solution above will not satisfy them and you have a different problem to solve.

==================================================================
## MEMBER: Devil's Advocate (sonnet-4.6)
==================================================================

## Core judgment

The framing of "blameless but accountable" is not a clever synthesis — it is a political contradiction your manager is asking you to launder into respectability. The two demands are genuinely in tension because blamelessness, taken seriously, means the system failed and no individual's judgment call is singled out for criticism; accountability, taken seriously, means a named person made a decision that contributed to the outage and they own that. Pretending these are separable by slicing time ("blameless for the past, accountable for the future") papers over the real question: do we believe Engineer X's decision at 2:47am was reasonable given what they knew, or not? If yes, there is nothing to be "accountable" for beyond fixing the system. If no, then the postmortem is not actually blameless — it just delays the blame until the action items are reviewed.

## Top risks

- You write a document that satisfies no one: engineers feel the "accountability" framing is a hidden blame trap, so they stop being candid in future postmortems, destroying the entire value of the practice
- The manager uses the accountability section to retroactively justify a personnel decision, and you have authored the paper trail
- The postmortem becomes so carefully hedged — never assigning individual judgment, always attributing everything to "the system" — that it produces no actionable signal about whether the on-call engineer needs more support, more training, or a different rotation
- You internalize the blameless frame so completely that a genuinely poor individual decision (ignoring an alert, skipping a runbook step) goes unaddressed, and it happens again
- The organization learns that postmortems are political documents, not honest ones, and the whole ritual becomes cargo cult compliance

## Recommended change

Write a decision-quality review, not a blameless postmortem. Name the decisions that were made — by whom, with what information, under what constraints — and evaluate whether those decisions were reasonable given the information available at the time. If the decision was reasonable and the outcome was bad, say so explicitly: the system failed this person, and here is how we fix the system. If the decision was not reasonable — the alert was ignored, the runbook was skipped without cause, a known risk was dismissed — say that too, with specificity, and attach a concrete support or training action to the person's name, not a vague team-level remediation. Then bring this framing to your manager before you write a word, and ask directly: "If the review shows an individual made a poor call, are we willing to say that? Because if not, I cannot write a document that's also honest." Force the conversation rather than resolving the contradiction in the document itself.

## Confidence

Medium — this recommendation trades short-term political friction for long-term organizational honesty, and that trade is only worth making if leadership will actually tolerate the honest version; in many orgs they will not, and the cost falls on the engineer who wrote the honest draft.

## Weakest assumption

The weakest assumption is that the manager's simultaneous demand for blamelessness and accountability reflects confused thinking rather than a deliberate strategy — in reality, some managers know exactly what they are asking for: a document that reads as psychologically safe to engineers while still providing cover to hold someone responsible later, and if that is the actual intent, no framing advice will fix it.

==================================================================
## REVIEWERS (5 × haiku-4.5, NEUTRAL grading frame) — 0 refusals (bug #6 fix held)
==================================================================
# Per-member mean across 5 reviewers (C/I/P/R → total /20):
#   Rhetorician      4.0 / 4.6 / 3.0 / 4.0 = 15.6  (TOP)
#   Audience Advocate 4.0 / 4.0 / 4.0 / 3.4 = 15.4
#   Devil's Advocate 3.6 / 5.0 / 2.0 / 4.6 = 15.2  (insight 5.0 every reviewer; practical 2.0 every reviewer — refuses "how to write it")
#   Strategist       3.4 / 3.6 / 4.2 / 3.6 = 14.8
#   Editor           4.0 / 3.0 / 4.0 / 3.2 = 14.2  (BOTTOM)
#
# Per-reviewer raw (C/I/P/R):
#   R1: Editor 4/3/4/4 | AudAdv 4/4/4/4 | Rhet 4/5/3/5 | Strat 4/4/5/4 | DA 4/5/2/5  | top Rhetorician, bottom Strategist
#   R2: Editor 4/3/4/3 | AudAdv 4/4/4/3 | Rhet 4/5/3/5 | Strat 4/3/4/4 | DA 3/5/2/5  | top Rhetorician, bottom DA
#   R3: Editor 4/3/4/3 | AudAdv 4/4/4/3 | Rhet 4/4/3/2 | Strat 3/4/4/3 | DA 3/5/2/4  | top DA, bottom Rhetorician
#   R4: Editor 4/3/4/3 | AudAdv 4/4/4/4 | Rhet 4/4/3/4 | Strat 3/3/3/4 | DA 4/5/2/5  | top AudAdv+DA, bottom Strategist
#   R5: Editor 4/3/4/3 | AudAdv 4/4/4/3 | Rhet 4/5/3/4 | Strat 3/4/5/3 | DA 4/5/2/4  | top Rhetorician, bottom DA
#
# SEVERE-DISAGREEMENT FLAG raised by all 5 reviewers: Devil's Advocate vs the other four on whether the
# blameless/accountable tension is structurally resolvable (Editor/AudAdv/Rhetorician/Strategist: yes — levels of
# analysis + zoned document) or a genuine political contradiction the manager wants laundered (DA: no — write a
# decision-quality review + force the manager conversation first). Genuine council split. Standard tier → NO debate
# round (per spec Stage 3 deep/paranoid only). DA's split preserved verbatim into Chairman dissent.
# Note: DA peer-WEAKEST on practical (2.0) but peer-HIGHEST on insight (5.0) — the recurring eval pattern.
