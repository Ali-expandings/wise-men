---
name: wise-men
description: Wise-men council — multi-persona deliberative answer pattern using Claude subagents. Distinct personas independently answer a hard question, peer-review each other anonymously, optionally debate when split, then a Chairman synthesizes a final answer with preserved dissent. Adaptive tier system (quick/standard/deep/paranoid) auto-scales effort to question stakes. Domain-aware persona auto-selection (engineering/product/strategy/research/creative/ethics). Smart model routing — haiku for routine roles, sonnet for adversarial/synthesis roles, opus for critical-stakes — driven by 3-axis difficulty (depth/stakes/novelty, max-dominates) with cascading fallback on validator failure. Use when the user asks for a "council", "panel", "wise men", "wisemen", "wise-men", "multiple perspectives", "deliberate", "debate", "second opinion x N", "stress-test", "war-game", "red team this", "high-stakes decision", or invokes /wise-men. Inspired by github.com/karpathy/llm-council; design choices drew on (but are not validated by) Du 2023 multi-agent debate, Liang 2024 divergent thinking, Khan 2024 debate-via-persuasion, Zheng 2024 LLM-as-judge bias. Pure Claude — no external APIs.
---

# wise-men

Multi-persona deliberative answer pattern. Same Claude model, different roles, structured peer review, optional debate, synthesized final.

## When to use vs not use

**Use**:
- Hard ambiguous question with multiple defensible answers
- High-stakes decision (irreversible, costly, affects others)
- Want diverse reasoning paths, not just one chain
- User explicitly asks for council/panel/debate/multiple-perspectives
- Need to surface hidden assumptions or stress-test an idea

**Don't use** (council overhead = waste):
- Simple factual lookups
- One-line questions
- Code edits the user has already decided on
- Cheap reversible choices (button color, variable name)
- When user just wants validation of a position they already hold

If unsure, ask the user: "want a quick answer or a council (slower, more thorough)?"

## Pre-flight check

Before spawning anyone, a 5-second sanity pass:

1. **Actually a question?** If user dumped context with no clear ask, ask: "What specifically do you want the council to decide / produce / evaluate?"
2. **Really one question?** If compound, split into separate councils. Don't mash.
3. **Answerable from given context?** If facts are missing, ask for them first. Council can't divine missing info.
4. **Council-shaped?** Look at "Don't use" list. If trivial, give a direct answer with one line acknowledging council would be overkill.

If all four pass: compute difficulty (next section), pick tier, proceed.

## Difficulty computation

Rate the question on 3 axes (1-5 each). Take the **max**, not average:

- **Reasoning depth**: 1=retrieval, 3=multi-step trade-off, 5=novel hard problem
- **Stakes**: 1=trivial-reversible, 3=real decision, 5=irreversible/reputational
- **Novelty**: 1=known answer exists, 3=known technique new domain, 5=edge of knowledge

`composite = max(depth, stakes, novelty)`

Max-dominates because each axis can independently break the answer. Hard axis wins.

## Tier selection

`composite` maps to tier. User can override (`/wise-men deep <question>`).

| Tier | Members | Debate | Calls | Used at composite |
|---|---|---|---|---|
| **quick** | 3 | no | ~6 | 1-2 |
| **standard** | 5 | no | ~10 | 3 (default if no override) |
| **deep** | 5-7 | conditional | ~15-20 | 4 |
| **paranoid** | 7 | yes (2 rounds) | ~25+ | 5 |

Bump up if the question framing has signals like "should I really", "irreversible", "high stakes".

## Model routing

Full routing algorithm, all overrides, all flags, cost analysis, and audit-trail format live in **`resources/model-routing.md`** — single source of truth. Do not duplicate routing logic here.

Quick reminder of the load-bearing rules:
- **Devil's Advocate is always +1 tier** vs the default (capped at opus). Weak DA = council theater.
- Chairman = main thread always.
- Smart routing saves 3-5x vs all-opus.

Run the validator after Stage 1; specification in `resources/model-routing.md`.

## The protocol

### Stage 0 — Persona selection

Auto-select 3-7 personas based on **question domain** + tier. Full library: `resources/personas.md`. Quick heuristics:

- **Engineering / code** → Pragmatist + Skeptic + Architect + Security + (Performance if perf-relevant)
- **Product / strategy** → User Advocate + Business Analyst + Devil's Advocate + Historian + (Designer if UX-relevant)
- **Research / claim verification** → Empiricist + Theorist + Methodologist + Skeptic + Integrator
- **Writing / communication** → Editor + Critic + Audience Proxy + Voice Coach + Fact-checker
- **Creative work** → Critic + Originality Checker + Audience Advocate + Genre Expert
- **Ethics / values** → Utilitarian + Deontologist + Virtue Ethicist + Rights Advocate
- **Personal decision** → Pragmatist + Devil's Advocate + Long-term Self + Empath

