# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 105204 | tool uses: 4 | duration: 462s
# note: the author's first name (inherited from global config) redacted to "the user" per PREREG Amendment 1

## Council

- **Opus** — architecture/correctness angle: aggregate boundaries, event schema evolution, snapshotting, projection consistency, replay determinism.
- **Sonnet** — implementation/operational angle: tooling maturity, debuggability, team skill curve, projection proliferation, velocity-collapse dynamics.
- **Opus** (reused) — contrarian/red-team angle: challenges the premise, argues fit-vs-execution.

Model-diversity note: the skill's default roster wants Opus + GPT-5.5 + an open-source/third frontier model. This harness only exposes Claude models, so GPT-5.5 was substituted with Sonnet for the implementation seat, and the open-source seat was filled per the skill's own fallback rule — no third model family was available, so Opus was reused with a deliberately adversarial angle instead of a redundant architecture pass. Diversity in that third seat came from perspective, not model family. Approval-before-launch was skipped per this run's operating instructions; this roster is the disclosure of that plan.

## Recommendation

Two things go wrong at once, not one. First, tutorials hide a real operational tax — schema evolution, projection rebuilds, eventual consistency, replay determinism — that's roughly constant no matter what domain you point event sourcing at. Second, most teams pay that tax on a domain that never needed event sourcing's actual payoff (immutable fact history, "what did we believe at time T," genuinely independent consumers of the same events). When the tax has no offsetting return, it reads as "the pattern is a mess," but the real diagnosis is a wrong-fit bet wearing a technical-complexity costume. Abandonment lands *mid*-implementation specifically because the cost is delayed and compounding — it crosses "worse than CRUD" at roughly the 6–18 month mark, often right when the one engineer holding the mental model together leaves or gets reassigned into a deadline.

## Why

- **Tutorials cheat on exactly what gets expensive over time.** One aggregate, one process, no concurrent writers, no schema changes, 2–3 hand-built projections, short in-memory streams. None of that is a lie, it's just scope that never survives contact with a real system. All three council members converge on this independently.
- **The compounding costs are concrete, not vibes.** Upcasters are a permanent tax that never gets smaller — old events never disappear. Every new query becomes a new projection with its own rebuild path and lag monitoring; teams extrapolate from the 2–3 they built in a spike and get blindsided at 15–20. Rebuild cost is real math: roughly a billion events at 5,000/sec is ~2.3 days per projection, which is why teams quietly start hand-patching read tables and lose the ability to rebuild from events at all.
- **The correctness bugs are specific and easy to miss until production volume.** Sequence numbers assigned on insert can commit out of order in SQL-backed stores, so a subscription silently skips an event and nothing errors. Business rules (uniqueness, stock limits) checked against a lagging read model just... don't hold. Non-deterministic handlers (`now()`, external calls, random IDs) quietly break replay.
- **Debuggability and skill curve turn technical cost into organizational cost.** "Why does this record say X" stops being a query and becomes replaying history through however many schema versions exist — that creates one or two bottleneck engineers. New hires take weeks to become productive and months to develop good event-granularity instincts; in the meantime they ship `CustomerUpdated`-shaped events that pass review individually and quietly defeat the point.
- **The contrarian reframe deserves real weight, not just a footnote.** The versioning/projection/consistency tax is roughly constant across domains — what varies is whether the domain actually needed the payoff. The diagnostic is concrete: draft the first ten event types; if more than two are `XUpdated`-shaped, it's CRUD wearing a costume, and no amount of execution discipline fixes that.

## Tradeoffs and risks

- **Real, unresolved disagreement in the council:** the architecture and implementation members lean toward "this is a genuine, underscoped execution problem, survivable with the right practices." The contrarian leans toward "this is a fit/decision problem that execution skill can't rescue." Both are right in different cases and not fully separable — a wrong-fit domain guarantees failure regardless of execution quality, but a well-fit domain still fails without the operational discipline listed above. Diagnosing the two companies needs both lenses, not one.
- **The contrarian's own caveat applies:** "poor fit" as an explanation risks being unfalsifiable if you only judge fit after the abandonment. It only works as a real diagnostic if applied at adoption time, not in hindsight.
- **Reporting bias:** public event-sourcing writing skews negative because teams that succeed with it rarely publish about it. All three reports draw on the same public pattern base, so the felt failure rate may be inflated.
- **Material unknown:** none of the three could speak to what actually happened at the user's two companies — event store choice, scope (one bounded context vs. system-wide), or whether the trigger was technical or organizational. The diagnostic below is built to be pointed at those two cases directly.

## Final call

Apply two questions to each of the two companies, in order:

1. **Fit** — did the domain need event sourcing's actual payoff: immutable fact history with correcting entries rather than edits, a named stakeholder who needs "what did we believe at time T," or genuinely independent consumers building different models off the same events? Fast tell: look at their first ten event types — mostly `XUpdated`-shaped means CRUD in costume.
2. **Execution**, only if (1) is yes — was the tax actually budgeted and owned: versioning discipline with upcasters, projection-lag monitoring and rehearsed rebuilds, checkpoints written in the same transaction as read-model updates, a non-rotating ES-literate owner, and kill criteria written down at adoption time, not invented after things went bad?

If (1) is no, both abandonments were very likely correct calls, not failures — cut losses is the cheapest exit there will ever be, and the postmortem should stop at "wrong tool," not "we executed badly." If (1) is yes and (2) was missing, the mess was avoidable, and it's worth revisiting on a future project scoped to a single bounded context, with the missing practices in place before the first production event rather than after the first bad incident.
