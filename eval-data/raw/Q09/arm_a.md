# Q09 Arm A raw output
# salvaged_from_context: false
# model: sonnet-4.6
# skill_suppression: applied
# contamination: none

Event sourcing fails in practice for a cluster of interconnected reasons that tutorials systematically hide.

**Tutorials cheat on the read model problem.** The write side — append an event, done — is genuinely clean. But every query you need is now your problem. Tutorials show one projection. Real systems have dozens, they drift out of sync, they need to be rebuilt when business logic changes, and rebuilding a projection over years of events takes time your SLA won't tolerate. Teams discover they've essentially built two databases and they're responsible for keeping them consistent.

**Snapshots arrive as an afterthought.** When your aggregate has 50,000 events and you need to load it to process one command, you need snapshots. Snapshot strategy, invalidation, versioning — none of that is in the tutorial. It's a second design problem that most teams hit in production, not in planning.

**Schema evolution is brutal.** Relational schemas are painful to migrate, but the pain is localized. Events are immutable and accumulate forever. When the business logic of "what OrderPlaced meant" changes — and it will — you have upcasting, versioning, or replay strategies to implement. Event versioning sounds manageable until you have six versions of the same event and code that has to handle all of them. Teams also routinely underestimate how often business requirements force semantic changes to past events, which is philosophically awkward because the whole premise is that the log is the truth.

**The tooling ecosystem is thin.** With a relational database, every problem you hit has a Stack Overflow answer, a mature migration tool, and a DBA you can hire. Event sourcing tooling is narrower. EventStoreDB is good but opaque to most ops teams. Rolling your own event store on Postgres is common and creates a maintenance burden that grows.

**Temporal queries get weird fast.** Tutorials show you rebuilding state as-of-now. Real product managers ask "what did the customer see on March 3rd?" and "show me all accounts that were in state X last Tuesday." These are solvable but require deliberate projection design upfront, and most teams don't think through the query surface they need before committing to the pattern.

**The organizational mismatch is underestimated.** Event sourcing shifts cognitive load from runtime to design time. You have to model the domain extremely carefully — the event stream is your schema. Most teams don't have that discipline, or have enough turnover that the original modelers leave. Within 18 months you get events that are underspecified, inconsistently named, overlap semantically, and the aggregate boundaries are wrong. Changing any of this is expensive.

The two-company pattern you saw is common. The typical arc: clean start, works well for the first bounded context, team adds two more, projections multiply, a new developer introduces an event that's slightly wrong, rebuild takes longer than expected, someone realizes half the read models are wrong because a projection handler had a bug that ran for three months, and at some point leadership asks "why is this so complicated." The answer — that the model captures full history and that's inherently complex to query — doesn't satisfy anyone at that moment.

It's genuinely a good pattern for specific problems: financial ledgers, audit-required domains, systems where temporal replay has business value. It's a bad default architecture, and tutorials sell it as a default.
