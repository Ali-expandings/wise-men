# arm: ecc-council (affaan-m/ECC 8321021c54d6) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: no-human (a clarifying question becomes a stated assumption) — see PREREG-2.md
# subagent tokens: 98353 | tool uses: 4 | duration: 354s

## Council: Why Event Sourcing Falls Apart Mid-Build

**Architect:** Tutorials never build the parts that make event sourcing expensive — schema versioning, projection rebuilds at scale, replay-safe side effects — because the toy domain's shape and query set never change. Real domains do, so the bill arrives as a deadline crisis instead of a design decision.
Why: fixed-shape tutorials never exercise the costs that only show up once the event log has to survive change.

**Skeptic:** The two abandonments are more likely evidence of good judgment than proof event sourcing is broken. Teams built the easy command → event → apply loop, hit the genuinely hard 20% — versioning, concurrent writes, deletion — unspiked, and walked away while the rewrite was still cheap.
Why: bailing mid-build is the cheap failure mode; the expensive failure is the company that finishes and ships an ES core it can no longer afford to remove.

**Pragmatist:** Event sourcing fails on economics, not technical merit. The cost front-loads — permanent schema contracts, no admin tooling, only one or two engineers who understand the model — long before the payoff shows up, so leadership pulls funding once velocity visibly craters against a CRUD baseline.
Why: nobody gated the decision on "do we actually have a second consumer of this event stream" before committing on day one.

**Critic:** The kill shot is usually one incident, not slow fatigue. Rebuilding a projection replays events through handlers that were never isolated from side effects — firing duplicate emails or double charges — and that single trust-destroying event is what actually gets the project pulled.
Why: scoping ES to a single subdomain, the standard mitigation, just relocates the same cost into sagas and anti-corruption layers at the boundary.

### Verdict
- **Consensus:** All four land on the same two structural traps, invisible in any tutorial: the event log is a permanent, unversioned contract that punishes any schema or aggregate-boundary mistake, and the number of projections/read-models grows faster than the team can maintain — because tutorials fix the domain and query set in advance, and production never does.
- **Strongest dissent:** The Skeptic rejects the question's framing. "What went wrong" assumes failure; abandoning mid-build while the rewrite is still cheap may be the team correctly cutting a bad bet early — a success case for risk management, not evidence event sourcing is unworkable.
- **Premise check:** Yes. The Skeptic explicitly challenges "what went wrong," reframing both abandonments as possibly the system working as intended rather than a technical failure.
- **Recommendation:** The Skeptic and Pragmatist independently converged on the same root cause — a decision made before the hardest problems were validated, not a failure of execution — which shifted this synthesis away from "event sourcing is inherently hard to run" toward "these teams committed before derisking it." Before adopting event sourcing on a core domain: spike the expensive 20% first — a live schema/event change, a concurrent-write conflict, a full projection rebuild with side effects isolated — and require a named second consumer of the event stream as the bar for "we need history, not just an audit trail." If nothing clears that bar, an append-only audit table plus a transactional outbox captures most of the value event sourcing was chosen for, at a fraction of the permanent cost. If something does clear it, budget the versioning and tooling layer as core scope from day one, not as later cleanup — that's the piece every abandoned build was missing when the bill came due.
