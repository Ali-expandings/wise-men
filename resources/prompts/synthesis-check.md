# Synthesis-check prompt template (Stage 4.5)

Spawn ONE fresh subagent (`wise-member`, mid tier; cheap tier at quick) after the Chairman drafts its synthesis and **before the user sees it**.

**Deliver it cheaply.** Do not re-type the member answers: tell the checker to Read the grading packet the reviewers used, plus one small file you write with the aggregated scores, the verification table and the draft. **Bound it**: the checker works in one pass and replies in the fixed form only — measured in round 3, this one call took 4–11 minutes and up to 70k tokens of deliberation, the largest single stage of a run. **Quick tier** (no peer review, no packet): send the question and the draft inline and ask for checks 1 (DISSENT), 4 (DISCLOSURE), 5 (CLAIMS) and 6 (COVERAGE) only; GROUNDING and CONFIDENCE need the member answers and are skipped; that is the tier's design, recorded in the council record, not a degradation for the footer.

**When it fires**: at every council tier (`quick`, `standard`, `deep`, `paranoid`). Solo tier has no council to check against.

**Why it exists**: the Chairman is the same thread that chose the personas, computed the difficulty, and picked the tier. It is grading its own homework. This is the only stage where an outside party looks at the result, and it is the cheapest available mitigation of the skill's one structural conflict of interest.

Frame it as a checking task, not an appeal to authority — no urgency language, no "you are the final arbiter", nothing that invites either rubber-stamping or contrarianism for its own sake.

---

## Prompt to send

```
Checking task. Below is a draft answer synthesized from several independent analyses, plus the analyses it was built from. Verify the draft against its sources. You are not rewriting it and not adding your own opinion on the underlying question — you are checking six specific properties. Work in one pass: read the material once, check each property against it, and reply in the fixed form at the end — no long deliberation, no restating the material.

The original question:
"""
{question}
"""

The context brief the analyses were given (the stated facts):
"""
{context brief, or "none"}
"""

Verification results (flagged claims the orchestrator checked before this draft — claim, method, result; or "none"):

{verification table}

The member answers (each with its conclusion, confidence, and weakest assumption):

{member answers, labeled by persona name; mark any that abstained}

The aggregated review scores:

{per-member rubric averages; note any reviewer excluded and why}

Any debate outcome:

{debate transcript summary, or "no debate round ran"}

The draft synthesis to check:

"""
{chairman draft}
"""

Answer these six, each with one line of evidence quoted or cited from the material above:

1. DISSENT — Is the Strongest counter-position section a clean COUNTER-position that argues against the Recommendation, rather than the majority thesis restated with hedges? Is it quoted rather than paraphrased into something softer? Does it attack the premise or mitigation the Recommendation leans on — or does something in the member answers, their risks or weakest assumptions, or the draft's own analysis attack the Recommendation more centrally than the counter-position chosen? (A "dissent" that agrees with the decision in weaker words fails this check; so does a well-argued side-hypothesis when a more central attack was available.)

2. GROUNDING — Does every substantive claim in the Recommendation, Why and What to do trace to something a member actually said or to the stated facts? Flag anything the draft asserts that no member supports.

3. CONFIDENCE — Does each stated confidence match the evidence behind its claim? (High confidence on a claim the members contested, or that nobody verified, fails; so does Low confidence on a claim backed by strong, verified evidence. Agreement, convergence and surviving debate are not evidence — a confidence justified by them fails.)

4. DISCLOSURE — Are all degradations visible in the material above — abstentions, excluded reviewers, a failed Devil's Advocate, a skipped debate round — disclosed in the footer? And does the memo avoid describing how it was produced, in any wording — members, "analyses", "perspectives", reviewers, votes, rounds, debate, convergence, head-counts, tier, stage results, transcript offers? Does the footer hold only real degradations and factual claims corrected after checking — no line about this check, a "late review", the tier or mode that ran, or that nothing degraded? Does anything precede `## Recommendation` or follow the footer, and does the draft name any source, paper or figure that its own body does not contain?

5. CLAIMS — Is every load-bearing precedent, legal or regulatory effect, statistic, base rate, comparative claim, date or timeline (including any claim that a delay is recoverable) in the stated facts, corrected per the verification results, marked unverified once with what to check, or cut? Fail it both ways: a shaky load-bearing claim stated plainly, and "(unverified)" tags on textbook facts, repeated tags, or a tag inside Recommendation or What to do. Do the draft's numbers and timelines agree with each other?

6. COVERAGE — Does the draft answer every part of the question as asked (each option, each sub-question, each "what can I do"), including the concrete steps and must-check facts the practitioner member gave — or name under Confidence what it leaves out? Does it say each thing once (quote any passage told twice), do its sections fit the question's shape (an evaluation question gets a test or triage, not a project plan), and does any recommended step hand an accuracy decision to an interested party?

Reply in exactly this form:

DISSENT: PASS / FAIL — [evidence]
GROUNDING: PASS / FAIL — [evidence]
CONFIDENCE: PASS / FAIL — [evidence]
DISCLOSURE: PASS / FAIL — [evidence]
CLAIMS: PASS / FAIL — [evidence]
COVERAGE: PASS / FAIL — [evidence]

MOST IMPORTANT FIX: [one sentence, or "none"]

If all six pass, say so plainly. Do not invent problems to seem useful — a clean draft is a valid outcome.
```

## What the Chairman does with the result

Any `FAIL` is **blocking**. Either fix the synthesis and log what changed in the council record — when no record is being written, log it nowhere: never above `## Recommendation`, never in the footer (a round-3 run delivered its checker report as the answer's first paragraph; in round 4 four of ten answers carried a note about the check, and judges marked it as residue) — or — if you genuinely disagree with the checker — ship your version **with the checker's objection quoted verbatim** in the output. Silently overriding it defeats the entire stage.

A checker that returns six PASSes is not wasted spend: it is the only evidence anywhere in the protocol that the synthesis survived a reader who wasn't invested in it.
