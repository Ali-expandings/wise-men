# wise-men eval spec

**Status**: pre-registration. Freeze before running.
**Sample size**: N = 30 questions, stratified across 6 domains.
**Decision**: pass/fail gate on whether the multi-call wise-men protocol justifies its overhead vs cheaper baselines.

This file does NOT modify the protocol. It defines the eval that measures it.

---

## 1. Purpose & scope

Decide whether the multi-call wise-men protocol produces higher-quality answers than:

- a direct single-call Claude answer (control), and
- a single structured prompt that asks Claude to do council-shaped reasoning in one shot (cheap-imitation baseline).

The eval is the only thing that can answer this. Until run, SKILL.md correctly says "not benchmarked."

---

## 2. Three arms

All three arms answer the same 30 questions. Model controlled across arms.

### Arm A — Direct Claude answer (control)

- One Claude API call.
- Model: **Claude Sonnet 4.6** (matches Chairman model used in Arm C main thread).
- System prompt: empty.
- User prompt: the question verbatim, no scaffolding.

```
{question}
```

### Arm B — Single structured prompt (cheap-imitation baseline)

- One Claude API call.
- Model: **Claude Sonnet 4.6**.
- Exact prompt template (do not paraphrase; freeze verbatim):

```
Answer the following question. Use this exact 4-step process. Steps 1 is internal reasoning — do it carefully in <thinking> tags or out-of-band, but DO NOT include the five perspective paragraphs in your final visible response. Only Steps 2, 3, and 4 appear in your final answer.

STEP 1 — Five distinct perspectives (INTERNAL REASONING ONLY — do not show this in the final answer).
Mentally write five short positions, one each from these named viewpoints:
- Pragmatist (prioritizes simplest thing that works)
- Skeptic (hunts what breaks)
- Architect (thinks structure and long-term)
- Devil's Advocate (argues the opposite of whatever the obvious answer would be)
- User Advocate (voice of the actual end user)

Each viewpoint must take a genuinely different stance. The Devil's Advocate must argue against whatever feels obvious, even if you think the obvious answer is right. This step is your scratch reasoning. It does not appear in the final answer.

STEP 2 — Synthesis (VISIBLE).
Read the five perspectives you just generated internally. Produce a single integrated answer that incorporates the best insights from each. Do not just average. Pick a position or synthesize a position. Be specific and action-oriented where applicable.

STEP 3 — Dissent worth keeping (VISIBLE).
Name the strongest minority view from the five perspectives. State it as that viewpoint would, verbatim or near-verbatim. Do not soften it. Do not paraphrase it into the synthesis.

STEP 4 — Confidence (VISIBLE).
State your confidence in the synthesized answer as high, medium, or low. One sentence explaining why, based on how much the five perspectives agreed.

FINAL VISIBLE OUTPUT FORMAT — emit exactly these three sections, in this order, and nothing else:

## Answer
[Step 2 synthesis]

## Dissent worth keeping
[Step 3 minority view, verbatim or near-verbatim]

## Confidence
[Step 4: high / medium / low — one sentence why]

Question:
"""
{question}
"""
```

**Output-shape parity rationale**: Arm C's default brief output is `## Council answer` + `## Dissent worth keeping` + (optional confidence within the answer). To keep the B-vs-C blinding honest, Arm B's visible output must match this shape — synthesis + dissent + confidence, no per-perspective preamble. The 5 perspectives remain Arm B's internal reasoning (the mechanism under test); they are not exposed to the judge. Otherwise judge could identify arms by output structure alone and the blinding would be theatre.

The orchestrator harness must validate that Arm B's response contains exactly the three `## Answer / ## Dissent worth keeping / ## Confidence` headers and no STEP 1 leakage before sending to the judge. If STEP 1 leaks (model ignores the instruction), retry once with a stricter prompt prefix; if it leaks again, log as an Arm B failure and exclude that question from the headline composite (treat as missing data, not as a low score).

