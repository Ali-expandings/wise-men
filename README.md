<p align="center"><img src="assets/banner.svg" alt="wise-men: a pixel-art council (a Devil's Advocate, an engineer, the chairman in a high-backed chair, an analyst and an elder) beside the tagline: a council of Claude subagents that argue, grade each other, and hand you one answer with the dissent kept intact" width="860"></p>

[![stars](https://img.shields.io/github/stars/Ali-expandings/wise-men?style=flat)](https://github.com/Ali-expandings/wise-men/stargazers) [![license](https://img.shields.io/github/license/Ali-expandings/wise-men)](LICENSE) [![check](https://github.com/Ali-expandings/wise-men/actions/workflows/check.yml/badge.svg)](https://github.com/Ali-expandings/wise-men/actions/workflows/check.yml) [![plugin](https://img.shields.io/badge/Claude%20Code-plugin-blue)](#install)

Most prompt patterns ask you to take their word for it. This one ships with the blind evals that tested it — raw answers, judgments, and the scripts that reproduce every number.

<p align="center">
  <strong>2nd of 8 in a pre-registered blind head-to-head, behind Warp's council and ahead of LifeOS Council, llm-council and ECC's council · best dissent score in both rounds · beat a structured prompt on 28 of 29</strong><br>
  <sub>Two evals, one blind judge per question, 5-axis rubric; each head-to-head round was pre-registered before its new arms ran. <a href="#does-it-actually-work">Charts, method and caveats</a>.</sub>
</p>

```
/plugin marketplace add Ali-expandings/wise-men
/plugin install wise-men@wise-men
```

Then: *"run a council on whether we should rewrite the billing service or strangle it incrementally"*.

---

## Does it actually work?

Two blind evals, both shipped raw in this repo. The first puts wise-men next to skills people already use. The second asks the question every prompt-skill eventually gets: does it beat just asking well?

### 1. Against the skills people already use (N=8, pre-registered, two rounds)

Eight hard questions — engineering, product, research, writing, ethics, a personal decision. Eight ways to answer each: wise-men, six of the most-used and best-known skills for stress-testing a decision ([picked by installs and stars](eval-data/head-to-head/COMPETITOR-SCAN.md)), and a plain answer with no skill. The same top-level model ran every arm with its skill file verbatim; council members ran on whichever Claude models each skill chose. A fresh blind judge per question scored the answers under letters, in an order sealed in advance. Round 1 had six arms; round 2 added the two most-installed general-purpose council skills, Warp's and ECC's, and re-judged every answer.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-v2-dark.svg"><img src="assets/h2h-v2.svg" width="860" alt="Round 2 mean total score out of 25 on 8 blind-judged questions: Warp council 23.4, wise-men 21.1, llm-council 19.4, LifeOS Council 19.1, ECC council 19.1, brainstorming 15.9, plain answer 15.3, grilling 13.8. Warp council, wise-men and llm-council beat the plain answer on all 8 questions."></picture></p>

| round 2 | total /25 (vs plain) | correct | insight | practical | risk | dissent | beat plain |
|---|--:|--:|--:|--:|--:|--:|--:|
| [Warp council](https://github.com/warpdotdev/common-skills) 24.5k installs | **23.4** (+8.1) | **4.9** | **4.8** | **4.9** | **4.9** | 4.0 | **8 of 8** |
| **wise-men** | 21.1 (+5.9) | 3.8 | 4.6 | 3.6 | 4.5 | **4.6** | **8 of 8** |
| [llm-council](https://github.com/aiwithremy/claude-skills-llm-council) 1.0k installs | 19.4 (+4.1) | 3.6 | 4.1 | 3.8 | 4.3 | 3.6 | **8 of 8** |
| [LifeOS Council](https://github.com/danielmiessler/LifeOS) 19k★ | 19.1 (+3.9) | 3.4 | 4.1 | 3.8 | 3.8 | 4.1 | 7 of 8 |
| [ECC council](https://github.com/affaan-m/ECC) 7.7k installs | 19.1 (+3.9) | 4.0 | 3.9 | 3.8 | 3.9 | 3.6 | 7 of 8 |
| [superpowers](https://github.com/obra/superpowers) brainstorming 366k installs | 15.9 (+0.6) | 3.9 | 3.3 | 3.9 | 2.9 | 2.0 | 5 of 8 |
| plain answer | 15.3 | 4.3 | 3.0 | 3.5 | 2.6 | 1.9 | — |
| [mattpocock](https://github.com/mattpocock/skills) grilling 718k installs | 13.8 (−1.5) | 3.4 | 2.9 | 3.3 | 2.8 | 1.5 | 2 of 8 |

Bold = best in the column (ties bolded together). Installs from the skills.sh registry; LifeOS Council ships inside a larger repo, so its stars are shown instead.

**What it shows.** Warp's council scored highest — 23.4, the top score (alone or shared) on 7 of 8 questions, and the lead on every axis except dissent. wise-men came second: ahead of llm-council, LifeOS Council and ECC's council, with the best dissent score of all eight, and it beat the plain answer on every question. The judgments show where it lost the points: in 6 of 8 the judge marked down process talk inside wise-men's answer (council meta, reviewer scores), its practical use was the lowest of the five councils, and its correctness sat below the plain answer's. All eight of Warp's answers share the same four core sections: recommendation, why, tradeoffs and risks, final call. Warp ran adapted: its skill asks for a model-diverse council (Opus-, GPT- and open-source-class members), and here every member was a Claude model, so its intended setup could score differently. brainstorming and grilling are built to interview you before deciding; with nobody to answer they had to assume, so this measures them on a job they were not designed for.

**Round 1** (six arms, before Warp and ECC were added): wise-men had the highest mean, 23.3, and scored 5/5 on risk and dissent on all eight questions. Round 2 re-judged those six answers unchanged; the judge gave each of them a lower mean, by 1.1 to 2.5 points, but kept their order apart from LifeOS Council and llm-council swapping places — so compare scores within a round, not across rounds.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-v2-axes-dark.svg"><img src="assets/h2h-v2-axes.svg" width="860" alt="Round 2 scoreboard, means over 8 questions. Total: Warp council 23.4, wise-men 21.1, llm-council 19.4, LifeOS Council 19.1, ECC council 19.1, brainstorming 15.9, plain answer 15.3, grilling 13.8. Warp council led correctness 4.9, insight 4.8, practical use 4.9 and risk awareness 4.9; wise-men led dissent quality with 4.6."></picture></p>

<details>
<summary>Every question, round 1, the cost, and how the study was run</summary>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-v2-questions-dark.svg"><img src="assets/h2h-v2-questions.svg" width="860" alt="Round 2 per-question scores: wise-men scored between 19 and 23; against the best of the other six skills it was tied on 1 question and behind on 7; Warp's council had the top score, alone or shared, on 7 of 8."></picture></p>

- **Pre-registered.** [`PREREG.md`](eval-data/head-to-head/PREREG.md) (round 1, seed 20260916) was committed before any arm ran; [`PREREG-2.md`](eval-data/head-to-head/PREREG-2.md) (round 2, seed 20260917) before its two new arms ran and before any re-judging. They fix the arms and their commits, the 8 questions, the judge prompt, the sealed blinding order and the analysis, with no significance test at N=8. The judge scores the same five axes on the same 1–5 scale as the N=29 eval below, but its prompt differs: it ranks all the answers first instead of comparing pairs, and it has no per-score anchors. The [competitor scan](eval-data/head-to-head/COMPETITOR-SCAN.md) that picked round 2's arms was committed with PREREG-2.
- **Parity.** Every arm ran in a fresh top-level subagent on the same model (Sonnet), with its skill file and the question verbatim; skills that spawn subagents did so, on the Claude models they chose. Pre-registered adaptations: brainstorming, grilling and ECC's council stated the answers they assumed instead of waiting for a human; Warp's council ran its members as Claude Code subagents on Claude models, with no pause for approval.
- **Normalization.** Headers and orchestrator status lines were stripped from every arm. wise-men's appended audit trail was stripped on 4 questions, because the skill shows it only on request; LifeOS Council's round-by-round debate was kept, because its output format makes the transcript the answer; Warp's member list stayed where it was a headed section and was cut on 2 questions where it sat as a short paragraph before the first heading, so the judge saw it on 6 of 8; and the header rule also removed a one-line title from 2 brainstorming answers. Normalization only removed text; apart from disclosed redactions of personal details, no answer was edited.
- **Deviations.** Round 1 ([`RESULTS.md`](eval-data/head-to-head/RESULTS.md)): one amendment after Q13 exposed that arms could read the author's files (from then on an arm reads only its own skill files), and five re-runs — two at Q13 (one arm had read private notes, one orchestrator returned early) and three at Q55 (killed by a rate limit before producing any output). Round 2 ([`RESULTS-V2.md`](eval-data/head-to-head/RESULTS-V2.md)): no re-runs, one parser fix for the extra answer labels, and one first name redacted before blinding.
- **Cost.** Median minutes per question: Warp's council 12.0, wise-men 8.2, ECC's council 5.1, llm-council 3.9, LifeOS Council 3.5, about a minute for brainstorming and grilling, and 15 seconds for a plain answer. wise-men chose deep tier on 4 of the 8 questions.
- **Limits.** N=8, one judge model, and every answer and judgment comes from the same model family. Installs from the skills.sh registry and stars from the GitHub API, 2026-09-17; star counts are for whole repos.

<details>
<summary>Round 1: charts and table (six arms)</summary>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-dark.svg"><img src="assets/h2h.svg" width="860" alt="Round 1 mean total score out of 25 on 8 blind-judged questions: wise-men 23.3, LifeOS Council 21.4, llm-council 20.8, brainstorming 17.9, plain answer 16.4, grilling 16.3. wise-men, LifeOS Council and llm-council beat the plain answer on all 8 questions."></picture></p>

| vs plain answer | total /25 | correct | insight | practical | risk | dissent | beat plain |
|---|--:|--:|--:|--:|--:|--:|--:|
| **wise-men** | **23.3** (+6.9) | **4.6** | **4.6** | 4.0 | **5.0** | **5.0** | **8 of 8** |
| [LifeOS Council](https://github.com/danielmiessler/LifeOS) 19k★ | 21.4 (+5.0) | 4.4 | 4.3 | 4.1 | 4.3 | 4.4 | **8 of 8** |
| [llm-council](https://github.com/aiwithremy/claude-skills-llm-council) 2.1k★ | 20.8 (+4.4) | 3.9 | 4.5 | 4.0 | 4.4 | 4.0 | **8 of 8** |
| [superpowers](https://github.com/obra/superpowers) brainstorming 288k★ | 17.9 (+1.5) | **4.6** | 3.8 | **4.4** | 3.3 | 1.9 | 4 of 8 |
| [mattpocock](https://github.com/mattpocock/skills) grilling 264k★ | 16.3 (−0.1) | 3.9 | 3.3 | 4.0 | 3.3 | 1.9 | 3 of 8 |
| plain answer | 16.4 | **4.6** | 3.3 | 4.0 | 2.9 | 1.6 | — |

Bold = best in the column (ties bolded together). Stars are for the whole repo.

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-axes-dark.svg"><img src="assets/h2h-axes.svg" width="860" alt="Round 1 per-axis mean scores, 1 to 5. Correctness: tie at 4.6 between wise-men, brainstorming and the plain answer. Insight: wise-men 4.6, plain 3.3. Practical use: brainstorming 4.4, wise-men and plain 4.0. Risk awareness: wise-men 5.0, plain 2.9. Dissent quality: wise-men 5.0, plain 1.6."></picture></p>

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/h2h-questions-dark.svg"><img src="assets/h2h-questions.svg" width="860" alt="Round 1 per-question scores: wise-men scored between 22 and 24 on every question; against the best of the other four skills it was ahead on 3 questions, tied on 2 and behind on 3."></picture></p>

</details>

Raw answers, blinded packets, judgments and parsed scores: [`eval-data/head-to-head/`](eval-data/head-to-head/). Reproduce the tables: `H2H_STUDY=v2 python3 eval-data/head-to-head/h2h.py readme` (round 2) and `python3 eval-data/head-to-head/h2h.py readme` (round 1); `report` prints the two-decimal means and win–tie–loss counts behind them.
</details>

### 2. Against a structured single prompt (N=29)

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/headline-dark.svg"><img src="assets/headline.svg" width="860" alt="Same 29 questions, three ways of answering: council 24.5, structured prompt 20.8, direct answer 16.3"></picture></p>

**Short version: the core loop is measured; the refinements on top are field-used, not measured.** The numbers above come from the **v2.3-era core loop** — a council with no context brief, no reasoning-procedure assignment, no validators, no synthesis-checker, and with the Devil's-Advocate model upgrade deliberately switched off so every member ran the same model. Everything this repo adds on top of that is *reasoned from* the result, not measured by it. (The head-to-head above did run the shipped v3.9.2 protocol end to end, but against other skills and a plain answer, not against this structured prompt. Version 3.10.0 then changed how the answer is written and how peer scores are used, on the evidence of those judgments and a recorded council run; those changes are not measured yet.) The measured configuration is weaker than what ships, so the shipped default should be at least as good — but treat that as an expectation, not a finding. The judge was a single blinded Claude model grading Claude outputs, which is exactly the bias described in one of the papers credited at the bottom of this file.

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

```mermaid
flowchart TB
    Q["<b>Your question, scored 1–5</b><br/>depth · stakes · novelty<br/>the hardest axis decides"]
    Q -->|"1–2"| T0
    Q -->|"on request"| T1
    Q -->|"3"| T2
    Q -->|"4"| T3
    Q -->|"5"| T4
    subgraph tiers["Spawns only the agents the question needs"]
        T0(["<b>solo</b><br/>0 agents · one pass"])
        T1["<b>quick</b><br/>~6 agents"]
        T2["<b>standard</b><br/>~8 agents"]
        T3["<b>deep</b><br/>~15–20 agents"]
        T4["<b>paranoid</b><br/>~25+ agents"]
    end
    T1 & T2 & T3 & T4 --> B["<b>Same verified facts</b><br/>one facts-only brief for all"]
    B --> M1 & M2 & M3
    subgraph council["3–7 members · different minds · no peeking"]
        M1["Member<br/>reasons from<br/><b>first principles</b>"]
        M2["Member<br/>reasons from<br/><b>base rates</b>"]
        M3["<b>Devil's Advocate</b><br/>on a stronger model<br/>attacks the framing"]
    end
    M1 & M2 & M3 --> G["<b>3–7 neutral graders</b><br/>score the verbatim answers<br/>check facts before scoring<br/>a score split forces debate"]
    G -.->|"debate: 1–2 rounds"| council
    G --> C["<b>Chairman</b><br/>evidence over votes<br/>dissent kept word for word<br/>shared blind spots lower confidence"]
    C --> K["<b>Independent check</b><br/>grounding · dissent · claims<br/>confidence · disclosure<br/><i>caught errors in 4+ runs</i>"]
    K -.->|"fails: redraft"| C
    K --> A("<b>Your answer</b><br/>a decision memo · first step<br/>strongest counter-case intact<br/>no council talk · shortcuts disclosed")

    classDef key stroke:#b8323a,stroke-width:2px
    class M3,C,K key
```

Easy questions skip the council (`solo` tier). Standard tier skips the debate and the independent check; deep and paranoid debate when the rule fires and always run the check, which also runs whenever a run degrades. `--debate` forces a debate at any tier.

**Each technique exists to block a specific failure:**

| Technique | Failure it prevents |
|---|---|
| Agents spawned to match the question — 0 for an easy one, ~25+ for an irreversible call — sized by the hardest of depth, stakes and novelty | a quick answer where a council was needed, or a council's worth of agents spent on a lookup |
| One verified, facts-only brief, identical for every member | members arguing from different — or invented — facts |
| A different reasoning method per member: first principles, base rates, precedent, incentives, falsification | five answers that agree for the same wrong reason |
| Members run as read-only agents and never see each other | groupthink, runaway subagents, a member editing your files |
| A Devil's Advocate on a stronger model, told to attack the framing | a token contrarian too weak to change the outcome |
| Fresh graders score the verbatim answers and check facts first | a confident error, or the orchestrator's paraphrase, winning the scores |
| A debate triggered by a fixed rule over scores and positions | skipping the argument because consensus *feels* settled |
| Dissent kept word for word; a blind spot several members share caps the confidence | watered-down dissent and false consensus |
| The answer is a decision memo — recommendation, why, what to do, risks, the strongest counter-position — and peer scores never count as evidence in it | council talk burying the answer, and unverified claims dressed as checked because reviewers liked them (both cost points in the head-to-head) |
| An independent check of the final synthesis, including every load-bearing number, date and precedent | fabricated attributions, unsupported specifics and undisclosed shortcuts — it rejected first drafts in 4+ real runs |

<details>
<summary>Stage by stage</summary>

```
Pre-flight → difficulty (depth / stakes / novelty, max-dominates) → tier
  Stage 0    pick personas by domain; Devil's Advocate is mandatory
             each member gets a distinct REASONING PROCEDURE
             (precedent · first principles · base rates · incentives · falsification)
  Stage 0.5  one shared, facts-only context brief — members are otherwise blind
  Stage 1    N members answer in parallel, fixed 5-section contract  → validator
  Stage 2    N fresh neutral graders score everyone on a 4-axis rubric → validator
  Stage 3    debate round if the council genuinely splits
  Stage 4    Chairman writes a decision memo — evidence over votes, dissent verbatim
  Stage 4.5  an independent checker audits the synthesis before you see it
```

</details>

Two design choices carry most of the weight:

**Diversity comes from reasoning procedures, not job titles.** Ensembles help when errors *decorrelate*. Five personas that all pattern-match the same way just agree with themselves five times, so each member is assigned a different way of reasoning about the problem.

**Dissent is structurally protected.** It's preserved verbatim, it can't be truncated by any brevity flag, and it must be a clean counter-position — re-stating the majority view with hedges doesn't count. The eval's single council loss was exactly that failure.

## How it compares

Measured against the skills people already use, see [the head-to-head](#1-against-the-skills-people-already-use-n8-pre-registered-two-rounds): second of eight in round 2, behind Warp's council; highest of six in round 1; the best dissent score in both rounds.

The question every prompt-skill gets asked — after ponytail's benchmark was matched by a seven-word prompt — is *does the skill beat just asking well?* The N=29 eval was built around that question. Arm B is one structured prompt (five perspectives + a dissent, no subagents); it is also shipped as the `solo` tier.

| vs direct answer (blind, 25-pt rubric, N=29) | score | beat the structured prompt | cost |
|---|---|---|---|
| **wise-men council** (standard tier) | **24.5** | **28 / 29** | ~5–7¢ |
| structured single prompt (= `solo` tier) | 20.8 | — | ~free |
| direct answer | 16.3 | 0 / 29 | ~free |

Against the other council skills for Claude Code (facts from their READMEs or skill files, 2026-09-16/17; full table with sources in [`resources/landscape.md`](resources/landscape.md)):

| | wise-men | [llm-council skill](https://github.com/aiwithremy/claude-skills-llm-council) 2.1k★ | [llm-council-skill](https://github.com/tenfoldmarc/llm-council-skill) 766★ | [council-review](https://github.com/ngmeyer/council-review) | [agent-review-panel](https://github.com/wan-huiyan/agent-review-panel) | [Warp council](https://github.com/warpdotdev/common-skills) 24.5k installs | [ECC council](https://github.com/affaan-m/ECC) 7.7k installs |
|---|---|---|---|---|---| --- | --- |
| Independent members, no keys | yes | yes | yes | yes | yes | yes | yes |
| Peer review | 4-axis rubric, parsed + validated | method unspecified | anonymized | anonymous, confidence | blind final score | — | — |
| Debate | conditional, mechanical trigger | — | inside review | adaptive multi-round | 1–3 rounds | optional second round | another round on request |
| Dissent preserved | verbatim, cannot be truncated | agree/clash | agree/clash | "What You Lose" | with judge rulings | consensus + disagreements | strongest dissent + premise check |
| Independent check of the synthesis | yes | — | — | — | Opus judge | — | — |
| Members structurally unable to spawn/run/write | yes | — | — | — | read-only shell | read-only by instruction | — |
| Cost tiers | 5, with spend ceiling | — | — | 5 modes | budget mode | — | — |
| Evidence in the repo | raw eval + script | none | none | one A/B figure | one cost audit | none | none |

<p align="center"><picture><source media="(prefers-color-scheme: dark)" srcset="assets/landscape-dark.svg"><img src="assets/landscape.svg" width="860" alt="Feature matrix: council skills for Claude Code, from their READMEs or skill files, 2026-09-16/17"></picture></p>

What they have that this doesn't: multi-vendor councils, convergence-driven long debates, consensus gates, code-specific scanners, HTML reports — listed honestly in the landscape file. The decision-memo answer shape of Warp's council, which outscored wise-men in round 2 of the head-to-head, was adopted in 3.10.0, unmeasured.

## Cost

Roughly: solo ~free, quick ~3-5¢, standard ~5-7¢, deep ~15¢, paranoid ~25-50¢ per question (2026-07 pricing, cheap models on routine roles). Cheap models grade; stronger models argue; the model mapping lives in one table in `resources/model-routing.md` — update it there when models change and nothing else moves.

## Limits (the ones that matter)

- **Single-model.** Every member is Claude, so persona diversity approximates but doesn't achieve architectural diversity. Shared blindspots survive.
- **The Chairman is the orchestrator.** Same thread picks the personas and writes the synthesis. Stage 4.5's external checker mitigates this; it doesn't remove it.
- **The refinements aren't isolated.** The N=29 eval validated the v2.3 core loop against a structured prompt; the head-to-head measured the shipped protocol end to end against six other skills, at N=8. No eval isolates what each refinement adds — which is the same circularity the skill would flag in your reasoning.
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
eval-data/head-to-head/   the pre-registered head-to-head (two rounds) vs six popular skills: raw answers, blinded packets, judgments, h2h.py
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
