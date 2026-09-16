# arm: grilling (mattpocock/skills 85f83d3fde1d) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# adaptation: no-human — see PREREG.md
# subagent tokens: 76434 | tool uses: 1 | duration: 57s

❓ **Q1** — **What counts as "event sourcing" here?** Full ES (append-only event log as the *only* source of truth, state rebuilt by replay, typically paired with CQRS) — or a looser event-driven/pub-sub architecture that tutorials also call "event sourcing"?

➡️ True ES: domain events persisted as the system of record, aggregates rehydrated by replaying them, read models built as projections.

✅ Assumed: full ES + CQRS, the textbook version — because that's the version that has the failure modes worth diagnosing.

---

❓ **Q2** — **When did the pain hit — build-phase or production?** "Abandoned mid-implementation" points at one or the other: did the teams die building the plumbing, or did they ship and then get killed by prod incidents?

➡️ Build-phase. Mid-implementation abandonment means the team stalled before full rollout — they hit a wall in the architecture itself, not an outage.

✅ Assumed: pain is front-loaded, in getting the system correct and complete enough to ship, not in running it.

---

❓ **Q3** — **What was ES being compared against?** The implicit alternative the team walked back to matters: plain CRUD with an audit table, CDC off a relational DB, or CQRS without full event sourcing?

➡️ CRUD + bolt-on audit log — the default most teams retreat to when they abandon ES, because it gets them 80% of the original motivation (history, undo, audit) for a fraction of the machinery.

✅ Assumed: the comparison baseline is CRUD-with-audit-trail.

---

❓ **Q4** — **(depends on Q1) Where does the complexity concentrate first — event schema evolution, or the read/projection side?**

➡️ Schema evolution hits first (you can't avoid versioning an event the moment a field's meaning changes), projections hit second (rebuilding N read models from a growing log gets slow and stateful fast).

✅ Assumed: versioning is the first wall; projection sprawl is the second, and together they're what stalls a build.

---

❓ **Q5** — **(depends on Q2) Is the build-phase pain infra/tooling debt, or a conceptual mismatch with the domain?**

➡️ Infra debt. Tutorials never show the "invisible 80%": idempotent handlers, snapshotting, replay tooling, dead-lettering, ordering guarantees, eventual-consistency UX. Teams budget for the 20% (aggregates, event store) and get blindsided by the 80%.

✅ Assumed: the gap is operational machinery the domain didn't obviously need, not a fundamental modeling error.

---

❓ **Q6** — **(depends on Q3) Was ES adopted for a real structural need, or because it's presented as "the right way" to do DDD?**

➡️ Usually adopted for audit trail / temporal queries / undo — legitimate needs, but needs that a much lighter mechanism (append-only audit table, outbox pattern) would also satisfy. Full ES gets chosen because tutorials frame it as the mature/correct architecture, not because the domain demanded event-first modeling.

✅ Assumed: over-adoption relative to actual requirement — the team bought the whole paradigm for a narrow need.

---

❓ **Q7** — **(depends on Q4 + Q5) What's the single thread tying versioning pain + projection sprawl + infra debt together?**

➡️ Tutorials model one aggregate, a handful of fixed-shape events, and one projection — so they never need to touch versioning, replay-at-scale, or cross-aggregate consistency. Real systems have dozens of aggregates, events whose shape *will* change, and read models that multiply with every new feature. The tutorial never shows the part that's actually hard, so teams estimate a project scoped to the toy and get a project scoped to the 80% no one warned them about.

✅ Assumed: this is the root cause underneath both companies' abandonment.

---

Frontier empty.

## Final recommendation

Event sourcing tutorials are clean because they're scoped to make the pattern look clean: one aggregate, three event types that never change shape, one projection, no cross-aggregate queries, no scale. Real codebases fail on the parts tutorials skip:

1. **Event schema versioning has no clean answer.** Every event shape will change. Tutorials never show v2 of an event; real systems accumulate upcasting chains, dual-schema handling, and "which version am I replaying" bugs within months.

2. **Projections multiply faster than expected.** Every new feature wants its own read model. Each one needs its own rebuild strategy, its own lag-handling, its own consistency story with the UI. This is where teams first feel "we're writing more code than CRUD would've taken."

3. **The 80% tutorials don't show is infrastructure, not domain logic**: idempotent consumers, snapshotting so replay doesn't take minutes, dead-letter handling, strict ordering guarantees, replay tooling for fixing bad projections. None of this appears in a blog post; all of it is required before the system is production-safe.

4. **Eventual consistency leaks into the UI and the team's head.** "Why doesn't my write show up yet" becomes a constant support/debugging question, and half the team never builds the mental model for it, so every bug triage starts with "is this a projection lag issue?"

5. **Debugging shifts from "read the current state" to "replay the history and infer the state,"** which is slower and requires tooling (event browsers, replay sandboxes) that most teams never build, so debugging becomes a specialist's job — usually whoever designed the system, creating a bus-factor problem.

6. **It's usually adopted for a narrower need than it solves.** Audit trail, undo, temporal reporting — real needs, but satisfiable with an append-only audit log or outbox pattern at a fraction of the operational cost. Full ES is adopted because it's presented as the "correct" DDD architecture, not because the domain forced event-first modeling — so the team is paying full framework cost for partial framework benefit.

7. **Event modeling is an underrated skill gap.** Deciding what is a true domain event vs. a state-change notification vs. a command in disguise is a real discipline (Event Storming, etc.) that most teams skip, leading to anemic or overly granular events that make both versioning and projections worse than they needed to be.

The pattern in both "abandoned mid-implementation" cases is almost certainly: the team estimated the tutorial's 20% (event store + aggregates), started hitting the 80% (versioning, projections, replay tooling, ops maturity) around month 2–3, and leadership pulled the plug before the investment paid off — because nothing in the payoff (audit trail, temporal queries) required the full paradigm in the first place. The fix isn't "do ES better" — it's scoping it to the aggregates that actually need append-only history and temporal replay, and using a lighter audit/outbox pattern everywhere else.
