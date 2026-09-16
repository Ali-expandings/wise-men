# Wise-men eval harness rules (post-salvage)

Every future batch MUST persist after each step. No context-only results.

## Persistence contract

For each question Q in batch:

1. **Arm A call** → immediately write `eval-data/raw/Q/arm_a.md`
   - Include header: `# model:`, `# salvaged_from_context:` (false for fresh runs), `# leakage_check:` (n/a for Arm A)
2. **Arm B call** → immediately write `eval-data/raw/Q/arm_b.md`
   - Check for STEP 1 leakage. If leaked outside `<thinking>`, retry once. Log retry in file header.
   - If retry still leaks, log failure and exclude that question's Arm B from aggregation
3. **Arm C** — for each subagent call (5 members, 5 reviewers, Chairman main-thread):
   - Append to `eval-data/raw/Q/arm_c_internals.md` with persona tag and result
   - After all members complete, run validator (5-section structure + non-empty per spec). Log validation result.
   - After all reviewers complete, parse rubric fenced blocks. Aggregate scores.
   - Write Chairman synthesis to `eval-data/raw/Q/arm_c.md`
4. **Blinding** → write `eval-data/blinded/Q.md` with all three responses labeled X/Y/Z per `blinding.yaml`
   - Strip `<thinking>` blocks, Arm B preambles, Arm C audit footers
   - Rename Arm C `## Council answer` → `## Answer`
   - Wrap Arm A plain prose under `## Answer` header
5. **Judge call** → write opus output to `eval-data/judgments/Q.md` immediately on return
6. **Parse scores** → extract fenced `scores` blocks → `eval-data/parsed/Q.yaml`
7. **Update progress.yaml** → mark question completed; update `eval-data/runs.yaml` with cost/latency

## Resume-safety

After each step, the run must be resumable from disk alone. If session hits limit mid-batch:
- All steps before the limit are persisted
- Steps after the limit are clearly missing on disk
- Continuation reads `progress.yaml` to know exactly what to resume

## Forbidden

- Skipping persistence "for speed"
- Storing partial results only in conversation context
- Modifying eval-spec.md after freeze (per spec § 11; only allowed for blocking-bug fix + rehash + restart)
- Modifying questions.yaml / pricing.yaml / judge-prompt.txt / blinding.yaml after freeze
- Modifying protocol files (`SKILL.md`, `resources/*`)
- Cherry-picking judge runs (rerun only if original failed; document rerun)

## Salvage protocol (when prior session left context-only data)

1. Stop and report what's missing on disk before doing anything
2. Get explicit user authorization for salvage path
3. Mark every salvaged file with `salvaged_from_context: true` in header
4. Note any reconstruction differences (e.g., subagent return strings vs main-thread re-transcription)
5. Only rerun fresh subagent calls for steps with no salvageable data
6. Document rerun explicitly (e.g., `rerun_judge: true`)

## File schema

```
eval-data/
  freeze.txt                   # spec hashes + freeze metadata
  questions.yaml               # frozen test set
  pricing.yaml                 # frozen pricing table
  judge-prompt.txt             # frozen judge prompt
  blinding.yaml                # sealed slot→arm map
  HARNESS.md                   # this file
  progress.yaml                # per-question status flags
  runs.yaml                    # per-question cost/latency + aggregate scores
  raw/
    Q<id>/
      arm_a.md
      arm_b.md
      arm_c.md                 # Chairman synthesis only
      arm_c_internals.md       # 5 members + 5 reviewers (future batches)
  blinded/
    Q<id>.md                   # X/Y/Z unlabeled responses + question
  judgments/
    Q<id>.md                   # full opus pairwise + absolute output
  parsed/
    Q<id>.yaml                 # extracted per-arm scores
```

## Pilot Q02/Q25/Q41 status

Pilot (3 questions, earlier in this conversation history) was never persisted. Lower priority than Q01/Q03/Q05 because pilot results documented in `progress.yaml` comments but raw responses live only in deep conversation history.

If pilot persistence becomes important: separate salvage pass needed. Otherwise treat pilot as informal harness-validation run; full statistical analysis uses Q01-onward freshly persisted data.
