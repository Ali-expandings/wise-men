# Q23 Arm B raw output
# salvaged_from_context: false
# model: sonnet-4.6
# leakage_check: CLEAN — STEP 1 stayed inside <thinking>; visible output = exactly 3 sections. Hardened anti-contamination wrapper used (opus-session council-spawn risk). No retry.
# note: <thinking> block stripped during blinding.

[<thinking> block stripped during blinding — 5 internal persona positions: Pragmatist, Skeptic, Architect, Devil's Advocate, User Advocate + synthesis notes]

[VISIBLE OUTPUT — judge sees:]
## Answer

Take it seriously but conditionally — the gray literature presence alone isn't the failure mode, it's what the gray literature is *doing* to the estimate. Here are the actual failure modes ranked by severity:

**Failure mode 1 — Gray lit carries the whole effect.**
The single most important diagnostic: re-run the meta-analysis excluding gray literature studies. If the effect shrinks toward zero or the confidence interval crosses zero, the finding is built entirely on unpublished work. Reputable meta-analyses will present this sensitivity analysis explicitly. If they don't, that's a red flag, not the 50% figure itself.

**Failure mode 2 — Asymmetric gray lit search.**
"Gray literature search" is not a standardized procedure. A motivated reviewer can search conference abstracts in fields likely to produce positive results while ignoring domains where they expect nulls. Pre-registration of the search protocol (PROSPERO registration before data collection) substantially mitigates this; absence of pre-registration makes it nearly unfalsifiable.

**Failure mode 3 — Quality heterogeneity contamination.**
A registered clinical trial suppressed by a sponsor is epistemically worth more than twenty conference posters from grad seminars. If the meta-analysis treats these as equivalent, or if the gray lit skews toward low-n, student-sample, or non-peer-reviewed-instrument studies, effect size inflation from researcher degrees of freedom compounds across studies. Check whether the meta-analysis coded studies by quality tier and ran moderation by tier.

**Failure mode 4 — Missing moderation data forcing imputation.**
Gray lit studies often lack the methodological detail needed to code moderators accurately, so reviewers either impute or exclude — both introduce noise that artificially inflates variance or distorts subgroup estimates.

**Failure mode 5 (often missed) — Gray lit pushing effects in the wrong direction.**
The usual effect of including gray literature is that it *reduces* effect size estimates by 10–30%, because the file drawer contains null and weak results. If including gray lit in this meta-analysis *increased* the overall effect, that is a strong signal of quality contamination or selection bias in the gray lit search, not correction of publication bias.

**What to actually check in the paper:**
- Funnel plot: gray lit inclusion should make it more symmetric, not less
- Egger's test and trim-and-fill estimate
- Table or forest plot stratified by publication status — compare effect sizes for published vs. gray lit
- Whether search strategy was pre-registered
- What specific sources count as "gray literature" (ClinicalTrials.gov ≠ conference abstract ≠ dissertation)

## Dissent worth keeping

Meta-analyses that exclude gray literature are the ones with the known, documented bias — not the ones that include it. The file-drawer problem has been empirically demonstrated to inflate published-only estimates. If you reflexively discount this meta-analysis because half the studies are unpublished, you are doing the opposite of what the methodology is designed to prevent. The correct prior is that 50% gray literature inclusion reflects an unusually thorough search, not unusual sloppiness. The burden of proof is on showing the gray lit is *doing something wrong*, not merely present.

## Confidence

High — these failure modes are well-established in the meta-science literature (Ioannidis, Cochrane Handbook, GRADE framework) and the directional logic of each failure mode is straightforward.
