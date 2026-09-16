# Q09 Arm C Chairman synthesis
# salvaged_from_context: false
# Council: 5 sonnet-4.6 members + 5 haiku-4.5 reviewers + main-thread chairman
# Stage 2 aggregate: DA 16.0 (top), Maintainer 15.0, Architect 14.4, Skeptic 13.6, Pragmatist 13.2

## Answer

Event sourcing looks clean in tutorials because tutorials model a closed world — one bounded context, a stable event schema, no operational pressure, no team turnover, and twenty events in the log. Real codebases are open systems, and the cleanliness collapses along six predictable seams:

1. **Schema evolution is a one-way door.** Events are immutable and accumulate forever. When `OrderPlaced` needs a new field eighteen months in, you own upcasting logic, a version registry, and the obligation to handle every historical shape correctly forever. Tutorials never show you event version 47.
2. **Projections rot and rebuilds become an ops crisis.** Every query is a custom projection you maintain. Rebuilding one over 200M events takes hours, not milliseconds — so every schema change becomes a maintenance window or a blue/green projection dance. Nobody owns projections proactively; they drift.
3. **Eventual consistency infects the UX contract.** "Command succeeded" followed by a stale read means users watch their own writes disappear. This is a product decision tutorials wave away and teams discover in QA.
4. **Snapshots arrive as an afterthought** — aggregate rehydration at event 2M is a performance cliff hit in production, not planning.
5. **Thin tooling** — outside a few mature stacks you're building infrastructure, and Kafka-as-event-store is a common category error.
6. **Knowledge bus factor** — the conceptual surface is large; when the one person who understood the upcaster chain leaves, the system is a black box.

But the deepest point — and the one that actually answers "what goes wrong" — is that event sourcing is not inherently messy. The mess comes from a specific, avoidable decision: **coupling the event log to the query model and treating the event store as a shared database across teams.** The concrete failure: Team A adds a field to `OrderPlaced` in month 4; Team B's fraud model, which replays from position 0 on cold start, silently drops events it can't deserialize; fraud scores go stale; a chargeback spike surfaces months later; root-cause tracing means replaying 18 months of events through three undocumented schema versions. A relational schema migration would have been visible, blocking, and centralized. Event sourcing made the schema change feel free — it was not.

**Recommendation:** Do not adopt event sourcing as a system-wide default. Use it surgically where the audit log or temporal query IS the core product requirement (financial ledgers, compliance domains) — not a side benefit. Everywhere else, CQRS with a CDC/outbox pattern on a normal relational model gives you ~70-80% of the benefit at ~10-20% of the operational cost. If you do adopt it: confine it to a bounded context where you control every consumer, stand up a schema registry (versioned event envelope) before writing the first event, build the projection-rebuild pipeline before go-live, and define your upcasting contract on day one. The litmus test: if you cannot name every consumer of every event stream on a whiteboard right now, you are not ready.

## Dissent worth keeping

Devil's Advocate, preserved (and rated highest by the council): the obvious answer — "event sourcing is too complex, wrong tool" — is wrong. The companies that abandon it write the retrospectives; the ones that succeed are too busy shipping. The two abandonments you saw may reflect team skill gaps and missing governance (no schema registry, shared event store across uncoordinated teams) rather than an inherent flaw in the pattern. Event sourcing may be a power tool that injures novices, not a broken tool — and the honest fix is "don't use it without someone who has done it before, and without a schema-governance contract," not "avoid event sourcing."

## Confidence

High — five members converged on the same six failure modes with strong real-world grounding (upcasting, projection rebuild cost, eventual-consistency UX, knowledge concentration), and the highest-rated member reframed the root cause from "ES is flawed" to "uncontrolled schema coupling across consumers," which is the actionable lever.
