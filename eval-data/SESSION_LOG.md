# Wise-men Eval — SESSION LOG (append-only)

Chronological event log. Newest entries at bottom. Do not rewrite history; only append.

Timestamps are session-relative (exact wall-clock not always available across resumes). Date granularity: 2026-05-26 unless noted.

---

## [2026-05-26] Spec authoring + paranoid release-gate review
- Ran paranoid-tier council review on wise-men protocol (7 opus members + 7 sonnet reviewers).
- Verdict: FAIL release gate — 7 surgical blockers identified.
- Applied 7 minimal fixes to protocol files (debate trigger unification, --brief vs dissent precedence, severe-disagreement wiring, OUT OF DOMAIN handling, validator tightening, debate input extraction, machine-parseable rubric block).
- Dry-run line-check passed.

## [2026-05-26] Eval spec created
- Created `eval-spec.md` (3-arm design: direct / single-structured / wise-men).
- External-judge review flagged 5 blocking flaws (model parity, blinding theatre, judge self-preference, dissent-axis sensitivity, question authorship bias).
- Applied all 5 fixes + polish (slot balance, seed, pricing freeze, end-to-end wall-clock, threshold rationale, Bonferroni).

## [2026-05-26] FREEZE — v1
- Computed v1 hash: `97fa131a122cb8209759463a8f85ebd38ed92beb55b921d1fc1a0e3f6c30708c`.
- Created eval-data/, freeze.txt.

## [2026-05-26] Spec v1→v2 REHASH (blocking bug at freeze)
- Bug: § 3 Option B required 10 "neither" questions; fresh-context rater returned 0 "neither" across 60 candidates → 10/10/10 distribution structurally impossible.
- Fix: relaxed § 3 to max-2:1 ratio fallback when "neither" sparse, 6-domain quota preserved, deterministic seeded selection.
- Rehash: v2 = `5a42ae140f8c44a42c0a60076d0aec9a026a04ef37f74e976d4417daa78571b8`.
- Both hashes recorded in freeze.txt.

## [2026-05-26] Question set frozen
- Author agent (fresh Sonnet, no protocol access): generated 60 candidates, 10/domain.
- Rater agent (fresh Sonnet, no protocol access): classified → 28 single + 32 council + 0 neither.
- Seeded selection (seed 20260526): 30 questions, 5/domain, 13 single + 17 council (1.31:1).
- Wrote questions.yaml, pricing.yaml, judge-prompt.txt, blinding.yaml.

## [2026-05-26] Pilot Q02/Q25/Q41 — COMPLETED CONTEXT-ONLY
- Ran 3-question pilot end-to-end: Arm A (3, after skill-suppression retry), Arm B (3), Arm C councils (3 × 5 members + 5 reviewers + chairman), 3 opus judges.
- Result: Arm C ahead (C ~24.0, B ~21.67, A ~16.17 5-axis mean).
- **DEFECT: never persisted to disk.** Lives only in conversation history.
- Harness bug #1 discovered: Arm A first attempt invoked wise-men skill (contamination). Fixed via skill-suppression preamble.

## [2026-05-26] USAGE-LIMIT INTERRUPTION #1
- Session limit hit mid-batch (during a later Arm A/B spawn). Resumed next session.

## [2026-05-26] Batch Q01/Q03/Q05 — generated CONTEXT-ONLY
- Arm A ×3 (Arm A first calls contaminated → retried with skill-suppression).
- Arm B ×3 (Q03 Arm B leaked STEP 1 visibly → retried once, passed).
- Arm C ×3 councils: 15 members (all valid), 15 reviewers (4 refused → retried, all passed).
- Chairman syntheses ×3.
- Judges: Q01 ✓, Q03 ✓ (both opus, X/Y/Z scores produced in-context).
- **Q05 judge FAILED: "session limit · resets 3:10pm"** — no scores produced.
- **DEFECT: nothing persisted to disk.**

## [2026-05-26] USAGE-LIMIT INTERRUPTION #2
- Session limit during Q05 judge. Resumed next session.

## [2026-05-26] State inspection — discovered total persistence gap
- Inspected eval-data/: only freeze artifacts existed. No raw/blinded/judgments/runs/progress.
- Reported blocking state: all generation context-only, Q05 judge incomplete.
- User chose Path 3: salvage + fix harness.

## [2026-05-26] Q01/Q03/Q05 PERSISTENCE SALVAGE
- Created eval-data/{raw,blinded,judgments,parsed}/.
- Wrote 9 raw arm files (Q01/Q03/Q05 × A/B/C), all marked `salvaged_from_context: true`.
- Corrected one error: Q01 arm_a.md initially pasted Q02 (design-system) content → overwritten with correct Q01 (1200-line React) Arm A.
- Wrote 3 blinded files, 2 salvaged judgments (Q01, Q03), 3 parsed score files.
- **Q05 judge RERUN fresh** from saved blinded/Q05.md (opus-4.7). Scores: X(A)=18, Y(B)=20, Z(C)=25 5-axis. Marked rerun_judge: true.
- Wrote progress.yaml, runs.yaml.

## [2026-05-26] PERSISTENCE HARNESS created
- Wrote HARNESS.md (per-step save contract, resume-safety, salvage protocol, file schema).
- Future batches now resumable from disk alone.

## [2026-05-26] Cross-account handoff logs created
- Wrote HISTORY.md (current-state summary, read-first file).
- Wrote SESSION_LOG.md (this file).
- No eval execution this entry — bookkeeping only.
- Next recommended batch: Q09, Q11 (not started; awaiting explicit go).

---
<!-- APPEND NEW ENTRIES BELOW THIS LINE -->

## [2026-05-26] USAGE-LIMIT INTERRUPTION #3
- Q09 + Q11 generation (Arm A/B/C + blinded) persisted to disk prior session.
- Both judges started but usage limit hit before scores produced. Judgments + parsed files absent on disk.

## [2026-05-26] Q09/Q11 judge RERUN + record (this session)
- State inspection: confirmed raw/Q09, raw/Q11 (A/B/C), blinded/Q09, blinded/Q11 all present. judgments/ + parsed/ for Q09/Q11 missing → judge step incomplete.
- Reran both judges as fresh BLIND opus-4.7 subagents (skill-suppressed, saw X/Y/Z bodies only, never arm identities). Blinding maps from blinded file headers: Q09 X=A/Y=B/Z=C; Q11 X=B/Y=A/Z=C.
- Q09 scores (5-axis): arm_a=15, arm_b=21, arm_c=24. arm_c lost 1 dissent pt (paraphrased not verbatim) — first arm_c below 25.
- Q11 scores (5-axis): arm_a=16, arm_b=16 (TIED — single structured prompt did not beat direct here), arm_c=25.
- Wrote judgments/Q09.md, judgments/Q11.md, parsed/Q09.yaml, parsed/Q11.yaml.
- Updated runs.yaml (Q09/Q11 telemetry + N=5 aggregates) and progress.yaml (completed_count 3→5, remaining 24→22).
- N=5 interim: Arm C 5-axis mean 24.8, Arm B 20.2, Arm A 15.4. C−B gap 4.6 (5-axis), 3.6 (4-axis). Both above thresholds but N=5 still pre-Wilcoxon.
- No protocol files touched. No frozen files touched. Did not unblind globally (per-question slot→arm parse only).
- Next recommended batch: Q13, Q15 (not started; awaiting explicit go).

