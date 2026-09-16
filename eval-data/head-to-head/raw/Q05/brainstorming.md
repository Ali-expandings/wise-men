# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q05 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# adaptation: no-human (asks, assumes likeliest answer, proceeds past approval gate) — see PREREG.md
# subagent tokens: 82138 | tool uses: 1 | duration: 64s

**Classification: Spike.** Feasibility question ("middle ground exist?") — output is a recommendation, not code kept in a repo.

**Probe + assumed nod:** Plan — compare full microservices split vs modular monolith vs coarse "macroservices" against an 8-eng team, find cheapest fix for the actual pain (can't deploy without cross-team coordination). Proceeding on assumed yes.

**Recommendation:**

Named pain: deploys need cross-team coordination. Root cause usually isn't "it's a monolith" — it's tight coupling + one shared deploy artifact + no enforced boundaries. Full microservices fixes coordination but taxes ops hard: every service needs own CI/CD, monitoring, on-call, network-call debugging. Rule of thumb — microservices need roughly a team per service to sustain. 8 engineers running 10+ services trades deploy-coordination pain for operational-toil pain. Not a win.

Real middle ground, three moves, additive, in order:

1. **Trunk-based dev + feature flags.** Highest leverage, cheapest, ship this week. Teams merge to main continuously, ship behind flags, unfinished work stays dark. Kills release-train coordination without touching architecture at all. Often solves most of the actual pain by itself.

2. **Modular monolith.** Enforce real internal boundaries — no cross-module DB reach-through, explicit APIs between modules, boundaries checked by an arch-lint tool (e.g. dependency-cruiser). Still one deploy artifact, so this alone doesn't grant independent deploys — but it kills cross-team coupling pain, lets CI run scoped per module, and sets up clean seams for step 3.

3. **Targeted strangler-fig extraction.** Once boundaries from step 2 are real, pull out only the 1-2 modules with genuinely different needs — different scaling profile, different release cadence, one team owns it end-to-end. Extract those as separate services. Everything else stays monolith. Aim for 2-4 services total, not a dozen. This is "macroservices" — coarse-grained, team-aligned — not microservices' fine-grained split.

Sequencing matters: do 1 first — no architecture change, near-zero cost, often solves 80% of the coordination pain outright. Do 2 over the following months. Only reach for 3 when a specific module demonstrably needs independent deploy or scale, not because "everyone says microservices."

Bottom line: yes, a middle ground exists, and for an 8-person team the cheap fix (flags + trunk-based dev) may make any architecture split unnecessary. Full microservices at this headcount is over-fit — team's too small to staff the resulting ops burden.
