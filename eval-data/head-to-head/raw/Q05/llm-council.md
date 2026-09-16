# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q05 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 124876 | tool uses: 20 | duration: 248s

## Council Verdict: Monolith vs. Microservices at 8 Engineers

### Where the Council Agrees
Every advisor converges on the same core diagnosis, independently: full microservices at 8 engineers is the wrong call, and the "spectrum" framing (monolith ↔ microservices) is itself misleading. Coordination pain is a coupling problem, not a deployment-topology problem — splitting processes without first splitting the coupling just relocates the pain into a network call, where it's harder to debug. The convergent prescription is a modular monolith: enforced module boundaries (linter/build-time check, not code-review vibes), independent deploy pipelines per module inside one repo, and feature flags to decouple "merged" from "live" — which directly attacks the stated symptom (release windows requiring cross-team scheduling) without adding infra. All five also agree that if extraction ever happens, it should be opportunistic and minimal (1-2 services, chosen because they've demonstrably earned it), never a wholesale target-architecture redesign up front. That's five independent arrivals at the same shape — a strong signal.

### Where the Council Clashes
The real split isn't architecture — it's sequencing. The Executor says start building next sprint: carve modules, add flags, extract later, and explicitly kill any attempt to "design the target architecture first" as wasted motion. The First Principles Thinker (backed strongly by peer review) says stop: spend a week first mapping actual coupling — which modules touch which tables, which changes historically caused breakage — because you cannot draw good boundaries without knowing where the real coupling lives, and guessing is exactly how you burn the months you're afraid of.

Both are right about different failure modes. The Executor is right that analysis-paralysis is a real risk for an 8-person team already in pain. The First Principles Thinker is right that if you skip diagnosis and the coupling is organizational (nobody owns clear boundaries) rather than technical (shared tables), you'll build enforced module boundaries this quarter and watch them get violated by the next reorg or deadline crunch — because a linter can't fix a boundary nobody agreed to defend. This isn't a contradiction to smooth over; it's a real tension between bias-to-action and bias-to-diagnosis, resolved by sequencing rather than picking a side.

### Blind Spots the Council Caught
Peer review surfaced two things no advisor raised on their own, and both are load-bearing:

**Data/schema coupling.** All five advisors talk about boundaries at the code level — packages, namespaces, import linters. None mention the database. If there's one shared schema with cross-module foreign keys and transactions, code-level module boundaries will not stop coupling at the data layer — and this is usually the actual reason a later extraction becomes a multi-quarter migration instead of a clean pull.

**Ownership/Conway's Law.** Every advisor treated this as a purely technical exercise and nobody asked who owns the boundaries organizationally. With 8 engineers stepping on each other, that's plausibly because nobody has standing authority to say "this is your module, stay out." A linter enforces a boundary; it doesn't create one. Without a named owner per module, boundaries erode under the next deadline the same way the current tangle did.

### The Recommendation
Build the modular monolith — enforced boundaries, per-module CI/deploy, feature flags to decouple ship-from-release. That part of the council's agreement is high-confidence and low-risk; don't relitigate it. But sequence it correctly: run diagnosis and construction in the same short window, not as two separate phases.

Concretely: don't spend a standalone week "mapping coupling" in the abstract — too slow, and the team is already in pain. Instead, use the act of picking the first two modules to extract as the diagnostic. Pick the two modules causing the most collisions, but before enforcing boundaries around them, check the two blind spots: (1) do those two modules share database tables or transactions — if yes, that's your real first target, not the code boundary; (2) name one owner (a person, not a team) per module who has authority to reject a cross-boundary PR. If you can't name that owner, the org problem is the actual blocker and no linter fixes it — go fix that first, it's a conversation, not a sprint.

This is not "it depends." Modular monolith, boundaries enforced by tooling, deploy decoupled via flags and path-based CI, extraction only when a module demonstrably earns it — that's the answer for an 8-engineer team, full stop. The only real risk is skipping the data-ownership and named-owner steps, because those are exactly the parts that don't show up in a demo and only surface as pain six months in.

### The One Thing to Do First
This week, before writing any linter config: get the 8 engineers in a room and, on a whiteboard, name the 3-4 module boundaries, who owns each one, and which of those boundaries currently share a database table with another module. If you can't finish that in an afternoon, that's the actual problem — not deployment topology — and it's cheaper to find out now than after you've built tooling around boundaries nobody agreed to.
