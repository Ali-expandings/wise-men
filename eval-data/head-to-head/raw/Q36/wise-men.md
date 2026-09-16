# arm: wise-men | question: Q36 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# skill: SKILL.md v3.9.2 (as written); standard tier selected by the skill (5 members, 3 reviewers)
# subagent tokens: 153066 | tool uses: 15 | duration: 344s

## Council answer

**TL;DR:** "Blameless" and "accountability" aren't opposites — they answer two different questions. Blameless governs *how you write about the cause* (systems language, no individual blame). Accountability governs *who owns the fix* (named owner, named deadline, in its own section). Structure carries the resolution. But before you draft anything, there's a real ambiguity you need to close with your manager first — see below.

**Decision:**

Write the causal/root-cause narrative in pure systems language: no name attached to a mistake, no "X forgot to," no character judgment — only gaps (missing guardrail, alert that didn't fire, stale runbook, a step skipped under time pressure). Be concretely specific about the decision and the constraint that produced it ("the deploy shipped without the canary stage because the on-call runbook doesn't budget time for it") rather than vague ("a change was made") — vague blamelessness reads as evasive, not safe, and destroys the trust the whole document depends on.

Then build a visibly separate remediation section. Every action item gets a named owner and a date. This is where "accountability" actually lives in the document — visible ownership of the fix, not blame for the failure. Two sections that look and read differently on purpose is the signal to both audiences (engineers, leadership) that you didn't quietly smuggle blame into "accountability" language.

Before you write a word, ask your manager one direct question: does "accountability" mean *owned, dated fixes* (prospective), or does it mean the *document should identify who's responsible for the outage* (retrospective/consequences)? Four of five council members built their structural advice on the assumption it's the first — and that advice only resolves the tension if that assumption holds. If it's the second, no clever wording of the postmortem fixes that; a document that assigns personal consequences isn't blameless anymore, full stop. Keep that conversation in a separate, personnel-facing channel — the moment engineers suspect the postmortem itself feeds consequences, the honesty of every future postmortem degrades, and that doesn't come back.

Cost of being wrong: this is recoverable if you catch it early — ask the clarifying question, rewrite before it ships. Skip it and guess wrong, and you'll ship a document that reads as evasive to leadership and as a betrayal to the team that trusted the "blameless" label, which is worse than either honest alternative.

**Confidence: Medium** — not High, because all five members' stated weakest assumption converges on the exact same unverified point: what your manager actually means by "accountability." That's not five independent confirmations, it's one open question wearing five coats. Resolve it before you draft.

## Dissent worth keeping

The Devil's Advocate pushed back on the whole "just structure it well" consensus: "accountability" is quietly doing two incompatible jobs — owned fixes vs. consequences for a person — and structural advice papers over which one your manager means. If a major, customer-facing outage is behind this ask, the base rate favors the manager actually wanting the second, since the pressure is usually coming from above him, not from a process-improvement impulse. In that case the honest move isn't a cleverer document; it's telling him that conversation doesn't belong in the postmortem at all.

---
*Council of 5 members, standard tier (Content Strategist, Editor, Rhetorician, Audience Advocate, Devil's Advocate — reasoning procedures: first principles, precedent, falsification, incentives, base rates). 3 reviewers, no severe-disagreement flags, no debate round (standard tier). Want the full audit trail — all five answers, rubric scores, reviewer notes? Ask for the transcript.*
