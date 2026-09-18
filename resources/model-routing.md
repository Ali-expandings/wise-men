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
| **cheap** | fast, structured grading work (reviewers), including spot-checking files an answer cites | Haiku 4.5 — `claude-haiku-4-5` | 1x |
| **mid** | the council's workhorse — members, debate, the Stage 4.5 checker | Sonnet 5 — `claude-sonnet-5` | ~3x |
| **strong** | adversarial + critical roles (DA, security, paranoid members) | Opus 5 — `claude-opus-5` | ~5x |
| **max** | optional ceiling for irreversible decisions (DA at paranoid, `--model=max`) | Fable 5.1 — `claude-fable-5-1` (Fable 5 was retired and replaced, not removed). If no model sits above `strong` on your plan, **max simply equals strong** — a normal state, not a misconfiguration. | ~10x |

**Before trusting this table, check it.** Model names move faster than documentation: run `/model` (or your plan's model list) and confirm each tier still points at a model that exists. If a name here is unfamiliar or missing, remap the tier and change nothing else — the protocol never references a model directly. Legacy ids (`claude-opus-4-8`, `claude-sonnet-4-6`, …) generally keep resolving, so a stale table degrades quietly rather than erroring, which is exactly why the check is worth thirty seconds.

Rules that survive any remapping: **reviewers = cheap** (mid when the grading packet contains claims about artifacts on disk — verification is judgment work), **members = mid**, **DA = one tier above members**, **Chairman = main thread (never routed)**, **auto-retry ceiling = strong** (max is never an auto-retry target). If a tier's model is unavailable on the user's plan, use the nearest available tier — the cheaper neighbour first, the dearer one only when nothing cheaper exists — warn once, and record requested vs actual model in the routing block. Never fail a council over a model id.

## Cost reality (measured 2026-09; relative costs only)

Per-million-token rates, 2026-07: cheap 1/5, mid 3/15, strong 5/25, max 10/50 (input/output USD). The relative costs in the table above are what routing decisions use, and they drift far more slowly than absolute prices.

**What a council actually costs — measured, head-to-head round 3** (twelve runs of 3.11.0, Sonnet orchestrator, the skill choosing its own tier; token counts as the harness reports them for the whole run, with no split between input, output and cached context, so no dollar figure is derived):

- Standard tier (9–10 subagent calls — 5 members, 3 reviewers, checker): 18–23 minutes uninterrupted, about 190k–230k tokens.
- Deep tier (13–20 calls): 31–69 minutes, about 240k–295k tokens.
- For scale, same harness and questions: Warp's council about 8 minutes and 100k–120k tokens; llm-council about 15 minutes and 120k–135k; a plain answer 1.4 minutes and about 75k–80k.

Versions up to 3.11.1 quoted a few cents per council (4-6 cents quick, 7-9 standard). Those figures assumed ~700-token member prompts; real member prompts carry the persona block, the brief and the contract, members Read files, and reviewers Read a packet of every answer, so real runs exceed that estimate by more than an order of magnitude. The figures are withdrawn; budget in calls and minutes.

**Smart routing still matters in relative terms**: the routed standard council (3 mid members + strong anchor + strong DA + 3 cheap reviewers + mid checker) costs roughly half of an all-strong council at the rates above, because reviewers and most members stay off the strong tier.

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

User-explicit tier overrides this (e.g., `/wise-men deep ...`, `/wise-men quick ...` or `--fast` for the 3-member council with no peer review, `--solo` to force solo).

## Base model per tier × stage

| Composite | Members default | Reviewers | Debate | Chairman |
|---|---|---|---|---|
| 1 (solo) | (none — main-thread pass) | (none) | (skip) | main thread |
| 2 (solo) | (none — main-thread pass) | (none) | (skip) | main thread |
| — (quick / `--fast`, explicit only) | sonnet (one domain member; anchor and DA on opus) | (none — no Stage 2) | (skip) | main thread |
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
| quick | sonnet | opus |
| 3 | sonnet | opus |
| 4 | sonnet | opus |
| 5 | strong | max tier (falls back to strong if no max-tier model is available on the plan) |

**Why**: Weak DA gives trivial counter-positions. DA must construct the genuinely-best opposing argument. Single most important model choice in the council — the eval's inverted-dissent wins all came from DA reframes strong enough to become the answer.

### Practitioner anchor — always +1 role tier (capped at strong)
| Composite | Default | Anchor override |
|---|---|---|
| 1-2 | (solo tier — no anchor call) | — |
| quick | sonnet | opus |
| 3 | sonnet | opus |
| 4 | sonnet | opus |
| 5 | strong | strong (max stays reserved for the DA) |

**Why**: the anchor owns correctness and completeness — the two axes where the head-to-head's winning rival led wise-men by the widest margin (correctness 4.88 vs 3.75, practical 4.88 vs 3.62), and that rival put its strongest model on its correctness seat in at least 7 of 8 runs. A council whose facts come from its cheapest seats loses exactly those axes.

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
| **Any member, reviewer, or the Stage 4.5 checker (default)** | **`wise-men:wise-member`** (plugin install) or **`wise-member`** (clone + copy install) — tool-restricted (Read/Grep/Glob only), makes recursion structurally impossible | ships with skill; falls back to `general-purpose` |
| Security persona, when the environment provides a security-review agent | that agent — **not tool-restricted** (see the boundary note below) | optional |
| Code-focused personas, when a code-review agent exists | that agent — **not tool-restricted**; some emit compressed output the orchestrator must handle | optional |
| Anything else / unknown | `wise-member` | — |

> **Boundary note**: only `wise-member` is structurally unable to spawn subagents, run commands or edit files. A seat filled by any other agent type keeps whatever tools that agent has, so the no-recursion guarantee does not cover that seat: use such agents for member seats only (never for reviewers or the Stage 4.5 checker), keep the prompt-level "do not spawn subagents" line, and say once in the output that the seat ran outside the restricted agent.
>
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
  2. Unless it abstained with that marker: are all 5 footer sections present AND non-empty?
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
  → if it still fails after retry: record the member as FAILED (timeout, spawn error, empty or
    malformed output are execution failures, not abstentions), leave it out of aggregation and
    disclose it in the footer (a failed DA means the council is degraded; see SKILL.md Stage 0)
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
- `--strong` → strong tier everywhere, DA on max (insurance for critical decisions; roughly twice the routed cost at standard council size)
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

Reviewer model: haiku × 3
Chairman: main thread (sonnet)

Validator: 0 retries triggered
Estimated cost: ~$0.10
```

This makes routing visible and auditable. User can see if cheap models are silently degrading their council.

## Edge cases

### User question is so simple it shouldn't be a council
If composite difficulty = 1 AND no irreversibility, the SKILL.md anti-patterns section says "give direct answer". Composite 1-2 that still deserves structure gets solo tier — never summon Haiku × 3 just to confirm the obvious.

### Model unavailable on user's plan
Apply the fallback rule from the model-mapping section: nearest available tier, cheaper neighbour first (cheap has none, so it moves up to mid; mid falls to cheap before strong; strong falls to mid). Warn once per session, not per call, and record requested vs actual model. If no Claude model resolves at all, fail with a clear error. Never silently fail.

**Max-tier unavailability is expected, not an error**: every max-tier route (DA at composite 5, `--strong` DA, `--model=max`) degrades to the strong tier automatically when no model above `strong` resolves on this plan. Models retire and plans differ; a missing model id must never break a council. Warn once, route down, continue.

### Stage 4.5 synthesis checker
One `wise-member` subagent at the **mid** tier at standard, deep and paranoid (spec in SKILL.md); at quick it runs on the **cheap** tier, because there it checks only the draft against the question (four checks, no member answers to cross-reference) and the whole point of the tier is a council at close to single-answer cost. Above quick, do not use the cheap tier (grounding a draft in five to seven answers is judgment, not formatting) and do not use strong/max (it verifies, it doesn't re-synthesize — mid is enough, and keeping it cheap keeps the incentive to actually run it).

### Member returns garbage after retry
Treat as abstain. Chairman handles in dissent section. Don't infinite-loop trying models.

### Validator itself produces false positives
Validator is heuristic. If it flags a real answer as garbage, you waste one retry. Acceptable false-positive rate. The 2-check version drastically reduced false positives vs the prior 4-check version.

### Cost spirals on paranoid tier with many retries
Worst case: 7 strong-tier members each retried once = 14 strong-tier calls plus the max-tier DA and its possible retry. Retries are capped at 1 per member, so total council cost stays bounded at roughly 2x the no-failure run — acceptable, and in practice retries are rare.

## How to invoke with model parameter

When spawning Agent calls, set the `model` field explicitly:

```
Agent({
  description: "Pragmatist persona",
  subagent_type: "wise-men:wise-member",  // "wise-member" if installed by clone + copy
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
