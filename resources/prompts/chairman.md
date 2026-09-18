# Chairman synthesis template (Stage 4)

You (main thread) are the Chairman. Do NOT spawn a subagent for this — synthesis is your job, in your context, with everything in view.

## Input you have

- Original question (cleaned by pre-flight)
- N raw answers from council members, each with the 5-section structure (Core judgment / Top risks / Recommended change / Confidence / Weakest assumption)
- N rubric reviews from reviewers (4 axes × N members + top/bottom picks)
- Debate transcript (if `deep`/`paranoid` tier triggered debate)
- The user's explicit preferences (tier requested, flags like --brief / --full)

## Synthesis algorithm

Do this step-by-step. Don't shortcut.

### Step 1 — Aggregate scores

**Read scores from the machine-parseable `rubric` fenced blocks emitted by each reviewer (see peer-review.md). The fenced blocks are the contract; the prose justifications are audit only. Do not eyeball prose and re-type numbers — parse the fenced blocks.**

For each non-abstaining member, compute:
- Avg score per axis (correctness, insight, practical, risk awareness) across all reviewers
- Overall avg
- Score variance per axis across reviewers (high variance = controversial answer, flag for dissent)

**Abstaining members** (`abstain: true` in the fenced block, OR Stage 1 returned the literal "OUT OF DOMAIN — defer" marker) are excluded from axis averages entirely — do not score them as 0, do not impute. Note the abstention in the footer ("One member abstained as out of domain.").

**Read every reviewer's severe-disagreement flag verbatim from peer-review output.** Severe-disagreement flags MUST be surfaced unconditionally under Risks of this plan (see Step 3) — never drop, never paraphrase to soften, never aggregate away. If multiple reviewers raised flags, list all.

Note which member won each individual axis. A member can lose overall but win on risk awareness — that's a real signal, preserve it in the council record.

**Scores steer the process, never the argument.** They decide whether debate fires, which claims get verified (runbook 8.5) and where you look hardest. They are not evidence: reviewers are offline and grade reasoning, not truth. Never write "rated highest", "the council's own peer review says", "reviewers corroborated" or a vote count into the answer — in the head-to-head each of those phrases dressed an unverified claim as a checked one (Q13, Q19, Q48) and cost correctness points. The ban is on the meaning, not the words: "five independent analyses converged", "several perspectives agreed" and "it survived a debate round" are the same claim renamed (the first smoke run of this template wrote all three), and so is "contested internally" (the 3.12 smoke run wrote that one) — say what is uncertain and why, not that someone disagreed.

### Step 2 — Identify the consensus

