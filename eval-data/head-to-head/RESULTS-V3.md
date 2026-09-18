# Head-to-head round 3 results

**Result.** wise-men 3.11.0 scored 24.42 of 25 on the eight round-2 questions (Part A, the highest mean) and 24.50 on the four held-out questions (Part B, the highest mean), with the top score on 11 of the 12 questions. Under the pre-registered wording it **beats every rival**: against each the mean per-question difference is positive and its 95% bootstrap interval excludes zero — Warp council +4.11 [+2.83, +5.22] on 12 questions, llm-council +5.64 [+4.83, +6.44] on 12 questions, LifeOS Council +5.29 [+3.50, +7.25] on 8 questions, ECC council +6.13 [+4.83, +7.79] on 8 questions, brainstorming +9.63 [+8.83, +10.67] on 8 questions, grilling +10.58 [+9.33, +11.83] on 8 questions, plain answer +8.92 [+7.50, +10.14] on 12 questions. Against its own previous version, wise-men 3.9.2, on Part A: +3.71 [+2.62, +4.75] (clearly ahead), the measured effect of versions 3.10.0 and 3.11.0. Part B is the check that the result is not a fit to round 2's judgments: wise-men 3.11.0 24.50 against Warp council 18.50, llm-council 19.17 and the plain answer 18.17.

Three blind Opus judges per question, each with its own sealed answer order ([`blinding3.yaml`](blinding3.yaml)); an arm's score on a question is the mean of the three judges; totals are out of 25 (five axes scored 1–5). Part A re-judges round 2's answers from eight arms next to fresh wise-men 3.11.0 answers to the same eight questions (judge prompt: [`judge-prompt-9.txt`](judge-prompt-9.txt), nine answers labelled A–I); Part B asks four held-out questions no head-to-head has used, with four arms ([`judge-prompt-4.txt`](judge-prompt-4.txt)). Answers are normalized as in rounds 1–2 (`normalize()` in `h2h.py`).

## Part A: round-2 questions (N=8)

| arm | total /25 | correctness | insight | practical | risk | dissent |
|---|--:|--:|--:|--:|--:|--:|
| wise-men 3.11.0 | 24.42 | 4.75 | 5.00 | 4.79 | 5.00 | 4.88 |
| Warp council | 21.25 | 4.63 | 4.25 | 4.58 | 4.46 | 3.33 |
| wise-men 3.9.2 | 20.71 | 3.88 | 4.38 | 3.83 | 4.21 | 4.42 |
| LifeOS Council | 19.13 | 3.54 | 4.17 | 3.67 | 3.71 | 4.04 |
| llm-council | 18.63 | 3.58 | 4.00 | 3.58 | 3.83 | 3.63 |
| ECC council | 18.29 | 3.88 | 3.88 | 3.63 | 3.58 | 3.33 |
| brainstorming | 14.79 | 3.83 | 3.08 | 3.79 | 2.58 | 1.50 |
| plain answer | 14.21 | 4.00 | 2.92 | 3.54 | 2.38 | 1.38 |
| grilling | 13.83 | 3.46 | 2.88 | 3.25 | 2.58 | 1.67 |

## Part B: held-out questions (N=4)

| arm | total /25 | correctness | insight | practical | risk | dissent |
|---|--:|--:|--:|--:|--:|--:|
| wise-men 3.11.0 | 24.50 | 5.00 | 5.00 | 4.58 | 5.00 | 4.92 |
| llm-council | 19.17 | 3.75 | 4.25 | 3.25 | 3.67 | 4.25 |
| Warp council | 18.50 | 4.33 | 3.67 | 3.83 | 4.00 | 2.67 |
| plain answer | 18.17 | 4.75 | 4.17 | 4.50 | 2.75 | 2.00 |

## All judged questions: the four arms in both parts (N=12)

