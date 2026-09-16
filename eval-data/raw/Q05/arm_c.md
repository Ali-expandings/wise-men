# Q05 Arm C Chairman synthesis
# salvaged_from_context: true
# Council: 5 sonnet-4.6 members (Pragmatist, Skeptic, Architect, Maintainer, Devil's Advocate)
# Reviewers: 5 haiku-4.5 (1 refused first call — retried successfully)
# Chairman: main thread sonnet-4.6

## Answer

Modular monolith with enforced boundaries. Eight engineers is too small for microservices — the operational tax (service discovery, distributed tracing, network failure handling, independent CI/CD per service, contract testing) would consume 2-3 of your 8 engineers and you would still have the underlying coordination problem because microservices solve organizational scale problems, not coupling-in-the-code problems.

Concretely:

1. **Identify the 2-3 real seams.** Where teams already mentally divide the system — billing, auth, core product, whatever your domains are. Don't draw boundaries by technical layer (auth-module, payments-module, notifications-module); draw them by business capability (orders-domain, fulfillment-domain). Aim for 3-6 bounded contexts total.

2. **Enforce boundaries with tooling, not convention.** Architecture-test rules (Dependency Cruiser for JS/TS, ArchUnit for JVM, `import-linter` for Python) that fail CI when one module imports another's internals. Without automated enforcement, the boundaries rot back to a big ball of mud within six months — every member of the council named this as the load-bearing failure mode.

3. **Separate database schema ownership per module.** No cross-module direct table access. If module A needs data owned by module B, it goes through B's interface. This is non-negotiable — schema-level coupling defeats application-level module boundaries every time.

4. **Decouple deployment from runtime.** Feature flags + trunk-based development + per-module CI gates let teams ship independently even from one artifact. Most "deployment coordination" pain is solved here, not by splitting the deployment unit.

5. **Conway's Law constraint.** With 8 engineers you likely have 2-3 sub-teams. Architecture should match. One team owns one module. If you can't draw this mapping cleanly, the real problem is org structure not architecture, and microservices won't fix it either.

6. **Extract a service only when you have a concrete forcing function.** Different scaling profile (one module needs 20× capacity), different language requirement, different security boundary, or radically different release cadence. Not because the industry says to. Revisit at 12-18 months or when you cross 15-20 engineers — whichever comes first.

## Dissent worth keeping

Skeptic + Devil's Advocate, both pointing at the same load-bearing risk, preserved: the diagnosis "monolith causes deployment coordination pain" may itself be wrong. If the actual bottleneck is process — shared release windows, manual deploy gates, no feature flags, long-lived branches, broken test suite requiring human sign-off — then architectural changes fix nothing and you will end up six months in with a beautifully modular monolith and exactly the same coordination pain. Before any code reorganization, audit the last 90 days of "hard deployments" and name the specific coordination event. If those events are 80% process and 20% code coupling, fix the process first; the architecture work is then optional. The Devil's Advocate phase model (Phase 1 enforce boundaries → Phase 2 per-module pipelines deploying same artifact → Phase 3 extract a service only for radical reason) is the right sequencing.

## Confidence

High on direction (modular monolith for 8 engineers is well-documented and the alternative is materially worse); medium on whether the user's coordination pain is actually a code-coupling problem versus a process problem, which the dissent flags as load-bearing.
