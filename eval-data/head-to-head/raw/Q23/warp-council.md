# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q23 | orchestrator: general-purpose/sonnet | run: 2026-09-18 (round 3, PREREG-3 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 118338 | tool uses: 4 | duration: 559s

## Council

No `run_agents` launcher in this harness, so each member ran as a direct, foreground, read-only subagent (no filesystem/web access, no file edits) — reasoning from domain knowledge only, independently, with no visibility into each other's answers. Cross-vendor model diversity (GPT/Codex, open-source) wasn't available in this harness — only Claude models were — so per the skill's own fallback rule, diversity came from three distinct model tiers paired with three non-redundant angles instead:

- **Opus** — methodological/statistical rigor reviewer (pooling models, heterogeneity, whether bias-detection tools still work here)
- **Sonnet** — practitioner/evidence-appraisal reviewer (checkable red/green flags, verification cost, context-dependent scrutiny)
- **Haiku** (weakest available model, used per the skill's "strongest remaining model" fallback since no third frontier or open-source model existed — noted as a real capability gap, not just a formality) — contrarian reviewer (steelman gray-lit inclusion, then find what survives the steelman)

## Recommendation

Don't discount it just because half the studies are unpublished — a deliberate gray-literature search is standard, bias-*reducing* practice (it's literally what Cochrane/PRISMA recommend to counteract the file-drawer problem), so the 50% figure alone isn't a red flag. But don't take the topline "significant" at face value either: treat it as provisional until two specific checks are done, which together do most of the work of turning "significant" into either "solid" or "fragile."

## Why

- All three council members converge on the same starting point: excluding unpublished studies is not the methodologically safe default, it's the biased one. Published-only literatures skew toward significant/positive results because that's what clears peer review; a gray-lit search is the field's standard corrective, not a shortcut.
- Convergent check #1, raised independently by all three: does the effect survive a **published-only or low-risk-of-bias-restricted sensitivity analysis**? If the paper doesn't report one, or reports one where the effect shrinks or loses significance, that's the single strongest sign the "significant" result is being carried by the harder-to-verify half of the evidence.
- Convergent check #2: do **published and unpublished studies show similar effect sizes**? Agreement is stronger evidence than either subset alone (it isn't just "exciting enough to clear review"); systematic divergence in either direction means the pooled point estimate is unstable and should be read as a range, not a fact.
- The statistical-rigor review adds a mechanical wrinkle worth knowing: random-effects pooling (the default model) gives relatively more weight to small studies, and gray lit skews small (theses, pilots, conference work) — so if any small-study effect is present, the "more careful" random-effects model can amplify it rather than guard against it. That cuts against the common intuition that random-effects is automatically the conservative choice.
- Source type matters more than the published/unpublished label itself: trial-registry or regulatory gray lit is often higher-quality than a journal article; industry-, advocacy-, or agency-funded gray lit can reintroduce the exact outcome-motivated selection that gray-lit searching was supposed to cure — "unpublished" is not a synonym for "disinterested."

## Tradeoffs and risks

Concrete failure modes, grouped:

- **Statistical mechanics that quietly inflate the estimate.** Standard heterogeneity estimators (e.g., DerSimonian-Laird) tend to understate between-study variance under real heterogeneity, giving a falsely tight/significant confidence interval unless a more robust adjustment (Hartung-Knapp-type) or a prediction interval is reported. Trim-and-fill — a tool often cited as reassurance — can adjust the pooled estimate in the *wrong* direction if the gray-lit skew is toward small, null-ish studies. A "fail-safe N" cited as a bias defense here is close to self-contradictory: it asks how many hidden null studies would overturn the result, inside a review whose entire premise is that it went and found them.
- **Retrieval isn't neutral.** "Gray literature search" spans everything from exhaustive trial-registry extraction to an afternoon on Google Scholar. Without a documented protocol (named sources, dates, search terms, a PRISMA-style flow diagram, ideally a dated pre-registration), you can't tell which end you're on — and the retrieval process itself is a fresh, non-random filter (who responds to author-contact requests, which institutions/languages get covered).
- **Duplication.** A thesis, a derived journal article, and a conference abstract from the same underlying dataset are much easier to double-count in gray lit than in an indexed published database — this artificially narrows the confidence interval and inflates the apparent evidence count.
- **Quality control gaps.** Risk-of-bias tools (RoB 2, ROBINS-I, GRADE) often can't be fully scored from thin gray-lit writeups. Missing information tends to get coded "unclear" and then quietly treated as neutral rather than flagged as genuinely unassessable — which specifically hides bias in the studies hardest to check.
- **Buried caveats.** A line like "effect was attenuated/non-significant when restricted to published studies" can sit in a supplement while the abstract headlines the full pooled number — the most decisive information often isn't in the part most readers actually read.

## Final call

Run this in order against the actual paper:

1. Check the methods section for a documented gray-lit protocol — named databases/registries, dates, search terms, a flow diagram, ideally pre-registration. A one-line mention of "gray literature was also searched" with no detail is a yellow flag.
2. Look for a published-only or low-risk-of-bias-only sensitivity analysis and whether the effect survives it. Highest-value check, usually minutes if it's reported at all.
3. Check whether the forest plot or results table breaks out effect size by publication status. Similar → reassuring. Divergent → treat the pooled estimate as a range, not a fact.
4. Identify what the "unpublished" studies actually are — trial-registry/regulatory data, dissertations, industry/advocacy reports, conference abstracts. That distinction predicts trustworthiness far better than the published/unpublished label does.
5. If a real decision (medical, financial, policy) rides on this and none of the above is resolvable from the paper, don't treat one meta-analysis as sufficient — look for an independent corroborating review before acting.

Confidence is high on checks 2 and 3 as the two highest-yield tests; lower on any single numeric verdict, since no field or specific paper was given — clinical/regulatory gray lit and advocacy-group gray lit carry very different risk profiles, and that distinction moves the read more than the 50% figure does.
