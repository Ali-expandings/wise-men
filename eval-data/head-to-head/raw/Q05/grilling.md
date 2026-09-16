# arm: grilling (mattpocock/skills 85f83d3fde1d; grill-me delegates to it) | question: Q05 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# adaptation: no-human (asks the frontier, assumes likeliest answers, continues) — see PREREG.md
# subagent tokens: 77191 | tool uses: 1 | duration: 67s

❓ **Q1** - **Root cause of the pain**: What's actually forcing cross-team coordination on deploy — (a) a shared release pipeline/deploy train where everyone's changes ship together, (b) shared DB schema/migrations that break if teams don't sequence, (c) blast radius fear (one team's bug takes down the whole app), or (d) code-level coupling/merge conflicts from shared modules?

➡️ (a), likely compounded by (d) — "hard to deploy without coordination" describes a shared release train, not a runtime failure mode.
✅ Assumed: (a) shared deploy pipeline is the primary pain, with (d) ownership/merge friction as a secondary driver.

---

❓ **Q2** - **Team trajectory**: Is headcount staying near 8 for the next 1-2 years, or is this a pre-hypergrowth team about to scale to 20-30+ engineers?

➡️ No hypergrowth signal in the framing — read as a steady team, maybe 8→12-15 over a couple years.
✅ Assumed: stays small-to-mid, not hypergrowth. This rules out full microservices' main justification (org-scaling, independent team-of-teams ownership).

---

❓ **Q3** - **Infra maturity**: Is there already CI/CD and containerization (the monolith ships as one containerized artifact through a pipeline), or is deployment still manual/legacy?

➡️ The complaint is about coordination, not tooling — implies CI/CD already exists, just gated as one artifact/one pipeline.
✅ Assumed: modern CI/CD exists; the constraint is that it produces a single deployable unit, not that automation is missing.

---

❓ **Q4** - **Source of the "go microservices" pressure**: Is this a leadership mandate, or informal peer/industry chatter?

➡️ "Everyone says" reads as ambient pressure, not a directive from above.
✅ Assumed: informal pressure — the team has latitude to pick the right-sized architecture rather than defend against a mandate.

---

❓ **Q5** - **Modular monolith vs. selective service extraction**: Given the pain is deploy coordination itself (not runtime blast radius), does enforcing module boundaries inside one deployable (a "modular monolith") solve it, or do you need a small number of independently deployable units so teams stop waiting on each other's release windows?

➡️ Since the complaint is specifically about not being able to deploy without coordinating, boundaries alone won't fix it — you need independent deployability, just not full service-per-team fragmentation.
✅ Assumed: split into a small number (not many) of independently deployable services, each still living in one codebase — the "macroservices" middle ground.

---

❓ **Q6** - **Data layer**: Keep one shared database for now (with enforced per-module schema ownership), or split databases per service immediately?

➡️ At 8 engineers, distributed data (sagas, eventual consistency, cross-service transactions) is the single biggest source of microservices pain and isn't justified yet.
✅ Assumed: keep one shared database, but each module only touches its own tables and exposes access through code — no cross-module joins. Physical DB split stays optional, deferred until real evidence demands it.

---

❓ **Q7** - **How many services, split along what axis**: Team-of-8 realistically supports how many independently deployable units, and chosen on what basis?

➡️ Sub-teams of 2-4 people naturally cap this around 2-3 services — more than that just recreates coordination overhead at a smaller scale.
✅ Assumed: 2-3 services, boundaries drawn around whichever domains generate the most concurrent PRs / merge conflicts today (the actual friction, not a theoretical domain model).

---

❓ **Q8** - **Shared code**: Extract common logic (auth, logging, shared models) into an internal shared package, or duplicate per service?

➡️ A monorepo already has the shared package as a compile-time import, not a network call — duplication only adds drift risk for no benefit.
✅ Assumed: internal shared package(s) in the same monorepo, versioned but not networked.

---

❓ **Q9** - **Repo layout**: Monorepo with multiple deploy targets, or split into polyrepos per service?

➡️ At this scale, polyrepo mainly adds cross-repo PR and dependency-bumping overhead with no real ownership benefit for 8 people.
✅ Assumed: monorepo, multiple deployable packages, path-based CI triggers per service.

---

❓ **Q10** - **Release process**: Trunk-based development with feature flags and independent per-service deploys off main, or keep shared release branches/trains?

➡️ Independent deploy pipelines only remove the coordination pain if paired with trunk-based dev + flags — otherwise branch-based release trains just recreate the same bottleneck one level down.
✅ Assumed: trunk-based main, feature-flagged incomplete work, each service deploys independently the moment its own tests pass.

---

**Final recommendation**

Don't go microservices. Go **modular monolith → macroservices**: split the current monolith into 2-3 independently deployable services along the boundaries that actually generate deploy contention today (not a theoretical domain model), keep them all in one monorepo, keep one shared database with per-service schema ownership enforced in code (no cross-service joins, no distributed transactions yet), share common logic via an internal package rather than a network call, and move to trunk-based development with feature flags so each service ships off main the moment its own tests pass — no shared release train, no cross-team sign-off.

This directly kills the stated pain (can't deploy without coordinating) without taking on what actually kills small teams under real microservices: distributed data consistency, service-mesh/observability overhead, and per-service on-call — none of which 8 engineers can staff. Revisit physical DB splitting or further service extraction only when a specific service's scaling or ownership needs force it, not preemptively.
