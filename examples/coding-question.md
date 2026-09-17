# Example: coding question — "should I split App.tsx?"

A worked end-to-end run. Shows what the council looks like in practice for a typical engineering question.

## User input

> Should I split App.tsx? It's 1179 lines. Mode logic, state, UI, swarm orchestration wiring all in one file. Works now but I'm worried about the long-term.

## Pre-flight (internal, not shown to user)

- Question: clear. Decision point: split vs leave alone.
- Single question (not compound).
- Context: user already shared file size + responsibilities + concern. Enough to answer.
- Council-shaped: yes (architecture decision, multiple defensible answers, has long-term consequences).
- Domain: engineering / architecture.
- Difficulty axes: depth=3 (multi-step trade-off), stakes=3 (real but reversible), novelty=2 (well-known pattern). Composite = 3.
- Tier: standard (from composite 3).
- Members: Pragmatist + Skeptic + Architect + Maintainer + Devil's Advocate (5).
- Model routing (per algorithm):
  - Pragmatist:        sonnet  (tier default)
  - Skeptic:           sonnet  (tier default)
  - Architect:         sonnet  (override: sonnet at standard+ ← matches default here)
  - Maintainer:        sonnet  (tier default)
  - Devil's Advocate:  opus    (override: DA always +1 tier → opus)
  - Reviewers × 3:     haiku   (tier default — rubric scoring is haiku-tolerant; floor is 3 at standard)
  - Debate:            n/a     (skipped at standard tier)
  - Chairman:          main thread
- Expected calls: 5 + 3 = 8.
- Estimated cost: ~$0.07 (4 sonnet members + 1 opus DA + 3 haiku reviewers + chairman on main).

## Stage 1 — 5 parallel Agent calls

Each persona answers independently. Example outputs (compressed for this doc):

**Pragmatist** (high confidence): "It works. 1179 lines is annoying but not broken. Splitting now without a concrete pain point = busywork. Wait until you actually feel friction adding a feature. Confidence: high. Weakest assumption: that the pain point will be obvious when it arrives."

**Skeptic** (medium confidence): "1179 lines hides bugs. Every state mutation is hard to trace. Test coverage is probably weak (or absent). Risk of regressions during the next feature add is real. Confidence: medium. Weakest assumption: that the file is actually as hard to navigate as line count implies — could be well-organized internally."

**Architect** (high confidence): "Single God Component is a recognized anti-pattern. Standard extraction: `useSwarm.ts`, `useChat.ts`, mode handler modules. Cost is ~1-2 days. Benefit: every future change becomes cheaper. Pay now, not later. Confidence: high. Weakest assumption: that future changes are coming — if project is stable and won't change much, the refactor is wasted."

**Maintainer** (medium confidence): "Putting myself in shoes of someone who inherits this in 6 months: I'd struggle. Mental model of mode-state-UI interactions has no clear seams. But — refactor without tests is risky too. Recommend: write integration tests first, then extract. Confidence: medium. Weakest assumption: that the user has time to write tests."

**Devil's Advocate** (high confidence): "The case for not splitting: file size isn't the enemy. Premature abstraction is. Splitting into 5 files of 230 lines each adds import noise, navigation friction, and false boundaries that don't match the actual coupling. Some monoliths are fine. Vite recompiles fast either way. The 'split it because it's big' impulse is pattern-matching to JS culture, not first-principles thinking. Confidence: high. Weakest assumption: that the user is in the 'file is genuinely cohesive' camp rather than the 'file is a dumping ground' camp."

## Stage 2 — 5 parallel Agent calls (peer review, stable persona labels)

Each reviewer gets all 5 answers labeled by persona name (neutral grading frame). Rubric scoring. Example aggregated scores:

```
              | Correct | Insight | Practical | Risk-aware | Avg
Pragmatist    |   4     |   3     |    4      |    3       | 3.5
Skeptic       |   4     |   3     |    3      |    5       | 3.75
Architect     |   5     |   4     |    4      |    4       | 4.25
Maintainer    |   4     |   3     |    4      |    4       | 3.75
Devil's Adv   |   4     |   5     |    3      |    4       | 4.0
```

Top picks: Architect (3 votes), Devil's Advocate (2 votes).
Bottom: Pragmatist (2 votes — "underweights long-term cost").

Severe disagreement: Architect vs Devil's Advocate are both highly scored but argue opposite conclusions.

## Stage 3 — skipped (standard tier)

Severe disagreement noted but `standard` doesn't trigger debate. (`deep` would.)

## Stage 4 — Chairman synthesis

You (main thread) synthesize:

```
## Recommendation

Split it — but stage the work, don't big-bang it. Write integration tests for the golden path first, extract `useSwarm.ts` as the first split, live with it for a week, then decide whether to go further.

## Why

- Tests first catch regressions during extraction.
- `useSwarm.ts` is the most contained slice, so it shows whether the seams are where you think before you commit to more.
- Every step is reversible, which beats both "split everything now" and "leave it alone".

## What to do

1. This week: write 2-3 integration tests covering mode switching and the swarm-orchestration golden path (~half a day).
2. Extract `useSwarm.ts`.
3. After a week of normal work, decide: extract `useChat.ts` and the mode handlers, or stop there.

## Risks of this plan

- Splitting because the file is big can create false abstractions that hurt more than they help.
- Skipping the tests turns the extraction into a regression hunt.
- Cost of being wrong: low — one extracted hook is a small revert.

## Strongest counter-position

"Not every big file needs splitting, and the 'split because it's big' reflex can introduce false abstractions that hurt more than they help." If the codebase feels noisier and harder to navigate after the first extraction, this file was cohesive: stop splitting, and trust that signal over the file-size number.

## Confidence

Medium that a staged split is right for this file — whether it needs splitting at all is genuinely contested. High that tests come first: nothing argued against it.
```

## What you'd send to user

The memo above, as is. Nothing about the council appears in it — no member names, scores or tier; the member answers, scores and position map go to the council record, and `--full` shows them.

## What was good about this run

- **Mandatory Devil's Advocate caught the over-splitting risk**. Without it, council probably converges on "split everything immediately" and user wastes 2 days on premature refactor.
- **Maintainer caught the "no tests" risk** that pure-architect persona missed.
- **Chairman didn't just pick highest-scoring member**. Synthesized a staged path that incorporates both sides' valid concerns.
- **Confidence is honest**: Medium on the contested call, high only where nothing argued against it.

## What could have failed

- If Architect had been the only "split" voice, council would've felt unanimous toward "leave it". DA being mandatory prevented that flatness.
- If all 5 personas were code-focused, none would've thought to suggest "write tests first" — that was Maintainer's contribution. Mixing persona types matters.
- If reviewers had scored persona reputation instead of reasoning quality ("the Architect is usually right"), peer review would've been corrupted by role bias — the rubric's per-axis justifications are the guard against that.
