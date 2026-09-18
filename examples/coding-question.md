# Example: coding question — "should I split App.tsx?"

An illustrative scenario, not a captured run: it shows what the council looks like for a typical engineering question. The members see only what the user wrote — no source file was supplied — so anything about the code beyond the user's words is marked unverified.

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
- Members: Pragmatist + Skeptic + Architect + Practitioner (a senior React engineer who maintains a large single-page app — the anchor, replacing the Maintainer seat it overlapped most) + Devil's Advocate (5).
- Model routing (per algorithm):
  - Pragmatist:        sonnet  (tier default)
  - Skeptic:           sonnet  (tier default)
  - Architect:         sonnet  (override: sonnet at standard+ ← matches default here)
  - Practitioner:      opus    (override: practitioner anchor +1 tier → opus)
  - Devil's Advocate:  opus    (override: DA always +1 tier → opus)
  - Reviewers × 3:     haiku   (tier default — rubric scoring is haiku-tolerant; floor is 3 at standard)
  - Debate:            n/a     (skipped at standard tier)
  - Synthesis checker: sonnet  (every council tier)
  - Chairman:          main thread
- Expected calls: 5 + 3 + 1 = 9.

## Stage 1 — 5 parallel Agent calls

Each persona answers independently. Example outputs (compressed for this doc):

**Pragmatist** (high confidence): "It works. 1179 lines is annoying but not broken. Splitting now without a concrete pain point = busywork. Wait until you actually feel friction adding a feature. Confidence: high. Weakest assumption: that the pain point will be obvious when it arrives."

**Skeptic** (medium confidence): "1179 lines with four responsibilities makes state mutations hard to trace. Whether tests exist wasn't said (unverified) — if they don't, the next feature add risks regressions nobody sees. Confidence: medium. Weakest assumption: that the file is actually as hard to navigate as line count implies — could be well-organized internally."

**Architect** (high confidence): "Single God Component is a recognized anti-pattern. Standard extraction: `useSwarm.ts`, `useChat.ts`, mode handler modules. Cost is ~1-2 days. Benefit: every future change becomes cheaper. Pay now, not later. Confidence: high. Weakest assumption: that future changes are coming — if project is stable and won't change much, the refactor is wasted."

**Practitioner** (medium confidence): "What I'd do Monday: check whether any tests cover mode switching and the swarm path (unverified — not stated); if not, write 2-3 integration tests first (~half a day); then extract the most self-contained slice, the swarm wiring, as one hook, and stop to see whether the seam was real. The question asks about the long term: whoever inherits this in six months needs seams, but a refactor without tests is how working apps break. Confidence: medium. Weakest assumption: that the swarm wiring really is the most separable part — I haven't seen the file."

**Devil's Advocate** (high confidence): "The case for not splitting: file size isn't the enemy. Premature abstraction is. Splitting into 5 files of 230 lines each adds import noise, navigation friction, and false boundaries that don't match the actual coupling. Some monoliths are fine. Vite recompiles fast either way. The 'split it because it's big' impulse is pattern-matching to JS culture, not first-principles thinking. Confidence: high. Weakest assumption: that the user is in the 'file is genuinely cohesive' camp rather than the 'file is a dumping ground' camp."

## Stage 2 — 3 parallel Agent calls (peer review, stable persona labels)

Each of the 3 reviewers Reads the grading packet with all 5 answers labeled by persona name (neutral grading frame). Rubric scoring. Example aggregated scores (means of 3):

```
              | Correct | Insight | Practical | Risk-aware | Avg
Pragmatist    |   4     |   3     |    4      |    3       | 3.5
Skeptic       |   4     |   3     |    3      |    5       | 3.75
Architect     |   5     |   4     |    4      |    4       | 4.25
Practitioner  |   4     |   3     |    5      |    4       | 4.0 
Devil's Adv   |   4     |   5     |    3      |    4       | 4.0
```

Top picks: Architect (2 of 3 reviewers), Devil's Advocate (1).
Bottom: Pragmatist (2 of 3 — "underweights long-term cost").

Severe disagreement: Architect vs Devil's Advocate are both highly scored but argue opposite conclusions.

## Stage 3 — skipped (standard tier)

Severe disagreement noted but `standard` doesn't trigger debate. (`deep` would.)

## Stage 4 — Chairman synthesis, then Stage 4.5

You (main thread) synthesize; one fresh checker then verifies the draft against the member answers (here: six PASS — the draft kept "whether tests exist" as an unknown instead of asserting it). The checked memo:

```
## Recommendation

Split it — but stage the work, don't big-bang it. Write integration tests for the golden path first, extract `useSwarm.ts` as the first split, live with it for a week, then decide whether to go further.

## Why

- Tests first catch regressions during extraction.
- `useSwarm.ts` is the most contained slice, so it shows whether the seams are where you think before you commit to more.
- Every step is reversible, which beats both "split everything now" and "leave it alone".

## What to do

1. This week: check what tests exist; if none cover mode switching and the swarm-orchestration golden path, write 2-3 integration tests for them (~half a day).
2. Extract `useSwarm.ts`.
3. After a week of normal work, decide: extract `useChat.ts` and the mode handlers, or stop there.

## Risks of this plan

- Splitting because the file is big can create false abstractions that hurt more than they help.
- Skipping the tests turns the extraction into a regression hunt.
- Cost of being wrong: low — one extracted hook is a small revert.

## Strongest counter-position

"Not every big file needs splitting, and the 'split because it's big' reflex can introduce false abstractions that hurt more than they help." If the codebase feels noisier and harder to navigate after the first extraction, this file was cohesive: stop splitting, and trust that signal over the file-size number.

## Confidence

Medium that a staged split is right for this file — whether it needs splitting at all is genuinely contested, and nobody here has seen the code. High that tests come before any extraction: the argument holds whichever way the split decision goes. Unknown: whether tests already exist.
```

## What you'd send to user

The memo above, as is. Nothing about the council appears in it — no member names, scores or tier; the member answers, scores and position map go to the council record, and `--full` shows them.

## What was good about this run

- **Mandatory Devil's Advocate caught the over-splitting risk**. Without it, council probably converges on "split everything immediately" and user wastes 2 days on premature refactor.
- **The practitioner anchor supplied the order of work** (check for tests, write them, extract one slice, stop) and kept "are there tests?" as a fact to check instead of assuming the answer from the line count.
- **Chairman didn't just pick highest-scoring member**. Synthesized a staged path that incorporates both sides' valid concerns.
- **Confidence is honest**: Medium on the contested call, high only where nothing argued against it.

## What could have failed

- If Architect had been the only "split" voice, council would've felt unanimous toward "leave it". DA being mandatory prevented that flatness.
- If all 5 personas were code-focused, none would've thought to suggest "write tests first" — that was the Practitioner's contribution. Mixing persona types matters.
- If reviewers had scored persona reputation instead of reasoning quality ("the Architect is usually right"), peer review would've been corrupted by role bias — the rubric's per-axis justifications are the guard against that.