**Devil's Advocate is mandatory** in every council. Inspired by (not validated by) Liang 2024.

If domain unclear, default to mixed: Pragmatist + Skeptic + Architect + Devil's Advocate + Empiricist.

### Stage 1 — Independent answers (parallel)

Spawn N personas as **parallel `Agent` calls** (one message, multiple tool calls). Each Agent prompt MUST be constructed as follows:

```
You are [IDENTITY].

[STANCE — from persona library]

[OUTPUT STYLE — from persona library]

[CONSTRAINTS — from persona library]

User question:
"""
{question verbatim}
"""

Reply with EXACTLY this 5-section structure (use these literal section headers):

## Core judgment
[Your direct answer to the question. 1-3 paragraphs.]

## Top risks
[Bulleted list of the top 1-5 risks or failure modes you see with the obvious answer. Each risk one line.]

## Recommended change
[The single most important thing the user should do differently, in concrete terms. One sentence.]

## Confidence
[low / medium / high] — [one sentence why]

## Weakest assumption
[One sentence naming the single assumption in your answer that, if wrong, breaks the rest.]

If this question is outside your domain, reply with ONLY: "OUT OF DOMAIN — defer to others on this question." Do not produce the 5 sections.
```

The orchestrator (main thread) MUST inject this footer into every persona's prompt. If the persona library's persona definition contradicts the 5-section structure, the 5-section structure wins.

**Subagent type + model**: per `resources/model-routing.md`. Set both `subagent_type` and `model` parameters on each Agent call.

### Validator (between Stage 1 and Stage 2)

Run after Stage 1. Two checks per member output:

1. **Did it engage with the question?** Either the 5-section structure is present, OR the explicit "OUT OF DOMAIN — defer" marker is present. Empty, refusal, or off-topic = fail.
2. **Are all 5 footer sections present and non-empty?** `## Core judgment`, `## Top risks`, `## Recommended change`, `## Confidence`, `## Weakest assumption` — all five literal headers must appear, and **each section must contain at least one substantive sentence** (not whitespace, not a single bullet marker, not a placeholder).

Fail → retry that member ONCE with model bumped +1 tier. **If member is already at opus (paranoid tier or `--strong`), skip retry and mark "OUT OF DOMAIN — defer" immediately.** Still fail after retry → mark "OUT OF DOMAIN — defer" and proceed.

The validator catches "model didn't try" or "model didn't follow the contract" failures. It does NOT detect reasoning errors — that's Stage 2's job.

### Stage 2 — Peer review (parallel)

After Stage 1 + validator, spawn N reviewers in parallel. Each reviewer sees:

- Original question
- All N answers labeled with **stable persona names** (`Member: Pragmatist`, `Member: Skeptic`, `Member: Devil's Advocate`, ...) in fixed order across all reviewers
- Their OWN answer is in there labeled with their persona name — they will recognize it, that's fine
- Explicit instruction: judge reasoning quality, not persona identity. The reviewer's own answer is included for self-comparison.

Why stable labels (not anonymized): the prior randomized-label scheme required the Chairman to un-map per-reviewer permutations back to original member identity. No mapping record was defined or transmitted, so cross-reviewer aggregation silently produced garbage. Stable labels are honest about what Claude can already infer (it knows its own persona prompts) and let the Chairman aggregate scores correctly. Anonymization-as-mitigation was a paper guarantee with no enforcement; dropped.

Reviewers fill a **structured rubric**. Score each member 1-5 on:

- **Correctness** — factually right? evidence cited? logic intact?
- **Insight** — novel? non-obvious? generative?
- **Practical usefulness** — actionable? appropriate scope?
- **Risk awareness** — acknowledges what could go wrong? hidden assumptions surfaced?

Plus one-line justification per axis. Plus pick a top and bottom with one-sentence reasons.

Full prompt template: `resources/prompts/peer-review.md`.

### Stage 3 — Conditional debate (`deep` / `paranoid` only)

After Stage 2, check for **severe disagreement** using the canonical trigger (single source of truth, identical in SKILL.md, peer-review.md, debate.md):

> **Debate-trigger formula**: variance ≥ 1.5 on any rubric axis OR a member ranked top-2 by some reviewers and bottom-2 by others on the same axis.

If found, spawn one **debate round**:
- Top-ranked + bottom-ranked member each see the other's answer + objections
- Each: UPDATE or HOLD position; must concede one valid opposing point
- Re-run a lightweight single-reviewer rubric on updated answers

`paranoid` runs 2 debate rounds. `deep` runs 1 conditional round. `standard` and `quick` skip.

Full prompt template: `resources/prompts/debate.md`.

### Stage 4 — Chairman synthesis (main thread)

You (main thread) act as Chairman. Do NOT spawn a subagent. Read all member answers, all rubric scores, debate outputs.

