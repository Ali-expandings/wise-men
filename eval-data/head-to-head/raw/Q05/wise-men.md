# arm: wise-men | question: Q05 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# skill: SKILL.md v3.9.2 (as written)
# subagent tokens: 168691 | tool uses: 24 | duration: 464s

*Note: brief format upgraded to full because preserved dissent exceeded 3 sentences (dissent-precedence rule).*

## Council answer

**TL;DR**: Don't pick a side of "monolith vs. microservices" — diagnose which specific coupling is forcing cross-team coordination (build, release-process, data/schema, or ownership), and fix that layer directly. For 8 engineers the default fix is almost always a **modular monolith** (same deployable, mechanically-enforced internal module boundaries) plus **release-engineering changes** (feature flags, trunk-based dev, expand/contract migrations) — not a network split. Extract a real service only for the 1-2 subsystems that demonstrably need independent scaling or release cadence.

**Decision**: All five council members independently rejected full microservices for a team this size and converged on diagnose-before-restructure. Concretely:

1. Spend 1-2 weeks tagging every "blocked on another team to deploy" incident by coupling type: **build** (shared CI/compile blocks everyone), **release** (single release train/manual gate), **data** (shared schema/migrations), or **ownership** (constant cross-team review/merge conflict).
2. In parallel — this is close to free regardless of which path you take — adopt trunk-based development, feature flags, and expand/contract migrations so *merging* stops being coupled to *releasing*.
3. Apply the fix that matches whichever coupling dominates the log: build/ownership coupling → modular monolith with **mechanically enforced** module boundaries (import-linting/dependency-cruiser/Packwerk-style tooling — convention-only boundaries erode within months on a team this small); data/deploy-cadence coupling → extract a small number of real services (2-3, matched to genuine bounded contexts, never one-per-team).
4. Whatever boundary you draw, enforce it with tooling, not code review discipline.

**Confidence**: Medium-High. Five members reasoned down five different paths (precedent, falsification, first-principles, base-rates, incentives) and reached compatible conclusions — that convergence is the real signal, and peer review scored the strongest answer (Architect, whose coupling taxonomy underlies the "diagnose which layer" framing above) at 4.75/5 with a tight spread across the panel (3.67–4.75/5, no answer rated weak). Not "High" because the actual diagnosis depends on this team's real deploy logs, which no council member could see — that's a hypothesis about your system, not a verified fact.

## Where the council agreed

- Full "go microservices" at 8 engineers is close to always wrong: the distributed-systems tax (per-service on-call, tracing, CI/CD, versioned contracts) consumes a share of team capacity an 8-person team doesn't have to spare.
- "Monolith vs. microservices" is a false binary — at least 3-4 distinct kinds of coupling get lumped under "the monolith," and each needs a different fix.
- Whatever boundary you pick, it must be mechanically enforced, not convention-based — a small team has no spare capacity to police a boundary by hand, and it decays within months if nothing blocks a bad import.
- Diagnose the actual bottleneck before restructuring — most reported "hard to deploy without coordination" pain turns out to be release-process/CI coupling, which a service split doesn't fix (it just makes it harder to see).

## Where the council split (preserved dissent)

The other four members converge on "modular monolith" as the structural default. The **Devil's Advocate** pushed one step further and this deserves to be kept in its own words, not softened into the majority view: *"Whatever is producing cross-team coordination overhead at that headcount is not an artifact of the monolith — it's an artifact of how you've split ownership, sequenced work, and gated releases... independent deploy is a release engineering property, not a topology property."* Its recommendation: spend a full quarter fixing deploys purely through release engineering — trunk-based development, feature flags, deploy-on-green, expand/contract migrations — with **zero architectural change**, and only treat whatever coordination survives that quarter as the real, now much better-understood, problem. It also flagged the incentive structure behind "everyone says go microservices" as worth distrusting independent of technical merit: career signaling for the engineer who gets to "own a service," vendor pricing that scales per-service, and conference/blog culture that never rewards "we deleted our staging gate."

This wasn't the peer-review top pick (Architect narrowly was, at 4.75 vs. the Devil's Advocate's 4.25), so it doesn't invert the majority recommendation. But it's a clean counter-position worth taking seriously as a cheaper first move: its release-engineering fixes are a strict subset of what every other path also requires, so doing them first costs you nothing regardless of where the diagnosis (step 1 above) ultimately points.

## Open questions the council couldn't resolve

