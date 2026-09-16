# Model routing — full algorithm

How to pick which Claude model each subagent uses. Goal: cheapest viable model per role per stage. Quality preserved via per-role overrides + cascading fallback when cheap model returns garbage.

This is loaded only when you need to compute routing. SKILL.md has the summary table; this file has the full algorithm, override flags, edge cases, and audit-trail format.

## Why route at all

Default behavior (use main thread's model for every subagent) is wasteful:

- Sonnet council on a "what variable name?" question burns 10x more tokens than needed
- Opus council on a routine question wastes 5-10x cost on roles that don't need it

Routing solves: spend tokens where reasoning depth is actually required.

## Cost reality (recalibrated, late 2025)

| Model | Input $/M | Output $/M | Relative cost | Relative speed |
|---|---|---|---|---|
| Haiku 4.5 | $1 | $5 | 1x | 1x (fastest) |
| Sonnet 4.6 | $3 | $15 | ~3-5x | 0.3x |
| Opus 4.7 | $15 | $75 | ~15-20x | 0.1x |

**10-call council, realistic token volumes** (~700 in / 400 out per member, ~2700 in / 300 out per reviewer):

- All-haiku: ~$0.03-0.05
- Smart-routed standard (4 sonnet members + 1 opus DA + 5 haiku reviewers): ~$0.08-0.12
- All-sonnet: ~$0.10
- All-opus: ~$0.50-0.60
- Paranoid tier (7 members + 2 debate rounds + dual Chairman): ~$1.50-3.00

**Smart routing saves 3-5x** vs all-opus at standard tier. Big win is haiku reviewers + DA being the only opus call. (Earlier "5-10x cheaper" claim was overstated; the math gives 3-5x at standard tier.)

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
composite 1-2  → quick tier
composite 3    → standard tier (default)
composite 4    → deep tier
composite 5    → paranoid tier
```

User-explicit tier overrides this (e.g., `/wise-men deep ...`).

## Base model per tier × stage

| Composite | Members default | Reviewers | Debate | Chairman |
|---|---|---|---|---|
| 1 (quick) | haiku | haiku | (skip) | main thread |
| 2 (quick) | haiku | haiku | (skip) | main thread |
| 3 (standard) | sonnet | haiku | sonnet | main thread |
| 4 (deep) | sonnet | sonnet | opus | main thread |
| 5 (paranoid) | opus | sonnet | opus | main thread |

Chairman = main thread always. Cannot be overridden by skill. Whatever model the user is running, that's the synthesizer.

## Per-role overrides (apply on top of tier defaults)

These overrides exist because certain roles **break the council if they're weak**, regardless of question difficulty.

### Devil's Advocate — always +1 tier (capped at opus)
| Composite | Default | DA override |
|---|---|---|
| 1 | haiku | sonnet |
| 2 | haiku | sonnet |
| 3 | sonnet | opus |
| 4 | sonnet | opus |
| 5 | opus | opus |

**Why**: Weak DA gives trivial counter-positions. DA must construct the genuinely-best opposing argument. Single most important model choice in the council.

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

### Pragmatist / User Advocate / Editor / Audience Proxy — haiku tolerant
Direct, opinionated, concrete output. Haiku does this fine. Save tokens here.

### All other personas — follow tier default

## Subagent type routing

Match persona role to best subagent type. Set the `subagent_type` parameter on the Agent call:

| Persona role | Best subagent type |
|---|---|
| Security reviewer (engineering) | `security-review` |
| Code reviewer (engineering) | `caveman:cavecrew-reviewer` |
| Code locator / investigator | `caveman:cavecrew-investigator` |
| Code-edit personas (rare in council use) | `caveman:cavecrew-builder` |
| General reasoning / strategy / writing / ethics / creative | `general-purpose` |
| Unknown | `general-purpose` |

> **Caveat**: `caveman:cavecrew-*` subagents return caveman-compressed output. Stage 2 reviewers and Stage 4 Chairman should expect compressed format from any member spawned through them. For non-code personas, prefer `general-purpose` to keep output format predictable.

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
  → BUT: if the member is already at opus (paranoid tier, or --strong override),
    skip retry and mark "OUT OF DOMAIN — defer" immediately — there is no +1 tier
    above opus, so retry has no valid target.
  → if it still fails after retry: mark as "OUT OF DOMAIN — defer" and proceed
  → never infinite loop
```

**What the validator detects**: "model didn't try" or "model didn't follow the contract" failures (refusal, empty, missing sections).

**What it cannot detect**: "model tried and reasoned wrongly" — fluent, confident, well-formatted but substantively wrong. That's Stage 2's job (peer review with rubric).

The 5-section structure (defined in SKILL.md Stage 1) is the actual contract. Validator checks structure compliance, not reasoning quality.

## User override flags

Let user force routing:

- `--model=opus` → all members + reviewers + debate use opus (Chairman still main thread)
- `--model=sonnet` → all use sonnet
- `--model=haiku` → all use haiku (Devil's Advocate stays sonnet; warn user this risks weak DA)
- `--cheap` → haiku everywhere including DA (loud warning: council may collapse)
- `--strong` → opus everywhere (expensive insurance for critical decisions)
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
If composite difficulty = 1 AND no irreversibility, the SKILL.md anti-patterns section says "give direct answer". Don't summon Haiku × 3 just to confirm the obvious.

### Model unavailable on user's plan
If haiku model unavailable, fall back to sonnet (warn once per session, not per call). If sonnet unavailable, opus. If opus unavailable too, fail with clear error. Never silently fail.

### Member returns garbage after retry
Treat as abstain. Chairman handles in dissent section. Don't infinite-loop trying models.

### Validator itself produces false positives
Validator is heuristic. If it flags a real answer as garbage, you waste one retry. Acceptable false-positive rate. The 2-check version drastically reduced false positives vs the prior 4-check version.

### Cost spirals on paranoid tier with many retries
Worst case: 7 members × opus × 1 retry = 14 opus calls. Cap retries at 1 per member, total council cost stays bounded. **At paranoid (members already opus), retry is skipped — failed members go straight to OUT OF DOMAIN.** So paranoid worst case is actually 7 opus member calls, no retries.

## How to invoke with model parameter

When spawning Agent calls, set the `model` field explicitly:

```
Agent({
  description: "Pragmatist persona",
  subagent_type: "general-purpose",
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
2. Pick tier from composite (1-2=quick, 3=standard, 4=deep, 5=paranoid)
3. Pick base model per stage (members/reviewers/debate)
4. Apply per-role overrides (DA always +1; security/architect/empiricist etc.)
5. Pick subagent type per persona role
6. Spawn subagents with explicit model + subagent_type parameters
7. Run 2-check validator after Stage 1, retry failures once with model+1
8. Show routing block in audit trail when --full
```
