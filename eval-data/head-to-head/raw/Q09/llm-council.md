# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 115218 | tool uses: 12 | duration: 235s

## Council Verdict: Why Event Sourcing Dies in Production

### Where the Council Agrees
All five advisors converge, independently, on **schema evolution as the real unsolved problem** — events are permanent contracts, tutorials never show v2, and real systems accumulate versioned event types, dead upcasters, and no clean way to fix a bad event emitted months ago.

Second convergence: **nobody budgets for the read side.** "One source of truth" quietly becomes two systems in a trenchcoat — the event log plus a projection layer nobody scoped as ongoing work.

Third, weaker but real: **abandonment is organizational, not purely technical.** The pattern requires a discipline (naming, projection ownership, a permanent migration process) that gets adopted as a technical decision by one enthusiast engineer, without the org agreeing to fund it. When that person leaves or gets reassigned, the discipline evaporates and the codebase is left half-migrated — the worst possible state.

### Where the Council Clashes
The Expansionist argued teams abandon too early — they pay the full architectural tax without cashing in the payoff (free read models, replay-based simulation, compliance-grade audit as product). Four independent peer reviews flagged this as the weakest response: it reframes documented failure modes (schema hell, dual-write reconciliation, 2am on-call debugging) as an internal-marketing problem, which is unfalsifiable and doesn't engage with what the other four converged on. It isn't wrong about the mechanism — under-committed event sourcing (one projection, no snapshotting) is a real anti-pattern — but the causality runs backward: thin commitment is a *symptom* of unfunded governance, not the root cause of failure.

Smaller clash: the Contrarian frames the core failure as **migration** — running event sourcing alongside a legacy system indefinitely via dual writes. No other advisor develops this, but nobody rebuts it either. It sits as a plausible fourth failure mode just outside the consensus cluster.

### Blind Spots the Council Caught
Peer review surfaced what no advisor raised solo:
- **Dual-write consistency as its own technical failure** — transactional outbox, idempotency, ordering bugs causing actual data corruption during migration, not just "dual truth" as a vague description.
- **Infra/tooling burden and vendor lock-in** — Kafka/EventStoreDB retention and operational maturity versus boring Postgres. Nobody priced this in.
- **GDPR right-to-erasure vs. immutability** — a legal collision with the entire premise, raised by zero advisors.
- **The actual mechanics of the kill decision** — every advisor explained *why* it fails but not *who pulls the plug, over what timeframe*. Abandonment is often silent, gradual reversion, not a formal decision.
- **Nobody asked what actually happened at the two companies.** All five pattern-matched from general priors instead of using the highest-signal data available — your own two data points.

### The Recommendation
Trust the four-way convergence over the outlier. Event sourcing fails for a small, recurring, well-understood set of reasons: schema evolution has no real answer at scale, the read side always needs a second system nobody scoped, and the organizational commitment required is bigger than the technical decision to adopt it. It gets adopted as an architecture choice and abandoned as a staffing problem. The Expansionist's "you didn't sell it hard enough" is real in a narrow band (thin, single-projection implementations) but is a symptom of the governance failure, not a competing explanation.

Practically: event sourcing is the wrong default. Reach for it only when "reconstruct exact state at any point in time" is a named, sourced business requirement — not because it's the elegant way to model domains. For nearly everyone else, CQRS-lite with an append-only audit table bolted onto a normal model gets most of the value at a fraction of the operational surface, without requiring an org to sustain a discipline it never agreed to fund.

### The One Thing to Do First
Go back to the two companies and ask what specifically killed each implementation — the postmortem, not the vibe. That's the highest-value data point available, and the council spent five perspectives pattern-matching from priors while it sat unused.
