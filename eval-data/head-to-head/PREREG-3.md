# Head-to-head round 3 — wise-men 3.11.0 against every rival, three judges per question (pre-registration)

Written and committed 2026-09-17, after rounds 1 and 2 were published and before any round-3 run. Nothing below changes after this commit except through dated amendments; results go in `RESULTS-V3.md`. Rounds 1 and 2 stand as published. This commit precedes every round-3 run in the repository's history; it is pushed with the results.

## Why round 3

Round 2 put Warp's council first (23.38 of 25) and wise-men 3.9.2 second (21.12). Versions 3.10.0 and 3.11.0 changed wise-men from round 2's judgments: a decision-memo answer with no council talk, peer scores never used as evidence, a claims and coverage check at every council tier, and a practitioner seat on the strong model. Round 3 measures whether those changes work, on the same eight questions (a direct comparison) and on four questions no head-to-head has used (because the changes were designed from the eight questions' judgments).

## Part A — the eight round-2 questions

Q05, Q09, Q13, Q19, Q25, Q36, Q48, Q55, text from `eval-data/questions.yaml`, unchanged. Nine arms per question:

- **wise-men 3.11.0** — new runs (arm id `wise-men-3.11`), the protocol files as committed in this commit.
- **wise-men 3.9.2** — the round-1/2 answers, unchanged (arm id `wise-men`).
- **Warp council, llm-council, LifeOS Council, ECC council, superpowers brainstorming, mattpocock grilling, plain answer** — the round-2 answers, byte-identical.

## Part B — four held-out questions

Selection rule, fixed here before any run: among the 22 questions in `eval-data/questions.yaml` no head-to-head has used, take the lowest-numbered question in each of the four domains with the most unused questions (research, writing, ethics and personal, four each), skipping Q41, which the N=29 eval still owes as its 30th question. Result: **Q23** (research), **Q32** (writing), **Q43** (ethics), **Q51** (personal).

Four arms per question, all new runs: **wise-men 3.11.0**, **Warp council** and **llm-council** (round 2's top two rivals) and the **plain answer**.

## Parity

Identical to rounds 1–2: a fresh `general-purpose` orchestrator on Sonnet 5 per arm per question receives the skill file and the question verbatim; skills spawn their subagents in the foreground; each arm may Read only its own skill files; it returns only the finished output; an incomplete run is re-run once, and a second failure is recorded and scored as absent. Prompts are the round-1/2 prompts word for word (Warp's adaptations as in PREREG-2), with two additions for wise-men 3.11.0, both disclosed: it may Read `SKILL.md` and `resources/` but not `eval-data/` (which now holds judged answers to the Part A questions), and it writes working files only to a scratch folder, not a council record. The author's first name, which subagents inherit from the author's global config, is redacted to "the user" in raw files before blinding (as in Amendment 1). Runs go in batches of at most four heavy arms at a time, to stay under rate limits.

## Blinding and judges

- **Three fresh Opus 5 judges per question**, 36 judgments in all. Each judge sees its own sealed answer order: `blinding3.yaml`, seed 20260918, generated in this commit.
- Judge prompts: `judge-prompt-9.txt` (Part A) and `judge-prompt-4.txt` (Part B), word for word `judge-prompt-8.txt` apart from the response count and letters. The judge instruction is round 2's, with the count and file changed.
- Normalization: `normalize()` in `h2h.py`, unchanged; wise-men 3.11.0 gets wise-men's rules.

## Analysis (fixed)

- **Question score** for an arm = the mean of its three judges' totals (max 25); axis scores likewise.
- Per arm: mean question score and per-axis means for Part A (8 questions), Part B (4), and — for the four arms in both parts — all 12.
- **wise-men 3.11.0 against each other arm**: wins, ties and losses on question scores, and the mean paired difference with a 95% percentile bootstrap interval over questions (10,000 resamples, seed 20260918), on the widest question set the two share (12 questions for Warp, llm-council and the plain answer; 8 for the rest).
- **wise-men 3.11.0 against wise-men 3.9.2** on Part A, the same way: this measures the 3.10.0–3.11.0 changes.
- **Judge agreement**: the mean, over every arm and question, of the standard deviation of the three judges' totals.
- No other significance test.

## Wording rules for claims (fixed now)

- "Ahead" / "behind": the mean paired difference is above / below zero.
- "Clearly ahead": the 95% interval's lower bound is above zero.
- "Beats every rival": clearly ahead of each rival, each on its widest shared question set. Otherwise the README states which rivals it is clearly ahead of, ahead of, and behind.

## Reporting

Reported whatever it shows, next to rounds 1 and 2, with every deviation disclosed. The README leads with round 3.
