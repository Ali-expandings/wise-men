# Peer-review prompt template (Stage 2)

Send this to each reviewer in parallel. Replace `{question}` and member-answer blocks before sending.

## Labeling: stable persona names, no anonymization

Each reviewer sees the N member answers labeled with **stable persona names** (`Member: Pragmatist`, `Member: Skeptic`, `Member: Devil's Advocate`, ...) in fixed order across all reviewers. No randomization, no anonymization.

Why: the prior randomized-label scheme required the Chairman to un-map per-reviewer permutations back to original member identity. That mapping was never defined, persisted, or transmitted, so cross-reviewer score aggregation silently produced garbage. Stable labels are honest about what Claude can already infer (it knows its own persona prompts) and let the Chairman aggregate scores correctly. Position bias is partially mitigated by the structured rubric instead of by ordering tricks.

---

## Prompt to send

```
You are reviewing answers from N council members. The members had distinct persona briefs (Pragmatist, Skeptic, Devil's Advocate, etc.) but answered the same question independently.

The original question:
"""
{question}
"""

Their answers (labeled by persona name):

--- Member: Pragmatist ---
{answer_pragmatist}

--- Member: Skeptic ---
{answer_skeptic}

--- Member: Devil's Advocate ---
{answer_devils_advocate}

[...continue for all N members]

---

Your task: rate every answer on the rubric below. Judge reasoning quality, not persona identity. One of these answers is your own from Stage 1 — that's fine; you can self-review with the same rubric. Be honest. The Devil's Advocate is told to argue against the obvious answer; weight DA contributions by how concretely a specific failure mode is named, not just by their presence.

**Abstaining members**: if a member's Stage 1 output is the literal "OUT OF DOMAIN — defer to others on this question." marker, **skip the rubric block entirely for that member** — do not score them, do not include them in your top/bottom picks. The orchestrator will treat that member as N/A in aggregation.

## Rubric — score each member 1-5 on every axis

For Member: Pragmatist:
- Correctness (1=wrong, 5=clearly right + evidence): [score] — [one-line justification]
- Insight (1=obvious, 5=novel/generative): [score] — [one-line justification]
- Practical usefulness (1=unactionable, 5=concrete + appropriately scoped): [score] — [one-line justification]
- Risk awareness (1=ignores risks, 5=names what could go wrong + mitigations): [score] — [one-line justification]

[Repeat for each non-abstaining member]

## Machine-parseable rubric block (REQUIRED — emit after prose justifications)

After the prose rubric above, emit one fenced block per non-abstaining member using exactly these keys. The orchestrator parses this block for Chairman aggregation — the prose above is for audit; the fenced block is the contract.

```rubric
member: Pragmatist
correctness: 4
insight: 3
practical: 4
risk: 3
abstain: false
```

```rubric
member: Skeptic
correctness: 5
insight: 4
practical: 4
risk: 5
abstain: false
```

[...one fenced `rubric` block per member, including abstainers with `abstain: true` and all axis scores set to `N/A`]

## Top pick + bottom pick

Top: Member: [name] — [one sentence why]
Bottom: Member: [name] — [one sentence why]

## Severe disagreement flag (only fill if applicable)

If you genuinely think one of the answers is dangerously wrong (would cause real harm if followed), say so here. Otherwise leave blank.

---

Be honest. If two answers are tied, say tied. If one answer is obviously the best, say so. If you have low confidence in your review, say so at the end.
```

## Why this rubric

- **4 axes, not 1** — rubric scoring on 4 specific dimensions forces engagement with concrete reasoning quality, not just gestalt preference. Inspired by (not validated by) Zheng 2024 finding that pairwise LLM judgment has substantial position bias; the rubric mitigation transfers in spirit but is not empirically established for single-model self-review.
- **1-5 scale** — wider than yes/no, narrower than 1-100. Enough granularity, not so much it becomes noise.
- **One-line justification per axis** — forces commitment, lets the Chairman read reasoning, not just scores.
- **Top + bottom + reason** — explicit comparison, prevents "all 4s" lazy responses.
- **Severe-disagreement flag** — catches "this answer would cause real harm" cases that average scoring would bury.

## Aggregation in Chairman stage

When you (main thread) aggregate:

1. Parse the machine-parseable `rubric` fenced blocks from every reviewer. The fenced blocks are the contract; prose justifications are audit only. Use stable persona names as keys.
2. Per non-abstaining member, average each rubric axis across reviewers. **Abstainers** (`abstain: true`) are excluded from axis averages entirely — do not score them as 0, do not impute. Note abstention explicitly in Chairman synthesis.
3. Average across axes per member → overall ranking (abstainers ranked N/A, not last).
4. **Compute per-axis variance per member across reviewers.** Apply the canonical debate trigger (single source of truth, identical in SKILL.md, peer-review.md, debate.md):

   > **Debate-trigger formula**: variance ≥ 1.5 on any rubric axis OR a member ranked top-2 by some reviewers and bottom-2 by others on the same axis.

   Trigger fires at `deep` / `paranoid` tiers only.
5. **Read every reviewer's severe-disagreement flag verbatim.** Surface them unconditionally in Chairman synthesis (dissent section) — never drop, never paraphrase to soften.
6. Note which member won which axis (a member can lose overall but win on, say, risk awareness — preserve that signal).

Because labels are stable persona names across reviewers, aggregation is straightforward: same persona name = same member, sum + average directly.

## When to skip peer review

Always run peer review for `quick` tier with N=3 and above. It's cheap and high-signal.

Skip only if user explicitly requests "just the panel of opinions, no judging".
