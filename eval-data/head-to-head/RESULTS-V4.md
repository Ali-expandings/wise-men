# Head-to-head round 4 results

**Stopped early: 5 of 8 questions.** The round was pre-registered at eight questions and stopped after five at the repository owner's request, to conserve the account's usage allowance. The decision was made while the fifth question was running, after the scores of the first three were known, so it was not a blind stop. R406, R407, R408 (writing, ethics, a personal decision) were never run: no answer or judgment exists for them, and nothing here says how any arm does on those kinds of question. Their sealed answer orders remain in `blinding4.yaml`, so the round can be finished later under the same rules. Every comparison below is over five questions; intervals are 95% percentile bootstraps over those five.

Eight questions written for this round by an author that knew nothing about the arms ([`PREREG-4.md`](PREREG-4.md), [`questions-r4.yaml`](questions-r4.yaml)); five arms; three blind Opus judges per question with sealed orders ([`blinding4.yaml`](blinding4.yaml)) and an error-first judge prompt ([`judge-prompt-5.txt`](judge-prompt-5.txt)). Minutes are the orchestrator's first-to-last transcript timestamp; calls are its subagent spawns; USD prices every token the run used — the orchestrator's and every spawned agent's, input, output, cache reads and cache writes — at the 2026-07 list rates in `resources/model-routing.md`. No council can be faster or cheaper than the plain answer; the pre-registered time and cost comparisons are against the rival councils.

| round 4 (5 of 8 questions) | total /25 | correct | insight | practical | risk | dissent | median minutes | median calls | median list-price USD |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| wise-men 3.13.0 (default) | 23.8 | 4.0 | 5.0 | 4.9 | 4.9 | 5.0 | 37.3 | 11.0 | 9.59 |
| wise-men 3.13.0 fast profile (experimental; removed in 3.14.0) | 23.3 | 4.3 | 4.7 | 4.7 | 4.9 | 4.7 | 10.8 | 4.0 | 2.09 |
| llm-council | 17.9 | 3.1 | 3.9 | 3.3 | 3.8 | 3.7 | 18.0 | 11.0 | 6.43 |
| Warp council | 17.5 | 3.4 | 3.5 | 4.0 | 3.7 | 3.0 | 9.3 | 3.0 | 2.03 |
| plain answer | 16.3 | 3.9 | 3.5 | 4.2 | 2.9 | 1.8 | 1.8 | 0.0 | 0.27 |

- wise-men 3.13.0 (default) against wise-men 3.13.0 fast profile (experimental; removed in 3.14.0): +0.5 [-0.1, +1.2], W–T–L 4–0–1 — ahead.
- wise-men 3.13.0 (default) against Warp council: +6.3 [+5.2, +7.3], W–T–L 5–0–0 — clearly ahead.
- wise-men 3.13.0 (default) against llm-council: +5.9 [+4.2, +7.8], W–T–L 5–0–0 — clearly ahead.
- wise-men 3.13.0 (default) against plain answer: +7.5 [+6.1, +8.9], W–T–L 5–0–0 — clearly ahead.
- wise-men 3.13.0 fast profile (experimental; removed in 3.14.0) against Warp council: +5.7 [+4.8, +6.7], W–T–L 5–0–0 — clearly ahead.
- wise-men 3.13.0 fast profile (experimental; removed in 3.14.0) against llm-council: +5.4 [+3.4, +7.9], W–T–L 5–0–0 — clearly ahead.
- wise-men 3.13.0 fast profile (experimental; removed in 3.14.0) against plain answer: +6.9 [+5.5, +8.3], W–T–L 5–0–0 — clearly ahead.

- wise-men 3.13.0 (default): highest mean on 4 of 5 axes; faster than neither rival council; cheaper than neither rival council.
- wise-men 3.13.0 fast profile (experimental; removed in 3.14.0): highest mean on 1 of 5 axes; faster than llm-council; cheaper than llm-council.

Judge agreement: mean SD of the three judges' totals 0.58.

## Per question (mean of three judges, total /25)

| question | wise-men 3.13.0 (default) | wise-men 3.13.0 fast profile (experimental; removed in 3.14.0) | Warp council | llm-council | plain answer |
|---|--:|--:|--:|--:|--:|
| R401 (engineering, choice) | 23.33 | 24.00 | 18.00 | 14.33 | 17.67 |
| R402 (engineering, diagnosis) | 24.33 | 23.67 | 18.33 | 20.00 | 15.00 |
| R403 (product, questionable-premise) | 23.67 | 23.00 | 19.00 | 16.00 | 17.67 |
| R404 (business, trust-a-number) | 23.67 | 23.33 | 16.00 | 20.00 | 14.33 |
| R405 (research, evidence) | 24.00 | 22.33 | 16.33 | 19.00 | 17.00 |

## Deviations and disclosures

- A fifth arm was judged in the same files: an experimental three-member fast profile of wise-men, added in 3.13.0 and pre-registered for this round. It scored 23.3, half a point behind the full council with an interval that includes zero, in 10.8 minutes at $2.09, and was clearly ahead of every rival. The pre-registered gate for replacing the default was met by the letter and not used: the default led on four of the five questions. After the round the owner chose to develop the fast profile as a separate project; 3.14.0 removes it from this skill and the README reports the full council only. Its answers, judgments and costs stay in this directory unchanged.
- Tier: the default arm chose its own tier, as the skill directs — deep on R401, R403 and R404 (11–13 subagent calls), standard on R402 and R405 (9–10). From the transcripts, the synthesis check took 9–11 minutes on every default run (0.5–2.1 on the fast profile, which uses the cheap tier and four of the six checks), and deep-tier reviewers 5–9 minutes each against about 2 at standard.
- Normalization is `normalize()` from rounds 1–3, unchanged: it cuts any text before a wise-men answer's first heading and nothing after the memo. On R402 that removed a paragraph in which the default arm described its checker's findings before the memo — the judges did not see it; a user would have. Closing notes about how the answer was produced (a late review, the requested fast mode, corrections after the check) stayed in the wise-men answers that carried them, and judges marked them as process residue. Fixed after the round in 3.13.1.
- Web access: the rival councils' members run as general-purpose agents and can browse. Warp's members did on R401 (33 web tool calls) and on no other question; llm-council's never did. wise-men members cannot browse.
- Time is the median over runs not interrupted by the usage limit (four of five for each council arm; all five for the plain answer). Cost and calls use all five runs; a resumed run's cost includes re-reading its own context after the wait.
- Every judge and every arm is a model from the same family, and every spawned agent in every arm inherits the account's global instruction to write tersely. No human grades and no grades from another model family were collected in this round.
- R402, wise-men 3.13.0 (default): interrupted by the account's usage limit after four of its five members had answered (the fifth died with the limit and was retried on resume), and resumed from its own transcript; left out of the time median
- R402, wise-men 3.13.0 fast profile (experimental; removed in 3.14.0): interrupted by the account's usage limit after its three members had answered, and resumed from its own transcript; left out of the time median
- R402, Warp council: interrupted by the account's usage limit after its three members had answered, and resumed from its own transcript; left out of the time median
- R402, llm-council: interrupted by the account's usage limit after its five advisors had answered, and resumed from its own transcript; left out of the time median

## Reproduce

`python3 eval-data/head-to-head/h2h4.py report` prints the table and comparisons; `results` rewrites this file. Time and cost were computed from local agent transcripts when each answer was saved and are stored in the raw file headers; the transcripts themselves are not in the repository.