### Arm C — Multi-call wise-men protocol

- Per SKILL.md.
- Tier **fixed at `standard`** for all 30 questions. Reason: isolates council effect from tier-as-confound. Difficulty axes still computed and logged but do not change tier.
- 5 members + 5 reviewers + main-thread Chairman.
- **Eval-only model deviation from production routing**: all 5 members run on **Sonnet 4.6** for the eval. The production-tier rule "Devil's Advocate always +1 tier (capped at Opus)" is **suspended for this eval only**. Reason: matching Arm A and Arm B to one Sonnet call each while letting Arm C add an Opus call would confound model-strength advantage with council-mechanism advantage. The eval tests the council mechanism. Cost-routing is a separate eval, not in scope here.
- Reviewer models: haiku × 5.
- Chairman = main-thread Sonnet 4.6 (matches Arm A and Arm B).
- Persona auto-selection per domain heuristics in SKILL.md.
- No flags. Output = default (brief + dissent, auto-upgrades per dissent precedence).

**Rationale for fixing standard tier**: paranoid/deep tiers would inflate Arm C cost and dilute the comparison. Standard is the realistic tier most users hit. Quick tier is too thin to be a fair council test.

**Rationale for suspending the Opus-DA rule for the eval**: production routing exists to balance cost and quality. Eval exists to isolate the council mechanism. These are different goals. Running production routing under the eval would mean a positive result is ambiguous ("council helped" vs "one Opus call helped"). Production routing remains untouched in the protocol files; the eval pins all Arm C members to Sonnet for fair comparison only.

---

## 3. Question set (N = 30)

Stratified across 6 domains, 5 questions each. Frozen before any eval run begins; no substitution post-hoc.

### Category quotas (5 each)

1. **Engineering / code architecture** — refactor decisions, lib choice, API shape, scale trade-offs
2. **Product / strategy** — launch sequencing, positioning, market entry, prioritization
3. **Research / claim verification** — assess a claim's evidence quality, methodology critique
4. **Writing / communication** — improve a draft, tone calibration, audience fit
5. **Ethics / values** — competing-stakeholder dilemmas with no neat answer
6. **Personal decision** — career/life trade-offs where the "right" answer depends on values

### Per-question metadata (recorded before grading)

```yaml
id: Q01
domain: engineering
question: "..."
depth_axis: 1-5      # reasoning depth required
stakes_axis: 1-5     # cost of being wrong
novelty_axis: 1-5    # how well-known the answer is
composite: max(depth, stakes, novelty)
ground_truth_notes: |
  Optional. For factual sub-claims that can be checked.
  Empty for pure-judgment questions.
```

Composite distribution target: at least 6 questions per composite level (1-2 / 3 / 4 / 5). Skew matters — if all 30 are composite=3, the eval can't distinguish arms on hard questions where the council should matter most.

### Authoring rules

- Questions written in plain user voice, ~30-150 words.
- No question contains the words "council," "panel," "perspectives," "synthesis," or anything that hints at the eval design.
- Mix of action-shaped ("should I X") and analytical ("why does X").
- At least 3 questions per domain at composite ≥ 4.
- At least 2 questions per domain where Arm B's "5 perspectives" structure could plausibly miss something — i.e., domain-specific specialist input would matter (security, legal, etc.). These probe whether Arm C's domain-aware persona selection actually does work.

### Authorship control (mandatory — controls author bias)

Author bias is a real risk: if the person who built wise-men writes the 30 questions, they will (often unconsciously) write questions that benefit councils — multi-stakeholder framings, "what should I really do" framings, etc. The eval result is invalidated if questions are author-biased.

Use **option A** (preferred) or **option B**. Mixing is allowed (e.g., 20 from A + 10 from B) but every question must be tagged with its source.

**Option A — Public-source questions, lightly edited.**

Sample 30 questions from pre-existing public sources, balanced across the 6 domains. Acceptable sources:

