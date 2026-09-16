# Model routing — full algorithm

How to pick which Claude model each subagent uses. Goal: cheapest viable model per role per stage. Quality preserved via per-role overrides + cascading fallback when cheap model returns garbage.

This is loaded only when you need to compute routing. SKILL.md has the summary table; this file has the full algorithm, override flags, edge cases, and audit-trail format.

## Why route at all

Default behavior (use main thread's model for every subagent) is wasteful:

- Sonnet council on a "what variable name?" question burns 10x more tokens than needed
- Opus council on a routine question wastes ~5x cost on roles that don't need it

Routing solves: spend tokens where reasoning depth is actually required.

## ⚙️ MODEL MAPPING — the one block to update when models change

Everything else in this file names models for readability, but what is load-bearing is the **role tier**. When Anthropic ships or retires a model, update THIS table only; the protocol is unchanged.

| Role tier | Means | Current mapping (verified 2026-09; Claude 5 generation) | Relative cost |
|---|---|---|---|
| **cheap** | fast, structured, low-judgment work (reviewers) | Haiku 4.5 — `claude-haiku-4-5` | 1x |
| **mid** | the council's workhorse — members, debate, the Stage 4.5 checker | Sonnet 5 — `claude-sonnet-5` | ~3x |
| **strong** | adversarial + critical roles (DA, security, paranoid members) | Opus 5 — `claude-opus-5` | ~5x |
| **max** | optional ceiling for irreversible decisions (DA at paranoid, `--model=max`) | Fable 5.1 — `claude-fable-5-1` (Fable 5 was retired and replaced, not removed). If no model sits above `strong` on your plan, **max simply equals strong** — a normal state, not a misconfiguration. | ~10x |

**Before trusting this table, check it.** Model names move faster than documentation: run `/model` (or your plan's model list) and confirm each tier still points at a model that exists. If a name here is unfamiliar or missing, remap the tier and change nothing else — the protocol never references a model directly. Legacy ids (`claude-opus-4-8`, `claude-sonnet-4-6`, …) generally keep resolving, so a stale table degrades quietly rather than erroring, which is exactly why the check is worth thirty seconds.

Rules that survive any remapping: **reviewers = cheap**, **members = mid**, **DA = one tier above members**, **Chairman = main thread (never routed)**, **auto-retry ceiling = strong** (max is never an auto-retry target). If a tier's model is unavailable on the user's plan, fall to the next tier down and warn once — never fail a council over a model id.

## Cost reality (2026-07 prices; recheck against current pricing)

Per-million-token rates: cheap 1/5, mid 3/15, strong 5/25, max 10/50 (input/output USD). Relative costs in the table above are what actually matter and drift far more slowly than absolute prices.

**10-call council, realistic token volumes** (~700 in / 400 out per member, ~2700 in / 300 out per reviewer):

- Solo tier: 1 main-thread pass, ~$0.01-0.02 — no routing needed
- All-haiku: ~$0.03-0.05
- Smart-routed standard (4 sonnet members + 1 opus DA + 5 haiku reviewers): ~$0.06-0.08
- All-sonnet: ~$0.10
- All-opus: ~$0.15-0.20
- Paranoid tier (7 opus members + sonnet reviewers + 2 debate rounds): ~$0.25-0.50

**Smart routing saves ~2-3x** vs all-opus at standard tier (was 3-5x under old Opus pricing). The gap narrowed because Opus got cheap; the routing still pays for itself, but `--strong` is no longer an extravagance.

These are per-call averages, not measured per question. Real cost varies ~2x with question length.

## Difficulty computation (do this in pre-flight)

Rate the user's question on 3 independent axes, 1-5 each:

### Axis A — Reasoning depth required
- 1: Direct retrieval ("what's the syntax for X?")
- 2: Single-step inference ("does this code have a bug here?")
- 3: Multi-step trade-off ("should I use REST or GraphQL for this?")
- 4: Cross-domain synthesis ("how should I restructure the data model?")
- 5: Novel hard problem ("what's our 5-year technical strategy?")

### Axis B — Stakes
- 1: Trivial, reversible in seconds (variable rename)
- 2: Small, reversible in minutes (UI tweak)
- 3: Real, reversible in days (refactor one module)
- 4: Costly to reverse (multi-week migration, public commitment)
- 5: Irreversible / reputation-scale (architecture lock-in, public launch)

### Axis C — Novelty
- 1: Well-known answer exists, just find it
- 2: Known patterns recombined for this case
- 3: Established techniques applied to a new domain
- 4: Genuinely new combination of ideas
- 5: Edge of known knowledge, no clear precedent

### Composite

```
difficulty = max(A, B, C)
```

**Take max, not average.** Each axis can independently break the answer:
- High depth + low stakes still needs strong reasoning
- High stakes + low depth still needs strong reasoning (cost of missing the one nuance is high)
- High novelty alone needs creative bandwidth that small models lack

Averaging would let easy axes wash out the hard one. Don't.

## Tier mapping from composite difficulty

```
composite 1-2  → solo tier (single structured main-thread pass, no subagents, no routing)
composite 3    → standard tier (default)
composite 4    → deep tier
composite 5    → paranoid tier
```

User-explicit tier overrides this (e.g., `/wise-men deep ...`, `/wise-men quick ...` for a 3-member haiku council, `--solo` to force solo).

## Base model per tier × stage

| Composite | Members default | Reviewers | Debate | Chairman |
|---|---|---|---|---|
| 1 (solo) | (none — main-thread pass) | (none) | (skip) | main thread |
| 2 (solo) | (none — main-thread pass) | (none) | (skip) | main thread |
| — (quick, explicit only) | haiku | haiku | (skip) | main thread |
| 3 (standard) | sonnet | haiku | sonnet | main thread |
| 4 (deep) | sonnet | sonnet | opus | main thread |
| 5 (paranoid) | opus | sonnet | opus | main thread |

Chairman = main thread always. Cannot be overridden by skill. Whatever model the user is running, that's the synthesizer.

## Per-role overrides (apply on top of tier defaults)

These overrides exist because certain roles **break the council if they're weak**, regardless of question difficulty.

### Devil's Advocate — always +1 role tier (capped at the max tier)
| Composite | Default | DA override |
|---|---|---|
| 1-2 | (solo tier — no DA call) | — |
| 3 | sonnet | opus |
| 4 | sonnet | opus |
| 5 | strong | max tier (falls back to strong if no max-tier model is available on the plan) |

**Why**: Weak DA gives trivial counter-positions. DA must construct the genuinely-best opposing argument. Single most important model choice in the council — the eval's inverted-dissent wins all came from DA reframes strong enough to become the answer.

### Security reviewer — sonnet minimum
- Composite 1 + security relevant: skip security persona entirely (overkill)
- Composite 2+: sonnet minimum
- Composite 4+: opus

**Why**: Security false-negatives are permanent.

### Architect (Engineering domain) — sonnet minimum at standard+
- Composite 1-2: haiku ok
- Composite 3+: sonnet minimum
- Composite 5: opus

**Why**: Structural reasoning about system design, coupling, abstraction quality. Architect on Haiku produces plausible-sounding but mechanically-assembled structures.

### Integrator (Research domain) — sonnet minimum at standard+
- Composite 1-2: haiku ok
- Composite 3+: sonnet minimum
- Composite 5: opus

**Why**: Bridging opposing views, finding the shared assumption being argued past. (Renamed from "Synthesizer" to avoid collision with the Chairman synthesis role.) Different function from Architect — Architect designs structures; Integrator reconciles disagreements.

### Empiricist / Fact-checker — sonnet at standard+, opus at deep+ (claims need to hold up)

### Historian — sonnet at standard+ (precedent reasoning needs depth)

### Theorist — sonnet minimum at standard+ (first-principles reasoning)

### Pragmatist / User Advocate / Editor / Audience Advocate — haiku tolerant
Direct, opinionated, concrete output. Haiku does this fine. Save tokens here.

### All other personas — follow tier default

## Subagent type routing

Match persona role to best subagent type. Set the `subagent_type` parameter on the Agent call:

**Only two subagent types are required**: `wise-member` (ships with this skill — install per README) and `general-purpose` (built in). Everything else below is an OPTIONAL enhancement — if a listed type isn't installed on this machine, silently use `wise-member`. Never fail or warn about a missing optional type.

| Persona role | Subagent type | Required? |
|---|---|---|
| **Any member, reviewer, or the Stage 4.5 checker (default)** | **`wise-member`** — tool-restricted (Read/Grep/Glob only), makes recursion structurally impossible | ships with skill; falls back to `general-purpose` |
| Security persona, when the environment provides a security-review agent | that agent | optional |
| Code-focused personas, when a code-review agent exists | that agent (note: some emit compressed output — the orchestrator must handle it) | optional |
| Anything else / unknown | `wise-member` | — |

> **Caveat**: some environment-provided agents return compressed or otherwise non-standard output. Stage 2 reviewers and the Stage 4 Chairman must handle whatever format a member was spawned through. When in doubt use `wise-member` — its output format is predictable.

## Per-stage overrides

### Stage 1 (member generation)
Use per-role rules above. Highest-value stage — answers feed everything.

### Stage 2 (peer review with rubric)
Almost always haiku-tolerant. Structured rubric scoring is within Haiku's wheelhouse.

**Exceptions**:
- Paranoid tier: bump to sonnet (cheap insurance)
- If member answers very long (>500 lines): use sonnet (long-context judgment is harder)

### Stage 3 (debate)
Sonnet minimum. Opus at paranoid. Debate requires genuine engagement with opposing argument.

### Stage 4 (chairman synthesis)
Main thread. Skill does not control this. Whatever main-thread model is, that's the synthesizer.

(Stage 5 self-consistency check was removed in v2.3 — the Agent tool does not expose a `temperature` parameter, so dual-Chairman runs produced near-identical outputs and the "self-consistency" detection mechanism was non-functional. Paranoid tier now ends at Stage 4 like other tiers, with the difference being member count + 2 debate rounds.)

## Validator step (between Stage 1 and Stage 2)

After Stage 1, before Stage 2, sanity-check each member output. **2 checks only**:

```
For each member output:
  1. Did it engage with the question?
     - Either: the 5-section structure is present
     - Or:     the explicit marker "OUT OF DOMAIN — defer to others on this question." is present
     - Empty, refusal, or off-topic = fail.
  2. Are all 5 footer sections present AND non-empty?
     - "## Core judgment"
     - "## Top risks"
     - "## Recommended change"
     - "## Confidence"
     - "## Weakest assumption"
     All five literal headers must appear (case-insensitive header match acceptable),
     AND each section must contain at least one substantive sentence
     (not whitespace, not a single bullet marker, not a placeholder).

If either fails:
  → retry that member ONCE with model bumped one tier up
       (auto-retry ladder: cheap → mid → strong. Ceiling = strong. The max tier is NEVER
        an auto-retry target — it enters only via the DA override at composite 5 or an
        explicit flag. Quick-tier members start at cheap, so their bump target is mid.)
  → if the member is already at the ceiling (strong, or max via DA/flags):
    retry ONCE at the SAME model instead — a bump has no target, but a fresh
    same-model attempt is cheap and usually recovers a formatting fluke.
  → if it still fails after retry: mark as "OUT OF DOMAIN — defer" and proceed
    (exception: a failed DA is never quietly abstained — flag the council as
    degraded in the output; see SKILL.md Stage 0)
  → never more than one retry per member, never infinite loop
```

**What the validator detects**: "model didn't try" or "model didn't follow the contract" failures (refusal, empty, missing sections).

**What it cannot detect**: "model tried and reasoned wrongly" — fluent, confident, well-formatted but substantively wrong. That's Stage 2's job (peer review with rubric).

The 5-section structure (defined in SKILL.md Stage 1) is the actual contract. Validator checks structure compliance, not reasoning quality.

### Stage 2 validator (reviewer output)

A second, lighter validator runs after Stage 2 before Chairman aggregation — full spec in SKILL.md. It checks that each reviewer emitted one parseable `rubric` fenced block per non-abstaining member with all four axis keys numeric; malformed → retry once, then exclude that reviewer from the score average (never feed a half-parsed block into aggregation). This is the Stage-2 analog of the Stage-1 contract check and closes the same silent-corruption class at the reviewer stage. Skipped at solo tier (no reviewers).

## User override flags

Let user force routing:

- `--model=max` → all members + debate use the max tier, reviewers mid (Chairman still main thread; very expensive — reserve for genuinely critical calls)
- `--model=opus` → all members + reviewers + debate use opus (Chairman still main thread)
- `--model=sonnet` → all use sonnet
- `--model=haiku` → all use haiku (Devil's Advocate stays sonnet; warn user this risks weak DA)
- `--cheap` → haiku everywhere including DA (loud warning: council may collapse)
- `--strong` → strong tier everywhere, DA on max (insurance for critical decisions; roughly 20 cents at standard council size)
- `--solo` → no routing at all (single main-thread pass)
- Default = compute-and-route per algorithm

## Show routing in audit trail

When `--full` flag is used, output:

```
## Model routing used

Composite difficulty: 3/5 (depth=3, stakes=3, novelty=2)
Tier: standard

Member models:
- Pragmatist:        sonnet
- Skeptic:           sonnet
- Architect:         sonnet
- Maintainer:        sonnet
- Devil's Advocate:  opus      (per-role override)

Reviewer model: haiku × 5
Chairman: main thread (sonnet)

Validator: 0 retries triggered
Estimated cost: ~$0.10
```

This makes routing visible and auditable. User can see if cheap models are silently degrading their council.

## Edge cases

### User question is so simple it shouldn't be a council
If composite difficulty = 1 AND no irreversibility, the SKILL.md anti-patterns section says "give direct answer". Composite 1-2 that still deserves structure gets solo tier — never summon Haiku × 3 just to confirm the obvious.

### Model unavailable on user's plan
If haiku model unavailable, fall back to sonnet (warn once per session, not per call). If sonnet unavailable, opus. If opus unavailable too, fail with clear error. Never silently fail.

**Max-tier unavailability is expected, not an error**: every max-tier route (DA at composite 5, `--strong` DA, `--model=max`) degrades to the strong tier automatically when no model above `strong` resolves on this plan. Models retire and plans differ; a missing model id must never break a council. Warn once, route down, continue.

### Stage 4.5 synthesis checker
One `wise-member` subagent at the **mid** tier, any tier where it fires (spec in SKILL.md). Do not use the cheap tier (the check is judgment, not formatting) and do not use strong/max (it verifies, it doesn't re-synthesize — mid is enough, and keeping it cheap keeps the incentive to actually run it).

### Member returns garbage after retry
Treat as abstain. Chairman handles in dissent section. Don't infinite-loop trying models.

### Validator itself produces false positives
Validator is heuristic. If it flags a real answer as garbage, you waste one retry. Acceptable false-positive rate. The 2-check version drastically reduced false positives vs the prior 4-check version.

### Cost spirals on paranoid tier with many retries
Worst case: 7 strong-tier members each retried once = 14 strong-tier calls (roughly 19 cents at current member-call sizes) plus the max-tier DA and its possible retry. Retries are capped at 1 per member, so total council cost stays bounded at roughly 2x the no-failure run — acceptable, and in practice retries are rare.

## How to invoke with model parameter

When spawning Agent calls, set the `model` field explicitly:

```
Agent({
  description: "Pragmatist persona",
  subagent_type: "wise-member",
  model: "haiku",  // ← from routing algorithm
  prompt: "[persona prompt + question]"
})
```

For each parallel call in Stage 1, set the model per the routing algorithm output.

## Anti-patterns

- **Don't use one model for everything "to keep it simple"**. The whole point is differential spend.
- **Don't downgrade Chairman by skipping the skill**. Chairman synthesis is irreplaceable.
- **Don't use Haiku for Devil's Advocate ever**. Weak DA = no real dissent = council is theater.
- **Don't use Opus for routine reviewers**. Rubric scoring doesn't need it. Pure waste.
- **Don't silently fail on model unavailability**. Tell the user.
- **Don't compute difficulty by averaging axes**. Max-dominates. Hard axis wins.
- **Don't skip the validator**. Cheap models will sometimes refuse or return empty. Catching it is the price of routing.
- **Don't pretend the validator catches "wrong reasoning"**. It catches "didn't try". The reasoning-quality check happens at Stage 2 rubric, not validator.

## Quick reference

```
1. Pre-flight: rate question on 3 axes (depth/stakes/novelty), take max
2. Pick tier from composite (1-2=solo, 3=standard, 4=deep, 5=paranoid; quick only on request)
3. Solo → single main-thread pass, done. Otherwise:
4. Pick base model per stage (members/reviewers/debate)
5. Apply per-role overrides (DA always +1 role tier, max tier at paranoid; security/architect/empiricist etc.)
6. Pick subagent type per persona role
7. Spawn subagents with explicit model + subagent_type parameters
8. Run 2-check validator after Stage 1, retry failures once with model+1
9. Show routing block in audit trail when --full
```