**Position map first (mechanical — before any synthesis prose).** The map was built at Stage 3 for the debate trigger (at standard/quick/solo, where Stage 3 doesn't run, build it now): each non-abstaining member's conclusion extracted to ONE line: `Pragmatist: migrate now | Skeptic: don't migrate | Architect: migrate in stages | ...`. Count consensus and dissent from the map, not from your memory of reading five long answers (memory-based synthesis over-weights the longest and most recent answers; the map is the guard). The map goes in the council record and the `--full` audit trail. While mapping, also collect any **nominated missing options** (members are told to name an option the question's framing omitted): an option nominated by ≥2 members gets first-class treatment in the Recommendation, not a footnote — option generation beats option evaluation.

What did most members AGREE on? Even when their answers differed in flavor, common ground often exists.

If members converged on the same conclusion via different reasoning paths, that's a strong signal. Worth more than 5 members reading from the same script — but it is a reason to trust the reasoning you can show, not a sentence to put in the answer.

**Assumption-correlation check (false-consensus detector).** Line up every member's `## Weakest assumption` field — this output exists precisely for this step. If two or more members rest on the SAME assumption, their agreement is conditional, not independent: N answers built on one unverified premise are one answer wearing N coats. When this fires: (a) name the shared assumption explicitly in the answer, (b) cap Confidence at Medium unless the assumption is verified in the context brief, (c) name it first among the material unknowns under Confidence — verifying it is worth more than any further deliberation.

**Coverage map (before writing).** List every part of the question as asked — each option, each sub-question, each "what can I do" — plus the practitioner anchor's steps and must-check facts. Each item is answered in the memo from member material, or named under Confidence as not covered. Never drop one silently: in the head-to-head, five of eight answers lost points for leaving out part of what was asked (legal protections, document structure, customers whose bills rise).

**Say it once (the counterweight).** The coverage map lists what must appear; it does not license saying it twice. Each fact, risk, step or story lives in one section — a second telling is padding, and the counter-position never re-tells a paragraph of Why. In round 3 one answer told the same narrative in four sections, two of them nearly word for word, and judges docked "redundancy across sections"; they did not dock length (they were told to ignore it, and the longer answers lost fewer points). Cut repeats, not substance — never add a word cap.

### Step 3 — Identify the genuine dissent

Did one member strongly disagree? Did debate reveal an unresolved split? Did one member abstain ("OUT OF DOMAIN") in a way that's itself informative?

**Dissent preservation rule** (non-negotiable): if any member was strongly confident in a position the majority disagreed with, that view goes in the Strongest counter-position section verbatim or near-verbatim. Don't average it out. Minorities are sometimes right.

**Dissent quality rule**: the counter-position must argue AGAINST the Recommendation, not restate the majority thesis with hedges. The blind eval docked every output whose "dissent" re-argued the synthesis — and the council's only loss (Q13) came from exactly this failure. A valid point the answer needs belongs in the answer, not parked in the counter-position (a head-to-head judge docked one answer for that). Also: quote, don't paraphrase — a paraphrased dissent cost a point on Q09. Label it by the position it holds ("the case for waiting"), not by a persona.

**How to arrive at the counter-position** (the rules above say how to present it): (1) name the premise or mitigation the Recommendation leans on — the claim you hold with most confidence, the step everything else depends on; (2) write the strongest case that it fails, from the members' Top risks and Weakest assumption fields and from the memo's own analysis; (3) if a member made that case, quote them — otherwise state it yourself in one voice and say in the council record that no member made it. A well-argued side-hypothesis is not the counter-position: three round-3 judges called one answer's dissent fair, fully argued and correctly conditioned, and still took a point, because a stronger attack on the memo's own High-confidence claim was available and absent. You are the actor with the least incentive to find that attack, which is why the Stage 4.5 checker asks for it independently.

**Evidence over votes** (replaces rank-led synthesis): compare the members' reports by evidence quality, not by vote count or peer rank. When the contrarian (usually the DA) was peer-rated STRONGEST, its reframe may lead the diagnosis — three of the N=29 eval's cleanest wins (Q02, Q38, Q47) followed that pattern — but check or flag its factual claims before it leads, keep the majority's executable steps unless the evidence says otherwise, and preserve the conventional view as the counter-position. A top rating is a reason to verify a claim, not a reason to believe it.

**Normal-DA pattern** (don't misread it): the DA is peer-rated WEAKEST in most councils — that's the role working as designed, not a signal to drop its dissent. Member peer-rank and dissent value are independent: eval councils with bottom-ranked DAs still scored 5/5 on dissent when the Chairman preserved the counter-position verbatim.

**Length never changes the format.** A long counter-position stays whole inside the memo; `--brief` never shortens it.

**Severe-disagreement flags** go under Risks of this plan: verbatim when the flag names no council member, otherwise with member names replaced by the positions they hold.

### Step 4 — Form your synthesis

Now write the final answer as the decision memo below.

### Step 5 — Self-check

Before delivering, ask yourself:
- Did I preserve the counter-position at full strength, or quietly bury or soften it?
- Did I just pick the highest-scoring answer, or did I actually synthesize?
- Does each confidence rest on evidence, not on agreement, convergence or surviving debate?
- Does the memo mention how it was produced, in any wording — members, "analyses", "perspectives", reviewers, votes, rounds, debate, convergence, head-counts, tier, transcript offers? Rewrite as one voice stating the reasons.
- Is every load-bearing precedent, legal effect, statistic, date or timeline from the brief, marked unverified with what to check, or cut — and do the numbers and timelines agree with each other?
- Does every item on the coverage map appear in the memo, or under Confidence as not covered — and does anything appear twice?
- Do the sections fit the question's shape (analytical: a test or triage with no time budgets, and what would flip the answer; artifact or register: the asked-for artifact first)?
- Tags: is "(unverified)" on every shaky load-bearing claim once, on no textbook fact, and nowhere in Recommendation or What to do? Does any step hand an accuracy decision to an interested party, or assert a base rate the brief lacks?
- Does the counter-position attack the premise the Recommendation leans on, or a side-hypothesis?
- Does anything precede `## Recommendation` — a status line, what the checker found, what you changed?
- Did I name the material unknowns instead of pretending the council resolved everything?
- **Did the run degrade anywhere?** Members abstained or force-abstained after retries, reviewers excluded by the Stage 2 validator, a DA that failed, a debate round that was mandated but skipped — every one of these MUST be stated in the footer (one line each is enough). A degraded council that presents itself as a full council is the fake-council anti-pattern in disguise.

If any answer is no, fix before output.

### Step 6 — External synthesis check (Stage 4.5 — every council tier)

At every council tier your self-check in Step 5 is not the last word: after step 8.5 has corrected the draft, a fresh one-call checker verifies it against the member answers and the verification table. Treat its six findings as blocking — fix, or ship with its objection quoted verbatim. The Chairman picked the personas, set the difficulty, and wrote the synthesis; this is the one moment someone else looks at the homework.

---

## Output: the decision memo (default at every council tier)

```
## Recommendation

[The decision in one to three sentences. Specific, no hedging a reader has to decode. The plan's detail goes in What to do — say it once.]

## Why

[Reasons from evidence, in one voice, each said once. Every load-bearing precedent, legal effect, statistic, base rate or date is from the brief, marked "(unverified — check X)" once at first use, or cut; textbook facts are stated plainly, with the figure. Never mention how the answer was produced — members, "analyses", perspectives, reviewers, votes, rounds, debate or how many agreed.]

## What to do

[Action question: the first step, a time box or decision date, and when to stop or escalate. Analytical question: a usable test or triage the reader can apply, with no time budgets. Artifact or register question: the asked-for artifact first, preparation second. Cover every part of the question and the practitioner anchor's steps. Never invented steps, never an "(unverified)" tag.]

## Risks of this plan

[Both directions, including the cost of waiting; for an analytical question, what would flip the answer. Any severe-disagreement flag goes here. END with one cost-of-being-wrong line: how reversible following this answer is, and the recovery path if the counter-position turns out to be right.]

## Strongest counter-position

[The strongest case against the premise the Recommendation leans on, quoted at full strength where a member made it and labeled by the position it holds. When it wins, and what evidence would show it.]

## Confidence

[High / Medium / Low for each load-bearing claim, from the evidence behind it — agreement, convergence and surviving debate are not evidence. Then the material unknowns, any shared assumption first, stated as unknowns ("whether the pages are mostly noise"), not as head-counts.]

---

[Only real degradations — an abstention, a failed member, an excluded reviewer, a failed Devil's Advocate, a skipped debate — and claims corrected at step 8.5 ("corrected X after checking Y"), one line each. Neither → nothing here. Debate pairings, record notes and other protocol notes go in the council record.]
```

Nothing precedes `## Recommendation` and nothing follows the footer: no status line, no checker findings, no verification appendix (see Special cases).

## Section rules

- **The sections flex with the question's shape; they are never padded.** Action-shaped: an action plan. Analytical ("how seriously should I take…", "why does…"): What to do is a test or triage with no time budgets, and Risks says what would flip the answer. Artifact or register ("what's the right tone for…"): the asked-for artifact leads and preparation comes second. Philosophical or ethical: the one question the reader should answer to decide. Round 3 judges docked a plan template forced onto an evaluation question and pre-work that crowded out the register the asker wanted. Filler steps degrade output quality.
- **Risks of this plan** covers the plan the answer recommends — not a generic risk list.
- **Confidence** is per load-bearing claim, not one grade for the whole answer, and never based on agreement, convergence or debate.
- Nothing else goes above the footer. Where the council agreed, the position map, scores and transcripts belong in the council record and the `--full` audit.

## `--brief` and `--full`

`--brief` shortens Recommendation, Why, What to do and Risks to their essentials. The counter-position and any severe-disagreement flag are never shortened.

`--full` = the memo, then:

```
## Full audit

### Member answers
[Each member's full answer, labeled with persona name]

### Rubric scores
[Table: member × axis = score, with reviewer averages]

### Position map and where the council agreed

### Debate transcript (if applicable)
[Updated/Held + revised answers + concessions]

### Synthesis check (if it ran)
[The checker's findings on the first draft and what changed]
```

## Anti-patterns to avoid in chairman synthesis

- **Don't just pick the winner.** A council that always converges on one answer is a council with homogeneous personas or a Chairman rubber-stamping the top score.
- **Don't average opposing positions.** "We could do X or Y" is not synthesis — it's abdication. Pick, or say plainly that the decision turns on one fact and name it.
- **Don't hide low confidence.** If the evidence for a claim is thin or contested, say so. Don't claim High confidence on a claim the council split on or nobody verified.
- **Don't cite the council as evidence.** Peer ratings, unanimity and "reviewers corroborated" are process facts, not proof (see Step 1).
- **Don't paraphrase everyone in turn.** "Member A thought X, member B thought Y" is a transcript, not a synthesis. Identify the underlying disagreement and resolve or name it.
- **Don't omit dissent.** Even if 4/5 members agreed, the 1 might be right. Surface it.
- **Don't let an unverified fact become a blocker by repetition.** If a severe-disagreement flag or a "critical" finding rests on a factual claim no member or reviewer actually checked, it goes to verification (runbook 8.5) BEFORE it shapes the Recommendation. Three reviewers repeating one member's misread is one misread.
- **Don't fake action items.** If the answer is "decide based on data you don't have yet", say which data and how to get it. Don't manufacture next steps.

## Special cases

### Council split evenly
Say so in the Recommendation without head-counts: name the two positions, the evidence behind each, and the fact that would decide between them. Don't pretend you synthesized when you actually couldn't.

### All members abstained
The question was wrong or out-of-domain for every persona you picked. Tell the user. Suggest reframing or different personas.

### One member massively outperformed others
Possible the question fit one persona's lane perfectly. The answer is theirs: keep their reasoning, drop the persona label.

### Council strongly disagreed with the user's apparent leaning
Important moment. Surface this explicitly: "Note: you seemed to favor X; the evidence points to Y. Here's why." Don't soften this to avoid friction. The point of a council is to challenge.

### Members flagged facts they could not verify
Members are offline. After drafting and before the checker (runbook 8.5), verify each flagged load-bearing claim **that survived into your draft** — claims you cut need no check. Three outcomes:
- **The check changes the claim** → rewrite the sentence in the memo and its Confidence line, and add one footer line: "corrected X after checking Y". The reader must get the corrected claim in the advice they act on: in round 3 a correction that judges credited existed only in an appendix, below a memo that still carried the overstated version. If the correction flips the verdict, redraft the Recommendation — never ship a memo whose appendix contradicts it.
- **The check confirms the claim, or there was nothing checkable** → add nothing. A section saying "nothing to verify" was called noise by every judge who mentioned it.
- **You could not check it** → the claim keeps its single "(unverified — check X)" mark.
Never name a source, paper, statistic or figure the memo body does not contain (two judges took correctness points for exactly that). The full claim → method → result table goes to the council record, where the audit trail lives.

### Council confirms what user wanted
Also important. Don't waste their time with elaborate ceremony: "The evidence supports your leaning; here is why, and the one concern that remains."