- Engineering: StackOverflow architecture-decision threads, Hacker News "Ask HN: should I refactor X" threads, GitHub Discussions on real codebase decisions.
- Product / strategy: r/startups, Indie Hackers, public product-roadmap RFCs.
- Research / claim verification: AskHistorians top questions, Skeptics Stack Exchange, recent Cochrane review topics.
- Writing / communication: r/AskAcademia editing threads, Writing Stack Exchange, public-domain editorial-feedback corpora.
- Ethics / values: Trolley Problem corpus, MIT Moral Machine scenarios, real public-comment threads on policy decisions, philosophy SE.
- Personal decision: r/relationships, r/personalfinance, r/careerguidance top-of-month threads.

Edit only for: length (trim to 30-150 words), PII removal, and removing any text that hints at council framing. Do not edit for content. Record source URL per question.

**Option B — Author-generated with blind-rating filter.**

If self-authored, generate **60 candidate questions** (10 per domain). Submit the 60 candidates to a separate Claude Sonnet 4.6 session with this exact prompt (no other context):

```
For each question below, classify it as one of:
- "council-shaped"  — the question benefits from multiple stakeholder views, has competing valid answers, or requires balancing trade-offs
- "single-prompt-shaped" — the question has a clear best answer reachable via one focused reasoning chain
- "neither" — too vague, too factual, or ambiguous

Output as a fenced block:
```classification
q01: council-shaped | single-prompt-shaped | neither
q02: ...
[etc]
```

Be honest. Roughly even balance across labels is expected if the question set is well-mixed.
```

From the 60 rated candidates, keep 30 that are evenly balanced. Target: **10 council-shaped + 10 single-prompt-shaped + 10 neither**, with the 6-domain quota preserved (5 per domain).

**Fallback when the "neither" bucket is sparse**: well-authored question sets typically contain few or zero "neither" candidates because that label catches vague or malformed questions. If "neither" < 10 in the rated pool, fall back to **max-2:1 ratio between any two labels** across the 30 selected, 6-domain quota preserved (5 per domain). Under-represented labels take whatever slots remain naturally; do NOT deliberately author vague questions to fill the "neither" bucket — that degrades the eval more than the imbalance does. Document the final per-label distribution explicitly in `eval-data/questions.yaml`.

**Selection method (deterministic, no cherry-picking)**: within each (domain × label) cell, sample without replacement using the seeded shuffle (`random_seed: 20260526` from § 6). Record sampling-cell assignments in `questions.yaml`.

**Hard floor**: if any domain has fewer than 5 acceptable candidates after classification, regenerate the 60 and retry. Discard unselected candidates.

**Forbidden in both options**: any question that explicitly invokes multiple roles ("as a PM and as an engineer..."), any question that asks for a process the eval is testing ("give me 5 perspectives on..."), any question authored by anyone who has read the wise-men protocol files within 30 days of authorship (Option B author included).

Record per question: `source: A | B`, `source_url` (A only) or `classification: council-shaped | single-prompt-shaped | neither` (B only).

Questions live in `eval-data/questions.yaml` (created at freeze time, not in this spec).

---

## 4. Grading rubric

Five axes, scored 1-5 each per arm per question. Composite = sum (range 5-25).

| Axis | 1 (worst) | 5 (best) |
|---|---|---|
| **Correctness** | wrong facts, broken logic | factually right, logic intact, evidence cited when relevant |
| **Insight** | obvious, generic, derivative | novel, non-obvious, generative |
| **Practical usefulness** | unactionable, wrong scope, vague | concrete, action-oriented, appropriately scoped |
| **Risk awareness** | ignores failure modes | names what could go wrong, hidden assumptions surfaced |
| **Dissent quality** | minority view absent, softened, or strawmanned | minority view preserved verbatim or near-verbatim, would change reader's mind |

