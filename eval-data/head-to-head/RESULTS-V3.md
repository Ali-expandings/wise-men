# Head-to-head round 3 results

**Interim.** 6 of the 12 pre-registered questions are fully judged (Q05, Q09, Q13, Q19, Q25, Q36); still to come: Q48, Q55, Q23, Q32, Q43, Q51. This file is regenerated from `parsed-v3/` as questions complete, so its numbers and wording can change; the pre-registered analysis covers all 12 ([`PREREG-3.md`](PREREG-3.md)).

Three blind Opus judges per question, each with its own sealed answer order ([`blinding3.yaml`](blinding3.yaml)); an arm's score on a question is the mean of the three judges; totals are out of 25 (five axes scored 1–5). Part A re-judges round 2's answers from eight arms next to fresh wise-men 3.11.0 answers to the same eight questions (judge prompt: [`judge-prompt-9.txt`](judge-prompt-9.txt), nine answers labelled A–I); Part B asks four held-out questions no head-to-head has used, with four arms ([`judge-prompt-4.txt`](judge-prompt-4.txt)). Answers are normalized as in rounds 1–2 (`normalize()` in `h2h.py`).

## Part A: round-2 questions (N=6)

| arm | total /25 | correctness | insight | practical | risk | dissent |
|---|--:|--:|--:|--:|--:|--:|
| wise-men 3.11.0 | 24.39 | 4.78 | 5.00 | 4.78 | 5.00 | 4.83 |
| Warp council | 21.22 | 4.56 | 4.28 | 4.56 | 4.39 | 3.44 |
| wise-men 3.9.2 | 20.28 | 3.89 | 4.28 | 3.78 | 4.06 | 4.28 |
| llm-council | 18.00 | 3.39 | 3.89 | 3.56 | 3.78 | 3.39 |
| ECC council | 18.00 | 3.89 | 3.78 | 3.50 | 3.61 | 3.22 |
| LifeOS Council | 17.94 | 3.17 | 3.94 | 3.44 | 3.67 | 3.72 |
| brainstorming | 14.67 | 3.78 | 3.06 | 3.67 | 2.56 | 1.61 |
| plain answer | 14.11 | 3.89 | 2.89 | 3.33 | 2.50 | 1.50 |
| grilling | 13.94 | 3.50 | 2.94 | 3.17 | 2.56 | 1.78 |

## Per question (mean of three judges, total /25)

| question | wise-men 3.11.0 | wise-men 3.9.2 | Warp council | llm-council | LifeOS Council | ECC council | brainstorming | grilling | plain answer |
|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|
| Q05 | 25.00 | 20.67 | 19.33 | 17.00 | 17.00 | 18.67 | 14.33 | 13.67 | 12.00 |
| Q09 | 23.67 | 22.33 | 24.33 | 16.33 | 18.00 | 18.67 | 15.33 | 14.33 | 13.67 |
| Q13 | 25.00 | 22.00 | 20.00 | 19.33 | 20.00 | 14.00 | 16.33 | 12.67 | 15.33 |
| Q19 | 25.00 | 20.00 | 20.67 | 21.00 | 14.67 | 19.00 | 16.00 | 16.33 | 15.00 |
| Q25 | 24.00 | 19.00 | 22.67 | 18.00 | 19.67 | 17.00 | 11.33 | 10.67 | 14.67 |
| Q36 | 23.67 | 17.67 | 20.33 | 16.33 | 18.33 | 20.67 | 14.67 | 16.00 | 14.00 |

## wise-men 3.11.0 against each arm

Mean per-question difference in total score, with a 95% percentile bootstrap interval over questions (10,000 resamples, seed 20260918), on the widest question set both arms share. Wording per PREREG-3: *clearly ahead* only when the interval's lower bound is above zero, *ahead* when only the mean difference is.

| against | N | difference | 95% interval | W–T–L | wording |
|---|--:|--:|--:|--:|---|
| wise-men 3.9.2 | 6 | +4.11 | [+2.83, +5.22] | 6–0–0 | clearly ahead |
| Warp council | 6 | +3.17 | [+1.33, +4.83] | 5–0–1 | clearly ahead |
| llm-council | 6 | +6.39 | [+5.22, +7.39] | 6–0–0 | clearly ahead |
| LifeOS Council | 6 | +6.44 | [+4.94, +8.28] | 6–0–0 | clearly ahead |
| ECC council | 6 | +6.39 | [+4.56, +8.56] | 6–0–0 | clearly ahead |
| brainstorming | 6 | +9.72 | [+8.67, +11.06] | 6–0–0 | clearly ahead |
| grilling | 6 | +10.44 | [+8.78, +12.06] | 6–0–0 | clearly ahead |
| plain answer | 6 | +10.28 | [+9.56, +11.39] | 6–0–0 | clearly ahead |

Clearly ahead of every rival skill and the plain answer on the questions judged so far: **yes** (interim; the pre-registered claim needs all 12 questions).

## What the numbers say, and what they don't

- Part A's questions, and round 2's judgments of them, are the evidence versions 3.10.0 and 3.11.0 were built on, so Part A can reward fitting those judgments. Part B's held-out questions test that; they have not been judged yet.
- Scores are relative within a round. The eight reused answers are the same files as in round 2, judged here next to a ninth answer by three judges instead of one; compare arms inside this round, not against round 2's numbers.
- Every answer and every judge is a Claude model. Judges see letters, not arm names, but a distinctive answer format can still be recognizable.
- The intervals resample questions, not judges, and the number of questions is small.

## Judge agreement

Mean standard deviation of the three judges' totals, over every arm and question: 0.56 points out of 25.

## Cost of the new runs

| question | arm | subagent tokens | tool uses | duration |
|---|---|--:|--:|--:|
| Q05 | wise-men 3.11.0 | 213,515 | 18 | 33 min |
| Q09 | wise-men 3.11.0 | 215,625 | 18 | 33 min |
| Q13 | wise-men 3.11.0 | 284,018 | 30 | 61 min |
| Q19 | wise-men 3.11.0 | 293,909 | 31 | 69 min |
| Q25 | wise-men 3.11.0 | 232,005 | 19 | 45 min |
| Q36 | wise-men 3.11.0 | 240,808 | 23 | 31 min |
| Q23 | plain answer | 80,654 | 0 | 3 min |
| Q32 | plain answer | 74,751 | 0 | 1 min |
| Q43 | plain answer | 73,248 | 0 | 1 min |
| Q51 | plain answer | 74,813 | 0 | 1 min |

## Deviations and disclosures

- Q05, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q09, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q13, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause
- Q19, wise-men 3.11.0: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause

## Reproduce

`python3 eval-data/head-to-head/h2h3.py report` prints these numbers, `results` rewrites this file, and `readme` prints the README table. Raw answers: `raw/<question>/`; blinded packets: `blinded-v3/`; judgments: `judgments-v3/`; parsed scores: `parsed-v3/`.