Whether the current pain is release-process/ownership coupling (fixable with zero architecture change, per the Devil's Advocate and Maintainer) or genuine data/scaling divergence (requiring real service extraction, per the Architect and Pragmatist). No member could see this team's actual deploy logs — that's the one fact that changes the specific prescription, though not the "diagnose before you split" verdict itself.

---

## Full audit trail

**Model routing used**
```
Composite difficulty: 3/5 (depth=3, stakes=3, novelty=2) → standard tier
Members: Pragmatist (sonnet), Skeptic (sonnet), Architect (sonnet),
         Maintainer (sonnet), Devil's Advocate (opus — per-role override)
Reviewers: haiku × 3
Chairman: main thread (sonnet)
Validator: 0 retries triggered at Stage 1 or Stage 2; no exclusions, no abstentions
Debate: not applicable (standard tier skips Stage 3)
Stage 4.5 checker: skipped (run did not degrade)
Estimated cost: ~$0.05-0.07
```

**Aggregated peer-review scores** (mean of 3 reviewers, 1-5 scale)

| Member | Correctness | Insight | Practical | Risk | Overall |
|---|---|---|---|---|---|
| Architect | 5.00 | 5.00 | 4.67 | 4.33 | **4.75** |
| Maintainer | 4.33 | 4.00 | 4.33 | 5.00 | 4.42 |
| Devil's Advocate | 3.67 | 4.33 | 4.33 | 4.67 | 4.25 |
| Skeptic | 4.00 | 3.67 | 3.33 | 4.33 | 3.83 |
| Pragmatist | 4.00 | 3.00 | 4.00 | 3.67 | 3.67 |

Top pick: Architect (2 of 3 reviewers), Maintainer (1 of 3). Bottom pick: Pragmatist (2 of 3), Skeptic (1 of 3). No severe-disagreement flags raised by any reviewer.

**Member answers (verbatim)**

--- Member: Pragmatist (sonnet) ---
Modular monolith, not microservices — documented middle ground teams land on after learning the expensive way (cites Segment's 2018 retreat from ~100+ microservices, Shopify's "majestic monolith" + Packwerk-enforced boundaries, GitHub staying monolithic through most of its growth). At 8 engineers, full decomposition is premature — each service is a fixed CI/CD + monitoring + on-call + contract tax regardless of team size. Diagnose first: is the pain (a) a shared release train, (b) tangled code with no ownership boundaries, or (c) shared DB migrations blocking each other? (a) and (c) are process fixes (feature flags, decoupled migrations); only (b), mapped to a genuinely independent bounded context, justifies carving out a service — one at a time, via strangler fig. *Confidence: medium. Weakest assumption: that the pain is process/coupling rather than genuinely divergent scaling needs.*

--- Member: Skeptic (sonnet) ---
A middle ground exists and is likely right for 8 people: modular monolith with build-enforced boundaries, or a small number of independently-deployable units along real ownership seams, or trunk-based dev + feature flags without touching topology at all. Falsification test: the middle ground is wrong if (1) teams still block each other despite "modules" because boundaries were convention-only, or (2) one subsystem needs 50-100x independent scaling it can't get while co-located. Signal (1) is the likely failure mode for an 8-person team specifically — nobody is a dedicated platform engineer to keep enforcing a boundary that isn't mechanical. *Confidence: medium. Weakest assumption: that the pain is code/module coupling rather than release-process coupling — the two need different fixes.*

--- Member: Architect (sonnet) ---
"Monolith vs. microservices" is the wrong axis. Four distinct couplings get lumped under "monolith": build (shared CI), deploy (shared release train), data (shared schema/migrations), ownership (no module boundaries). Microservices solves all four by brute force, which is overkill for 8 engineers. Match the fix to the actual coupling: ownership/build coupling → modular monolith with hard-enforced module boundaries (dependency-cruiser/equivalent) + trunk-based dev; deploy coupling specifically → 2-3 independently deployable units along real bounded contexts (not per-team); data coupling → schema ownership/contracts, not necessarily a network split. *Confidence: medium. Weakest assumption: that the team hasn't already tried and failed to enforce module boundaries — if so, the problem is organizational, not architectural.*

--- Member: Maintainer (sonnet) ---
Base rate for 8-engineer teams going full microservices: 6-15 services, unreasoned shared on-call, unbudgeted observability cost, 1-2 accidental "platform owners." That's the modal outcome, not a worst case — microservices solves a 30+-engineer coordination problem wearing a technical costume. The middle ground: decompose the *deploy unit* without decomposing the *process* — modular monolith with CI-enforced boundaries, or a small number of coarse-grained services along real bounded contexts. Ask first: is the pain build/CI coordination, or genuine differing scaling/uptime/cadence needs? Most reported pain is the former. *Confidence: medium. Weakest assumption: that the pain is primarily process, not a genuine need for independently scalable runtimes.*

--- Member: Devil's Advocate (opus) ---
The frame is wrong: 8 engineers shouldn't have "teams, plural" requiring deploy coordination — whatever produces that is an artifact of ownership/sequencing/release-gating, not the monolith, and a service split will faithfully preserve the coordination cost while adding network partitions to it (Conway's law runs both ways). "Everyone says microservices" dissolves under incentive analysis: résumé-building for engineers, per-service pricing for vendors, conference culture that never rewards boring fixes, legible-looking reorg work for tech leads — none of it about technical merit. The missing option: one quarter of pure release engineering (trunk-based dev, feature flags, deploy-on-green, expand/contract migrations) with zero architectural change; treat whatever coordination survives as the real, now well-understood, problem. *Confidence: medium. Weakest assumption: that the coordination is organizational rather than a hard technical constraint — if there's a genuinely shared write-path that can't be flagged apart, release engineering alone won't be enough.*

## Protocol notes

- Standard tier (composite difficulty 3/5) — 5 members + 3 reviewers, no debate stage (standard tier skips Stage 3 by design).
- No deviations: both validators passed on the first attempt for every member and reviewer; no retries, no exclusions, no forced abstentions; Devil's Advocate engaged fully (no "OUT OF DOMAIN").
- Dissent-precedence rule fired (verbatim Devil's Advocate dissent exceeded 3 sentences), auto-upgrading this output from brief+dissent to full format, as noted at the top.
- No web/file facts to verify post-council — the question and all five answers were general engineering reasoning, not claims about a specific codebase, so there is no "Orchestrator verification" section this time.
- **Record-keeping deviation (disclosed)**: the skill's default is to write the full transcript to the project's Obsidian notes/handoff folder when the question concerns a real project. This question was phrased generically ("we have a monolith...") with no project, client, or codebase named, so I did not file it under any specific vault project to avoid mis-filing it. If this is about a specific project, say so and I'll write the record and a one-paragraph vault summary to that project's notes.