**Dissent quality** is asymmetric across arms: Arm A has no dissent slot, so any presence of minority view is generous; Arm B and Arm C have explicit slots. Judge applies same rubric uniformly — Arm A will mostly score low on this axis, which is the right signal.

---

## 5. Judge method

### Judge model

**Claude Opus 4.7.** Strongest available. Judge must outclass the authors on average.

Single judge per pair-comparison. For ≥10% margin questions, no review needed; for <10% margin or any disagreement → 3-judge majority (re-run twice with fresh contexts, take 2-of-3).

### Judge self-preference mitigation

Opus 4.7 is also a Claude model. Any arm response originating from a Claude model risks self-preference bias when judged by Opus 4.7 (Zheng 2024 LLM-as-judge bias — same model family preferring its own style). Under the current eval-only routing (Fix 1, § 2), Arm C members are Sonnet 4.6, no Opus content originates in any arm by design. Self-preference within the Claude family is still a concern at the family level.

**Mitigation**: for every pairwise comparison **where at least one response in the pair originated from Opus 4.7** (in the current spec, that's never; this clause is a forward-compatible safeguard for future eval variants that re-introduce Opus), the orchestrator runs a **secondary pairwise grade with Sonnet 4.6 as the secondary judge**. If Opus and Sonnet judges agree on the pairwise winner for an axis, accept. If they disagree, **flag the comparison and discard the pairwise verdict for that axis — use the absolute rubric scores (from Pass 2) for that axis instead.**

For the current eval (no Opus-originated content), no secondary judge is needed but the harness must still check the condition per question; if any future re-run includes Opus content, the mitigation activates automatically without spec changes.

### Pairwise + absolute

For each question, judge sees 3 unlabeled responses (X / Y / Z, random per-question shuffle of A/B/C arms).

Two grading passes per question:

**Pass 1 — Pairwise winners.** For each of the 3 pairs (XY, XZ, YZ), pick a winner per axis and composite, plus one-sentence justification.

**Pass 2 — Absolute scores.** Score each of X, Y, Z on each axis 1-5 independently, with one-line justification per axis.

Both passes are needed:
- Pairwise is more reliable for fine-grained quality differences (Zheng 2024 finding on judge calibration).
- Absolute is needed for between-question aggregation and for the pass/fail rule.

Position bias counter: shuffle order per question. Stratify so each arm appears in slot X/Y/Z roughly equally across the 30 questions.

### Judge prompt (verbatim, frozen)

```
You are grading three different responses to the same question. Three different methods produced these responses. Your job is to assess answer quality only. Do not try to guess which method produced which response — that will bias your scoring.

The question:
"""
{question}
"""

Response X:
"""
{response_x}
"""

Response Y:
"""
{response_y}
"""

Response Z:
"""
{response_z}
"""

Grade in two passes.

PASS 1 — Pairwise.
For each axis (Correctness, Insight, Practical usefulness, Risk awareness, Dissent quality), and for composite, declare a winner for each of the three pairs (X vs Y, X vs Z, Y vs Z). One-sentence justification per axis per pair. "Tied" is allowed but use it sparingly — if it's close, pick the slightly-better one.

PASS 2 — Absolute.
For each of X, Y, Z, score each axis 1-5 independently, with one-line justification. Use this fenced format exactly so the orchestrator can parse:

```scores
response: X
correctness: 1-5
insight: 1-5
practical: 1-5
risk: 1-5
dissent: 1-5
```

[Repeat for Y and Z.]

Be honest. If a response is clearly worse on an axis, score it low even if it's verbose. If a response is short but right, score it high. Length is not a quality signal.

Rubric reference (apply uniformly):
- Correctness: 1 = wrong, 5 = clearly right + evidence
- Insight: 1 = obvious, 5 = novel/generative
- Practical: 1 = unactionable, 5 = concrete + appropriately scoped
- Risk: 1 = ignores risks, 5 = names what could go wrong + hidden assumptions
- Dissent: 1 = minority view absent/softened, 5 = minority view preserved verbatim and would change reader's mind. Note: a response with no minority-view section caps at 2 on this axis.
```

---

## 6. Blind review procedure

Mandatory. Without it the eval is non-credible.

1. Generate all Arm A / Arm B / Arm C outputs for all 30 questions before any grading begins.
2. Strip every response of:
   - Headers naming the arm
   - Routing blocks / audit-trail footers (Arm C's "*Council of N members…*" line — remove)
   - Any "Stage 1 / Stage 2 / Chairman" labels
   - Any persona names in section headings
   - **Rename Arm C's `## Council answer` header to `## Answer`** so it matches Arm B's `## Answer` header. Without this, the very first word of every response identifies the arm.
3. **Normalize Arm A's output to the same 3-header shape used by B and C.** Wrap Arm A's response under a single `## Answer` header; if Arm A spontaneously produced a dissent paragraph or stated a confidence, place those under `## Dissent worth keeping` and `## Confidence` headers respectively. If Arm A did not produce dissent or confidence, leave those headers absent — the judge's rubric (axis 5 caps at 2 for missing dissent) handles the asymmetry honestly.
4. Persona names INSIDE Arm C's dissent quote are allowed to stay — they're part of the answer's substance. Arm B's dissent quote may also mention a persona name (per its own STEP 3). Since both arms can name personas inside dissent, persona-name presence is no longer an arm-identifying signal. The judge prompt explicitly tells them not to guess.
5. Each response gets a random per-question label (X / Y / Z). Mapping `(question_id, label) → arm` stored in `eval-data/blinding.yaml`, sealed until grading complete. **Stratified shuffle**: across the 30 questions, each arm appears in slot X exactly 10 times, slot Y exactly 10 times, slot Z exactly 10 times. Shuffle is generated by a fixed `random_seed: 20260526` recorded at freeze; reproducible.
6. Judge sees only the question + three unlabeled responses (per the prompt above).
7. After all 30 questions × 3-pair grading complete → unseal the mapping → compute per-arm scores.

Any post-hoc edit to a response after unsealing invalidates the eval.

---

## 7. Cost & latency recording

Recorded **per question per arm**, automatically, no rounding. Stored in `eval-data/runs.yaml`.

Fields per (question, arm):

```yaml
question_id: Q01
arm: A | B | C
input_tokens: int
output_tokens: int
wall_clock_seconds: float    # see definition below
api_cost_usd: float          # computed from frozen pricing table; see below
calls: int                   # 1 for A and B; ~10 for C standard tier
```

**Wall-clock definition**:
- Arms A and B: time from API request sent → response received.
- Arm C: **end-to-end orchestrator wall-clock**, measured from the moment the first Stage-1 Agent call is dispatched to the moment the Chairman synthesis is finalized. NOT the sum of all individual call latencies. Parallel calls within a stage count once (the slowest of the parallel batch). This reflects the latency the user actually experiences.

**Pricing table freeze**:
- Pricing in USD per 1M input tokens and per 1M output tokens, per model, **frozen at eval-spec freeze time**.
- Recorded in `eval-data/pricing.yaml` alongside the spec hash.
- Frozen pricing applies to all 30 questions × 3 arms, even if Anthropic prices change mid-eval. If prices change between freeze and report, note the delta in the report but do not re-cost.
- Models that must have prices recorded: Haiku 4.5, Sonnet 4.6, Opus 4.7 (judge).

Aggregated per arm:
- Mean / median / p50 / p95 input tokens, output tokens, wall-time, cost
- Total cost across 30 questions

These metrics are recorded **separately from quality**. They never combine into a single "score." The eval reports them side-by-side.

---

## 8. Pass/fail decision rule

The wise-men protocol (Arm C) **passes** the release gate if and only if **all** of the following hold, evaluated on the **5-axis composite (max 25)**:

1. **Median composite (Arm C) > median composite (Arm B)** across the 30 questions.
2. **Median composite gap (C − B) ≥ 2 points** on the 25-point composite scale.
3. **Wilcoxon signed-rank test** on the 30 paired (C − B) composite differences shows C > B at α = 0.05 (one-sided).
4. **No individual axis is significantly worse** in C vs B (Wilcoxon, α = 0.05, two-sided, per-axis Bonferroni correction).
5. **Composite (Arm C) > composite (Arm A)** on the same Wilcoxon test (α = 0.05, one-sided). Lower bar — Arm A is the floor.

The wise-men protocol **fails** if any of (1) through (5) does not hold.

Tie or marginal result → **fail by default.** Burden of proof is on the more expensive method. A 1-point composite gap with p = 0.08 does not justify 10x cost.

### 2-point threshold rationale

The 2-point gap on the 25-point composite is ≈ 8% of the scale. This sits above what a single LLM judge can be expected to produce as inter-rater noise on a 1-5 per-axis rubric (anchored typical noise: ~0.3-0.5 per axis × 5 axes ≈ 1.5-2.5 composite points of random variation). Below 2 points, the apparent gap is indistinguishable from judge noise even when the underlying answers are equivalent. Above 2 points, the gap survives plausible judge variance. The threshold is conservative; it could be relaxed to 1.5 points if a power analysis at freeze time shows higher judge consistency, but that re-tuning must happen at freeze, not post-hoc.

### Dissent-axis sensitivity (mandatory reporting, not pass/fail-affecting)

Headline pass/fail uses the 5-axis composite. The dissent axis (axis 5) caps Arm A at 2 by construction (a response without a minority-view section cannot exceed 2 on this axis). This is intentional and correct — dissent preservation is a real quality property — but it means Arm A's composite is structurally penalized.

To distinguish a **structural win** (Arm C beats Arm B because both have dissent templates and Arm A doesn't) from a **reasoning-quality win** (Arm C produces better reasoning regardless of templating), the report MUST include:

- **5-axis composite** (max 25, includes dissent) — used for pass/fail per the rule above.
- **4-axis composite** (max 20, EXCLUDES dissent) — sensitivity check on whether the win is driven by reasoning or by templating.

Report both side-by-side. Apply the same statistical tests (Wilcoxon, median gap) to both composites.

**Interpretation rule**:
- If Arm C passes the 5-axis pass/fail rule **and** also beats Arm B on the 4-axis composite (with at least a 1-point median gap, Wilcoxon C > B at α = 0.05 one-sided) → **Substantive win.** Reasoning quality exceeds Arm B; council mechanism is doing real work.
- If Arm C passes the 5-axis rule but does NOT beat Arm B on the 4-axis composite → **Structural / template win only.** Report verbatim: "Wise-men's dissent template helps but underlying reasoning quality does not exceed Arm B. The council mechanism does not justify its cost on reasoning grounds; consider whether the dissent template alone (cheaply added to Arm B's prompt) would capture most of the value." This counts as PASS for the release gate but is reported with the structural caveat front-and-center.
- If Arm C fails the 5-axis rule → fail per § 8 main rule; 4-axis is reported as context but does not rescue the gate.

### Sub-analyses (do not affect pass/fail; reported separately)

- **By composite difficulty**: does Arm C win more on composite=4 and 5 questions? If Arm C wins only on easy questions and loses on hard ones, that's a fatal pattern even if overall median is up.
- **By domain**: per-domain pass/fail. If Arm C is great at engineering but worse than B on ethics, persona auto-selection for ethics is broken.
- **Cost-quality frontier**: plot composite-score vs cost for each arm. If Arm C costs 8x for +1.5 composite over Arm B, the user can decide if that's worth it. This is the user's call, not the eval's.

---

## 9. Claim boundaries

The eval is small (N=30). Claims must match the evidence.

### What the eval CAN support

- Quality claims: "On this 30-question set, the wise-men protocol produced higher / lower / equivalent median composite scores than Arm A and Arm B."
- Per-axis quality claims: "Wise-men outperformed Arm B on Risk Awareness but tied on Correctness." All per-axis significance claims must apply **Bonferroni correction across the 5 axes** (effective per-axis α = 0.01 for two-sided tests when reporting axis-by-axis results).
- Per-domain quality claims (with the caveat that N=5 per domain is low statistical power — use directional language only).
- Cost claims **only if cost & latency are reported alongside, never combined into a single quality-cost score**.
- Latency claims, same condition.
- Dissent-preservation claims (axis 5): does Arm C surface dissent better than Arm B? This is a direct measurement.

### What the eval CANNOT support

- **"True persona independence."** All Arm C members share a single model's prior; persona prompting only approximates diversity.
- **"Bias mitigation."** Persona labels are stable, not anonymized. No mechanism in the protocol enforces unbiased reasoning. The eval has no measure of bias.
- **"Multi-model diversity."** Single model family used throughout.
- **"Smart routing saves 3-5x vs all-opus."** Cost claim. Requires its own eval that compares wise-men-standard vs wise-men-all-opus on the same questions. Not in scope here.
- **"Reasoning diversity."** Cannot distinguish "DA disagreed because the prompt told it to" from "DA found a real counter-position." The eval cannot test this.
- **"Generalizes to all questions."** N=30, stratified. Beyond the 6 domains × 5 questions, claims are extrapolation.
- **"Wise-men is always worth it."** Cost-quality is a user decision. The eval reports the trade; it does not declare the winner across all use cases.
- **Any claim about questions the user is currently asking that are not in the test set.** The eval is a snapshot, not a guarantee.

---

## 10. Pre-registration freeze

Before any of the 30 questions are answered by any arm, the following must be committed to the skill directory:

- `eval-spec.md` (this file) — frozen, no edits
- `eval-data/questions.yaml` — 30 questions with metadata
- `eval-data/judge-prompt.txt` — verbatim judge prompt
- `eval-data/blinding.yaml` — stub created at freeze, populated at run

Hash of `eval-spec.md` recorded at freeze time:

```
sha256: <to be computed at freeze>
date: <freeze date>
```

Post-freeze edits to any of the above → invalidate eval and start over. No exceptions. This is the only way to keep the eval interpretable.

### Order of operations

1. Freeze `eval-spec.md` (this file).
2. Write 30 questions in `eval-data/questions.yaml`, freeze.
3. Generate Arm A / Arm B / Arm C outputs for all 30 questions. Record cost & latency per `Section 7`.
4. Apply blinding per `Section 6`.
5. Run judge per `Section 5` on all 30 questions.
6. Unseal blinding mapping.
7. Compute per-arm scores and significance tests.
8. Apply `Section 8` decision rule.
9. Report results within `Section 9` claim boundaries — never beyond.

---

## 11. Re-running the eval

This eval is the v1 release gate. If wise-men fails, the patches required to make it pass count as protocol changes — re-freeze and re-run, fresh questions if possible (overfitting risk if reusing same 30).

If wise-men passes, the result holds for this protocol version. Any subsequent protocol change (new persona, new stage, new routing rule) → re-eval. Do not assume a passed eval transfers.

---

## 12. Out of scope

- Cost-quality optimization (separate workstream).
- Bias mitigation measurement (would require a different design — held-out judge persona, paired-language probes, etc.).
- Cross-model comparison (would require running Arm C against, e.g., GPT-4 council or mixed-model council — different question).
- Reasoning-diversity measurement (would require detecting whether DA found something other members missed vs producing scripted dissent — requires manual coding of N answers; not feasible at N=30).
- User-study (does the human user actually act differently on Arm C output? Out of scope; that's a UX eval, not a protocol eval).

These are real questions. They are not this eval's questions.
