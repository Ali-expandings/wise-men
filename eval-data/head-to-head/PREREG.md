# Head-to-head: wise-men vs the skills people already use — pre-registration

Written and committed 2026-09-16 before any arm was run. Nothing below changes after this commit except RESULTS.md.

## Question
On the same hard questions, blind-judged with the same rubric, how does wise-men compare with the most-installed Claude Code skills a user would otherwise reach for when they want a decision stress-tested?

## Arms (6)
| arm | source | commit | license | how it is run |
|---|---|---|---|---|
| wise-men | this repo, `SKILL.md` v3.9.2 | HEAD | MIT | as written; orchestrator = fresh Sonnet subagent; members `wise-men:wise-member` |
| brainstorming | obra/superpowers `skills/brainstorming/SKILL.md` (288k★ repo) | b36e0829c6d0 | MIT | as written, with the no-human adaptation below |
| grilling | mattpocock/skills `skills/productivity/grilling/SKILL.md` (263k★ repo; `grill-me` delegates to it) | 85f83d3fde1d | MIT | as written, with the no-human adaptation below |
| lifeos-council | danielmiessler/lifeos `LifeOS/install/skills/Council/` SKILL.md + CouncilMembers/RoundStructure/OutputFormat (19k★ repo) | 36c6f01e9c2c / 3baba67056a0 | MIT | as written; the `localhost:31337` voice notification is skipped (no LifeOS install) |
| llm-council | aiwithremy/claude-skills-llm-council `SKILL.md` (2.1k★, the viral "Claude Council") | 1162f272ab94 | none stated — used locally, not redistributed | as written |
| direct | no skill | — | — | the question, answered plainly |

Excluded: karpathy/llm-council (25k★) — requires an OpenRouter key and external models; not a Claude Code skill.

**Parity rules.** Every arm runs inside a fresh `general-purpose` subagent on Sonnet 5 that receives (a) the skill file(s) verbatim, (b) the question verbatim, (c) the instruction "run this skill exactly as written and return the final answer as the skill would present it to the user". Skills that spawn subagents may do so. The orchestrator model is the same for all arms, including wise-men (whose Chairman is therefore Sonnet, as in the original eval).

**No-human adaptation** (brainstorming, grilling — both are designed to interview the user): "No human is available to answer. Ask the questions you would ask, state the most likely answer to each from the question's own context, and then deliver the final recommendation." This is disclosed on the chart. It is the only change to any competitor's instructions.

## Questions (8, fixed)
Q05 engineering (council-shaped, composite 4) · Q09 engineering (single-prompt-shaped, 4) · Q13 product (council-shaped, 5 — wise-men's one loss in the N=29 eval) · Q19 product (council-shaped, 4) · Q25 research (single-prompt-shaped, 5) · Q36 writing (council-shaped, 4) · Q48 ethics (council-shaped, 5) · Q55 personal (council-shaped, 5). Text from `eval-data/questions.yaml`, unchanged.

## Judge
One fresh Opus subagent per question, no skills, sees six responses labeled A–F in the sealed order from `blinding.yaml` (seed 20260916, generated before any run). Rubric and scale identical to the N=29 eval (`judge-prompt.txt`): correctness, insight, practical usefulness, risk awareness, dissent quality, 1–5 each, composite = sum (max 25), with the prompt extended from three to six slots. Wrappers, status lines, and transcripts are stripped from responses before blinding; content is never edited.

## Analysis (fixed)
Per arm: mean composite and per-axis means over the 8 questions; wins vs `direct`; wins vs `wise-men`. Chart: every arm vs the direct baseline, ponytail-style, plus per-axis. With N=8 no significance test is claimed; the chart says N=8.

## Persistence
After every subagent returns: `raw/<Q>/<arm>.md`. Then `blinded/<Q>.md`, `judgments/<Q>.md`, `parsed/<Q>.yaml`. A failed arm is re-run once; a second failure is recorded as a failure and scored as absent, not imputed.
