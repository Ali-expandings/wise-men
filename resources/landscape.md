# Landscape — where wise-men sits among council / debate / review tools

Snapshot taken 2026-09-16 (stars from the GitHub API that day; feature facts from each project's README the same day — they will drift, and if you find one wrong, open an issue). "Evidence shipped" means raw data + a reproducible script in the repo, not a number in a README.

**Measured, not just compared:** a pre-registered blind head-to-head against four popular skills — superpowers' brainstorming, mattpocock's grilling, LifeOS Council and llm-council — is in [`eval-data/head-to-head/RESULTS.md`](../eval-data/head-to-head/RESULTS.md) (2026-09-17).

## The comparison people actually make

Two skills readers already know set the bar for "prove it": **ponytail** (140k★) ships a benchmark table against a no-skill baseline, and **caveman** (106k★) lists who measured it and what they found — including JetBrains measuring 8.5% against an advertised 65%. The critique that followed ponytail (Scott Logic, June 2026) was the one every prompt-skill fears: *a seven-word prompt matched it.* wise-men's eval was designed around that exact question before the critique existed. Arm B is the seven-word-prompt equivalent — one structured prompt asking for five perspectives and a dissent, no subagents — and the council beat it on 28 of 29 questions (24.5 vs 20.8 / 25). Arm B is also shipped as the `solo` tier, because it captures most of the gain for none of the cost and readers should have it.

## Direct competitors — council skills that run inside Claude Code

| Project | ★ | Members | Independent | Peer review | Debate | Dissent in output | Synthesis check | Tool-restricted members | Cost tiers | Evidence shipped | API keys |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **wise-men** (this) | new | 3–7 by tier, DA mandatory | yes, offline, shared facts-only brief | 4-axis rubric, stable labels, machine-parsed, validated | conditional, 3-clause trigger, early-stop | verbatim, cannot be truncated by any flag | yes — independent checker before output | yes — `wise-member` (Read/Grep/Glob only) | solo/quick/standard/deep/paranoid, spend ceiling | N=29 blind eval, raw arms + judgments + Wilcoxon script; ~35 logged live runs | none |
| [aiwithremy/claude-skills-llm-council](https://github.com/aiwithremy/claude-skills-llm-council) | 2.1k | 5 advisors | yes | "review each other" — method unspecified | not mentioned | agree / clash sections | no | not mentioned | not mentioned | none | none |
| [tenfoldmarc/llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill) | 766 | 5 thinking styles | yes | anonymized cross-review | inside peer review | agree / clash | no | not mentioned | not mentioned | none | none |
| [ngmeyer/council-review](https://github.com/ngmeyer/council-review) | 16 | 5 reasoning methods | yes | anonymous, confidence-rated | adaptive multi-round (KS convergence) | "What You Lose" section | no | not mentioned | full / quick / adaptive / jury | V1→V2 A/B figure cited (3.8→4.8); data not in README | none |
| [amgadelgamal/claude-council](https://github.com/amgadelgamal/claude-council) | 17 | 4 (2–8) | yes, isolated context | anonymous ranking | not mentioned | consensus + dissent | no | not mentioned | full / quick | one worked example (~173k tokens) | none |
| [wan-huiyan/agent-review-panel](https://github.com/wan-huiyan/agent-review-panel) | 35 | 4–6 reviewers (code/plans) | yes | private reflection + blind final score | 1–3 adversarial rounds | disagreements with judge rulings | Opus "supreme judge" | read-only shell commands | budget mode, trace tiers | one cost audit ($162 run) | none |
| [vinitjhawar/opencouncil](https://github.com/vinitjhawar/opencouncil) | 1 | 10 board (5 light) | yes | 8-of-10 consensus gate, vetoes | up to 3 revision loops | one-line diff; full with `--verbose` | no | not mentioned | light / medium / heavy | token-per-mode figures | none |
| [danielmiessler/LifeOS Council](https://github.com/danielmiessler/lifeos/blob/main/LifeOS/install/skills/Council/SKILL.md) | (part of LifeOS) | 4–6 briefs | parallel per round | none | 3-round or 1-round | round-by-round transcript | no | `general-purpose` required | not mentioned | none | none |
| [boshu2/agentops council](https://www.claudemarketplace.net/skills/council) | 349 | 2–6 judges | yes | consensus aggregation | `--debate` (validate mode) | DISAGREE verdict | no | not mentioned | quick / deep / mixed | none | none |
| [alirezarezvani adversarial-reviewer](https://github.com/alirezarezvani/claude-skills) | (in a 25k★ collection) | 3 personas (code only) | sequential | none | none | severity promotion, no dissent | no | not mentioned | none | none | none |

## The lineage — standalone apps (need API keys, not a coding-agent skill)

| Project | ★ | What it adds | Evidence shipped |
|---|---|---|---|
| [karpathy/llm-council](https://github.com/karpathy/llm-council) | 24.9k | the pattern: independent answers → anonymous ranking → chairman; OpenRouter, "Saturday hack" | none |
| [jacob-bd/the-ai-counsel](https://github.com/jacob-bd/the-ai-counsel) / [llm-council-plus](https://github.com/jacob-bd/llm-council-plus) | 114 / 358 | 12+ providers, multi-round debate with convergence stop, persona advisors, disagreements table | none |
| [hex/claude-council](https://github.com/hex/claude-council) | 751 | asks several coding agents the same question, shows answers side by side (no synthesis) | none |
| [gcpdev/llm-council-skill](https://github.com/gcpdev/llm-council-skill) | 442 | Claude Code skill that consults ChatGPT + Gemini (external) | none |
| [dubs3c/council](https://github.com/dubs3c/council), [focuslead/ai-council-framework](https://github.com/focuslead/ai-council-framework), [ghdna/persona-council](https://github.com/ghdna/persona-council) | 10 / 25 / 6 | persona debate to consensus; claim-level agreement scoring; persona-bound Karpathy fork | none |
| Perplexity "Model Council" (Max plan) | — | the pattern as a product feature | none public |

## What is actually different here

Most council skills are the Karpathy three stages ported to subagents. The differences that matter are not "more stages":

1. **The evidence is in the repo, not the README.** Raw arms, blinded copies, judgments, parsed scores, the frozen protocol that was measured, and a script that reproduces the p-value. Every other entry above ships a claim or nothing.
2. **The single-prompt control exists.** The question that sank ponytail's benchmark was asked here first, and the answer (Arm B, 20.8) is shipped as a tier.
3. **Dissent is a contract, not a section.** It must be a clean counter-position, quoted verbatim, and no brevity flag can cut it. The eval's one council loss was a dissent that re-argued the majority — that became a rule.
4. **Members are structurally offline.** `wise-member` cannot spawn, run, or write. Recursion (a member running a council) is impossible, not discouraged. Only agent-review-panel is in the same neighbourhood (read-only shell).
5. **Someone checks the Chairman.** A fresh checker audits the synthesis against the member answers before you see it. In live use it has rejected the Chairman's first draft for real errors in at least six runs — including twice on the councils that reviewed this release.
6. **Every deviation is disclosed.** A council that quietly dropped a stage looks like a full one. Here it can't.

## What others do that wise-men does not

- **Multiple model families.** Karpathy's original, the-ai-counsel, and agent-review-panel can mix vendors; wise-men is Claude-only by design (no keys, runs on your plan) and says so as its first limit.
- **Convergence-driven multi-round debate** (ngmeyer, the-ai-counsel, opencouncil). wise-men runs at most two rounds and only when a mechanical trigger fires — a deliberate cost choice, not a capability gap, but a gap in practice for questions that need iteration.
- **Consensus gates / vetoes** (opencouncil, agentops). wise-men synthesizes; it does not block output on a vote.
- **Code-specific signal detection** (agent-review-panel's auto-detected signal groups, adversarial-reviewer's OWASP persona). wise-men is domain-general; the Security persona is a seat, not a scanner.
- **HTML reports** (tenfoldmarc, agent-review-panel). wise-men writes markdown council records.

## Sources

Star/fork counts: GitHub API, 2026-09-16. Feature facts: each repository's README or SKILL.md as fetched 2026-09-16. Ponytail critique: Scott Logic, "Ponytail? YAGNI!" (2026-06-16). Caveman measurement: JetBrains AI blog, "Speaking to AI Agents like Cavemen…" (2026-07). Directories consulted: danielrosehill/Awesome-LLM-Council-Projects, claudemarketplace.net, claudedirectory.org, firecrawl.dev "14 Best Claude Code Skills 2026".