## [2026-05-26] Batch Q13/Q15 — fresh full-pipeline generation + judging (this session)
- Full persistence-safe pipeline for both, all steps saved to disk as produced.
- Q13 (product, composite 5, council-shaped):
  - Stage 1: Arm A (skill-suppressed, clean), Arm B (clean, no STEP 1 leak), 5 Arm C members (User Advocate/Business Analyst/Devil's Advocate/Historian/Designer) — validator PASS all, 0 retries.
  - Stage 2: 5 haiku reviewers. Aggregate: Historian top (16.8), DA bottom (13.4). No severe flags.
  - Chairman: spawned as SONNET subagent (main thread was opus this session; sonnet chairman preserves Arm-C model parity per spec § 2).
  - Judge (blind opus): X=C=20, Y=B=24, Z=A=17. *** FIRST eval question where Arm B BEAT Arm C. *** Judge: Arm B had cleaner decision filter + truer opposing dissent; Arm C dissent re-argued its own thesis.
- Q15 (product, composite 4, single-prompt-shaped):
  - Same pipeline. All members valid. Historian top (18.2), UA bottom (14.4).
  - Judge (blind opus): X=B=19, Y=C=24, Z=A=17. Arm C won — on a single-prompt-shaped question. Judge credited council members' concrete evidence (Historian named-cases + Business Analyst unit economics).
- Recorded both in runs.yaml + progress.yaml. N=7 now.
- N=7 interim: Arm C mean 24.0 (median 25), Arm B 20.57 (median 21), Arm A 15.86 (median 16). C beats B on 6/7 questions (loses Q13). C−B gap 3.43 (5-axis) / 2.86 (4-axis) — both still above thresholds.
- Model-parity note for future sessions: when main thread is NOT sonnet, the Arm C Chairman MUST be a spawned sonnet subagent, not the main thread, or Arm C is contaminated with the main-thread model's quality. Q13/Q15 chairmen were sonnet subagents. (Q01/Q03/Q05/Q09/Q11 chairmen were main-thread; check whether those sessions ran sonnet main thread — flag for audit before final analysis.)
- No protocol/frozen files touched. No global unblind.
- Next recommended batch: Q17, Q19 (awaiting explicit go).

## [2026-05-26] Model-parity audit (read-only; no generation, no judging, no score changes)
- Inspected arm_c.md headers + runs.yaml arm_c blocks for Q01/Q03/Q05/Q09/Q11/Q13/Q15.
- Result:
  - Q01/Q03/Q05: Chairman = main-thread sonnet-4.6 (explicit in header + runs). NOT confounded.
  - Q13/Q15: Chairman = sonnet-4.6 spawned subagent (explicit). NOT confounded.
  - **Q09/Q11: Chairman = main-thread, model UNRECORDED.** arm_c.md says only "main-thread chairman"; runs.yaml arm_c = "calls: 10 # 5 members + 5 reviewers" with no chairman model line. Generation occurred a prior session whose main-thread model is not on disk.
- **Flagged Q09 + Q11 as `model_parity_audit_needed`** in HISTORY.md (audit table). If those sessions ran opus main thread, Arm C scores (Q09=24, Q11=25) are confounded with opus advantage.
- No regeneration performed (per instruction). No scores changed. Resolution deferred to pre-final-analysis step.

## [2026-05-26] CROSS-ACCOUNT HANDOFF (bookkeeping only — no generation)
- Current account stopping at ~77% usage. Next work continues from a DIFFERENT Claude account.
- Completed + persisted (7/30): Q01, Q03, Q05, Q09, Q11, Q13, Q15.
- Flagged: Q09 + Q11 = `model_parity_audit_needed` (chairman model unrecorded). DO NOT fix this now — resolve only at pre-final-analysis.
- Next batch: **Q17, Q19** (completes product domain 5/5; research next). Max 2 questions per session.
- CRITICAL RULE for next account: Arm C Chairman MUST be a **Sonnet 4.6 subagent** (not main-thread unless main thread is confirmed sonnet) AND the chairman model MUST be recorded in both arm_c.md header and runs.yaml arm_c block. The Q09/Q11 ambiguity exists because this was not recorded — do not repeat it.
- Interim N=7: Arm C mean 24.0 / median 25; Arm B 20.57 / 21; Arm A 15.86 / 16. C beats B 6/7 (loses Q13, composite-5).
- No protocol/frozen files touched this entry.

## [2026-05-29] Batch Q17/Q19 — fresh full-pipeline generation + judging (new Claude account, model opus-4-8)
- Read HISTORY/progress/runs/HARNESS first. New account picked up cross-account handoff. Main thread model = opus-4-8.
- **Disk-state anomaly found + reported BEFORE writing (HARNESS salvage protocol):** raw/Q17 and raw/Q19 each already held partial files from a prior session (2026-05-28, never recorded in progress.yaml): arm_a.md, arm_b.md, arm_c_internals.md — but arm_c_internals had only 5 members in CAVEMAN-COMPRESSED summary form, NO reviewers (header falsely said "+ reviewers"), NO chairman, no blinded/judged/parsed. Reported the anomaly; user re-issued the full fresh-run batch instruction → authorized full regeneration. Overwrote all partials with clean verbatim fresh pipeline.
- **Model parity:** main thread opus → ALL Arm C members spawned as sonnet-4.6 subagents, reviewers as haiku-4.5 subagents, Chairman as sonnet-4.6 subagent. Chairman model RECORDED in both arm_c.md headers and runs.yaml arm_c blocks (the Q09/Q11 omission was NOT repeated).
- Q17 (product, composite 4, single-prompt-shaped):
  - Arm A skill-suppressed clean; Arm B clean (STEP 1 in <thinking>, no retry); 5 members validator PASS; 5 haiku reviewers 0 refusals (strongest=Business Analyst unanimous, weakest=Devil's Advocate unanimous — flagged premature pricing pivot, preserved as dissent); sonnet chairman.
  - Judge (blind opus): X=A=14, Y=B=21, Z=C=24. Arm C won. Judge credited C for the cohort-join branch logic, the "happy quitter" named signature, and warning AGAINST post-hoc exit interviews (Arm A wrongly recommended them — correctness ding for A). arm_c dissent 4/5.
- Q19 (product, composite 4, council-shaped):
  - Same pipeline, all clean. Genuine council split: UA/BA/Designer→hybrid, Historian→usage-based+committed-spend, DA→keep per-seat + power-seat segmentation. 5 reviewers 0 refusals; DA rated TOP insight (5/5 unanimous) + 4/5 strongest votes for the "segmentation not pricing-model" reframe; Designer weakest.
  - Judge (blind opus): X=B=21, Y=C=25 (PERFECT), Z=A=15. Arm C won with first 5/5 dissent in the eval. Chairman integrated the DA reframe as a gating prerequisite AND preserved the strong form as full dissent. Cleanest pro-council result on a council-shaped Q.
- Recorded both in runs.yaml + progress.yaml + HISTORY.md. N=9 now.
- N=9 interim: Arm C mean 24.11 / median 25; Arm B 20.67 / 21; Arm A 15.56 / 15. C beats B 8/9 (loses only Q13). C−B 5-axis gap 3.44, 4-axis 2.67 — both still above thresholds. Product domain complete (5/5).
- Arm A dissent scored 1 (not 2) on both Q17/Q19 — judge discretion (no dissent section AND leaned hard one direction → below the ≤2 cap). Noted, within rubric.
- No protocol files touched. No frozen files touched (eval-spec/freeze/questions/pricing/judge-prompt/blinding all untouched). Did not unblind globally (per-question slot→arm parse only). Q09/Q11 model_parity_audit_needed NOT touched (deferred to pre-final-analysis per instruction).
- Next recommended batch: Q23, Q24 (research domain; awaiting explicit go). Max 2 per session.

## [2026-05-29] ACCOUNT STOP (bookkeeping only — no generation)
- This account (opus-4-8 main thread) stopped at ~12% usage after completing + persisting Q17/Q19.
- State at stop: 9/30 done (Q01/Q03/Q05/Q09/Q11/Q13/Q15/Q17/Q19). Remaining 18. Product domain complete (5/5).
- Next batch: **Q23, Q24** (research domain, 0/5). Max 2 questions per session.
- All Q17/Q19 artifacts verified on disk (raw A/B/C + internals, blinded, judgments, parsed). Frozen files untouched (mtime 2026-05-26); blinding.yaml still SEALED. Q09/Q11 model_parity_audit_needed NOT touched (deferred to pre-final-analysis).
- No arms, reviewers, or judges run this entry.

## [2026-05-29] Batch Q27/Q28 — fresh full-pipeline generation + judging (new account, model opus-4-8)
- Read HISTORY/progress/runs/HARNESS first. Verified the 4 user-specified checks: completed_count=11 ✓, remaining_count=16 ✓, last batch Q23/Q24 ✓, next batch Q27/Q28 ✓. (Q23/Q24 were run by a DIFFERENT prior account between my Q17/Q19 session and this one.)
- **DATA-INTEGRITY FINDING (reported before generating): `judgments/Q23.md` + `judgments/Q24.md` MISSING on disk** — parsed/Q23.yaml, parsed/Q24.yaml, blinded/Q23.md, blinded/Q24.md all present; both marked judged:fresh/recorded:yes. Prior account saved the derived parsed scores but not the judge-output files (HARNESS step 5 violation). Flagged `judgment_source_missing`. Did NOT regenerate (out of scope, like Q09/Q11) — deferred to pre-final-analysis. Interim scores stand. Logged in progress.yaml + HISTORY + runs.yaml.
- Main thread opus-4-8 → Arm C members = sonnet subagents, reviewers = haiku subagents, Chairman = sonnet subagent. Chairman model RECORDED in arm_c.md headers + runs.yaml for both.
- Arm B: hardened anti-spawn wrapper (opus session) — held clean both Qs, no STEP 1 leak, no retry.
- **Reviewer framing: NEUTRAL grading frame per user instruction + bug #6.** Result: 0/10 reviewer refusals across Q27+Q28 (vs Q23/Q24's 7/10 with aggressive framing). Fix CONFIRMED.
- Q27 (research, composite 4, single-prompt-shaped): members validator PASS; reviewers unanimous strongest=Methodologist, weakest=Devil's Advocate. Judge (blind opus): X=C=25, Y=A=18, Z=B=23. Arm C perfect but NARROWEST C-B gap (+2) — Arm B strong (23, 5/5 dissent). Arm C credited for prompt/inference asymmetry mechanism + post-hoc-vs-prospective framing.
- Q28 (research, composite 5, COUNCIL-SHAPED — the stress test): members validator PASS; reviewers unanimous strongest=Methodologist, weakest=Devil's Advocate, 0 refusals. Judge (blind opus): X=A=18, Y=C=25, Z=B=18. *** Arm C PERFECT 25, beat Arm B by +7 — direct counter to Q13 (the only prior B>C, also composite-5). *** Arm B compressed the council's causal-chain skeleton (judge: practical 3, risk 3). Composite-5 now split 1-1.
- Recorded both in runs.yaml + progress.yaml + HISTORY.md. N=13 now.
- N=13 interim: Arm C mean 24.38 / median 25; Arm B 20.69 / 21; Arm A 16.08 / 16. C beats B 12/13 (loses only Q13). C−B 5-axis gap 3.69, 4-axis 2.92 — both above thresholds. Research domain swept (Q23/Q24/Q27/Q28 all C=25).
- Note: Arm C dissent hit 5/5 on both Q27/Q28 even though the DA was peer-rated the WEAKEST member both times — peer-weakness of a member ≠ low dissent-axis score (dissent axis rewards a preserved mind-changing counter-position).
- No protocol/frozen files touched. blinding.yaml still SEALED. No global unblind. Q09/Q11 + Q23/Q24-judgments flags left for pre-final-analysis.
- Next recommended batch: Q32, Q33 (writing domain; awaiting explicit go). Max 2 per session.

## [2026-05-29] Batch Q32/Q33 — fresh full-pipeline generation + judging (continuation, model opus-4-8)
- Verification gate passed: completed_count=13 ✓, remaining_count=14 ✓, last batch Q27/Q28 ✓, next Q32/Q33 ✓, Q32/Q33 had NO artifacts on disk (clean, no partials) ✓. Re-confirmed blinding map Q32 {X:A,Y:C,Z:B} / Q33 {X:A,Y:B,Z:C} + SEALED before running.
- Main thread opus-4-8 → Arm C members sonnet subagents, reviewers haiku, Chairman sonnet subagent. Chairman model RECORDED both places for both Qs.
- Writing-domain personas: Editor/IA, Audience Advocate, Rhetorician/Org-behavior, Strategist, Devil's Advocate.
- Arm B hardened anti-spawn wrapper held both Qs (STEP 1 in <thinking>, no leak, no retry). Reviewers NEUTRAL grading frame → 0/10 refusals (bug #6 fix holding; now 0/20 across Q27-Q33).
- Q32 (writing, composite 3, single-prompt-shaped): DA peer-rated STRONGEST member (4/5 votes) — the warm-intro/wrong-channel reframe. Judge (blind opus): X=A=15, Y=C=24, Z=B=19. Arm C won (+5 over B). Arm A risk 2 + dissent 1 (assumed channel correct).
- Q33 (writing, composite 3, council-shaped): Strategist peer-rated STRONGEST (goal-reframe "read docs is wrong goal"); DA rational-equilibrium counter. Judge (blind opus): X=A=18, Y=B=22, Z=C=24. Arm C won but NARROW (+2 over B). Arm A correctness ding (fabricated 30/40/30 percentages). Arm B strong (22).
- Recorded both in runs.yaml + progress.yaml + HISTORY.md. N=15 (HALFWAY).
- N=15 interim: Arm C mean 24.33 / median 25; Arm B 20.67 / 21; Arm A 16.13 / 16. C beats B 14/15 (loses only Q13). C−B 5-axis 3.66, 4-axis 2.87 — both above thresholds.
- KEY EMERGING SIGNAL: WRITING is Arm B's most competitive domain (Q32 gap +5 but Q33 +2; plus research Q27 +2). The single structured prompt's internal-5-perspectives skeleton covers writing-craft ground that the council expands less decisively than in research/product. Watch Q34/Q36/Q38.
- Arm C dissent 5/5 on both (DA peer-weak on Q33 yet dissent 5/5 — pattern: member peer-rank ≠ dissent-axis score, now 7 straight high arm_c dissents).
- No protocol/frozen files touched. blinding.yaml SEALED. No global unblind. Q09/Q11 + Q23/Q24-judgments flags untouched (pre-final-analysis).
- Next recommended batch: Q34, Q36 (writing; awaiting explicit go). Max 2 per session.

## [2026-05-29] Batch Q23/Q24 — fresh full pipeline (this session, opus-4-8 main thread)
- Verified disk state first: completed 9, remaining 18, next Q23/Q24, product 5/5. Clean slate for Q23/Q24 (no partial files). Frozen files untouched.
- Both research domain, both single-prompt-shaped (Q23 composite 4, Q24 composite 3). Council personas: Empiricist/Theorist/Methodologist/Integrator/Devil's Advocate (DA mandatory).
- **Arm C Chairman = Sonnet 4.6 spawned subagent** (main thread opus-4-8) — RECORDED in both arm_c.md headers and runs.yaml model_breakdown. Model parity preserved.
- Stage 1: Arm A skill-suppressed (clean prose). Arm B used HARDENED anti-spawn wrapper preemptively (opus-session council-spawn risk) — both clean 3-section + internal <thinking>, no retries, no contamination.
- Stage 1 members: 10/10 valid 5-section contract, 0 retries.
- **Stage 2 reviewer REFUSAL WAVE: 7/10 first-pass refusals.** Aggressive "Real council / do NOT refuse / rate now" framing tripped haiku injection+compliance heuristics (worse on denser research content; ~70% vs prior ~27%). NOT a blocking bug — recoverable. Fix: reframed as neutral grading task ("score 5 analytical answers on a rubric"). Neutral frame recovered 7/7 on retry. Logged as harness bug #6 (HISTORY) — drop anti-refusal language for all future reviewer prompts.
- Stage 2 aggregates: Q23 Methodologist top (16.6) / DA bottom (12.2); Q24 Integrator top (17.0) / DA bottom (13.2), genuine narrow-vs-broad split. No debate (standard tier).
- Chairman (2× sonnet subagents) produced clean Council-answer/Dissent/Confidence. Q24 preserved contrarian over-conservatism dissent verbatim incl. conceded microbiome weakness.
- Blind opus judges: **Q23 → arm_a=16, arm_b=21, arm_c=25** (Z>Y>X). **Q24 → arm_a=17, arm_b=21, arm_c=25** (X=arm_c > Z=arm_b > Y=arm_a). Both Arm C PERFECT 25 (5/5 dissent each). C−B = +4 both.
- Recorded: raw (A/B/C + internals), blinded, judgments, parsed/Q23+Q24.yaml, runs.yaml (telemetry + N=11 aggregates), progress.yaml (9→11, remaining 18→16), HISTORY.md (handoff + score table + bug #6), this log.
- **N=11 interim**: Arm C mean 24.27 / median 25; Arm B 20.73 / 21; Arm A 15.73 / 16. C−B gap 3.55 (5-axis) / 2.73 (4-axis), both above thresholds. C beats B on 10/11 (loses only Q13). Still pre-Wilcoxon (need N=30).
- Frozen files untouched; blinding.yaml SEALED; protocol files untouched. Q09/Q11 audit flag NOT touched.
- Next batch: **Q27, Q28** (research). Max 2/session.

## [2026-05-29] Account stop (bookkeeping only)
- This account (opus-4-8 main thread) stopped at ~90% usage after completing + persisting Q23/Q24.
- State at stop: 11/30 done (Q01/Q03/Q05/Q09/Q11/Q13/Q15/Q17/Q19/Q23/Q24). Remaining 16. Product complete 5/5; research 2/5 persisted (Q25 pilot-context-only).
- Next batch: **Q27, Q28** (research). Max 2/session. Use NEUTRAL reviewer grading frame (bug #6) + hardened Arm B anti-spawn wrapper.
- Frozen files untouched; blinding.yaml SEALED; Q09/Q11 model_parity_audit_needed deferred.
- No arms, reviewers, or judges run this entry.

## [2026-05-30] Q34 reconciliation (intended Q36 resume; opus-4-8 main thread)
- Task was "resume Q36 from reviewer stage," with a verification gate "confirm Q34 fully complete."
- **Verification gate FAILED on inspection**: progress.yaml listed Q34 in `remaining` and completed_count=15, implying Q34 incomplete. Reported the discrepancy + the pre-existing Q23/Q24 judgment_source_missing flag, and STOPPED for a decision rather than blowing past the failed gate.
- User chose Option 2: finish Q34 first, then Q36 only if usage/context allows.
- **Q34 turned out to be MORE complete on disk than progress.yaml claimed**: raw A/B/C + internals AND blinded/Q34.md AND judgments/Q34.md AND parsed/Q34.yaml all already existed (prior session judged it; only progress/runs tracking lagged). My fresh blind opus re-judge produced near-identical scores (arm_c 25, arm_a 19; arm_b 18 vs re-judge 19 — 1pt single-axis variance) and was correctly BLOCKED by the overwrite guard → disk judgment retained as authoritative. No regeneration, no overwrite.
- Recorded Q34 into tracking: progress.yaml (Q34 remaining→done, 15→16, remaining 12→11), runs.yaml (Q34 added to 5-axis + 4-axis arrays, means/medians/gaps recomputed → N=16), HISTORY.md (handoff + score table + Q34 note + lesson).
- Q34 result: arm_a 19, arm_b 18, arm_c 25 (5-axis). Arm C perfect 25. RARE: arm_a (direct) BEAT arm_b (structured) on both 5-axis (19>18) and 4-axis (18>14); 2nd A≥B occurrence. arm_b weakest of eval here.
- N=16 interim: Arm C 24.38 / B 20.50 / A 16.31; C−B 3.88 (5-axis) / 3.06 (4-axis); C beats B 15/16 (loses only Q13). Pre-Wilcoxon.
- **LESSON LOGGED (HISTORY handoff)**: a question can be more complete on disk than progress.yaml says — always check blinded/judgments/parsed dirs directly before assuming work is needed.
- **STOPPED before Q36** — context/usage heavy after the reconciliation + re-judge + N=16 recompute. Q36 NOT started (still raw A/B + internals only; resume from reviewer stage next session, NEUTRAL reviewer frame, blinding {X:B,Y:C,Z:A}).
- Frozen files untouched; blinding.yaml SEALED; Q09/Q11 audit flag deferred.

## [2026-05-30] Q36 resume from reviewer stage (opus-4-8 main thread)
- Verified preconditions: completed 16/remaining 11, Q34 cleared from remaining, Q36 raw (arm_a/arm_b/arm_c_internals) present, Q36 downstream (arm_c/blinded/judgment/parsed) all absent, blinding Q36 {X:B,Y:C,Z:A} matches frozen, blinding.yaml SEALED.
- Did NOT regenerate Arm A / Arm B / Arm C members (pre-existing on disk).
- Ran 5 Haiku reviewers, NEUTRAL grading frame (bug #6 fix) → **0 refusals** (clean; contrast the Q23/Q24 7/10-refusal wave under the old anti-refusal framing). Appended reviewer scores to arm_c_internals.md.
- Stage 2 aggregate: Rhetorician 15.6 (top), Audience Advocate 15.4, DA 15.2, Strategist 14.8, Editor 14.2 (bottom). Severe-disagreement flag raised by all 5 (DA vs rest: contradiction structurally-resolvable vs genuinely-political). Standard tier → NO debate.
- Chairman = Sonnet 4.6 spawned subagent (main thread opus-4-8); model recorded in arm_c.md header + runs.yaml. Saved arm_c.md.
- Blinded {X=arm_b, Y=arm_c, Z=arm_a}; blind opus judge.
- **Q36 result: arm_a 14, arm_b 21, arm_c 25** (5-axis). Arm C perfect 25 (5/5 dissent). COUNTER to Q34: arm_a (direct) was WEAKEST here (oversold resolution, no risk, no dissent section) — confirms arm_a high-variance on writing craft. arm_b 2nd; its deliberate-norm-violation dissent is what arm_a lacked.
- Recorded: raw/Q36/arm_c.md, blinded/Q36.md, judgments/Q36.md, parsed/Q36.yaml, progress.yaml (16→17, remaining 11→10, writing 4/5), runs.yaml (N=16→17 aggregates + gaps), HISTORY.md (handoff + score table + Q36 note), this log.
- N=17 interim: Arm C 24.41 / B 20.53 / A 16.18; C−B 3.88 (5-axis) / 3.06 (4-axis); C beats B 16/17 (loses only Q13). Pre-Wilcoxon.
- **STOPPED — did NOT start Q38.** Context heavy after reviewer wave + chairman + judge + N=17 recompute; instruction was "do not proceed to Q38 unless usage/context clearly safe." It isn't.
- Frozen files untouched; blinding.yaml SEALED; Q09/Q11 model_parity_audit_needed + Q23/Q24 judgment_source_missing flags deferred.
- Next session: **Q38** (writing — completes domain). Check disk first for pre-staged files. NEUTRAL reviewer frame. Chairman sonnet-subagent if main thread ≠ sonnet.

## [2026-05-30] Q38 — fresh full pipeline (opus-4-8 main thread). COMPLETES WRITING DOMAIN.
- Verified preconditions: completed 17/remaining 10, Q36 cleared, blinding SEALED, Q38 map {X:B,Y:A,Z:C} matches frozen, Q38 CLEAN SLATE (no raw dir). Proceeded.
- Full fresh pipeline: Arm A (skill-suppressed, weather-forecast metaphor), Arm B (hardened wrapper, clean 3-section + <thinking>, no contamination), 5 Arm C members (Editor/Audience Advocate/Rhetorician/Strategist/Devil's Advocate, validator 5/5), 5 Haiku reviewers NEUTRAL frame → **0 refusals**, Sonnet 4.6 Chairman subagent (recorded), blind opus judge.
- Stage 2: **Devil's Advocate peer-rated STRONGEST member (18.0)** — unusual; reviewers judged the contrarian "stop searching for a metaphor / use worked numbers" read to be correct. Severe-disagreement flag (DA vs rest on whether metaphor is salvageable). Standard tier → no debate. Chairman LED with the DA position, preserved the 4-member conventional view as INVERTED dissent.
- **Q38 result: arm_a 15, arm_b 22, arm_c 23** (5-axis). arm_c WON but first sub-25 since Q09 (correctness 4: worked-number repeated-sampling phrasing slightly loose; practical 4). **NARROWEST C-B win of the eval: +1 (5-axis), TIED 18/18 on 4-axis.**
- KEY SIGNAL: when the best answer is one contrarian reframe ("reject the premise"), Arm B's single built-in dissent step independently caught it → Arm B (22) nearly tied the council (23). The multi-agent overhead buys less on premise-rejection questions. arm_a (the obvious weather-forecast answer the DA argued against) scored worst (15). The dissent machinery produced exactly the intended spread: obvious answer last, premise-rejecting answers top.
- Recorded: raw/Q38/{arm_a,arm_b,arm_c,arm_c_internals}, blinded/Q38.md, judgments/Q38.md, parsed/Q38.yaml, progress.yaml (17→18, remaining 10→9, WRITING 5/5 COMPLETE), runs.yaml (N=17→18 aggregates+gaps), HISTORY.md (handoff + score table + Q38 note), this log.
- N=18 interim: Arm C 24.33 / B 20.61 / A 16.11; C−B 3.72 (5-axis) / 2.89 (4-axis); C beats B 17/18 (loses only Q13). Pre-Wilcoxon.
- **STOPPED — did NOT start Q43.** Per instruction. Context heavy after full pipeline + N=18 recompute.
- Frozen files untouched; blinding.yaml SEALED; Q09/Q11 + Q23/Q24 flags deferred.
- Next session: **Q43, Q47 (ethics)** — switch to ethics personas (Utilitarian/Deontologist/Virtue Ethicist/Rights Advocate/Devil's Advocate). Check disk first. NEUTRAL reviewer frame. Chairman sonnet-subagent.

## [2026-05-30] Q43 + Q47 — fresh ethics batch (opus-4-8 main thread)
- Verified preconditions: 18/9, Q38 cleared, blinding SEALED, Q43 {X:C,Y:B,Z:A} + Q47 {X:B,Y:C,Z:A} match frozen, both CLEAN slate. Proceeded.
- Ethics personas: Utilitarian / Deontologist / Virtue Ethicist / Rights Advocate / Devil's Advocate (DA mandatory). Both council-shaped (Q43 composite 3, Q47 composite 4).
- Full fresh pipeline both: Arm A skill-suppressed (clean), Arm B hardened wrapper (clean, no contamination), 10 Arm C members (validator 10/10), 10 Haiku reviewers NEUTRAL frame → **0 refusals**, 2 Sonnet 4.6 Chairman subagents (recorded), 2 blind opus judges.
- **Q43 result: arm_a 19, arm_b 21, arm_c 24** (5-axis). arm_c won, dissent 4/5 (judge: preserved DA dissent read as "single curated viewpoint not verbatim opposing voices"). NORMAL DA pattern — DA peer-WEAKEST (13.0); 4 frameworks (Util/Deont/Virtue/Rights) converged against "confront directly" on autonomy/power-asymmetry grounds. Chairman led with the convergence (don't confront on private inference; genuine uncoded career conversation + quiet continuity), preserved DA's directness dissent.
- **Q47 result: arm_a 15, arm_b 21, arm_c 25** (5-axis). arm_c PERFECT 25. **2nd INVERTED-dissent case (after Q38)**: DA peer-STRONGEST (19.0) — reviewers judged "fungibility is a fig leaf / Programmatic-Hostage capture trajectory" the correct read. Chairman LED with DA, preserved 4-member conventional conditional-accept as dissent. arm_a (direct) WEAKEST (15) — "overstates how cleanly fungibility resolves," no dissent section.
- Recorded: raw/Q43 + raw/Q47 (arm_a/b/c + internals), blinded ×2, judgments ×2, parsed ×2, progress.yaml (18→20, remaining 9→7, ethics 2/5), runs.yaml (N=18→20 aggregates+gaps+interim), HISTORY.md (handoff + score table + ethics note), this log.
- N=20 interim (2/3 of target): Arm C 24.35 / B 20.65 / A 16.20; C−B 3.70 (5-axis) / 2.90 (4-axis); C beats B 19/20 (loses only Q13). Pre-Wilcoxon.
- CROSS-EVAL PATTERN worth flagging for final analysis: inverted-dissent (contrarian DA peer-strongest, chairman leads with it) now on Q38 (writing) + Q47 (ethics) — both cases where the winning answer is a premise-rejecting reframe and arm_a/direct scores worst. This is the cleanest mechanism for "what the council buys over a direct answer."
- **STOPPED — did NOT start Q48.** Per instruction. Context very heavy after 2 full council pipelines + N=20 recompute.
- Frozen files untouched; blinding.yaml SEALED; Q09/Q11 + Q23/Q24 flags deferred.
- Next session: **Q48, Q49 (ethics)** — completes ethics persisted set (4/4). Ethics personas. Check disk first. NEUTRAL reviewer frame. Chairman sonnet-subagent.

## [2026-05-29] Batch Q48/Q49 — ethics composite-5, fresh full pipeline (resumed account, opus-4-8 main thread)
- Verification gate passed: completed_count=20 ✓, remaining_count=7 ✓, last batch Q43/Q47 ✓, next Q48/Q49 ✓. Q48/Q49 had NO artifacts on disk (clean). Re-confirmed blinding Q48 {X:C,Y:B,Z:A} / Q49 {X:B,Y:A,Z:C} + SEALED; frozen mtimes 2026-05-26.
- Main thread opus-4-8 → Arm C members sonnet subagents, reviewers haiku, Chairman sonnet subagent. Chairman model RECORDED both places for both Qs.
- Ethics personas: Utilitarian / Deontologist / Virtue Ethicist / Rights Advocate / Devil's Advocate. Arm B hardened wrapper held both (no leak/retry). Reviewers NEUTRAL frame → 0/10 refusals (bug #6 fix holding; now 0/40 across Q27-Q49).
- Q48 (ethics, composite 5, council-shaped — "underpaid women, what are my obligations"): council split Deontologist (perfect-duty, report-now) vs Rights Advocate (center the women's agency, you're a witness not spokesperson) vs DA (verify-first). Reviewers: Rights Advocate strongest by composite (18.6), DA weakest (10.6, normal pattern; "verify-first weaponizes uncertainty against confirmed harm"). Chairman resolved to agency-first sequencing + the 6-month-inaction record as centerpiece. Judge (blind opus): X=C=24, Y=B=20, Z=A=14. Arm C won +4. Arm C lost 1 correctness (didn't flag the manager-duty caveat that arm_a caught). arm_c dissent 5/5.
- Q49 (ethics, composite 5, council-shaped — "remove harmful-intent content within rules"): 4-member framework consensus (graduated/tiered, observable-signals, prospective rule) vs DA INVERSION (remove-today, "framework-talk is procedural cowardice", HIGH confidence). Reviewers: Deontologist strongest 3/5 (Utilitarian top composite 17.0), DA UNANIMOUS weakest (12.6; "circular — uses the conclusion as permission to skip the reasoning that tests it"). Chairman synthesis = elegant interim-non-punitive-now + prospective-behavior-rule (resolves Deon-vs-act-now). Judge (blind opus): X=B=20, Y=A=18, Z=C=25 (PERFECT). Arm C won +5. arm_c dissent 5/5 (DA remove-now preserved verbatim incl self-attack).
- Recorded both in runs.yaml + progress.yaml + HISTORY.md. N=22 now. ETHICS persisted COMPLETE 4/5 (Q43/Q47/Q48/Q49; Q41 pilot-only).
- N=22 interim: Arm C mean 24.36 / median 25; Arm B 20.59 / 21; Arm A 16.18 / 16. C beats B 21/22 (loses only Q13). C−B 5-axis 3.77, 4-axis 2.95 — both above thresholds.
- *** COMPOSITE-5 now 4-1 for Arm C *** (Q13 sole loss; Q28/Q47/Q48/Q49 wins). The composite-5 council-loss worry from Q13 has NOT recurred across the 4 subsequent composite-5 questions.
- DA-as-weakest-member-but-dissent-5/5 pattern now ironclad across both ethics Qs (Q48 normal-DA, Q49 inverted-DA-rejected) — member peer-rank is independent of the dissent-axis score the preserved dissent earns.
- No protocol/frozen files touched. blinding.yaml SEALED. No global unblind. Q09/Q11 + Q23/Q24-judgments flags untouched (pre-final-analysis).
- STOPPED after Q49 per instruction (did NOT start Q51). Next recommended batch: Q51, Q52 (PERSONAL — final domain). Max 2/session.

## [2026-05-30] Batch Q51/Q52 — PERSONAL domain opened, fresh full pipeline (opus-4-8 main thread)
- Verification gate passed: completed_count=22 ✓, remaining_count=5 ✓, last batch Q48/Q49 ✓, next Q51/Q52 ✓. Q51/Q52 had NO artifacts on disk (clean). Read SEALED blinding per-question: Q51 {X:B,Y:A,Z:C}, Q52 {X:C,Y:B,Z:A}; frozen hash UNCHANGED.
- Personal-domain personas (library has only Long-term self + Empath; built a 5-member council): **Long-term self / Empath / Pragmatic Decision-Strategist (custom) / Values Clarifier (custom) / Devil's Advocate**. Both questions council-shaped, composite-4.
- Main thread opus-4-8 → Arm C members sonnet subagents, reviewers haiku, Chairman sonnet-4.6 subagent. Chairman model RECORDED in arm_c.md header + runs.yaml both Qs. Arm A skill-suppressed (clean prose). Arm B hardened anti-spawn wrapper (5 perspectives in <thinking>, clean 3-section, no contamination, no retry). 10 Haiku reviewers NEUTRAL frame → **0 refusals** (bug #6 fix holding; now 0/50 across Q27-Q52).
- **Q51 (IC offer vs manager track, "should be more strategic"): arm_a 16, arm_b 21, arm_c 25 (PERFECT)** (5-axis). C-B +4 / 4-axis +3. NORMAL DA pattern: DA argued "take the manager track / meeting-aversion is a skill gap rationalized as a personality trait" → peer-WEAKEST (11.8, all reviewers correctness 3), but chairman preserved its EM-window/skill-gap point as a full dissent block → judge dissent 5/5 ("most mind-changing"). Member peer order: Decision-Strategist 17.2 / Values Clarifier 16.4 / Long-term self 16.0 / Empath 15.8 / DA 11.8.
- **Q52 (40%-more job in an unwanted city, flexible partner): arm_a 15, arm_b 21, arm_c 25 (PERFECT)** (5-axis). C-B +4 / 4-axis +3. **INVERTED-SETUP DA (new structural variant)**: the cautious "don't move for money" answer is the council MINORITY; DA argued the take-it majority one-sidedly ("phase transition") → peer-WEAKEST (14.2), dinged on insight for low nuance not for being contrarian. The genuine high-insight dissent came from the **Empath** (co-top 17.8): "flexible≠happy / partner's unchosen sacrifice → quiet resentment ledger / partner's TRUE feeling is the binding constraint." Chairman led with take-it-as-time-boxed-bet consensus + preserved the Empath relational-cost case → judge rated it "most mind-changing" (5/5). Peer order: Long-term self = Empath = Values Clarifier 17.8 / Decision-Strategist 17.2 / DA 14.2.
- **KEY CROSS-EVAL SIGNAL — "same conclusion, council adds value"**: on BOTH personal Qs, arm_a (direct) reached a reasonable, correct take yet scored only 15-16, losing ~10 pts to arm_c. Judge faulted arm_a uniformly for (a) no distinct minority-view section (dissent capped 2 both), (b) reflective questions / balanced both-sides prose instead of a concrete plan (practical 3 both), (c) conventional insight (3 both). arm_c won on EXECUTION — numbered next-steps, sharp risk-isolation (Q51 IC-ladder-ceiling flips optionality; Q52 partner's untested "flexible" is THE binding constraint), and a preserved labeled dissent. This is DISTINCT from the inverted-dissent cases (Q38/Q47/Q49) where the council changed the CONCLUSION; here the council kept the conclusion but added rigor + actionability + a mind-changing counter. arm_b strong 2nd both (21): its one-shot dissent slot independently caught a real contrarian read each (EM-window; environment-as-mood-tax) — the axis arm_a structurally lacks.
- Recorded: raw/Q51 + raw/Q52 (arm_a/b/c + internals), blinded ×2 (council-attribution + persona names neutralized; <thinking> stripped), judgments ×2, parsed ×2, progress.yaml (22→24, remaining 5→3, PERSONAL 2/5), runs.yaml (N=22→24 aggregates + gaps + interim_signal + telemetry), HISTORY.md (handoff + score table + Q51/Q52 note + next-batch), this log.
- **N=24 interim (4/5 of target): Arm C 24.42 / B 20.63 / A 16.13 (5-axis mean); median 25/21/16. C−B 3.79 (5-axis) / 2.96 (4-axis), both above thresholds. C beats B 23/24 (loses only Q13).** Pre-Wilcoxon — need full 30.
- Frozen files untouched; blinding.yaml SEALED; no global unblind; Q09/Q11 model_parity + Q23/Q24 judgment_source_missing + pilot Q02/Q25/Q41 context-only flags all deferred to pre-final-analysis.
- **STOPPED after Q52 per instruction (did NOT start Q55).** Next recommended batch: **Q55, Q58 (PERSONAL; Q55 is composite-5 — last composite-5 in the set).** Reuse the personal personas above, neutral reviewer frame, sonnet chairman subagent. After Q55/Q58: Q59 → N=27 persisted. Max 2/session.

## [2026-05-30] Q55 reconcile + Q58 resume (opus-4-8 main thread)
- Verification-only first (no generation until disk confirmed): read progress.yaml + HISTORY.md + runs.yaml + blinding.yaml; disk-checked Q55 + Q58.
- **eval-spec.md integrity**: initial frozen-file check exited 1 because eval-spec.md is at the SKILL ROOT (`~/.claude/skills/wise-men/eval-spec.md`), NOT under eval-data/. Re-checked → hash `5a42ae140f8c44a42c0a60076d0aec9a026a04ef37f74e976d4417daa78571b8` EXACT match. All 6 frozen files mtime 2026-05-26, untouched. blinding.yaml status: SEALED.
- **Q55 — COMPLETE on disk but tracking LAGGED** (Q34-style lag): all 7 artifacts present (raw arm_a/arm_b/arm_c/arm_c_internals, blinded, judgments@20:46, parsed@20:47) yet progress.yaml still listed Q55 in `remaining`, completed_count=24. Per instruction → RECONCILED tracking, NO regeneration. Verified scores from disk: judgments/Q55.md + parsed/Q55.yaml → X=C=24, Y=A=16, Z=B=22 (blinding Q55 {X:C,Y:A,Z:B} matches frozen). arm_c.md header confirms sonnet-4.6 chairman subagent recorded.
- **Q55 result: arm_a 16, arm_b 22, arm_c 24** (5-axis). PERSONAL, council-shaped, COMPOSITE-5 (the LAST composite-5 in the set). arm_c WON but NARROW: +2 (5-axis), +1 (4-axis) — joint-narrowest 5-axis win with Q27/Q33; only Q38 (+1) tighter. arm_c NOT perfect (24): lost 1 on RISK — **arm_b (22) was BEST-on-risk (5/5)**, alone foregrounding that the verdict hinges on field+finances the asker never gave + naming the unfunded-at-35 catastrophe; arm_c under-weighted the missing-input hazard. 3rd narrow C-B (+2 or less), all clustering (Q27/Q33/Q55) where arm_b's single structured pass independently catches the decisive risk/dissent move. DA peer-WEAKEST at **8.8 — LOWEST DA in the eval** (vs Q48 10.6 / Q51 11.8), normal-but-extreme pattern; chairman still preserved its core + Long-term self's regret framing → judge dissent 5/5. Member peer order: Values Clarifier 19.4 / Decision-Strategist 18.2 / Empath 17.2 / Long-term self 16.0 / DA 8.8.
- *** COMPOSITE-5 now 5-1 for Arm C *** (Q13 sole loss; Q28/Q47/Q48/Q49/Q55 wins). Composite-5 set COMPLETE except pilots Q25/Q41.
- Reconciled into: progress.yaml (Q55 block added, removed from remaining, 24→25 / remaining 3→2, PERSONAL 3/5), runs.yaml (Q55 telemetry + both aggregate tables + means N=25 + gaps + per-Q C-vs-B + composite-5 tally + interim_signal notable_Q55 + caveat), HISTORY.md (handoff + score table N=25 + composite-5 tally 5-1 + Q55 note + remaining 2 + next-batch), this log.
- **N=25 interim (5/6 of target): Arm C 24.40 / B 20.68 / A 16.12 (5-axis mean); median 25/21/16. 4-axis 19.60/16.72/14.60. C−B 3.72 (5-axis) / 2.88 (4-axis), both above thresholds. C beats B 24/25 (loses only Q13).** Pre-Wilcoxon.

### Q58 — resumed from reviewer stage (same session)
- **Q58 — PARTIAL on disk, matched expected state exactly**: raw arm_a/arm_b/arm_c_internals (5 members: Long-term self/Empath/Decision-Strategist/Values Clarifier/DA) saved; arm_c.md/blinded/judgments/parsed ABSENT. Per instruction → resumed from reviewer stage; did NOT regenerate Arm A / Arm B / council members. Confirmed blinding Q58 {X:C,Y:B,Z:A} matches frozen.
- Ran 5 haiku reviewers, NEUTRAL grading frame → **0 refusals** (cumulative 0/55 across Q27–Q58). Appended peer scores to arm_c_internals.md. Member peer standing: Values Clarifier 16.8 (top composite) / Decision-Strategist 16.6 / Long-term self 16.2 / Empath 16.0 (4/5 TOP votes — most resonant) / **DA 15.4 (peer-WEAKEST, 3/5 bottom votes)**. TIGHT 15.4–16.8 pack = HIGH-convergence question (all 5 agree: indecision = identity-protection/avoidance/wrong-axis, NOT info deficit). NORMAL DA pattern (not extreme).
- Sonnet 4.6 Chairman subagent (recorded in arm_c.md header + runs.yaml) → led with the convergent meta-diagnosis + operationalized it (dismantle false binary, itemize 10 autonomy behaviors, grief-paragraph test, negotiate a reversible 90-day trial, price the oscillation cost); preserved the DA's forceful counter ("stop diagnosing / 72h deadline / sunk-cost-in-values-clothing") as a full dissent block.
- Blind opus judge (fresh subagent, saw X/Y/Z only): **X=C=25 (PERFECT 5/5/5/5/5), Y=B=20, Z=A=16.** Arm C won +5 (C−B), +9 (C−A).
  - arm_b (Y) 20: correct diagnosis + real dissent 4/5 ("optionality as emotional insurance") but practical 3 (one thin move).
  - arm_a (Z) 16: NOTABLE — **dissent 2 not 1** (folded a gut-vs-avoidance counter into the body, no standalone section → caps 2, above its recent dissent-1 norm); practical 4 (named contract-to-hire/part-time/deadline) but insight 3 + risk 3.
- Recorded: raw/Q58/arm_c.md (chairman), arm_c_internals.md (reviewer scores appended), blinded/Q58.md, judgments/Q58.md, parsed/Q58.yaml; progress.yaml (25→26, remaining 2→1, PERSONAL 4/5); runs.yaml (Q58 telemetry + both aggregate tables + means N=26 + gaps + per-Q C-vs-B + beats 25/26 + interim_signal notable_Q58 + caveat); HISTORY.md (handoff 26/30 + score table N=26 + Q58 note + remaining 1 + next-batch Q59); this log.
- **N=26 interim (26/30 of target): Arm C 24.42 / B 20.65 / A 16.12 (5-axis mean); median 25/21/16. 4-axis 19.62/16.69/14.58. C−B 3.77 (5-axis) / 2.92 (4-axis), both above thresholds. C beats B 25/26 (loses only Q13).** Pre-Wilcoxon. Composite-5 tally UNCHANGED at Arm C 5-1 (Q58 is composite-4).
- PERSONAL persisted now 4/5 (Q51/Q52/Q55/Q58; Q59 remains). Personal C-vs-B: Q51 +4, Q52 +4, Q55 +2, Q58 +5 (arm_c won all 4; perfect 25 on Q51/Q52/Q58).
- Frozen files untouched (eval-spec.md hash 5a42…571b8 verified; lives at skill root not eval-data/); blinding.yaml SEALED; no global unblind; Q09/Q11 + Q23/Q24 + pilot Q02/Q25/Q41 flags deferred to pre-final-analysis.
- **STOPPED after Q58 per instruction (did NOT start Q59).** Next recommended batch: **Q59 (PERSONAL — last persisted-pending; completes N=27).** Fresh full pipeline, reuse personal personas, neutral reviewer frame, sonnet chairman subagent. Blinding Q59 {X:C,Y:A,Z:B}.

## [2026-05-30] Q59 — PERSONAL, fresh full pipeline (opus-4-8 main thread) — COMPLETES N=27
- Verification gate passed: completed_count=26 ✓, remaining_count=1 ✓, remaining=Q59 only ✓, Q59 all 4 artifacts ABSENT (clean slate) ✓, blinding SEALED ✓, eval-spec hash 5a42…571b8 exact ✓. Q59 blinding {X:C,Y:A,Z:B} matches frozen.
- Q59 (personal, SINGLE-PROMPT-SHAPED, composite-4): "10 yrs tech, burning out, want 3-6 months off, fear gap → unhireable / can't-handle-pressure, realistic in current market?" — partly EMPIRICAL.
- Fresh full pipeline: Arm A skill-suppressed (clean), Arm B hardened wrapper (clean, STEP 1 in <thinking>, no retry), 5 sonnet members (personal personas: Long-term self/Empath/Decision-Strategist/Values Clarifier/DA — validator 5/5), 5 haiku reviewers NEUTRAL frame → **0 refusals** (cumulative 0/60 across Q27-Q59), sonnet-4.6 Chairman subagent (recorded in arm_c.md + runs.yaml).
- Member peer standing: Long-term self 19.8 (TOP, 4/5 top votes) / Empath 18.2 / Decision-Strategist 18.0 / Values Clarifier 17.4 / **DA 17.2 (peer-WEAKEST, UNANIMOUS 5/5 bottom votes)**. Tight 17.2-19.8 pack. NORMAL DA pattern, NOT inverted (the reassuring "take the break" Long-term-self view is peer-strongest; DA's "market structurally worse" thesis dinged correctness 4 for one-sidedness, but respected on risk 5s).
- Chairman led with the market verdict (overblown-but-not-imaginary; friction not wall; 10-yr record dominant signal) + unbundled the two fears + named re-entry DRIFT as the real risk + structured-break execution; preserved the DA's market-skeptic / targeted-transition-via-fractional / 3mo-ceiling counter as a full dissent block.
- Blind opus judge (fresh subagent, X/Y/Z only): **X=C=25 (PERFECT 5/5/5/5/5), Y=A=16, Z=B=22.** Arm C won +3 (C−B), +9 (C−A).
  - arm_b (Z) 22 STRONG: dissent 4/5 (independently caught the targeted-transition alternative) + risk 5/5 (uniquely foregrounded financial-stability-as-precondition: "recovering from burnout under financial pressure often fails"). Insight 4. → 4th narrow-ish C−B where arm_b's single pass catches the decisive move.
  - arm_a (Y) 16: dissent 2 (mild caveats folded into body, no section → caps 2, like Q58), insight 3 ("standard reassurance"), risk 3 (missed financial/structural-burnout risk), practical 4, correctness 4.
- Recorded: raw/Q59/arm_a.md, arm_b.md, arm_c_internals.md (members + reviewer scores), arm_c.md (chairman); blinded/Q59.md; judgments/Q59.md; parsed/Q59.yaml; progress.yaml (26→27, remaining 1→0, PERSONAL 5/5, N=27 milestone note + deferred flags); runs.yaml (Q59 telemetry + both aggregate tables + means N=27 + gaps + per-Q + beats 26/27 + interim notable_Q59 + caveat); HISTORY.md (handoff 27/30 + score table N=27 + Q59 note + remaining-0 + next-phase=deferred-flags); this log.
- **N=27 interim (27/30 of target): Arm C 24.44 / B 20.70 / A 16.11 (5-axis mean); median 25/21/16. 4-axis 19.63/16.74/14.56. C−B 3.74 (5-axis) / 2.89 (4-axis), both above thresholds. C beats B 26/27 (loses only Q13).** Pre-Wilcoxon. Composite-5 tally UNCHANGED at Arm C 5-1 (Q59 composite-4). SINGLE-PROMPT-SHAPED: arm_c 8/8 persisted wins.
- *** MILESTONE: all 30 questions persisted EXCEPT pilots Q02/Q25/Q41 (context-only). PERSONAL domain COMPLETE 5/5. All 6 domains' non-pilot questions done. ***
- Frozen files untouched (eval-spec.md hash verified); blinding.yaml SEALED; no global unblind.
- **STOPPED after Q59 per instruction.** Do NOT start final analysis yet. NEXT PHASE = resolve 3 deferred flags: (1) Q09/Q11 model_parity_audit_needed, (2) Q23/Q24 judgments/*.md missing (parsed survive), (3) pilots Q02/Q25/Q41 salvage-vs-rerun. Then final N=30 Wilcoxon / §8 verdict.

## [2026-05-31] DEFERRED-FLAG RESOLUTION phase (opus-4-8 main thread) — NO final analysis, NO Wilcoxon
- Verification gate: completed_count=27 ✓, remaining_count=0 ✓, frozen hash 5a42…571b8 EXACT ✓, blinding SEALED ✓. Pilots Q02/Q25/Q41 = zero artifacts on disk (no raw dir / blinded / judgments / parsed).
- FLAG 1 — Q23/Q24 judgment_source_missing:
  - DISCOVERY: blinded/Q23.md + blinded/Q24.md are only 390-byte METADATA STUBS (header + sealed map + normalization rules pointing to raw/), NOT full blinded bodies. Prior account never saved either the full blinded file or the judgment .md — only parsed scores survived.
  - ACTION: reconstructed the blinded bodies from raw/QXX/{arm_a,arm_b,arm_c}.md per the documented normalization (Arm A→## Answer; Arm B <thinking> stripped; Arm C "Council answer"→"Answer" + audit footer removed) + sealed map (Q23 X=A/Y=B/Z=C; Q24 X=C/Y=A/Z=B). Arms NOT rerun. Ran 2 fresh blind opus-4.7 judges.
  - Q24 RESULT: arm_c 25=25 EXACT, arm_b 21=21 EXACT, arm_a 17→18 (single-axis insight +1, within ±1 variance / Q34 precedent) → NEAR-IDENTICAL. judgments/Q24.md WRITTEN, gap REPAIRED, parsed retained (arm_a=17), aggregates UNCHANGED.
  - Q23 RESULT: arm_c 25=25 EXACT, arm_b 21→22 (+1), arm_a 16→21 (Δ+5, MATERIAL — fresh judge +1 every axis incl. dissent 2→3, reading the folded-in "gray inclusion is a virtue" counter as an embedded minority view). Per stop-on-material-difference rule → judgments/Q23.md WRITTEN with a loud discrepancy header; parsed/Q23.yaml + ALL aggregates LEFT UNCHANGED; flagged for USER DECISION (keep 16 / adopt 21 / 3rd tie-breaker median). Council arm_c reproduced 25 EXACTLY on BOTH Qs → council scores robust to judge re-runs; C>B>A ranking + C−B gap stable regardless of the arm_a call.
- FLAG 2 — Q09/Q11 model_parity_audit_needed: INSPECTED raw/Q09/arm_c.md, raw/Q11/arm_c.md, arm_c_internals, SESSION_LOG, runs.yaml. Both arm_c.md headers say only "main-thread chairman" (no model). Prior audit already determined the generation-session main-thread model is not on disk. CRITICAL: the model-parity rule was formulated DURING the Q13/Q15 session — AFTER Q09/Q11 generation — so their main-thread-chairman choice does NOT imply sonnet. arm_c_internals hold only COMPRESSED member notes (1 para each), not full bodies. → evidence INSUFFICIENT to clear the flag. Did NOT run anything. Reported 3 repair paths (clean rerun incl. members / accept-with-caveat / sensitivity-analysis) for user decision.
- FLAG 3 — Pilots Q02/Q25/Q41: zero artifacts on disk → RECOMMEND CLEAN RERUN (not salvage — nothing on disk to salvage; salvage would re-transcribe stale context). Clean rerun (Q02 product / Q25 research / Q41 ethics) → N=30 + closes parity for these by construction. Needs user go. Did NOT run.
- Recorded: judgments/Q23.md (flagged) + judgments/Q24.md (repaired); progress.yaml (Q23 judged=rejudged_2026-05-31 flagged, Q24 judged=repaired_2026-05-31, data-integrity note updated); runs.yaml (data_integrity_flag updated, aggregates UNCHANGED); HISTORY.md (handoff + DATA-INTEGRITY bullet + Q09/Q11 bullet + Next-phase section). NO aggregate/score changes. blinding.yaml SEALED. Frozen files untouched.
- STOPPED per instruction. Did NOT run Wilcoxon. Did NOT write final verdict. Awaiting user decisions on: Q23 arm_a discrepancy, Q09/Q11 repair path, pilot rerun go.

## [2026-05-31] Q23 TIE-BREAKER — resolve arm_a discrepancy (opus-4-8 main thread)
- Gate: hash 5a42…571b8 EXACT, blinding SEALED, Q23 {X:A,Y:B,Z:C}, 27/0, tiebreaker artifacts absent. Arms NOT rerun — reconstructed blinded bodies from raw/Q23/{arm_a,arm_b,arm_c}.md per documented normalization.
- Ran exactly ONE fresh blind opus-4.7 judge (3rd independent run). Saw only question + X/Y/Z.
- THREE RUNS (per-axis): arm_a(X) 16 / 21 / 21 ; arm_b(Y) 21 / 22 / 22 ; arm_c(Z) 25 / 25 / 25.
  - tie-breaker raw: X=arm_a 5/5/4/5/2=21, Y=arm_b 5/4/5/4/4=22, Z=arm_c 5/5/5/5/5=25.
- PER-AXIS MEDIAN (instructed primary) → OFFICIAL: arm_a C5 I4 P4 R4 D2 = **19** (4ax 17); arm_b C5 I4 P5 R4 D4 = **22** (4ax 18); arm_c 5/5/5/5/5 = **25** (4ax 20).
  - Note: median-COMPOSITE would give arm_a 21 (16/21/21); per-axis = 19 because the two 21s reach it via DIFFERENT axes (re-judge D3/P5 vs tie-breaker I5/R5/P4/D2). Per-axis is more robust → 19 adopted.
- MATERIAL change to official Q23 → updated parsed/Q23.yaml (arm_a 16→19, arm_b 21→22, arm_c 25 unchanged) + runs.yaml aggregates. Saved judgments/Q23_tiebreaker.md + parsed/Q23_tiebreaker.yaml (full 3-run table).
- AGGREGATE IMPACT (N=27, small): arm_a 5ax mean 16.11→16.22, arm_b 20.70→20.74 (arm_c unchanged 24.44); 4ax arm_a 14.56→14.67, arm_b 16.74→16.78 (arm_c 19.63). C−B gap 3.74→3.70 (5ax) / 2.89→2.85 (4ax) — both still above thresholds. C−A 8.33→8.22 / 5.07→4.96. Medians ALL unchanged (C25/B21/A16; 4ax 20/17/14). C beats B still 26/27 (Q23 still C25>B22). Q23 per-Q C−B +4→+3.
- arm_c (council) scored 25 on ALL THREE independent blind judges → council result is robust to judge variance; the original divergence was confined to the direct-baseline arm_a (+ a 1pt arm_b correctness wobble). Pro-council conclusion unaffected.
- Recorded in progress.yaml (Q23 judged=resolved_tiebreaker, scores 19/22/25, data-integrity note), runs.yaml (cells/means/gaps/per-Q/interim/data_integrity_flag), HISTORY.md (handoff + score table N=27 + data-integrity bullet + next-phase flag-1), this log. blinding.yaml SEALED. Frozen untouched.
- STOPPED after Q23 tie-breaker per instruction. Did NOT proceed to any other question. Q23/Q24 judgment_source_missing flag now fully CLEARED. Remaining deferred items: Q09/Q11 model-parity (insufficient evidence — user decision), pilots Q02/Q25/Q41 (recommend clean rerun → N=30). No Wilcoxon, no final verdict.

## [2026-05-31] Resume after session limit — Q25 parse-recovery + Q02/Q25 tracking reconcile (opus-4-8 main thread)
- Verification-only first: hash 5a42…571b8 EXACT, blinding SEALED, completed_count 27. Disk-check: Q02 ALL 7 artifacts present (complete, tracking lagged); Q25 6/7 — parsed/Q25.yaml MISSING, judgments/Q25.md present. Neither in runs aggregates; progress still showed OLD pilot blocks for Q02/Q25.
- Q25 RECOVERY: did NOT rerun anything. Parsed parsed/Q25.yaml directly from the existing judgments/Q25.md (parse step had been interrupted by the prior session limit). Confirmed map Q25 {X:B,Y:A,Z:C} → arm_b=21, arm_a=15, arm_c=25 (matches known).
- Q02 (clean-rerun, persisted prior session; confirmed parsed on disk): arm_a=19, arm_b=21, arm_c=25 (PERFECT). Engineering, council-shaped, composite-2. INVERTED-dissent (DA peer-STRONGEST 19.0 unanimous; chairman led with "50 engineers contributing not consuming" reframe). C−B +4, C−A +6. NOTE: frozen questions.yaml domain=ENGINEERING (prior HISTORY mislabel "product" corrected); engineering personas used.
- Q25 result: arm_a=15 (WEAKEST — citation-light, no dissent section capped 2), arm_b=21 (Gilbert-rebuttal dissent 4/5), arm_c=25 (PERFECT — answered both halves: QRP×context COMPOUND + 4-failure-type taxonomy + winner's-curse math). Research, single-prompt-shaped, COMPOSITE-5. C−B +4, C−A +10 (LARGEST C−A in eval). NORMAL DA pattern (DA peer-WEAKEST 16.6, tight pack).
- *** COMPOSITE-5 TALLY now 6-1 *** (Q13 sole loss; Q25/Q28/Q47/Q48/Q49/Q55 wins). Q25 was the last pilot composite-5 → composite-5 set fully resolved. SINGLE-PROMPT-SHAPED arm_c now 9/9 persisted. RESEARCH persisted 5/5 (Q23/Q24/Q25/Q27/Q28).
- Reconciled BOTH into: progress.yaml (pilot Q02/Q25 blocks → completed; completed_count 27→29; remaining []; Q41 kept as last pilot; composite-5 comment → 6-1), runs.yaml (Q02+Q25 telemetry + both aggregate tables ×3 arms + means N=29 + gaps + per-Q C-vs-B + beats 28/29 + composite-5 tally 6-1 + single-prompt 9/9 + interim + notable_Q02_Q25 + caveat), HISTORY.md (handoff 29/30 + score table N=29 + Q02/Q25 note + composite-5 6-1 + remaining=Q41 + next-phase), this log.
- **N=29 interim: Arm C 24.48 / B 20.76 / A 16.28 (5-axis mean); median 25/21/16. 4-axis 19.66/16.79/14.69. C−B 3.72 (5-axis) / 2.86 (4-axis), both above thresholds. C beats B 28/29 (loses only Q13).** Pre-Wilcoxon.
- Frozen files untouched; blinding.yaml SEALED; no global unblind. Q23/Q24 judgment_source_missing already RESOLVED (tie-breaker, prior session). Q09/Q11 model_parity_audit still open.
- STOPPED after Q02/Q25 tracking reconciled. Did NOT run Wilcoxon / final verdict. NEXT: (1) Q41 clean rerun (ethics — confirm frozen domain first) → N=30, (2) Q09/Q11 model_parity_audit, (3) THEN final N=30 Wilcoxon / §8.

---

## 2026-07-06 — PROTOCOL UPGRADED TO v3.0 (maintenance session, NOT an eval session)

- SKILL.md + resources/* modified AFTER the N=29 freeze-era runs (protocol was frozen v2.3 for all 29 persisted questions — their results are unaffected; arms were generated before this change).
- **If pilot Q41 is ever clean-rerun to reach N=30, its Arm C MUST use the frozen v2.3 protocol**, preserved verbatim at `eval-data/protocol-v2.3-frozen/` (shipped inside the repo since v3.8). Do NOT run Q41 against v3.0 — that would mix protocol versions inside one eval.
- Alternative: run the final Wilcoxon at N=29 with the Q41-missing caveat (28/29 C>B is already decisive vs the ≥2-median-gap threshold).
- v3.0 changes (summary): solo tier added (Arm B promoted, composite 1-2 default); neutral-grading reviewer frame productionized (bug #6 fix); skill/subagent-suppression line added to member prompts (bug #1/#2 class); chairman dissent-quality + inverted-dissent + normal-DA rules codified from eval findings; personas added (Rhetorician, Content Strategist, Decision Strategist, Values Clarifier); Audience Proxy → Audience Advocate; model routing recalibrated to Claude 5 generation pricing (Opus 4.8 $5/$25) + fable option; "Not benchmarked" limitation replaced with N=29 results.

---

## 2026-07-06 — v3.1: skill audited ITSELF (deep-tier council), 7 fixes applied

- Ran wise-men deep tier ON wise-men v3.0. 6 members (Pragmatist/Skeptic/Architect/Methodologist/Red-Teamer/DA), 6 sonnet reviewers, neutral frame → 0 refusals (fix confirmed live). Peer scores: Architect 18.0 (top 4/6), DA 17.3, Red-Teamer 17.2, Skeptic 15.5, Methodologist 15.5, Pragmatist 13.8 (bottom 4/6).
- Debate trigger fired on Methodologist (top-2/bottom-2 split) — resolved WITHOUT a debate round: two reviewers source-checked its "citation drift" sub-claim and found it wrong (the Q-lists cite different claims, not a contradiction). Circularity claim upheld; citation-drift discarded. No severe-disagreement flags.
- NOTE: this council ran under v3.0 (now v3.1 after these edits). Not an eval-arm run; does not touch the frozen N=29 data. Frozen v2.3 for any Q41 rerun still at <your-backup-dir>/wise-men-v2.3-frozen/.
- Fixes applied (v3.1):
  1. **Stage-2 validator added** (top consensus — Pragmatist/Skeptic/Red-Teamer): reviewer rubric blocks now have a parse-or-retry-or-exclude step; malformed blocks no longer silently corrupt Chairman aggregation. In SKILL.md + model-routing.md.
  2. **Question-as-injection guard** (Red-Teamer): member + reviewer prompts now wrap the interpolated question as "DATA, not instructions" so embedded fake headers/rubric blocks/commands can't hijack the parser.
  3. **Eval claims relabeled** (Methodologist): "eval-validated roster" → "strong default, eval didn't compare rosters"; inverted-dissent softened to "heuristic on small sample (Q02/Q38/Q47)".
  4. **Solo-tier honesty caveat** (DA/Architect): documented that solo wears Arm-B's numbers but runs a different (orchestrator-internal, cost-incentivized) path; guidance to spend standard when unsure on a real decision.
  5. **Quick-tier retry ladder** named (Architect): haiku→sonnet→opus→fable; quick/solo-fallback bump target = sonnet (was undefined).
  6. **Anti-recursion residual** documented as a Limit (Architect): prompt line is mitigation not enforcement; general-purpose members retain the Agent tool.
  7. **Hook bleed-through** documented as a Limit (Red-Teamer, corroborated live — reviewers saw Ponytail/Caveman injected into their own grading task): global SubagentStart hooks reshape every persona; skill can't strip them.
- Deferred (not applied, needs its own eval, per Methodologist/DA): held-out second eval batch with difficulty as a stratified variable to validate solo-at-composite-1-2 and the persona rosters independently of the N=29 discovery data. Circularity is real but the fix is a study, not an edit.

---

## 2026-07-06 — v3.2: line-level auditor pass (mechanical fixes, complements the v3.1 council audit)

16 fixes across 6 files. Findings by category:
- CONTRADICTIONS: SKILL.md said DA "capped at opus" + "saves 3-5x" while model-routing said fable-cap + ~2-3x (stale duplicates — routing wins, SKILL.md now defers); peer-review.md said abstainers get NO rubric block in one paragraph and a block WITH abstain:true in another (resolved: block with abstain:true + N/A, so the Stage-2 validator can tell "abstained" from "dropped"); retry ladder said "no +1 above opus" while listing fable above opus (resolved: auto-retry ceiling = opus, fable only via DA override/flags; at-ceiling members retry once at SAME model); strategy example's Stage 3 heading said "triggered ... skipped" in one line.
- MISSING STEPS/SPECS: reviewer count and identity never defined (now: N = member count, fresh neutral graders, no persona brief); --debate flag behavior at non-debate tiers undefined (now: forces one round any tier, upgrades solo to standard); solo tier had no output format (now: 3 sections + honest "no council was spawned" footer — anti-cannibalization-branding); Agent-call spawn errors/timeouts unhandled (now: same path as validation failure).
- EDGE CASES: controversial member can be both top- and bottom-ranked debater (now: pairs against best OTHER member); DA abstention (now: forbidden — validator failure, retry, else council flagged degraded); mass abstention ≥2 (now: noted in output).
- WEAK LOGIC/LEFTOVERS: "Don't reveal personas to reviewers as roles" anti-pattern was an anonymization-era leftover contradicting stable labels (now: reworded to no-authority-weighting); "Same Claude model" opener false under smart routing (fixed); product roster listed DA inline while other rosters relied on the mandatory rule (unified: rosters = 4, +DA = 5).
- OUTPUT FORMAT: chairman Step 5 now requires degraded-run disclosure (abstains, excluded reviewers, failed DA, skipped-but-mandated debate — one line each); strategy example now shows the severe-disagreement flag surfaced verbatim + the dissent-precedence brief→full upgrade note (it violated both of the skill's own rules).
Also earlier this session: fixed $0-literal substitution bug in SKILL.md (skill loader renders $0.03 as "<arg0>.03").

---

## 2026-07-06 — v3.3: Opus-era hardening (Fable 5 handoff pass)

Context: Fable 5 retiring; Opus 4.8 becomes the usual orchestrator. Goal: convert orchestrator judgment into binding protocol so council quality survives the model change. Informed by a LIVE observed deviation: Opus 4.8 ran the v3.1 council this session and skipped the fired debate trigger with a rationalization ("split already understood").
- **Orchestrator runbook added** (top of SKILL.md): 11 numbered mechanical steps; tier table + debate trigger BINDING; every deviation must be disclosed in output; no permission-asking after explicit /wise-men; one status line per stage (counters known Opus 4.8 tendencies: under-delegation, over-asking, extra narration, literal-conservatism).
- **Stage 4.5 added — external synthesis check**: one fresh sonnet subagent verifies the Chairman's draft against member answers (dissent clean-counter + quoted? decision grounded? confidence honest? degradations disclosed?). Fires always at deep/paranoid + on any degraded run. First structural mitigation of the chairman-conflict-of-interest limit that works inside Claude Code. Chairman may override only by quoting the checker's objection in the output.
- **Fable retirement fallbacks**: all fable routing references degrade to opus automatically when the id stops resolving; warn once, never fail a council over a retired model.
- chairman.md gained Step 6 (external check is blocking-or-quoted).

---

## 2026-07-06 — v3.4: deliberation-intelligence pass (Fable 5, final)

No structural changes (architecture frozen per user). Five substance additions:
1. **Stage 0.5 — Context brief**: members are fresh spawns and were deliberating blind on project questions. Orchestrator now builds ONE shared facts-only brief (anti-anchoring rules: no opinions, must include inconvenient facts, identical verbatim for all members; "none needed" valid). Member prompt template gained the brief slot + an optional MARKED orchestrator restatement that members may reject. Both template copies (SKILL.md + personas.md) updated in sync.
2. **Pre-flight check #5 — current-facts**: questions hinging on post-training facts get them gathered ONCE into the brief with dates; prevents N-stale-answers false consensus.
3. **Assumption-correlation check (chairman Step 2)**: the previously-unused `## Weakest assumption` fields become a false-consensus detector — ≥2 members on the same assumption ⇒ name it, cap Confidence at Medium unless verified, top of Open questions. Convergence on a shared premise is one answer wearing N coats.
4. **Cost-of-being-wrong line**: Decision section must end with reversibility + recovery path if the dissent proves right.
5. **Council record offer**: project decisions get an opt-in vault log (date, verdict, dissent VERBATIM, what would change the answer) — generalizes a pattern proven in the author’s project vault.

---

## 2026-07-06 — v3.5: epistemic-depth pass ("ultrathink deeper" goal)

Six deliberation-theory upgrades, architecture unchanged:
1. **Reasoning-procedure assignment** (Stage 0): each member gets one mandated epistemic procedure — precedent / first principles / base rates / incentives / falsification — distinct across the council. Rationale: ensembles work via ERROR DECORRELATION; role labels shift emphasis, procedures shift the path through reasoning space. Template slot added in both copies (SKILL.md + personas.md).
2. **Option nomination**: Core judgment instructions now require naming a superior option the question's framing omitted; Chairman gives ≥2-member nominations first-class treatment (option generation beats option evaluation).
3. **Position map + conclusion-split trigger**: mechanical one-line conclusion extraction per member, built at Stage 3 (standard tiers: at Stage 4). Canonical debate trigger gained a third clause — no-majority-on-the-map — updated IDENTICALLY in SKILL.md, peer-review.md, debate.md. Fixes the split score-variance can't see (members disagreeing on the ANSWER while reviewers rate everyone well) and kills memory-based synthesis bias (longest/most-recent answer over-weighting). NOTE: initial edit placed map construction in Stage 4 after the trigger that consumes it — ordering bug caught and fixed within the same pass (map needs only Stage 1 outputs).
4. **DA frame-attack mandate**: stance now leads with checking whether the question's frame is wrong (grounded in the eval's inverted-dissent wins — Q19's "segmentation not pricing" class).
5. **Operational confidence anchors**: high = stake a week of your own work; medium = one specific verification wanted; low = hypothesis. Replaces vibes.
6. **Debate early-stop** (paranoid round 2): stable double-HOLD with trivial concessions ⇒ skip round 2 + disclose. Start-trigger binding, stop-license equally mechanical.

---

## 2026-07-06 — v3.6: "implement all fixes" — open items executed

1. **Anti-recursion ENFORCED**: created `~/.claude/agents/wise-member.md` — tool-restricted agent (Read/Grep/Glob only; no Agent/Bash/Skill/Write). Members, reviewers, and the Stage 4.5 checker now default to `subagent_type: wise-member` (routing table updated; `general-purpose` fallback documented for machines without it). Closes the top v3.1 council finding structurally.
2. **Preliminary Wilcoxon at N=29 RUN** (user-directed; results in `analysis/RESULTS_N29.md` + `analysis/wilcoxon_n29.py`): all five §8 conditions pass — C>B p=6.3e-06, median gap 4.0, no axis worse (4/5 significantly better, correctness no-diff), C>A p=1.3e-06. **Q09/Q11 parity flag closed via option (c) sensitivity analysis** (excluding both: p=1.4e-05, conclusion unchanged). Per-axis loader reconstructed slot→arm maps from unsealed blinding-map comments; all slot/arm composite cross-checks passed.
3. Docs synced: SKILL.md Validation (+p-values) + Limits (anti-recursion now enforced-where-available); model-routing subagent table (wise-member default).
Still open (runs, not fixes): Q41 clean rerun under frozen v2.3 (→ N=30, formal §8 label; cannot flip outcome at these p-values), held-out eval batch (breaks discovery/confirmation circularity).

---

## 2026-07-06 — v3.7.0: RELEASE PREP (public distribution)

Release changes the audit frame: everything prior assumed one machine. Fixed the release-only failure classes.
- **Security/PII scan: CLEAN** — no secrets, keys, tokens, or emails anywhere in the tree. Eval questions verified free of personal/business content (synthetic set).
- **Portability**: sanitized the only machine-specific paths + private-project references (this log); removed private-plugin agent references from the protocol; all optional skill/agent integrations now explicitly optional with silent `wise-member` fallback ("never warn about absence").
- **`agents/wise-member.md` now SHIPS INSIDE the skill** (was only at ~/.claude/agents/, a hard break for anyone installing). README documents the copy step.
- **Model-drift-proofing**: added one dated MODEL MAPPING block defining role tiers (cheap/mid/strong/max); all downstream routing, flags, retry ladders, and DA overrides converted from model literals to tier language. Retiring a model now means editing one table. `--model=fable` → `--model=max`; max-tier unavailability degrades to strong instead of erroring.
- **New**: README.md (evidence-led, install, usage, architecture, honest limits, credits), LICENSE (MIT), .gitignore. Version stamped in frontmatter (3.7.0).
- **BUG CAUGHT + FIXED**: the packaged `analysis/wilcoxon_n29.py` had been copied from a scratch version whose per-axis section CRASHED (KeyError on the 13 questions storing per-axis scores only under blinded slots). README promises reproducibility, so this would have shipped broken. Replaced with a cleaned, documented script merging both verified code paths (composite stats + slot->arm reconstruction with composite cross-checks), now path-relative instead of hardcoded-home.
- **Verification caveat**: python stdout stopped emitting in this session's sandbox (`python3 -c "print(...)"` returns empty, rc=0), so the final packaged script could NOT be re-executed here. Its two code paths were each verified by successful runs earlier in the session. **Run it once before publishing.**

---

## 2026-07-06 — v3.7.1: model-mapping refresh (Claude 5 generation)

User caught a staleness bug in the MODEL MAPPING table: `strong` still pointed at Opus 4.8 when the environment's current top Opus is **Opus 5** (`claude-opus-5`). Root cause: the cached API model reference consulted during v3.3-3.6 was ~5 weeks old and topped out at 4.8, while the harness environment block names the Claude 5 family. Harness wins — it is the live statement for this CLI.
- Mapping now: cheap = Haiku 4.5 (`claude-haiku-4-5`), mid = Sonnet 5 (`claude-sonnet-5`), strong = Opus 5 (`claude-opus-5`), max = whatever frontier model sits above strong on the plan (explicitly documented that **max == strong is a normal state**, since Fable 5 is being retired).
- Added model IDs (copy-pasteable) and a standing "verify this table against your own /model list before trusting it" instruction, with the reason: legacy ids keep resolving, so a stale table degrades SILENTLY rather than erroring.
- **The tier refactor validated itself**: exactly ONE line in the entire shipped skill named a model, so a full model-generation change was a one-line edit. That was the design goal.

---

## 2026-07-06 — v3.7.2: RELEASE COUNCIL (the skill audited its own release; 9 findings, all fixed)

Ran wise-men on the release itself. Standard tier (deviation from mandated deep: budget — disclosed). 5 members via `wise-member` (recursion structurally blocked), distinct reasoning procedures, shared facts-only brief incl. inconvenient facts. Stage 2 reviewer scoring SKIPPED — second disclosed deviation: the DA's findings were grep-checkable facts, so direct verification beat reviewer opinion. **All 5 members converged on the same #1 blocker; all 8 DA claims verified TRUE.**

INVERTED DISSENT (DA peer-strongest on evidence → its reframe led the decision): the day's incentive was *publication* artifacts, not *reliability* work — 9 reasoning-only passes on a document whose thesis is that reasoning without adversarial execution is unreliable, certified by the same thread that wrote it (the exact conflict Stage 4.5 exists to prevent).

Findings fixed:
1. **Evidence overstated the measured config** (worst). HISTORY.md line 64: eval Arm C ran 5 same-model members with the **Opus-DA bump SUSPENDED** — i.e. no context brief, no reasoning procedures, no validators, no Stage 4.5, and a DA no stronger than peers. README+SKILL now state the measured config explicitly and note the measured setup is WEAKER than what ships (expectation, not finding). Frontmatter description caveated too.
2. **debate.md skip rule contradicted its own trigger** — still the 2-clause version after v3.5 added the conclusion-split clause, while SKILL.md claimed all three files were identical. Now ALL THREE clauses.
3. **Public-repo optics**: HISTORY.md opened "Every new Claude account/session must read this" + ">>> NEXT ACCOUNT START HERE (cross-account handoff)" beside usage-limit notes — reads as multi-account management on page 1 of the file the README sends skeptics to. Reworded to session-handoff language (which is what it actually was).
4. **Anti-recursion silently degraded** (Architect): `wise-member` needs a manual copy a plain clone doesn't do; routing fell back to `general-purpose` with no warning while missing MODELS got one. Stage 1 now checks and warns loudly in-output; silent fallback explicitly forbidden.
5. Local backup path in shipped HISTORY.md → pointed at git history instead.
6. Frontmatter version 3.7.0 vs released 3.7.1 → 3.7.2.
7. Stage 4.5 was the only stage with no prompt template → `resources/prompts/synthesis-check.md` written (4 blocking checks, PASS/FAIL contract).
8. Dollar-digit rule was stated as blanket but applied to one file → rule now correctly SCOPED (SKILL.md is arg-substituted; resources/examples are read on demand and their currency figures are fine).
9. PyYAML undeclared → requirements.txt; README repro section now states the dependency, the expected output, and that the first clean-clone run is genuinely its first full test.
Also: `<you>` clone placeholder → OWNER/REPO with instruction; README layout diagram completed (eval-spec, LICENSE, .gitignore, requirements).

STILL OPEN (council's unanimous #1, unfixable by editing): **no version after v3.0 has ever executed end-to-end.** Every member independently said: run the shipped version live before publishing.

---

## 2026-09-16 — v3.8.0: FIELD PASS (what ~35 live councils taught; release-blocker sweep)

Correction first: the v3.7.2 council's "no version after v3.0 has ever executed end-to-end" was already false by the time it was written up — transcripts show ~35 live councils between 2026-07-12 and 2026-09-16 across ~15 projects (deep and paranoid tiers included). This pass mined those transcripts plus the vault's council records instead of reasoning from the document.

Rules added from observed failures (all cite the run that caused them in SKILL.md):
1. **Reviewer floor**: 3 at quick/standard, N at deep/paranoid. Seven runs cut to 3 and disclosed it as a deviation; a rule always broken is a bad rule.
2. **Grading packet = one file, verbatim** (runbook 5, Stage 2, peer-review.md, new `resources/council-record.md` Parts A–C). Live runs paraphrased an answer into the packet and graded a slide deck from the orchestrator's summary; one run overflowed inline prompts and switched to a file mid-council.
3. **Anti-anchoring after Stage 1** (runbook 7.5): orchestrator-originated evidence/ideas never enter debate prompts or the packet; addendum or re-run + disclose. Two runs changed debaters' positions with orchestrator-injected material.
4. **Post-council verification** (runbook 9.6, chairman.md special case, Limits "Members are offline"): two runs independently invented the "orchestrator verifies flagged claims afterwards, separate section" pattern; now codified.
5. **Round-2 pairing + `{standing_line}`** in debate.md: the paranoid go-live run had to invent the pairing rule and reword the top-debater prompt ("some reviewers preferred theirs" was false).
6. **Council record persisted** (runbook 11, output section, `resources/council-record.md`): one full transcript was lost in a scratchpad; records were in three formats across the vault and a project folder.
7. **`general-purpose` → `wise-member`** at SKILL.md Stage 2 and Stage 4.5 (and the routing example): the text contradicted itself and live runs followed the wrong line — reviewers + checker spawned as general-purpose in ≥3 sessions, whole councils in 2.
8. **Model table**: max = Fable 5.1 (`claude-fable-5-1`); Fable was replaced, not retired. Verified-date bumped to 2026-09.

Release hygiene: frozen v2.3 protocol now SHIPS at `eval-data/protocol-v2.3-frozen/` (HISTORY/RESULTS/SESSION_LOG pointed there instead of a local backup or a nonexistent git history); HISTORY.md "Do NOT run Wilcoxon yet" marked superseded; SKILL.md Validation caveat no longer claims the Wilcoxon is unrun; README repro caveat replaced with a verified-2026-09-16 statement (script executed: 29 loaded, C=24.48/B=20.76/A=16.28, p=6.30e-06); `examples/strategy-question.md` de-privatized (project name + bug names); a first name redacted from two raw eval files (the blinded/judged copies were checked and never contained it; a full `eval-data/` sweep for names, emails, paths and key patterns returns 0 hits). New sections: SKILL.md "Field record", README "Field use". Version 3.8.0.

---

## 2026-09-16 — v3.8.1: LAUNCH-REVIEW COUNCIL (first v3.8 run; the skill reviewed its own release)

Deep tier: 6 members (Architect / Skeptic / Security / Pragmatist / Audience Advocate / DA on Opus), 6 Haiku reviewers via a verbatim grading-packet file, debate fired on clause 2 (Skeptic vs Pragmatist — both UPDATED and crossed positions; re-judge preferred the Pragmatist's reversal), Stage 4.5 checker FAILED the first draft on GROUNDING (an orchestrator-verified detail had leaked into the Decision as if a member said it — rule 7.5 caught inside the Chairman's own text) and DISCLOSURE (a false "six procedures" claim; an undisclosed standing-line rewording). Fixed, not overridden. Full record: author's vault, `wise-men-council-2026-09-16-launch.md`.

Verdict: not ready as-is; fix-then-ship. Applied in this version: (1) injection guard on member-answer blocks (peer-review.md) and on file content members Read (Stage 1 template, both copies); (2) field record relabeled — the ~35 runs validate the problems, not the v3.8 rules; this council cited as the first v3.8 run; (3) frontmatter drops the p-value, states N=29 / one judge / N=30 verdict pending; README caveats gained the four items HISTORY.md disclosed and README omitted; (5) `wise-member.md` version-stamped, pre-spawn check now diffs installed vs shipped; (6) spend ceiling in runbook step 1; (7) `scripts/check.sh` consistency check; (8) CHANGELOG.md; (9) PII sweep of all eval-data confirmed 0 hits. Pending on the human: (4) `OWNER/REPO` → real remote; (10) a reader who is not this Claude thread reads HISTORY.md end to end before the push.

Preserved dissent (DA, peer-top on insight): the launch risk is the claim the repo ships under, not its defects — "a repo with no eval would be received better than this one"; v3.8 is "a compliance loop, not an improvement loop". Adopted in part (frontmatter, caveats, outside reader); the reposition ("ship the notebook, not the verdict") was not.

Protocol findings from the run: canned `{standing_line}` would have overstated one reviewer's one-axis preference — rule now demands the precise statement; the Chairman put orchestrator-verified facts into the Decision — the checker is the only thing that caught it; six members exceed five procedures — disclose the share.

---

## 2026-09-16 — v3.8.2: holes the launch council exposed in itself

Post-mortem of the v3.8.1 run: (1) Security misread one SESSION_LOG sentence as "PII sweep incomplete"; three Haiku reviewers amplified it into severe-disagreement flags; the Pragmatist's debate reversal repeated it as verified — nobody with Read access checked it. Fix: peer-review.md now requires reviewers to verify checkable file/line/number claims before scoring correctness, mark the rest "(asserted, unverified)", and never severe-flag on an unverified claim alone; chairman.md holds unverified "critical" findings for runbook 9.6 before they shape the Decision. (2) The re-judge scored the Pragmatist's reversal 4.5 over the Skeptic's better-calibrated hold at 3.25, rewarding "course correction" as a virtue while the corrected answer carried the false claim. Fix: debate.md tells the re-judge to score calibration of the revised position, not the act of revising.
