# Debate round prompt template (Stage 3, deep/paranoid tiers only)

Spawn only when peer-review shows severe disagreement, per the canonical trigger (single source of truth, identical in SKILL.md, peer-review.md, debate.md):

> **Debate-trigger formula**: variance ≥ 1.5 on any rubric axis OR a member ranked top-2 by some reviewers and bottom-2 by others on the same axis.

Two debaters: the most-praised member + the most-criticized member. Each sees the other's answer + the specific objections raised against their own.

## Input extraction (orchestrator-side)

Before sending the prompts below, the orchestrator constructs `{objections_against_you}` and `{reasoning_against_you}` from upstream data — these are NOT free-form; they have a defined extraction rule:

- `{objections_against_you}` = concatenated verbatim of (a) every reviewer's per-axis one-line justification addressed to this member on the axes where they scored lowest, plus (b) any reviewer's severe-disagreement-flag content that names this member.
- `{reasoning_against_you}` = same construction, but targeting the bottom-ranked debater (the reviewer reasoning for why the opponent's answer outranked this debater's).

If no severe-disagreement flag names the member, omit clause (b). If a member has no rubric justifications below their mean, fall back to the lowest-scored axis's justification. Never invent objections; if upstream is empty, abort the debate round for that pair.

---

## Prompt for the top-ranked debater

```
You wrote this answer to a question:

"""
{your_original_answer}
"""

Another council member wrote a competing answer:

"""
{opponent_answer}
"""

Some reviewers preferred theirs over yours. Their specific objections to your answer:

{objections_against_you}

You may now either:
(a) UPDATE your answer in response to their critique
(b) HOLD your position and rebut their critique

Reply in this format:

DECISION: UPDATED / HELD

REVISED ANSWER (if UPDATED) or REBUTTAL (if HELD):
[Your full revised answer OR a tight rebuttal of their objections, depending on (a)/(b)]

CONFIDENCE: low / medium / high

ONE THING YOU CONCEDE TO THEM:
[Even if you HELD, name one valid point they raised. Honest debate, not stonewalling.]
```

## Prompt for the bottom-ranked debater

```
You wrote this answer to a question:

"""
{your_original_answer}
"""

Another council member wrote a competing answer that some reviewers preferred:

"""
{opponent_answer}
"""

Their answer was ranked above yours. Reviewer reasoning for that ranking:

{reasoning_against_you}

You may now either:
(a) UPDATE your answer in response to their critique
(b) HOLD your position and rebut

Reply in this format:

DECISION: UPDATED / HELD

REVISED ANSWER (if UPDATED) or REBUTTAL (if HELD):
[full revised answer or tight rebuttal]

CONFIDENCE: low / medium / high

ONE THING YOU CONCEDE TO THEM:
[name one valid point even if you HELD]
```

## After debate

Run a **lightweight Stage 2**: spawn one reviewer (any persona type) to re-rank the two updated answers on the same rubric. Single reviewer, single round — debate is cheap, re-judging it doesn't need a full panel.

The result feeds Chairman synthesis. Chairman should:
- Note which debater UPDATED and which HELD
- Note what each conceded (these concessions often hold the real signal)
- Weight the final answer toward whoever's position survived the rebuttal cleaner

## Why this works

- **Forced concession** ("ONE THING YOU CONCEDE") — prevents pure stonewalling. Every debater names a valid opposing point. Honest debate.
- **Update or hold choice is explicit** — Claude won't drift into wishy-washy "you raise a good point but..." — must commit.
- **Two debaters, not all N** — debate among everyone = chaos. Two is enough to see if a position survives pressure.
- **Single re-judge afterward** — full re-judging would double the cost. One reviewer is enough to see if the picture changed.

## Skip conditions

Skip when the canonical debate-trigger formula does NOT fire — i.e., variance < 1.5 on every rubric axis AND no member is ranked top-2 by some reviewers and bottom-2 by others on the same axis. Also skip when:

- User specified `quick` or `standard` tier
- Question is low-stakes (council shouldn't debate "what variable name to use")
- All non-abstaining members had similar scores AND no severe-disagreement flag was raised by any reviewer

## Cost note

One debate round adds ~3 subagent calls (2 debaters + 1 re-judge). `deep` tier adds 1 round. `paranoid` adds 2. Don't run debate by default — it's high cost, high signal, save it for when the council actually splits.