Produce structured synthesis:

```
## TL;DR
[1-2 sentences, the council's answer]

## Decision / Answer
[Full answer. Action-oriented. Specific.]

## Confidence
[High / Medium / Low] — [1-sentence why, based on actual council agreement level]

## Where the council agreed
[Consensus points]

## Where the council split (preserved dissent)
[Minority view, verbatim or near-verbatim + why it might be right]

[OPTIONAL — include only if applicable]
## Action items
[Concrete next steps, only when question is action-shaped]

## Open questions the council couldn't resolve
[What remains uncertain, only when real open questions exist]
```

**Dissent preservation rule**: if a member was strongly confident in a position the majority disagreed with, that view goes in the dissent section verbatim or near-verbatim. Do not paraphrase to soften.

**Dissent precedence rule** (resolves prior conflict with brief output):
If the verbatim dissent is longer than 3 sentences, **auto-promote the output to `--full` format**. Do not truncate dissent to fit brief format. State the format upgrade at the top of the output: *"Note: brief format upgraded to full because preserved dissent exceeded 3 sentences."*

Full synthesis template: `resources/prompts/chairman.md`.

## Output format (to user)

Default = brief + dissent (unless dissent-precedence upgrade triggered):

```
## Council answer
[TL;DR + Decision section, clean]

## Dissent worth keeping
[The minority view, up to 3 sentences]

---
*Council of N members, M tier. Want the full audit trail? Ask "show me the council transcript".*
```

Flags:
- `--brief` → truncates **non-dissent** sections only. Dissent precedence wins: dissent is preserved verbatim, and if dissent exceeds 3 sentences the output auto-upgrades to `--full`. `--brief` cannot suppress dissent.
- `--full` → answer + full audit trail (all member answers, all reviews, routing block, full chairman output)
- `--debate` → show full peer-review + debate transcript
- Default → brief + dissent (auto-upgraded to full if dissent precedence triggers)

Model-override flags (`--model=...`, `--cheap`, `--strong`) live in `resources/model-routing.md`.

## Anti-patterns

- **Don't spawn personas serially.** Parallel only. Sequential council wastes wall time.
- **Don't reveal personas to reviewers as roles.** Members labeled by name is fine; "the security reviewer says..." is not.
- **Don't let Chairman just pick a winner.** Synthesize. Preserve dissent.
- **Don't run paranoid tier by default.** Match tier to stakes.
- **Don't summon council on questions where one expert + Google would suffice.**
- **Don't fake the council.** Don't say "the council found X" if you didn't run one. Just give the direct answer.
- **Don't trust manufactured DA dissent uncritically.** Weight by specificity (concrete failure mode named), not by presence alone.
- **Don't duplicate routing logic in SKILL.md.** `resources/model-routing.md` is the single source.

## Limits

- **Single-model**: all members are Claude. No bias cancellation from architectural diversity. Persona prompting approximates diversity; Claude shares blindspots with itself across personas.
- **Cost**: even quick = 6+ subagent calls. Match tier to stakes.
- **Chairman is main thread**: same thread that selected personas and computed difficulty also synthesizes. Conflict of interest is structural; dissent preservation partially mitigates.
- **Not benchmarked**: skill has not been measured against a single-prompt baseline. Treat as a structured-thinking aid, not a validated quality multiplier. Eval spec lives in repo notes (not in SKILL.md).

## Quick reference — minimum viable council

3-member quick tier:

```
Stage 0: Pragmatist + Skeptic + Devil's Advocate (DA on +1 tier model)
Stage 1: 3 parallel Agent calls, 5-section output structure required
Validator: 2-check pass (structure present + 5 sections present)
Stage 2: 3 parallel Agent calls, rubric scoring on stable persona labels
Stage 3: skipped
Stage 4: main thread Chairman synthesis
```

Total: 6 subagent calls. ~25-50s wall time. Cost: ~$0.03-0.05.

## Skill chaining

- **`humanizer`** — polish Chairman output before showing to user
- **`caveman:cavecrew-reviewer`** — subagent type for code-focused reviewer personas (output is caveman-compressed; orchestrator must handle compressed format)
- **`security-review`** — subagent type for security persona slot
- **`verify`** — run after a council decides on a code change

## Resources

- `resources/personas.md` — full persona library with prompt templates per role
- `resources/model-routing.md` — full routing algorithm, override flags, audit-trail format, edge cases
- `resources/prompts/peer-review.md` — Stage 2 rubric template
- `resources/prompts/debate.md` — Stage 3 debate template
- `resources/prompts/chairman.md` — Stage 4 synthesis template
- `examples/coding-question.md` — worked example: "should I split App.tsx?"
- `examples/strategy-question.md` — worked example: "should I launch on Product Hunt or Reddit first?"

SKILL.md alone is enough to run `quick` or `standard` tier. Sub-files on demand.
