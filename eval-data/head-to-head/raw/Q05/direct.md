# arm: direct (no skill) | question: Q05 | general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 69140 | tool uses: 0 | duration: 15s

Yes. Middle ground exists, has a name: **modular monolith** with independent deploy paths, or "macroservices" if you want partial extraction.

**Options, cheapest first:**

1. **Modular monolith + strict boundaries.** Split codebase into modules with enforced interfaces (no shared DB tables across modules, no reaching into internals). Use a linter/build rule to enforce it (e.g. Nx, ArchUnit, Go internal packages). Teams own modules, not the whole deploy. This alone kills most "coordinate across teams" pain — most of that pain is really about unclear ownership and tangled code, not lack of network hops.

2. **Deploy the monolith in slices.** If build/deploy time is the real problem, not the code coupling: separate build artifacts per module, feature flags for risky changes, branch-by-abstraction instead of long-lived branches. You get independent release cadence without independent runtimes.

3. **Extract only the 1-2 services that actually need it.** Usually it's one hot path (payments, a queue-heavy worker, something with different scaling needs) — pull that out, leave the rest monolithic. This is "macroservices": 2-4 deployables instead of 1 or 20.

4. **Strangler fig at the edges.** New features go in a new service behind a gateway; old monolith shrinks over time. No big-bang rewrite, no 8-engineers-running-12-services problem.

**What to avoid at 8 engineers:** full microservices decomposition (one service per domain). That's an ops-and-coordination tax that outweighs a monolith's coordination tax below ~20-30 engineers. You'd trade "wait for someone to review my deploy" for "debug distributed tracing across 12 services with the same 8 people," which is worse.

**Diagnostic question before picking:** is the pain actually deploy coordination (people stepping on each other's release window) or code coupling (can't change module A without breaking module B)? Modular monolith fixes coupling. Independent build/deploy slicing fixes coordination. They're different problems and often only one is real.
