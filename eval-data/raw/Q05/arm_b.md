# Q05 Arm B raw output
# salvaged_from_context: true
# salvage_note: <thinking> block contained STEP 1 5 perspectives + synthesis. Stripped during blinding. Visible output: ## Answer / ## Dissent / ## Confidence per frozen prompt.
# model: sonnet-4.6
# leakage_check: PASSED (no retry)

[<thinking> block stripped during blinding contained 5 persona positions: Pragmatist (modular monolith with deployment tooling), Skeptic (boundaries rot without enforcement), Architect (Conway's Law + team topology), Devil's Advocate (the diagnosis itself may be wrong), User Advocate (engineers want fast safe deploys + clear ownership)]

[VISIBLE OUTPUT — judge sees:]
## Answer

The middle ground is a **modular monolith with enforced boundaries plus deployment tooling** — and you need both halves, not just one.

**The two problems are separate.** Deployment coordination pain and codebase coupling pain feel the same but have different fixes:

- **Deployment coordination** → fix with CI/CD discipline: trunk-based development, feature flags for in-progress work, per-module ownership in CODEOWNERS, and automated deploy gates. Teams can ship independently even from one artifact if feature flags decouple "code in main" from "feature is live."

- **Codebase coupling** → fix with hard module boundaries enforced by tooling, not convention. This means separate packages/namespaces per domain, with no cross-module imports except through declared interfaces. Critically, enforce this with architecture linting tools (e.g., Dependency Cruiser for JS/TS, ArchUnit for JVM, or custom import-graph checks in CI). Without automated enforcement, the boundaries rot back to mud within months.

**On the seams question:** With 8 engineers, you likely have 2–3 natural sub-teams. Apply Conway's Law deliberately — your deployment units should match your team topology, so 2–3 modules owned by those sub-teams. If one domain is causing disproportionate pain *and* has a clean interface, use strangler fig to extract it as a separate service — but extract exactly one at a time, validate the overhead, and only continue if the tradeoff is clearly positive.

**What not to do:** Don't split into microservices speculatively across the whole codebase. Distributed systems multiply your operational surface area (service discovery, network failure, observability, contract testing) and 8 engineers will be crushed maintaining more than 3 services before your product matures.

## Dissent worth keeping

A modular monolith still lets everyone touch everything — the discipline required to maintain module boundaries in a shared codebase might actually be *higher* than just forcing service boundaries, because with services, cross-boundary violations are impossible by definition, whereas with modules, violations are always just one bad PR review away. If your team's code-review culture is weak, microservices enforce ownership structurally in a way no amount of linting will match.

## Confidence

Medium — the perspectives largely converged on modular monolith with tooling enforcement, but the enforcement point introduces meaningful team-culture dependency that can flip the answer if your review discipline is low.
