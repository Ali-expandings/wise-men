# Q23 Arm C Chairman synthesis
# salvaged_from_context: false
# chairman_model: sonnet-4.6 (spawned subagent — main thread was opus-4-8 this session; model parity preserved per spec §2 + HISTORY rule)
# council: 5 sonnet-4.6 members (Empiricist, Theorist, Methodologist, Integrator, Devil's Advocate) + 5 haiku-4.5 reviewers + sonnet-4.6 chairman subagent
# stage2 aggregate: Methodologist 16.6 (top), Integrator 15.2, Theorist 15.0, Empiricist 13.6, DA 12.2 (bottom). No severe-disagreement flag. Standard tier — no debate.
# reviewer note: 7/10 first-pass reviewer refusals (aggressive "do NOT refuse" framing tripped injection heuristic); all recovered via neutral grading-frame retry. Harness fix logged.

## Council answer

The single highest-value move: run the published-only vs full-sample comparison. If the effect survives in the published-only subset at roughly the same magnitude, confidence rises substantially. If the effect appears only because of the gray literature, the meta-analysis is doing exactly what you should worry about — it is load-bearing on the unpublished studies, and scrutiny should be severe.

Ranked failure modes, in order of concern:

1. **Selective gray retrieval is not file-drawer correction.** Gray search typically catches preliminary-positives (conference abstracts, dissertations of things that worked) rather than the true file drawer of never-written nulls. It replaces one non-random filter with a different non-random filter that likely leans positive. This is the most important failure mode because it is structural, not fixable by statistical adjustment.

2. **Effect size is probably inflated, CI is definitely too narrow.** Pooled N rises, so precision rises, but the N reflects study collection effort, not epistemic reliability. The narrow CI is false confidence. Treat the headline effect as an upper bound, not a point estimate.

3. **Funnel asymmetry becomes uninterpretable.** Once gray studies are added, funnel-plot symmetry and Egger's test lose their diagnostic value — you can select gray studies to fill the left side of the funnel and manufacture a symmetric funnel that passes Egger's test while real asymmetry remains. Trim-and-fill is also underpowered below ~20 studies and unreliable at high heterogeneity.

4. **Asymmetric quality floors.** Unpublished studies have no peer-review floor. A large-N flawed dissertation weighted by inverse variance can dominate the estimate. If quality was not assessed independently of results, inclusion decisions themselves become a source of bias.

5. **Heterogeneity masking.** I² likely jumps when gray is added. If I² >75%, the pooled effect is probably an artifact of averaging incompatible populations. Check whether the meta-analysis reports I² separately for published vs full samples.

6. **Gray search reproducibility is buried.** The methods section often buries whether the gray search used named databases, date ranges, languages, and explicit inclusion thresholds — or was a convenience sample of what the authors had network access to. Vague description = steep discount.

What to check in the paper:

- Does the forest plot break out publication status? If not, request it or treat the analysis as opaque.
- Is there a sensitivity analysis with published-only studies? Absence of this is a red flag.
- What exactly was the gray literature search protocol? Named databases (ProQuest Dissertations, SIGLE, ClinicalTrials.gov, WHO ICTRP), explicit search strings, language filters, author-contact attempts — all must be named. "We searched for gray literature" without specifics means a curated convenience sample.
- Did authors code reason for non-publication? Almost none do, but if they did, it changes interpretation substantially.
- Are quality/risk-of-bias scores reported separately by publication status? Do the gray studies cluster at lower quality?
- What is the p-curve of the published-only subset? That is the cleanest signal you have.

Treat the meta-analysis as hypothesis-generating until the published-only sensitivity check passes. If that check is absent from the paper, that absence is itself informative.

## Dissent worth keeping

The Devil's Advocate position deserves to be stated at full strength: "Gray literature = junk" is itself a documented bias, and including unpublished studies is methodologically correct because it combats publication bias, the single largest distorting force in meta-analytic literature. A meta-analysis that excluded gray would be the one to distrust — it would be knowingly pooling a filtered, positive-skewed sample and calling it comprehensive. The instinct to discount gray-inclusive meta-analyses is exactly backwards if you take publication bias seriously.

Furthermore, field dependence matters and inverts the prior. In regulatory and toxicology contexts, mandatory null reporting requirements mean the gray literature is where the suppressed nulls live — gray inclusion in those fields genuinely corrects bias rather than amplifying it. The framing of "gray studies = preliminary positives" is accurate in nutrition, psychology, and some medical subspecialties, but not universal. Before applying skepticism, identify whether the field has systematic null-reporting requirements, industry-trial registries, or government dissemination norms that would make the gray literature a true correction rather than a convenience sample.

Finally: in nutrition, psychology, and some medical subspecialties, the published literature is so extensively p-hacked and HARKed that the premise "published = better quality floor" has already collapsed. In those fields the gray/published quality gap may run in the opposite direction from what intuition suggests.

## Confidence

Medium. The council converged on the core diagnostic (published-only sensitivity check) and the top failure modes, but the correct interpretation depends heavily on field context that the question does not specify — and that field-dependence point alone can invert the conclusion.
