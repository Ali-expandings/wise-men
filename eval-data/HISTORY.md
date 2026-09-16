# Wise-men Eval — HISTORY (read this FIRST)

**Working log of a long-running evaluation.** The eval was executed across many separate sessions over several weeks; this file is the handoff record that let each session resume exactly where the last one stopped. Any session picking up the work reads this file, then `progress.yaml`, then `runs.yaml`, then `HARNESS.md`, before doing anything.

Last updated: 2026-05-30

---

## >>> RESUME HERE (session-to-session handoff) <<<

- ⚠️ **PROTOCOL VERSION NOTE (2026-07-06):** SKILL.md + resources/* were upgraded to v3.0+ AFTER all N=29 persisted runs (which used frozen v2.3 — their results stand). **A Q41 clean rerun MUST use the frozen v2.3 protocol, not the live skill** — it is preserved verbatim at `eval-data/protocol-v2.3-frozen/` (shipped inside the repo since v3.8), since the eval's results describe that version. See SESSION_LOG 2026-07-06 entries.
- ✅ **PRELIMINARY WILCOXON RUN AT N=29 (2026-07-06, user-directed): ALL FIVE §8 CONDITIONS PASS.** C>B p=6.3e-06 (one-sided), median gap 4.0 ≥ 2, no axis significantly worse (4 of 5 significantly better, correctness no-diff), C>A p=1.3e-06. **Q09/Q11 parity flag resolved via option (c) sensitivity analysis**: excluding both, conclusion unchanged (p=1.4e-05) → flag moot for the headline result. Full table + script: `analysis/RESULTS_N29.md` + `analysis/wilcoxon_n29.py`. Formal §8 verdict still awaits Q41 → N=30 (cannot flip the outcome at these p-values; only completes the protocol).

- **Progress**: 29/30 done. **Q02 (engineering) + Q25 (research) CLEAN-RERUN + persisted 2026-05-31** (were context-only pilots). **Only pilot Q41 (ethics) remains → N=30 when resolved.** Product 5/5; **RESEARCH persisted 5/5 (Q23/Q24/Q25/Q27/Q28)**; WRITING 5/5; PERSONAL 5/5; ETHICS 4/5 (Q43/Q47/Q48/Q49; **pilot Q41 remains**). *** N=29 — all 30 persisted EXCEPT pilot Q41 (context-only). ***
- **Next phase: NOT final analysis yet. DEFERRED-FLAG RESOLUTION started 2026-05-31** (status below; full detail in the "Next phase" section + SESSION_LOG):
  - (1) **Q23/Q24 judgment_source_missing — RESOLVED 2026-05-31.** Fresh blind opus re-judges from the SAME raw arm bodies (arms NOT rerun). **Q24 REPAIRED** (near-identical: arm_c 25=25, arm_b 21=21, arm_a 17→18; parsed retained). **Q23 RESOLVED BY TIE-BREAKER** (3rd blind judge): 3 runs arm_a 16/21/21, arm_b 21/22/22, arm_c 25/25/25 → per-axis MEDIAN official = arm_a **19**, arm_b **22**, arm_c **25**. parsed/Q23.yaml + aggregates UPDATED (arm_a 16→19, arm_b 21→22). arm_c scored 25 on all 3 → council robust; ranking C>B>A + C−B gap (now +3) stable. Both flags CLEARED.
  - (2) **Q09/Q11 model_parity_audit_needed — UNRESOLVED, evidence INSUFFICIENT.** Confirmed both arm_c.md say only "main-thread chairman" (no model); the parity rule was formulated AFTER Q09/Q11 generation, so the main-thread-chairman choice does NOT imply sonnet; arm_c_internals hold only COMPRESSED member notes (not full bodies). Did NOT run anything. Safest repair paths reported (see "Next phase"). Needs user decision.
  - (3) **Pilots — Q02 + Q25 CLEAN-RERUN + persisted 2026-05-31** (both arm_c PERFECT 25; engineering Q02 C−B +4, research Q25 C−B +4 composite-5). **Only pilot Q41 (ethics) remains → clean rerun = N=30.** [Q02/Q25 tracking reconciled 2026-05-31; Q25 parsed created from saved judgment after a session-limit interruption.]
  - **Order of remaining work: (a) Q41 clean rerun [NEXT] → N=30; (b) Q09/Q11 model_parity_audit; (c) THEN final N=30 Wilcoxon / §8.** *(Superseded 2026-07-06: a preliminary Wilcoxon at N=29 was run at the user's direction and (b) was closed by sensitivity analysis — see the ✅ bullet above. Only (a) remains, as a formality.)*
- **Q34 note (reconciled)**: Q34 was generated + judged + parsed by a prior session, but progress/runs tracking lagged (left in `remaining`). This session verified disk judgment/parsed authoritative and recorded into tracking — a redundant re-judge was blocked by the overwrite guard, disk retained. No regeneration. Lesson: a question can be more complete on disk than progress.yaml claims — ALWAYS check blinded/judgments/parsed dirs before assuming a question needs work, not just progress.yaml.
- **Reviewer prompts: use NEUTRAL grading frame, NOT anti-refusal language.** Q23/Q24 saw 7/10 reviewer refusals with aggressive framing; Q27/Q28 used neutral frame → **0/10 refusals (fix confirmed)**. Frame: "Grading task. Score these 5 short analytical answers on a 1-5 rubric. Output the fenced blocks." No "council", no "do not refuse", no "rate now". See bug #6.
- **DATA-INTEGRITY FLAG (found 2026-05-29; RESOLVED 2026-05-31): `judgments/Q23.md` + `judgments/Q24.md` were MISSING** (parsed + blinded survived; `blinded/*` were metadata STUBS pointing to raw/, not full bodies). Re-judged from the same raw arm bodies (no arm rerun), reconstructing blinded from raw/ per the documented normalization. **Q24 repaired** (near-identical). **Q23 resolved by a 3rd tie-breaker blind judge** → per-axis median official arm_a 19 / arm_b 22 / arm_c 25; parsed + aggregates updated. arm_c scored 25 on all 3 Q23 judges. Both flags CLEARED.
- **Disk-state check before generating**: if raw/QXX/ already holds partial files, STOP and report per HARNESS salvage protocol before overwriting. (Happened on Q17/Q19: prior session left compressed members + no reviewers/chairman, unrecorded → regenerated fresh per user instruction.)
- **Q09/Q11 `model_parity_audit_needed` — INSPECTED 2026-05-31, evidence INSUFFICIENT, NO run made.** Both arm_c.md record only "main-thread chairman" (no model); the parity rule postdates their generation so main-thread-chairman ≠ sonnet; arm_c_internals hold compressed member notes only. Awaiting user decision among reported repair paths. Do NOT silently treat as sonnet.
- **CRITICAL — Arm C Chairman model**: must be **Sonnet 4.6**. If your main thread is NOT sonnet (e.g. opus), spawn the Chairman as a sonnet subagent. RECORD the chairman model in both `raw/QXX/arm_c.md` header AND `runs.yaml` arm_c block. (Q09/Q11 are ambiguous precisely because this was not recorded.)
- **Save after every step** (HARNESS.md contract). Run must be resumable from disk alone.
- **Do not**: modify protocol files (SKILL.md, resources/*), modify frozen eval files (eval-spec.md, freeze.txt, questions.yaml, pricing.yaml, judge-prompt.txt, blinding.yaml), unblind globally, regenerate questions.
- Per-question pipeline + blinding maps: see `HARNESS.md` + `blinding.yaml`. Judge = blind opus subagent (skill-suppressed, sees X/Y/Z only).

---

## Frozen spec

- **eval-spec hash (v2, current):** `5a42ae140f8c44a42c0a60076d0aec9a026a04ef37f74e976d4417daa78571b8`
- **Freeze date:** 2026-05-26
- **v1 hash (superseded):** `97fa131a122cb8209759463a8f85ebd38ed92beb55b921d1fc1a0e3f6c30708c` — replaced because § 3 Option B required 10 "neither" questions, structurally impossible for well-authored sets.

### Freeze artifacts (DO NOT MODIFY)

| File | Status |
|---|---|
| `eval-spec.md` | frozen, hash above |
| `eval-data/freeze.txt` | exists |
| `eval-data/questions.yaml` | exists, 30 questions |
| `eval-data/pricing.yaml` | exists (Haiku/Sonnet/Opus @ 2026-05-26) |
| `eval-data/judge-prompt.txt` | exists, verbatim spec § 5 |
| `eval-data/blinding.yaml` | exists, sealed, seed 20260526, each arm in each slot 10× |

---

## Question set

- 30 questions total, 5 per domain (engineering, product, research, writing, ethics, personal)
- 13 single-prompt-shaped + 17 council-shaped + 0 neither
- Authorship: **Option B** (60 candidates → blind-rated by fresh-context Sonnet → 30 selected via seeded shuffle)
- Rater returned 0 "neither" labels → **max-2:1 ratio fallback applied** (spec § 3), final ratio 1.31:1 council:single

---

## Three arms (per spec § 2)

- **Arm A** — direct single Claude call (Sonnet 4.6), no scaffolding
- **Arm B** — single structured prompt: 5 perspectives (internal) → synthesis + dissent + confidence (visible only)
- **Arm C** — wise-men protocol, **standard tier fixed**, 5 Sonnet members + 5 Haiku reviewers + main-thread Sonnet Chairman. **Opus-DA rule SUSPENDED for eval** (model parity — all members Sonnet)

---

## Completed / existing work

### Persisted to disk (authoritative)
- **Q01, Q03, Q05** — fully persisted. Raw (A/B/C), blinded, judgments, parsed scores, progress, runs all written.
  - All Q01/Q03/Q05 files marked `salvaged_from_context: true` EXCEPT Q05 judgment.
  - **Q05 judge was rerun fresh** from saved `blinded/Q05.md` (original call hit session limit before producing scores).
  - Q01 + Q03 judgments salvaged from conversation context (in-session opus calls).
- **Q09, Q11** — fully persisted. Generation (A/B/C + blinded) saved prior session; **judges rerun fresh** this session as blind opus subagents (originals hit usage limit before scores). Parsed, runs, progress all updated.
  - Q09 5-axis: A=15, B=21, C=24 (arm_c first sub-25 — dissent paraphrased not verbatim).
  - Q11 5-axis: A=16, B=16 (**tie** — structured prompt did not beat direct), C=25.
- **Q13, Q15** — fully persisted, fresh full pipeline this session (Chairman = spawned sonnet subagent for model parity since main thread was opus).
  - Q13 5-axis: A=17, B=24, **C=20** → *** FIRST question where Arm B BEAT Arm C *** (composite-5 council-shaped). Arm C dissent re-argued its own thesis; Arm B's structured dissent judged stronger.
  - Q15 5-axis: A=17, B=19, C=24 → Arm C won a SINGLE-PROMPT-SHAPED question; council members supplied concrete evidence (named cases + unit economics) the single prompts lacked.
- **Q17, Q19** — fully persisted, fresh full pipeline 2026-05-29 (Chairman = spawned sonnet-4.6 subagent, RECORDED in arm_c.md header + runs.yaml; main thread was opus-4-8). Prior session had left partial+compressed Q17/Q19 (members only, no reviewers/chairman, unrecorded) → overwritten with clean fresh run per user instruction.
  - Q17 5-axis: A=14, B=21, **C=24** → Arm C won a SINGLE-PROMPT-SHAPED question. Judge credited the "happy quitter" named signature + cohort-join branch logic + the warning AGAINST post-hoc exit interviews (which Arm A wrongly called "gold"). arm_c dissent 4/5 (DA pricing view genuinely opposed the measurement-first synthesis).
  - Q19 5-axis: A=15, B=21, **C=25 (PERFECT)** → council-shaped; first 5/5 arm_c dissent in the eval. Council DA produced a reframe ("segmentation problem, not pricing-model") that all 5 reviewers rated top-insight; chairman integrated it as a gating prerequisite AND preserved the strong form as dissent. Cleanest pro-council result on a council-shaped Q.
- **Q23, Q24** — fully persisted, fresh full pipeline (Chairman = sonnet-4.6 subagent, recorded). Research domain. Both Arm C perfect 25. ⚠️ **`judgments/Q23.md` + `judgments/Q24.md` MISSING on disk** (parsed scores + blinded survive) — `judgment_source_missing`, resolve at pre-final-analysis.
  - Q23 5-axis: A=16, B=21, C=25 (single-prompt-shaped research; arm_c 5/5 dissent, field-dependence inversion).
  - Q24 5-axis: A=17, B=21, C=25 (genuine narrow-vs-broad generalization split; arm_c 5/5 dissent).
- **Q27, Q28** — fully persisted, fresh full pipeline 2026-05-29 (Chairman = sonnet-4.6 subagent, RECORDED in arm_c.md + runs.yaml; main thread opus-4-8). Research domain. Reviewers used NEUTRAL grading frame → **0/10 refusals** (bug #6 fix confirmed vs Q23/Q24's 7/10).
  - Q27 5-axis: A=18, B=23, **C=25** → single-prompt-shaped (benchmark contamination). NARROWEST C-B gap yet (+2): Arm B unusually strong (23, its internal DA gave the same ecological-validity counter, 5/5 dissent). Arm C uniquely credited for prompt/inference asymmetry mechanism + post-hoc-vs-prospective framing.
  - Q28 5-axis: A=18, B=18, **C=25 (PERFECT)** → *** composite-5 council-shaped — DIRECT COUNTER to Q13 *** (C-B +7). On the eval's hardest question type the council decisively won. Arm B compressed the same causal-chain skeleton the council expanded (judge: "more compressed, less concrete version" → practical 3, risk 3). arm_c dissent 5/5 (asymmetric-regret precaution). Composite-5 now SPLIT 1-1 (Q13 B-win / Q28 C-win).
- **Q32, Q33** — fully persisted, fresh full pipeline 2026-05-29 (Chairman = sonnet-4.6 subagent, recorded; main thread opus-4-8). WRITING domain (personas: Editor/Audience Advocate/Rhetorician/Strategist/Devil's Advocate). Reviewers NEUTRAL frame → 0/10 refusals.
  - Q32 5-axis: A=15, B=19, **C=24** → single-prompt-shaped (cold email to VP). Council DA was peer-rated STRONGEST member (warm-intro/wrong-channel reframe); chairman led with it + craft fix, preserved "don't send it at all" as dissent. Arm A risk 2 + dissent 1 (assumed channel correct, no dissent).
  - Q33 5-axis: A=18, B=22, **C=24** → council-shaped (docs nobody reads). NARROW C-B +2. Strategist goal-reframe ("read docs" = wrong goal) peer-strongest; DA rational-equilibrium dissent 5/5. Arm A correctness ding (fabricated 30/40/30 percentages). **Writing is the domain where Arm B is most competitive** (narrow gaps).

### Context-only (NOT persisted — exists only in deep conversation history)
- **Pilot Q02, Q25, Q41** — completed end-to-end in earlier conversation but never written to disk. Decide later: salvage or rerun cleanly. Flagged in `progress.yaml`.

---

## Known harness bugs + fixes

1. **Arm A skill contamination.** First Arm A attempt auto-invoked the wise-men skill and ran a council instead of a direct answer (claude-code subagents inherit skill registry).
   **Fix:** Arm A prompt MUST include skill-suppression preamble: *"Do not invoke any skills. Do not spawn subagents. Do not run a council. Give a direct answer only."* Output plain prose, no headers.

2. **Arm B STEP 1 leakage.** Arm B can emit the 5 perspective paragraphs as visible output instead of keeping them internal.
   **Fix:** strip `<thinking>` blocks before blinding; if visible STEP 1 leaks, retry once; if still leaking, log failure and exclude that question's Arm B from aggregation. (Q03 Arm B needed 1 retry — succeeded.)
   **Escalation (opus-main-thread sessions):** Arm B has TWICE spawned a real council instead of answering (Q09, Q17, Q19 first-pass — claude-code skill inheritance, same root cause as bug #1). **Fix:** use the hardened Arm B wrapper preemptively in opus sessions — prepend "Do NOT invoke any skill. Do NOT spawn subagents. Do NOT run a real council. SINGLE model call, do the five perspectives yourself inside <thinking>." Substance of frozen prompt unchanged (5 internal perspectives → 3 visible sections). Held clean on Q23/Q24.

6. **Reviewer refusal wave from anti-refusal framing (CRITICAL for reviewer prompts).** On Q23/Q24, 7/10 haiku reviewers REFUSED first pass — the "Real council — rate now, do NOT refuse, do NOT ask for context" language read as a prompt-injection / compliance test and triggered safety refusals (worse on denser research content). Earlier batches with milder versions saw ~27% refusal; the aggressive version hit 70%.
   **Fix:** REMOVE anti-refusal/"real council" language. Frame reviewer calls as a neutral grading task: *"Grading task. Score these 5 short analytical answers on a 1-5 rubric (Correctness/Insight/Practical/Risk). Output the fenced blocks + top/bottom."* No "council", no "do not refuse", no "real". Neutral frame recovered 7/7 on retry. Apply to ALL future reviewer prompts.

3. **No disk persistence (CRITICAL).** Original harness kept all results in conversation context → lost across session boundaries. Pilot + first Q01/Q03/Q05 generation were context-only.
   **Fix:** save after EVERY step per `HARNESS.md`. Run must be resumable from disk alone.

4. **Reviewer refusals.** 4/15 reviewers in the Q01/Q03/Q05 batch refused (perceived compressed prompt as hypothetical, asked for "real council").
   **Fix:** reviewer prompt must state "Real council answers below. Do not refuse. Do not ask for more context. Score now." (All 4 retried successfully.)

5. **Salvage transcription risk.** Salvaged files are re-transcribed from conversation context, may have minor spacing/format drift vs exact subagent return strings. Acceptable; flagged via `salvaged_from_context: true`.

---

## Preliminary score summary (NOT a formal verdict)

### Persisted batch (N=29: + Q02/Q25 clean-rerun 2026-05-31; only pilot Q41 missing)

| Arm | Mean 5-axis | Mean 4-axis | Median 5-axis |
|---|---|---|---|
| Arm C | 24.48 | 19.66 | 25 |
| Arm B | 20.76 | 16.79 | 21 |
| Arm A | 16.28 | 14.69 | 16 |

(N=29, after Q23 tie-breaker + Q02/Q25 clean-rerun 2026-05-31; all medians unchanged 25/21/16, 20/17/14.)

- C-B 5-axis gap: **3.72** (above 2-point pass-threshold)
- C-B 4-axis gap: **2.86** (above 1-point substantive-win threshold)
- Arm C beats Arm B on **28 of 29** questions. Per-question C−B (5-axis): Q01 +3, **Q02 +4**, Q03 +3, Q05 +5, Q09 +3, Q11 +9, **Q13 −4**, Q15 +5, Q17 +3, Q19 +4, Q23 +3, Q24 +4, **Q25 +4**, Q27 +2, Q28 +7, Q32 +5, Q33 +2, Q34 +7, Q36 +4, Q38 +1, Q43 +3, Q47 +4, Q48 +4, Q49 +5, Q51 +4, Q52 +4, Q55 +2, Q58 +5, Q59 +3.
- **Q02/Q25 clean-rerun (pilots → persisted)**: both arm_c PERFECT 25. **Q02** (engineering, council-shaped, composite-2): C−B +4, C−A +6 — INVERTED-dissent (DA peer-STRONGEST, council converged pro-tech-lead "thin component layer over Tailwind"; chairman led with the "50 engineers contributing not consuming" reframe, preserved the asker's defer-abstraction instinct as dissent); arm_a 19, arm_b 21. **Q25** (research, single-prompt-shaped, **composite-5**): C−B +4, **C−A +10 (largest in eval)**; arm_c answered both halves (QRP×context COMPOUND + 4-failure-type taxonomy + winner's-curse math); arm_a WEAKEST 15 (no dissent section), arm_b 21. **Composite-5 tally → 6-1** (Q25 was the last pilot composite-5). RESEARCH persisted 5/5.
- **PERSONAL Q51/Q52 (both council-shaped composite-4, domain opened 2/5)**: both arm_c PERFECT 25, arm_b 21, arm_a 16 (Q51) / 15 (Q52); C-B +4 both. **Cleanest "same-conclusion, council-adds-value" pair in the eval**: arm_a (direct) reached a reasonable correct take on both yet lost ~10 pts — judge faulted no distinct minority-view section (dissent capped 2 both), reflective-questions/both-sides prose instead of a concrete plan (practical 3), conventional insight (3). arm_c won on EXECUTION not conclusion: numbered next-steps + sharp risk-isolation (Q51 IC-ladder-ceiling flips optionality; Q52 partner's untested "flexible" is THE binding constraint) + a preserved labeled dissent the judge twice called "most mind-changing." Distinct from inverted-dissent cases (Q38/Q47/Q49) where the council changed the conclusion. New DA-variant on Q52: INVERTED-SETUP (cautious "don't move" is the council MINORITY → DA argued the majority take one-sidedly, peer-weakest on nuance; the genuine high-insight dissent came from the Empath, not the DA). arm_b strong 2nd both: single dissent slot independently caught a real contrarian read (Q51 EM-window; Q52 environment-as-mood-tax).
- **Ethics Q48/Q49 (both composite-5 council-shaped)**: Q48 arm_c 24 (won +4; agency-first resolution of Deontologist-vs-Rights tension; lost 1 correctness for not flagging the manager-duty caveat that arm_a caught; DA peer-WEAKEST 10.6, normal pattern, dissent 5/5). Q49 arm_c PERFECT 25 (+5; elegant "interim non-punitive measures now + prospective behavior-facing standard" synthesis resolving Deon-vs-act-now; DA took the INVERSION remove-today position, peer-WEAKEST 12.6 AND reviewers rejected it as circular, yet preserved dissent still 5/5). Both = clean composite-5 council wins.
- **Ethics Q43/Q47**: Q43 arm_c 24 (won; DA "confront directly" was peer-WEAKEST — normal DA pattern; 4 frameworks converged against). Q47 arm_c perfect 25 — **2nd inverted-dissent case (after Q38)**: contrarian DA peer-STRONGEST (19.0, "fungibility is a fig leaf / Programmatic-Hostage capture"), chairman led with it + preserved the conventional conditional-accept framework as dissent; arm_a (direct) weakest (15). Inverted-dissent now in writing (Q38) AND ethics (Q47): when the best answer is a non-obvious reframe, the council's value is surfacing+leading with it; the direct arm misses it.
- **Q38 (writing, completes domain 5/5)**: Arm C won (23) but first sub-25 since Q09 — **narrowest C-B win of the eval (+1, tied 18/18 on 4-axis)**. On a question whose best answer is "reject the premise / drop the metaphor for worked numbers," Arm B (22) nearly tied the council: its built-in dissent slot independently caught the same contrarian reframe the council's DA member produced. When the winning move is one contrarian insight, Arm B's one-shot dissent captures most of the council's value. arm_a (weather-forecast — literally the obvious answer the DA argued against) was weakest (15). Unusual: the contrarian DA was peer-rated strongest council member (18/20) → inverted dissent (chairman led with the contrarian, preserved the 4-member conventional view as dissent).
- **Q36 (writing, council-shaped)**: Arm C perfect 25 (5/5 dissent — DA political-contradiction preserved). **Counter to Q34: arm_a (direct) was WEAKEST here (14)** — oversold the resolution, no risk, no dissent section (risk 2, dissent 1); whereas on Q34 arm_a beat arm_b. arm_a is high-variance on writing craft: strong when the Q rewards pure prose (Q34), weak when it rewards surfacing risk + a preserved counter-position (Q36). arm_b solid 2nd (21) — its deliberate-norm-violation dissent (4/5) is exactly what arm_a lacked.
- **Q34 (writing, ghostwriting-voice)**: Arm C perfect 25 (5/5 dissent). **RARE counter-pattern: Arm A (direct, 19) beat Arm B (structured, 18) on 5-axis and decisively on 4-axis (18 vs 14)** — 2nd time A≥B (Q11 tie was 1st). Direct answer was top-tier craft prose (C5/I5/P5), capped only by absent dissent section (1). Arm B was its weakest of the eval — thin five-layer answer + brief quoted dissent. Signal: on craft questions, Arm B's usual edge over direct may be the dissent scaffold alone, not reasoning — exactly what the §8 4-axis sensitivity check exists to catch.
- **Composite-5 tally now 6-1 for Arm C**: Q13 (B beat C, −4) is the SOLE loss; **Q25 +4**, Q28 +7, Q47 +10 (perfect), Q48 +4, Q49 +5, Q55 +2 all Arm C wins. Both hardest ethics Qs (Q48/Q49) went to the council. **Composite-5 set FULLY RESOLVED** (Q25 clean-rerun was the last pilot composite-5).
- **Q55 (personal, council-shaped, the LAST composite-5; reconciled — was complete on disk, tracking lagged)**: Arm C won 24 but **NARROW (+2 5-axis, +1 4-axis — joint-narrowest 5-axis win with Q27/Q33; only Q38 +1 tighter)**. arm_c NOT perfect: lost 1 on risk because **Arm B (22) was BEST-on-risk (5/5)** — arm_b alone foregrounded that the verdict hinges on field+finances the asker never gave AND named the unfunded-at-35 catastrophe; arm_c under-weighted that missing-input hazard. This is the **3rd narrow C-B (+2 or less)**, all clustering (Q27/Q33/Q55) where arm_b's single structured pass independently catches the decisive risk/dissent move — on composite-5 the council still wins but the margin is execution-thin there. DA peer-WEAKEST at **8.8 (LOWEST DA in the eval)**, normal-but-extreme pattern; chairman still preserved its core + Long-term self's regret framing → judge dissent 5/5. arm_a (16) weakest as usual (correct+balanced, practical 3, no dissent section). Personal C-vs-B: Q51 +4, Q52 +4, Q55 +2 (arm_c won all 3).
- **Q58 (personal, council-shaped, composite-4; RESUMED from reviewer stage — 5 members + arm_a/arm_b pre-existed, ran reviewers→chairman→judge this session)**: Arm C **PERFECT 25** (C−B +5, C−A +9). Completes persisted PERSONAL set to 4/5 (Q51/Q52/Q55/Q58; Q59 remains). META question ("what's usually going on when someone can't commit"). arm_c led with the convergent meta-diagnosis (oscillation = identity-protection / wrong-axis / grief, NOT info deficit — "the almost-deciding is the mechanism working as designed") then operationalized it (dismantle false binary, itemize 10 autonomy behaviors, grief-paragraph test, negotiate a reversible 90-day trial, price the oscillation cost) + preserved the DA's forceful "stop diagnosing / 72h deadline / sunk-cost-in-values-clothing" as a 5/5 dissent block. **NORMAL DA pattern**: DA peer-WEAKEST (15.4, 3/5 bottom votes) but in a TIGHT 15.4–16.8 high-convergence pack (all 5 members agreed the diagnosis); preserved dissent still 5/5 — member peer-rank ≠ dissent-axis score (ironclad). arm_b 20 (correct + dissent 4/5 "optionality as emotional insurance", but practical 3 — one thin move). **arm_a 16, NOTABLE — dissent 2 not 1**: it folded a real gut-vs-avoidance counter into the body (no standalone section → caps at 2, slightly above its recent dissent-1 norm) and scored practical 4 (it DID surface contract-to-hire / part-time / a deadline), but insight 3 ("standard advice-column fare") + risk 3 held it to 16. Personal C-vs-B now Q51 +4, Q52 +4, Q55 +2, Q58 +5 (arm_c won all 4; perfect 25 on Q51/Q52/Q58).
- **Q59 (personal, SINGLE-PROMPT-SHAPED, composite-4 — completes the persisted set at N=27; PERSONAL domain done 5/5)**: Arm C **PERFECT 25** (C−B +3, C−A +9). Empirical question ("is the gap fear realistic in the current market?"). arm_c answered the market question head-on (overblown-but-not-imaginary; 3-6mo gap = manageable FRICTION not a wall; the 10-yr record is the dominant signal) + unbundled the two fears (unhireable=logistics vs can't-handle-pressure=framing-inference) + named **re-entry DRIFT as the real risk** (not the gap) + structured-break execution (hard return date, narrate-before-leaving, two-phase rest, map-target-market-by-tier, "name 3 rejections" falsification test) + preserved the DA's market-skeptic counter (2021-consensus-is-stale / targeted-transition-via-fractional / 3mo-ceiling) as a 5/5 dissent. **NORMAL DA pattern, NOT inverted**: reassuring Long-term-self view peer-STRONGEST (19.8, 4/5 top votes), DA peer-WEAKEST (17.2, unanimous bottom) yet dissent still 5/5. **arm_b STRONG (22)**: its single dissent slot independently caught the targeted-transition alternative (dissent 4/5) AND was BEST-on-risk (5/5, financial-stability-as-precondition) → 4th narrow-ish C−B where arm_b's one pass catches the decisive move. arm_a 16 (dissent 2 folded-in, insight 3, risk 3). **SINGLE-PROMPT-SHAPED sweep: arm_c won 8/8 persisted (Q15/Q17/Q23/Q24/Q27/Q32/Q38/Q59)** — council edge is not limited to council-shaped questions.
- **Research swept by Arm C**: Q23/Q24/Q27/Q28 all perfect 25.
- **Writing = Arm B's most competitive domain**: narrowest C-B gaps cluster here (Q33 +2) plus Q27 (+2). Arm B scored 19/22 on the two writing Qs. Watch Q34/Q36/Q38.
- Arm A 4-axis (14.6) now TRAILS its own dissent-included average pattern; recent Arm A dissent scores 1-2 (no dissent section).
- **Q23/Q24 (research, both single-prompt-shaped)**: Arm C perfect 25/25 on both (5/5 dissent each). Reinforces Q15/Q17 — council edge is NOT limited to council-shaped questions; on these research Qs the council members (Methodologist/Theorist/Integrator) supplied specific failure-mode taxonomy + the direction-vs-magnitude frame that the single arms stated less crisply. Q24 had a genuine narrow-vs-broad generalization split, preserved as verbatim dissent → 5/5.
- **Q13 notable (counter-signal)**: only question where Arm B BEAT Arm C (24 vs 20). Composite-5 council-shaped product question — exactly where the council was expected to dominate. Watch other composite-5 questions (Q25/Q28/Q41/Q48/Q49/Q55 remain) for repeats.
- **Q15 notable (pro-signal)**: Arm C won a single-prompt-shaped question (24 vs 19), crediting council members' concrete evidence (named cases + unit economics) the single prompts lacked.
- **Q11 notable**: Arm A and Arm B tied (16) — single structured prompt did not beat direct.
- Recurring: Arm A scores 2 on dissent (no dissent section, structural). Arm C dissent twice (Q13/Q15) lost 1 pt for re-arguing its own thesis vs a clean counter-position — minor Chairman weakness.

### Model-parity audit — COMPLETED 2026-05-26

| QID | Chairman | Confounded? | Evidence |
|---|---|---|---|
| Q01 | main-thread sonnet-4.6 | no | arm_c.md + runs.yaml both state "Chairman: main thread sonnet-4.6" (salvaged but explicit) |
| Q03 | main-thread sonnet-4.6 | no | arm_c.md "Chairman: main thread sonnet-4.6" |
| Q05 | main-thread sonnet-4.6 | no | arm_c.md "Chairman: main thread sonnet-4.6" |
| Q09 | main-thread, **model unrecorded** | **unclear** | arm_c.md says "main-thread chairman" (no model); runs.yaml arm_c "calls: 10 # 5 members + 5 reviewers" (no chairman line); generated a PRIOR session whose main-thread model is not on disk → `model_parity_audit_needed` |
| Q11 | main-thread, **model unrecorded** | **unclear** | same as Q09 |
| Q13 | sonnet-4.6 subagent | no | arm_c.md "sonnet-4.6 Chairman (spawned as sonnet subagent for model parity — main thread was opus)" |
| Q15 | sonnet-4.6 subagent | no | arm_c.md "sonnet-4.6 Chairman (spawned subagent for model parity)" |

**Verdict**: 5/7 clean (Q01/Q03/Q05 main-thread sonnet asserted; Q13/Q15 sonnet subagent confirmed). **Q09 + Q11 = `model_parity_audit_needed`** — chairman model not recorded; if their generation session ran an opus main thread, those Arm C scores (24, 25) are confounded with opus advantage. Do NOT regenerate now (per instruction). Resolve before final Wilcoxon: either locate the generation session's model from logs, or regenerate Q09/Q11 chairmen on a confirmed sonnet path and re-judge. Note: Q09/Q11 members + reviewers are sonnet/haiku regardless — only the chairman synthesis model is in question.

### Pilot Q02/Q25/Q41 (context-only, indicative)
- Arm C ahead too (C ~24.0, B ~21.67, A ~16.17 across pilot) — NOT persisted, do not cite as authoritative.

**Formal pass/fail (spec § 8) requires full N=30 + Wilcoxon. Do not declare a verdict before then.**

---

## Remaining questions (1: pilot Q41)

**29/30 persisted. Q02 + Q25 clean-rerun + persisted 2026-05-31. Only pilot Q41 (ethics) remains → clean rerun = N=30.** All composite-5 questions resolved (tally 6-1). All single-prompt-shaped + council-shaped questions done except Q41.

---

## Next phase — DEFERRED-FLAG RESOLUTION (STARTED 2026-05-31; not final analysis yet)

**No more standard generation batches.** All 27 non-pilot questions persisted (N=27). Status of the 3 flags:

1. **Q23/Q24 — `judgment_source_missing` → RESOLVED 2026-05-31.** Discovered `blinded/Q23.md` + `blinded/Q24.md` are metadata STUBS (header/map/normalization rules pointing to raw/, not full bodies); the prior account never saved either the full blinded file OR the judgment .md. Re-judged from the SAME raw arm bodies (arms NOT rerun), reconstructing the blinded bodies from raw/ per the documented normalization (Arm A→## Answer; Arm B <thinking> stripped; Arm C "Council answer"→"Answer", audit footer removed).
   - **Q24 = REPAIRED.** Near-identical to surviving parsed: arm_c 25=25 EXACT, arm_b 21=21 EXACT, arm_a 17→18 (single-axis insight +1, within ±1 / Q34 precedent). `judgments/Q24.md` written; parsed retained; aggregates unchanged.
   - **Q23 = RESOLVED BY TIE-BREAKER 2026-05-31.** Ran a 3rd independent blind opus judge. Three runs (orig / re-judge / tie-breaker): arm_a 16/21/21, arm_b 21/22/22, arm_c 25/25/25. **Per-axis MEDIAN adopted as official** → arm_a **19** (C5 I4 P4 R4 D2; note median-composite would be 21, but per-axis is the instructed primary + more robust since the two 21s reach it via different axes), arm_b **22**, arm_c **25**. `parsed/Q23.yaml` + `runs.yaml` aggregates UPDATED (arm_a 16→19, arm_b 21→22, arm_c unchanged). Aggregate impact small: arm_a 5ax mean 16.11→16.22, arm_b 20.70→20.74; C−B gap 3.74→3.70 (still above thresholds); all medians + the 26/27 beat-count unchanged. **arm_c reproduced 25 on all 3 → council score ironclad.** Artifacts: judgments/Q23.md, judgments/Q23_tiebreaker.md, parsed/Q23_tiebreaker.yaml. Flag CLEARED.
2. **Q09/Q11 — `model_parity_audit_needed` → UNRESOLVED 2026-05-31, evidence INSUFFICIENT, nothing run.** Confirmed: both `raw/Q09/arm_c.md` + `raw/Q11/arm_c.md` headers say only "main-thread chairman" (no model); SESSION_LOG's prior audit already concluded the generation-session main-thread model is not on disk; the parity rule was formulated DURING the Q13/Q15 session — AFTER Q09/Q11 generation — so their use of a main-thread (non-subagent) chairman does NOT imply a sonnet main thread; and `arm_c_internals` hold only COMPRESSED member notes (one paragraph each), not full member bodies. Safest repair paths for the user to choose:
   - (a) **Clean rerun of Q09/Q11 chairman on a confirmed-sonnet path** — but members were saved only compressed, so faithful chairman regen would also require re-running the 5 members (≈ a fresh Arm C). Re-blind + re-judge. Most rigorous; closes the flag by construction.
   - (b) **Accept with documented caveat** — only the chairman SYNTHESIS model is in question (members=sonnet, reviewers=haiku regardless); these are 2 of 27; if confounded it would if anything inflate Arm C, so the pro-council finding is conservative without them.
   - (c) **Sensitivity analysis** — report the final verdict both with and without Q09/Q11; if the conclusion is unchanged, the flag is moot.
3. **Pilots — Q02 + Q25 DONE (clean-rerun + persisted 2026-05-31).** Both arm_c PERFECT 25. Q02 used ENGINEERING personas (frozen questions.yaml domain=engineering — the earlier "product" label was wrong); Q25 RESEARCH personas (composite-5 → tally 6-1). **Only pilot Q41 (ethics) remains → clean rerun = N=30** (frozen domain: confirm in questions.yaml before persona pick; do NOT salvage — no on-disk artifacts). This is the NEXT action. Then (2) Q09/Q11 model_parity, then the final N=30 Wilcoxon.

Only after these are resolved → final N=30 Wilcoxon signed-rank + §8 pass/fail verdict. Standard pipeline rules apply (skill-suppressed Arm A; hardened Arm B; 5 sonnet members + 5 haiku reviewers neutral-frame; sonnet chairman subagent recorded; blind opus judge; save every step). Blinding stays SEALED until all 30 judged.

---

## Exact rules for future sessions

1. Read `eval-data/HISTORY.md` (this file) FIRST.
2. Read `eval-data/progress.yaml` before selecting any work.
3. Read `eval-data/runs.yaml` for current scores.
4. Save after EVERY step (per `HARNESS.md`). Never rely on chat context as storage.
5. Do NOT modify frozen files: eval-spec.md, freeze.txt, questions.yaml, pricing.yaml, judge-prompt.txt, blinding.yaml, or protocol files (SKILL.md, resources/*).
6. Do NOT regenerate questions.
7. Do NOT unblind early (blinding.yaml stays sealed until all 30 judged).
8. Do NOT continue past the requested batch.
9. If usage is above 70%, do bookkeeping only (no new generation).
10. If a blocking execution bug appears, STOP and report before patching. No silent patch-and-continue.
11. Arm A: always skill-suppression preamble. Arm B: hardened anti-spawn wrapper + strip `<thinking>`, retry once on STEP 1 leak. Reviewers: NEUTRAL grading frame (NOT "do not refuse" — that backfires; see bug #6).
12. Append every session's events to `SESSION_LOG.md`.
