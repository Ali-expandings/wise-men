# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q05 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 106444 | tool uses: 4 | duration: 645s

## Council

Model diversity was limited to the Claude family in this harness (no GPT- or OSS-class model available) — per the skill's substitution rule, noted here and compensated with distinct assigned angles across Opus/Sonnet/Haiku rather than redundant same-angle review.

- **Opus** — architect/correctness: named middle-ground patterns (modular monolith, Self-Contained Systems, strangler-fig/Citadel), coupling risk, Conway's-law sizing for 8 engineers.
- **Sonnet** — contrarian/red-team: stress-tested whether architecture is even the right lever, versus a pure release-process fix.
- **Haiku** — implementation/ops feasibility: concrete pipeline changes, sprint-level cost, smallest first step.

## Recommendation

Skip full microservices at 8 engineers — none of the three reviewers defended it at this headcount. The real middle ground is sequential, not architectural-only: fix the deploy pipeline itself first (trunk-based deploys, feature flags, per-module CI), then enforce a modular monolith with real module *and data* boundaries, and only strangler-fig a service out later for the one or two pieces that genuinely need independent scaling or ownership.

## Why

- **The pain is usually process, not architecture.** All three reviewers converged on this: a shared deploy gate, batched release trains, a slow/flaky shared test suite, and no feature flags reproduce exactly this coordination symptom with zero code coupling involved. That's fixable in days-to-weeks with no rewrite risk, and often removes most of the pain by itself.
- **A modular monolith only works if it splits data, not just packages.** All three independently flagged the same trap: teams draw clean module boundaries in code but leave one shared database and one CI gate in place. That's "theater" — it relocates the pain behind nicer folders instead of removing it. The boundary has to include table/schema ownership to count.
- **The team-size math rules out full microservices.** Conway's law and Team Topologies put a sustainable team at 5–9 people; 8 engineers can responsibly own maybe 2–4 independently deployable boundaries, not 6–10 services each needing its own pipeline, on-call, and observability. The one steelman for microservices at this size (fully-owned domains, no shared DB, ops mostly offloaded to managed platforms) doesn't match a team currently fighting a shared monolith's deploy gate.

## Tradeoffs and risks

- Feature flags and rolling deploys carry their own correctness risk — old and new code run concurrently against one schema, so this needs expand/contract migration discipline and a flag inventory, not just a toggle.
- If the coordination is actually people needing to genuinely discuss shared business logic (essential complexity), no repackaging fixes that — it's an ownership/product conversation, not an infrastructure one.
- Every service you do extract adds a permanent recurring tax (its own pipeline, tracing, on-call) carried by the same 8 people indefinitely — only justified for a piece with a real reason to be separate (different scaling profile, compliance boundary, genuinely independent data), not for decomposition's own sake.

## Final call

Do now (1 week): pull the last ~20–30 deploys and tag what actually caused each coordination wait — shared test gate, batched release train, a migration forcing lockstep shipping, or a genuine cross-team design discussion — and note which modules/tables tend to change together. That answer picks the branch: if it's mostly pipeline, ship trunk-based deploys + feature flags + parallelized per-module CI next (days-to-weeks, no architecture change). If it's real code/data coupling, run the modular-monolith pass — enforced boundaries, contract tests, split table ownership, roughly a quarter at partial capacity. Treat pulling out an actual service as optional future hardening, done only afterward and only for a component with its own data and a concrete reason to scale or own it separately — not as the starting move.
