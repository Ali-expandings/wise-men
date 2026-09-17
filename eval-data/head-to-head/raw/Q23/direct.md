# arm: direct (no skill) | question: Q23 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (round 3, PREREG-3 rules)
# subagent tokens: 80654 | tool uses: 0 | duration: 165s

**Bottom line:** half-unpublished, found via gray-lit search, is not itself a red flag. Cochrane and PRISMA both mandate searching gray literature — it's the standard countermeasure to the file-drawer problem, not a shortcut around it. A meta-analysis that skipped gray lit entirely should worry you more than this one. Judge it on execution, not the ratio.

Actual failure modes to check for:

**Search wasn't really systematic.** "Gray literature search" covers a huge range — from OpenGrey/ProQuest Dissertations/trial registries with documented search strings and dual independent screening, down to Googling around and emailing colleagues. Ad hoc search just swaps one selection bias (what journals accepted) for another (what the analysts happened to stumble on — their network, language, digitization luck). Check the methods section for named databases, search strings, date range, independent screeners.

**No peer review, more undetected errors.** Unpublished work skipped the one filter that catches coding mistakes, selective outcome reporting, and shaky stats. Check whether they ran formal risk-of-bias scoring (RoB2, Newcastle-Ottawa) and whether the unpublished studies scored worse.

**Incomplete reporting forces imputation.** Missing SDs, vague randomization, thin methods — common in theses and reports — get patched with assumptions. Each patch is a hidden researcher degree of freedom you can't see in the forest plot.

**Direction usually cuts the other way.** Methods literature on this (McAuley et al. 2000 is the classic) generally finds unpublished studies show smaller effects than published ones, not larger. A real gray-lit search usually pulls the pooled estimate toward null. So an effect that stays significant after honestly folding in the unpublished half is evidence for it, not against — conditional on the search actually being systematic.

**Unless the gray lit was itself selectively released.** Industry white papers, advocacy-org reports, think-tank output: "unpublished" but not randomly so. Favorable ones get released; unfavorable ones sit in a corporate drawer instead of a journal one. Same file-drawer dynamic, one layer up, minus peer review. Check authorship/funding of the gray-lit half for conflict-of-interest patterns.

**Small-study effects confound the bias story.** Gray lit skews small — pilot data, single-site theses. Funnel-plot asymmetry from that can reflect genuine small-study effects (heterogeneity, real precision-effect correlation), not publication bias per se. Don't auto-read an asymmetric funnel as "biased."

**A significant pooled effect can hide heterogeneity.** Check I²/tau², and especially the prediction interval, not just the CI on the mean. High heterogeneity plus a prediction interval crossing zero means "significant on average" is fully compatible with a lot of individual studies showing nothing.

What actually tells you whether to trust it — look for:
- Named gray-lit sources, search strings, screening process (systematic vs. ad hoc)
- Risk-of-bias assessment, broken out by published/unpublished status
- Sensitivity analysis: published-only subset vs. full pool — same conclusion either way?
- Heterogeneity stats plus prediction interval, not just the pooled p-value
- Leave-one-out / influence diagnostics
- Funnel plot plus Egger's test or PET-PEESE even after gray-lit inclusion — residual bias can survive it
- Whether the gray-lit search was pre-registered (PROSPERO protocol) or added after the published-only result looked weak — the latter opens a new p-hacking surface at the meta-analysis level itself

The published/unpublished ratio alone tells you almost nothing. What tells you something is whether the search was reproducible, whether quality was actually assessed rather than assumed, and whether the effect holds up under subgroup and sensitivity analysis. A rigorous 50/50 split beats a lazy journals-only search that never looked for the file drawer in the first place.
