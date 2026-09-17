<p align="center"><img src="assets/banner.svg" alt="wise-men — a council of Claude subagents that argue, grade each other, and hand you one answer with the dissent kept intact" width="860"></p>

[![stars](https://img.shields.io/github/stars/Ali-expandings/wise-men?style=flat)](https://github.com/Ali-expandings/wise-men/stargazers) [![license](https://img.shields.io/github/license/Ali-expandings/wise-men)](LICENSE) [![check](https://github.com/Ali-expandings/wise-men/actions/workflows/check.yml/badge.svg)](https://github.com/Ali-expandings/wise-men/actions/workflows/check.yml) [![plugin](https://img.shields.io/badge/Claude%20Code-plugin-blue)](#install)

Most prompt patterns ask you to take their word for it. This one ships with the blind evals that tested it — raw answers, judgments, and the scripts that reproduce every number.

<p align="center">
  <strong>Highest mean score in a blind head-to-head with superpowers' brainstorming, mattpocock's grilling, LifeOS Council and llm-council · 5/5 on risk and dissent on every question · beat a structured prompt on 28 of 29</strong><br>
  <sub>Two evals, one blind judge each, 5-axis rubric; the head-to-head was pre-registered before any arm ran. <a href="#does-it-actually-work">Charts, method and caveats</a>.</sub>
</p>

```
/plugin marketplace add Ali-expandings/wise-men
/plugin install wise-men@wise-men
```

Then: *"run a council on whether we should rewrite the billing service or strangle it incrementally"*.

---

## Does it actually work?

Two blind evals, both shipped raw in this repo. The first puts wise-men next to skills people already use. The second asks the question every prompt-skill eventually gets: does it beat just asking well?

### 1. Against the skills people already use (N=8, pre-registered)

Eight hard questions — engineering, product, research, writing, ethics, a personal decision. Six ways to answer each: wise-men, four popular skills a Claude Code user would otherwise reach for to think a decision through, and a plain answer with no skill. The same model ran every arm with its skill file verbatim. A fresh blind judge per question scored the six answers as A–F, in an order sealed before anything ran.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-dark.svg"><img src="assets/h2h.svg" width="860" alt="Mean total score out of 25 on 8 blind-judged questions: wise-men 23.3, LifeOS Council 21.4, llm-council 20.8, brainstorming 17.9, plain answer 16.4, grilling 16.3. wise-men, LifeOS Council and llm-council beat the plain answer on all 8 questions."></picture></p>

| vs plain answer | total /25 | correctness | insight | practical | risk awareness | dissent | beat the plain answer |
|---|--:|--:|--:|--:|--:|--:|--:|
| **wise-men** | **23.3** (+6.9) | **4.6** | **4.6** | 4.0 | **5.0** | **5.0** | **8 of 8** |
| [LifeOS Council](https://github.com/danielmiessler/LifeOS) · 19k★ repo | 21.4 (+5.0) | 4.4 | 4.3 | 4.1 | 4.3 | 4.4 | **8 of 8** |
| [llm-council](https://github.com/aiwithremy/claude-skills-llm-council) · 2.1k★ | 20.8 (+4.4) | 3.9 | 4.5 | 4.0 | 4.4 | 4.0 | **8 of 8** |
| [brainstorming](https://github.com/obra/superpowers) from superpowers · 288k★ repo | 17.9 (+1.5) | **4.6** | 3.8 | **4.4** | 3.3 | 1.9 | 4 of 8 |
| [grilling](https://github.com/mattpocock/skills) from mattpocock/skills · 264k★ repo | 16.3 (−0.1) | 3.9 | 3.3 | 4.0 | 3.3 | 1.9 | 3 of 8 |
| plain answer, no skill | 16.4 | **4.6** | 3.3 | 4.0 | 2.9 | 1.6 | — |

Bold = best in the column (ties bolded together).

**What it shows.** wise-men had the highest mean and was the only arm to score 5 on risk awareness and on dissent on all eight questions; its lowest total on any question was 22. The two other councils also beat the plain answer every time — structured multi-voice deliberation works — and wise-men's lead over them (+1.9 and +2.5 points) holds on this sample but is small enough that N=8 cannot settle it. brainstorming and grilling are built to interview you before deciding; with nobody to answer they had to assume, so this measures them on a job they were not designed for. Where wise-men did **not** lead: correctness was a three-way tie, brainstorming was rated more practical, and in 7 of 8 judgments the judge criticised the process talk inside wise-men's answers — the clearest thing to fix next.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-axes-dark.svg"><img src="assets/h2h-axes.svg" width="860" alt="Per-axis mean scores, 1 to 5. Correctness: tie at 4.6 between wise-men, brainstorming and the plain answer. Insight: wise-men 4.6, plain 3.3. Practical use: brainstorming 4.4, wise-men and plain 4.0. Risk awareness: wise-men 5.0, plain 2.9. Dissent quality: wise-men 5.0, plain 1.6."></picture></p>

<details>
<summary>Every question, the cost, and how the study was run</summary>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-questions-dark.svg"><img src="assets/h2h-questions.svg" width="860" alt="Per-question scores: wise-men scored between 22 and 24 on every question; against the best of the other four skills it was ahead on 3 questions, tied on 2 and behind on 3."></picture></p>

- **Pre-registered** in [`PREREG.md`](eval-data/head-to-head/PREREG.md) before any arm ran: arms pinned to commits, the 8 questions fixed, the judge rubric identical to the N=29 eval below, the blinding order sealed (seed 20260916), the analysis fixed, and no significance test at N=8.
- **Parity.** Every arm ran in a fresh subagent on the same model, with its skill file and the question verbatim; skills that spawn subagents did so. brainstorming and grilling got the one pre-registered adaptation: ask your questions, state the likely answers, carry on.
- **Normalization.** Headers and orchestrator status lines were stripped from every arm. wise-men's appended audit trail was stripped on 4 questions, because the skill shows it only on request; LifeOS Council's round-by-round debate was kept, because its output format makes the transcript the answer. Nothing was edited.
- **Deviations**, all disclosed in [`RESULTS.md`](eval-data/head-to-head/RESULTS.md): one amendment after Q13 exposed that arms could read the author's files (from then on an arm reads only its own skill files), and five re-runs — two at Q13 (one arm had read private notes, one orchestrator returned early) and three at Q55 (killed by a rate limit before producing any output).
- **Cost.** wise-men was the slowest arm: a median of 8.2 minutes per question, against 3.5 for LifeOS Council, 3.9 for llm-council, about a minute for brainstorming and grilling, and 15 seconds for a plain answer. It chose deep tier on 4 of the 8 questions.
- **Limits.** N=8, one judge model, and every answer and judgment comes from the same model family. Star counts are for whole repos (superpowers and mattpocock/skills ship many skills), from the GitHub API on 2026-09-17.

Raw answers, blinded packets, judgments and parsed scores: [`eval-data/head-to-head/`](eval-data/head-to-head/). Reproduce the table: `python3 eval-data/head-to-head/h2h.py report`.
</details>

### 2. Against a structured single prompt (N=29)

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/headline-dark.svg"><img src="assets/headline.svg" width="860" alt="Same 29 questions, three ways of answering: council 24.5, structured prompt 20.8, direct answer 16.3"></picture></p>

**Short version: the core loop is measured; the refinements on top are field-used, not measured.** The numbers above come from the **v2.3-era core loop** — a council with no context brief, no reasoning-procedure assignment, no validators, no synthesis-checker, and with the Devil's-Advocate model upgrade deliberately switched off so every member ran the same model. Everything this repo adds on top of that is *reasoned from* the result, not measured by it. (The head-to-head above did run the shipped v3.9.2 protocol end to end, but against other skills and a plain answer, not against this structured prompt.) The measured configuration is weaker than what ships, so the shipped default should be at least as good — but treat that as an expectation, not a finding. The judge was a single blinded Claude model grading Claude outputs, which is exactly the bias described in one of the papers credited at the bottom of this file.

With that stated plainly, the table behind the chart — 30-question blind evaluation, 3 arms per question, 5-axis rubric (max 25):


| Arm | Mean | Median |
|---|---|---|
| **C — full council** | **24.5** | 25 |
| B — one structured prompt (5 perspectives + dissent, single call) | 20.8 | 21 |
| A — direct answer | 16.3 | 16 |

- The council beat the structured single prompt on **28 of 29** persisted questions.
- Wilcoxon signed-rank: **p = 6.3 × 10⁻⁶** (council > structured prompt), **p = 1.3 × 10⁻⁶** (council > direct).
- No rubric axis was significantly worse; four of five were significantly better.
- It won **13/13** questions labeled single-prompt-shaped (written to favour one structured prompt).

<details>
<summary>Every question, and where the gap comes from</summary>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/questions-dark.svg"><img src="assets/questions.svg" width="860" alt="Council vs structured prompt on every question, sorted by gap; council ahead on 28 of 29"></picture></p>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/axes-dark.svg"><img src="assets/axes.svg" width="860" alt="Per-axis means: correctness no difference; insight, practical, risk, dissent significantly better"></picture></p>

Charts regenerate from `eval-data/parsed/` with `python3 scripts/make_charts.py`.
</details>

**Read the caveats too** — they're in `eval-data/HISTORY.md` and they're real: one blind judge, Claude judging Claude, N=29 with the 30th question outstanding, a p-value computed one question short of the pre-registered stopping rule (`HISTORY.md` literally says "do not declare a verdict before then"), the measured-vs-shipped gap described above, a treatment change to Arm B mid-eval (an anti-spawn wrapper), a reviewer-prompt fix that was reversed mid-eval, two early judgments salvaged from chat context rather than captured from disk, one question (Q23) resolved by a third blind judge, and two questions (Q09/Q11) whose Chairman model was never recorded — dropping them leaves the result unchanged (N=27, 26/27, p=1.4e-05; `eval-data/analysis/RESULTS_N29.md`).

**Reproducing the numbers.** Requires Python 3 and PyYAML (`pip install pyyaml`), then:

```bash
python3 eval-data/analysis/wilcoxon_n29.py
```

It prints `Loaded 29 questions`, means C=24.48 / B=20.76 / A=16.28, and `C > B ... p=6.30e-06` (last verified 2026-09-16 on the packaged script). **If it doesn't, that's a bug — please open an issue.** The exact v2.3 protocol the eval measured ships verbatim in `eval-data/protocol-v2.3-frozen/`.

The other honest finding: **a single structured prompt (Arm B, 20.8) captures most of the gain for none of the cost.** That's shipped here as `solo` tier and it's the default for easy questions. Spend the full council when the decision is worth ~10 subagent calls.

---

## Field use (Jul–Sep 2026)

Versions 3.0–3.7 of this protocol ran ~35 real councils across ~15 projects — code cutovers, business plans, hiring, brand, security, one go-live audit at paranoid tier. That is use, not measurement, and it validates the *problems* the v3.8 rules fix, not the rules themselves: those were written from the transcripts afterwards, and their first live run was the skill reviewing its own release (2026-09-16, deep tier, record in `CHANGELOG.md`). The synthesis checker (Stage 4.5) rejected the Chairman's first draft in at least four runs for real errors (fabricated attributions, a pre-debate quote presented as post-debate, undisclosed shortcuts). What broke in the field became v3.8: a reviewer floor instead of a rule every run violated, a verbatim grading packet, an anti-anchoring rule for the orchestrator, a post-council verification step, defined round-2 pairing, and a persisted council record. Details in `SKILL.md` → "Field record".

## Install

**Plugin (recommended — one step, the member agent registers itself):**

```
/plugin marketplace add Ali-expandings/wise-men
/plugin install wise-men@wise-men
```

**Or clone into your skills folder:**

```bash
git clone https://github.com/Ali-expandings/wise-men.git ~/.claude/skills/wise-men
mkdir -p ~/.claude/agents && cp ~/.claude/skills/wise-men/agents/wise-member.md ~/.claude/agents/
```

The second line matters for the clone path: `wise-member` is a **tool-restricted agent** (read-only, no ability to spawn agents or run commands) used for every council member. It makes runaway recursion structurally impossible instead of merely asking the model not to. The plugin install registers it automatically (as `wise-men:wise-member`); the clone install needs the copy. Without it the skill still runs — just on a politer guarantee.

Requires [Claude Code](https://claude.com/claude-code). No API keys, no external services, no Python (except to re-run the eval stats). Restart Claude Code, then:

```
/wise-men:wise-men should we rewrite the billing service or strangle it incrementally?
```

(`/wise-men` with the clone install; plain language — "run a council on…", "red team this" — works with both.)

## Usage

```
/wise-men <question>              # auto-picks effort from the question's stakes
/wise-men deep <question>         # 5-7 members + a debate round when they split
/wise-men paranoid <question>     # 7 members, two debate rounds — irreversible calls
/wise-men <question> --solo       # zero subagents, one structured pass
```

Flags: `--full` (whole audit trail), `--brief`, `--debate`, `--model=…`, `--cheap`, `--strong`.

It also answers to plain language — "run a council on this", "red team this plan", "stress-test this idea".

**Don't** use it for lookups, one-liners, or decisions you've already made. It says so itself and will hand you a direct answer instead.

## How it works

```
Pre-flight → difficulty (depth / stakes / novelty, max-dominates) → tier
  Stage 0    pick personas by domain; Devil's Advocate is mandatory
             each member gets a distinct REASONING PROCEDURE
             (precedent · first principles · base rates · incentives · falsification)
  Stage 0.5  one shared, facts-only context brief — members are otherwise blind
  Stage 1    N members answer in parallel, fixed 5-section contract  → validator
  Stage 2    N fresh neutral graders score everyone on a 4-axis rubric → validator
  Stage 3    debate round if the council genuinely splits
  Stage 4    Chairman synthesizes — dissent preserved verbatim
  Stage 4.5  an independent checker audits the synthesis before you see it
```

Two design choices carry most of the weight:

**Diversity comes from reasoning procedures, not job titles.** Ensembles help when errors *decorrelate*. Five personas that all pattern-match the same way just agree with themselves five times, so each member is assigned a different way of reasoning about the problem.

**Dissent is structurally protected.** It's preserved verbatim, it can't be truncated by any brevity flag, and it must be a clean counter-position — re-stating the majority view with hedges doesn't count. The eval's single council loss was exactly that failure.

## How it compares

Measured against the skills people already use, see [the head-to-head](#1-against-the-skills-people-already-use-n8-pre-registered): highest mean score, and 5/5 on risk and dissent on all 8 questions.

The question every prompt-skill gets asked — after ponytail's benchmark was matched by a seven-word prompt — is *does the skill beat just asking well?* The N=29 eval was built around that question. Arm B is one structured prompt (five perspectives + a dissent, no subagents); it is also shipped as the `solo` tier.

| vs direct answer (blind, 25-pt rubric, N=29) | score | beat the structured prompt | cost |
|---|---|---|---|
| **wise-men council** (standard tier) | **24.5** | **28 / 29** | ~5–7¢ |
| structured single prompt (= `solo` tier) | 20.8 | — | ~free |
| direct answer | 16.3 | 0 / 29 | ~free |

Against the other council skills for Claude Code (facts from their READMEs, 2026-09-16; full table with sources in [`resources/landscape.md`](resources/landscape.md)):

| | wise-men | [llm-council skill](https://github.com/aiwithremy/claude-skills-llm-council) 2.1k★ | [llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill) 766★ | [council-review](https://github.com/ngmeyer/council-review) | [agent-review-panel](https://github.com/wan-huiyan/agent-review-panel) |
|---|---|---|---|---|---|
| Independent members, no keys | yes | yes | yes | yes | yes |
| Peer review | 4-axis rubric, parsed + validated | method unspecified | anonymized | anonymous, confidence | blind final score |
| Debate | conditional, mechanical trigger | — | inside review | adaptive multi-round | 1–3 rounds |
| Dissent preserved | verbatim, cannot be truncated | agree/clash | agree/clash | "What You Lose" | with judge rulings |
| Independent check of the synthesis | yes | — | — | — | Opus judge |
| Members structurally unable to spawn/run/write | yes | — | — | — | read-only shell |
| Cost tiers | 5, with spend ceiling | — | — | 5 modes | budget mode |
| Evidence in the repo | raw eval + script | none | none | one A/B figure | one cost audit |

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/landscape-dark.svg"><img src="assets/landscape.svg" width="860" alt="Feature matrix: council skills for Claude Code, from their READMEs 2026-09-16"></picture></p>

What they have that this doesn't: multi-vendor councils, convergence-driven long debates, consensus gates, code-specific scanners, HTML reports — listed honestly in the landscape file.

## Cost

Roughly: solo ~free, quick ~3-5¢, standard ~5-7¢, deep ~15¢, paranoid ~25-50¢ per question (2026-07 pricing, cheap models on routine roles). Cheap models grade; stronger models argue; the model mapping lives in one table in `resources/model-routing.md` — update it there when models change and nothing else moves.

## Limits (the ones that matter)

- **Single-model.** Every member is Claude, so persona diversity approximates but doesn't achieve architectural diversity. Shared blindspots survive.
- **The Chairman is the orchestrator.** Same thread picks the personas and writes the synthesis. Stage 4.5's external checker mitigates this; it doesn't remove it.
- **The refinements aren't isolated.** The N=29 eval validated the v2.3 core loop against a structured prompt; the head-to-head measured the shipped protocol end to end against other skills, at N=8. No eval isolates what each refinement adds — which is the same circularity the skill would flag in your reasoning.
- **One judge model, same family.** Both evals use a single blind judge model grading answers from the same model family. The skill's own synthesis checker exists because that kind of judge has known biases.
- **Members are offline.** `wise-member` cannot browse or run anything. Facts go in through the context brief; flagged claims are verified by the orchestrator afterwards, in a separately labeled section.
- **Verbose.** `SKILL.md` is long. A casual invocation reads it, improvises, and mostly gets the protocol right; the numbered runbook at the top exists to keep that honest.

## Repo layout

```
.claude-plugin/           plugin + marketplace manifests
SKILL.md                  the protocol (the only file auto-loaded)
agents/wise-member.md     tool-restricted member agent — auto-registered by the plugin install
resources/                personas · model routing · stage prompt templates · council-record template · landscape (competitors, sourced)
examples/                 two worked end-to-end runs
eval-spec.md              the frozen evaluation design (written before the eval ran)
eval-data/                the N=29 blind eval: questions, raw arms, judgments, stats, frozen v2.3 protocol
eval-data/head-to-head/   the pre-registered head-to-head vs four popular skills: raw answers, blinded packets, judgments, h2h.py
scripts/check.sh          consistency check — run before every commit (trigger sync, no $-digit, agent copy, PII)
scripts/make_charts.py    regenerates assets/*.svg (light + dark) from both evals' parsed scores
assets/                   banner + README charts (hand-authored SVG, a light and a dark file each)
CHANGELOG.md              condensed version history (detail in eval-data/SESSION_LOG.md)
requirements.txt          PyYAML — only needed to re-run the eval stats
AGENTS.md · CONTRIBUTING.md · SECURITY.md · LICENSE · .gitignore
```

The skill itself has **no runtime dependencies** — it is markdown that Claude Code reads. Python and PyYAML are needed only if you want to recompute the eval statistics yourself.

## Credits

Inspired by [karpathy/llm-council](https://github.com/karpathy/llm-council). Design choices drew on — but are **not validated by** — Du et al. 2023 (multi-agent debate), Liang et al. 2024 (divergent thinking), Khan et al. 2024 (debate via persuasion), Zheng et al. 2024 (LLM-as-judge bias).

Built and audited in Claude Code, including by running the council on itself.

## License

MIT — see [LICENSE](LICENSE).
