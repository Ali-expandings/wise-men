# Synthesis-check prompt template (Stage 4.5)

Spawn ONE fresh subagent (`wise-member`, mid tier) after the Chairman drafts its synthesis and **before the user sees it**.

**When it fires**: always at `deep` / `paranoid`; at any tier when the run degraded (a reviewer was excluded, a member force-abstained, the DA failed, or a mandated debate round was skipped).

**Why it exists**: the Chairman is the same thread that chose the personas, computed the difficulty, and picked the tier. It is grading its own homework. This is the only stage where an outside party looks at the result, and it is the cheapest available mitigation of the skill's one structural conflict of interest.

Frame it as a checking task, not an appeal to authority — no urgency language, no "you are the final arbiter", nothing that invites either rubber-stamping or contrarianism for its own sake.

---

## Prompt to send

```
Checking task. Below is a draft answer synthesized from several independent analyses, plus the analyses it was built from. Verify the draft against its sources. You are not rewriting it and not adding your own opinion on the underlying question — you are checking five specific properties.

The original question:
"""
{question}
"""

The context brief the analyses were given (the stated facts):
"""
{context brief, or "none"}
"""

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

Answer these five, each with one line of evidence quoted or cited from the material above:

1. DISSENT — Is the Strongest counter-position section a clean COUNTER-position that argues against the Recommendation, rather than the majority thesis restated with hedges? Is it quoted rather than paraphrased into something softer? (A "dissent" that agrees with the decision in weaker words fails this check.)

2. GROUNDING — Does every substantive claim in the Recommendation, Why and What to do trace to something a member actually said or to the stated facts? Flag anything the draft asserts that no member supports.

3. CONFIDENCE — Does each stated confidence match the evidence behind its claim? (High confidence on a claim the members contested, or that nobody verified, fails; so does Low confidence on a claim backed by strong, verified evidence. Agreement, convergence and surviving debate are not evidence — a confidence justified by them fails.)

4. DISCLOSURE — Are all degradations visible in the material above — abstentions, excluded reviewers, a failed Devil's Advocate, a skipped debate round — disclosed in the footer? And does the memo avoid describing how it was produced, in any wording — members, "analyses", "perspectives", reviewers, votes, rounds, debate, convergence, head-counts, tier, stage results, transcript offers? Does the footer hold only real degradations?

5. CLAIMS — Is every load-bearing precedent, legal or regulatory effect, statistic, date or timeline (including any claim that a delay is recoverable) in the stated facts, marked unverified with what to check, or cut? Do the draft's numbers and timelines agree with each other?

Reply in exactly this form:

DISSENT: PASS / FAIL — [evidence]
GROUNDING: PASS / FAIL — [evidence]
CONFIDENCE: PASS / FAIL — [evidence]
DISCLOSURE: PASS / FAIL — [evidence]
CLAIMS: PASS / FAIL — [evidence]

MOST IMPORTANT FIX: [one sentence, or "none"]

If all five pass, say so plainly. Do not invent problems to seem useful — a clean draft is a valid outcome.
```

## What the Chairman does with the result

Any `FAIL` is **blocking**. Either fix the synthesis and state what changed, or — if you genuinely disagree with the checker — ship your version **with the checker's objection quoted verbatim** in the output. Silently overriding it defeats the entire stage.

A checker that returns five PASSes is not wasted spend: it is the only evidence anywhere in the protocol that the synthesis survived a reader who wasn't invested in it.