| arm | total /25 | correctness | insight | practical | risk | dissent |
|---|--:|--:|--:|--:|--:|--:|
| wise-men 3.11.0 | 24.44 | 4.83 | 5.00 | 4.72 | 5.00 | 4.89 |
| Warp council | 20.33 | 4.53 | 4.06 | 4.33 | 4.31 | 3.11 |
| llm-council | 18.81 | 3.64 | 4.08 | 3.47 | 3.78 | 3.83 |
| plain answer | 15.53 | 4.25 | 3.33 | 3.86 | 2.50 | 1.58 |

## Per question (mean of three judges, total /25)

| question | wise-men 3.11.0 | wise-men 3.9.2 | Warp council | llm-council | LifeOS Council | ECC council | brainstorming | grilling | plain answer |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Q05 | 25.00 | 20.67 | 19.33 | 17.00 | 17.00 | 18.67 | 14.33 | 13.67 | 12.00 |
| Q09 | 23.67 | 22.33 | 24.33 | 16.33 | 18.00 | 18.67 | 15.33 | 14.33 | 13.67 |
| Q13 | 25.00 | 22.00 | 20.00 | 19.33 | 20.00 | 14.00 | 16.33 | 12.67 | 15.33 |
| Q19 | 25.00 | 20.00 | 20.67 | 21.00 | 14.67 | 19.00 | 16.00 | 16.33 | 15.00 |
| Q25 | 24.00 | 19.00 | 22.67 | 18.00 | 19.67 | 17.00 | 11.33 | 10.67 | 14.67 |
| Q36 | 23.67 | 17.67 | 20.33 | 16.33 | 18.33 | 20.67 | 14.67 | 16.00 | 14.00 |
| Q48 | 24.67 | 21.33 | 22.67 | 20.00 | 23.33 | 19.67 | 16.00 | 13.00 | 14.67 |
| Q55 | 24.33 | 22.67 | 20.00 | 21.00 | 22.00 | 18.67 | 14.33 | 14.00 | 14.33 |

| question | wise-men 3.11.0 | Warp council | llm-council | plain answer |
|---|--:|--:|--:|--:|
| Q23 | 24.33 | 19.00 | 19.67 | 21.00 |
| Q32 | 24.33 | 19.00 | 20.33 | 16.33 |
| Q43 | 24.67 | 18.00 | 18.00 | 19.00 |
| Q51 | 24.67 | 18.00 | 18.67 | 16.33 |

## wise-men 3.11.0 against each arm

Mean per-question difference in total score, with a 95% percentile bootstrap interval over questions (10,000 resamples, seed 20260918), on the widest question set both arms share. Wording per PREREG-3: *clearly ahead* only when the interval's lower bound is above zero, *ahead* when only the mean difference is.

| against | N | difference | 95% interval | W–T–L | wording |
|---|--:|--:|--:|--:|---|
| wise-men 3.9.2 | 8 | +3.71 | [+2.62, +4.75] | 8–0–0 | clearly ahead |
| Warp council | 12 | +4.11 | [+2.83, +5.22] | 11–0–1 | clearly ahead |
| llm-council | 12 | +5.64 | [+4.83, +6.44] | 12–0–0 | clearly ahead |
| LifeOS Council | 8 | +5.29 | [+3.50, +7.25] | 8–0–0 | clearly ahead |
| ECC council | 8 | +6.13 | [+4.83, +7.79] | 8–0–0 | clearly ahead |
| brainstorming | 8 | +9.63 | [+8.83, +10.67] | 8–0–0 | clearly ahead |
| grilling | 8 | +10.58 | [+9.33, +11.83] | 8–0–0 | clearly ahead |
| plain answer | 12 | +8.92 | [+7.50, +10.14] | 12–0–0 | clearly ahead |

Clearly ahead of every rival skill and the plain answer on the questions judged so far: **yes**.

## What the numbers say, and what they don't

- Part A's questions, and round 2's judgments of them, are the evidence versions 3.10.0 and 3.11.0 were built on, so Part A can reward fitting those judgments. Part B's held-out questions test that.
- "Held-out" means held out of every head-to-head round and of the judgments the current version was built from. The four questions are not new to the project: like all twelve, they come from `eval-data/questions.yaml`, the 30-question file of the N=29 eval that the v2.3 core loop answered in May 2026.
- One judgment shows the ceiling is generous: on Q23, judge 2 credits another answer with correcting "a mistake the other three make" about what a published-only significance flip shows, yet scores wise-men 3.11.0, one of those three, 5 for correctness. Its memo calls that check "decisive in both directions", which overstates it (dropping half the studies also drops power).
- Scores are relative within a round. The eight reused answers are the same files as in round 2, judged here next to a ninth answer by three judges instead of one; compare arms inside this round, not against round 2's numbers.
- Every answer and every judge is a Claude model. Judges see letters, not arm names, but a distinctive answer format can still be recognizable.
- The intervals resample questions, not judges, and the number of questions is small.

## Judge agreement

Mean standard deviation of the three judges' totals, over every arm and question: 0.63 points out of 25.

## Cost of the new runs

| question | arm | subagent tokens | tool uses | duration |
|---|---|--:|--:|--:|
| Q05 | wise-men 3.11.0 | 213,515 | 18 | 33 min |
| Q09 | wise-men 3.11.0 | 215,625 | 18 | 33 min |
| Q13 | wise-men 3.11.0 | 284,018 | 30 | 61 min |
| Q19 | wise-men 3.11.0 | 293,909 | 31 | 69 min |
| Q25 | wise-men 3.11.0 | 232,005 | 19 | 45 min |
| Q36 | wise-men 3.11.0 | 240,808 | 23 | 31 min |
| Q48 | wise-men 3.11.0 | 293,824 | 29 | 763 min |
| Q55 | wise-men 3.11.0 | 244,600 | 27 | 766 min |
| Q23 | wise-men 3.11.0 | 206,989 | 18 | 23 min |
| Q23 | Warp council | 118,338 | 4 | 9 min |
| Q23 | llm-council | 131,877 | 12 | 18 min |
| Q23 | plain answer | 80,654 | 0 | 3 min |
| Q32 | wise-men 3.11.0 | 193,136 | 18 | 21 min |
| Q32 | Warp council | 101,969 | 4 | 7 min |
| Q32 | llm-council | 135,451 | 12 | 17 min |
| Q32 | plain answer | 74,751 | 0 | 1 min |
| Q43 | wise-men 3.11.0 | 200,107 | 19 | 18 min |
| Q43 | Warp council | 111,156 | 4 | 8 min |
| Q43 | llm-council | 120,945 | 12 | 12 min |
| Q43 | plain answer | 73,248 | 0 | 1 min |
| Q51 | wise-men 3.11.0 | 244,544 | 24 | 36 min |
| Q51 | Warp council | 110,240 | 5 | 8 min |
| Q51 | llm-council | 131,424 | 12 | 14 min |
| Q51 | plain answer | 74,813 | 0 | 1 min |

Median minutes per run, uninterrupted runs only: wise-men 3.11.0 26.8, Warp council 8.2, llm-council 15.1, plain answer 1.4.

## Deviations and disclosures

- Q05, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q09, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q13, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q19, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q48, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q55, wise-men 3.11.0: the orchestrator paused for approval before the synthesis check, against its instructions, and was told to continue; the answer is otherwise its own; duration includes the pause
- Q51, Warp council: the orchestrator wrote its output in the compressed register that the author's global config asks of every agent (an environment condition shared by every arm in all three rounds); kept as produced, since the run was complete

## Reproduce

`python3 eval-data/head-to-head/h2h3.py report` prints these numbers, `results` rewrites this file, and `readme` prints the README table. Raw answers: `raw/<question>/`; blinded packets: `blinded-v3/`; judgments: `judgments-v3/`; parsed scores: `parsed-v3/`.
