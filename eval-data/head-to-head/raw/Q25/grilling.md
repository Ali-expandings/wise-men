# arm: grilling (mattpocock/skills 85f83d3fde1d) | question: Q25 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 77273 | tool uses: 1 | duration: 63s

❓ **Q1** - **Scope**: Should "psychology" here mean the field broadly, or specifically the corner most associated with the replication crisis — social psychology, priming effects, ego depletion, and similar personality/social-cognition work (as opposed to, say, psychophysics or basic cognitive/perception research, which replicates much better)?

➡️ The question's phrasing ("effects that seemed very robust") points to the flagship crisis-era findings — social priming, ego depletion, power posing, facial feedback — so the answer should center on that corner of the field while noting it generalizes unevenly across psychology.

✅ Settled: focus on social/personality psychology's flagship effects, note cognitive/perceptual psych fares better.

---

❓ **Q2** - **Binary framing**: The question poses "just p-hacking retroactively exposed" vs. "something deeper" as an either/or. Is that a real fork to pick a side on, or a rhetorical setup expecting a synthesis that ultimately weighs toward "deeper"?

➡️ Read as rhetorical setup — the user already suspects there's more to it than p-hacking (why else ask), so the answer should synthesize both and land on a verdict rather than just picking one.

✅ Settled: synthesize, verdict favors "deeper, with p-hacking as the visible layer."

---

❓ **Q3** - **Technical register**: The user correctly uses "p-hacking" unprompted. Should the answer use adjacent technical vocabulary (researcher degrees of freedom, winner's curse, regression to the mean, forking paths) without over-explaining, or stay fully lay?

➡️ User is technically literate; use the vocabulary but gloss each term in one clause rather than assuming full familiarity.

✅ Settled: technical-but-glossed register.

---

❓ **Q4** - **Structure**: Given Q1–Q3, should the answer be a flat list of causes, or a layered argument (statistical → structural/incentive → epistemic) that builds to the verdict from Q2?

➡️ Layered argument — it mirrors the question's own two-tier structure (surface cause vs. deeper cause) and makes the verdict land as a conclusion rather than an assertion.

✅ Settled: three-layer structure (statistical, incentive, epistemic) culminating in a verdict.

---

❓ **Q5** - **Examples**: Given Q1 settled on flagship effects, should the answer name specific cases (power posing, ego depletion, facial feedback hypothesis) as evidence, or stay abstract?

➡️ Name 2–3 concretely — abstract claims about "effects" are hard to evaluate without anchors, and the user clearly knows this literature well enough to reference "very robust" effects.

✅ Settled: include power posing, ego depletion, and facial-feedback as illustrative cases.

---

❓ **Q6** - **Stance on the field's legitimacy**: Should the answer frame this as evidence psychology is "not real science," or as a field-specific vulnerability (small, noisy, context-dependent effects) layered on an incentive problem common to all of science?

➡️ Avoid the "not real science" framing — physics and biology have their own replication problems (cancer biology's is arguably worse); psychology's issue is that its true effects are typically smaller and more context/moderator-dependent relative to measurement noise, which makes the same universal incentive problems bite harder there.

✅ Settled: psychology as the canary, not the outlier — same disease, more exposed organ.

---

❓ **Q7** - **Include reforms?**: The question is purely diagnostic ("why"), not "what's being done." Should the answer still close with a brief note on preregistration / Registered Reports / Many Labs, or stay strictly causal?

➡️ One brief closing line adds completeness (shows the field responded) without derailing into a different topic the user didn't ask about.

✅ Settled: one-sentence close on reforms, no deep dive.

---

Frontier is empty. Final recommendation:

**It's not just p-hacking — p-hacking is the legible symptom of a deeper structural and epistemic problem.**

**Layer 1 — statistical.** Original studies were typically small-sample, and true effects in social/personality psychology tend to be modest. Under those conditions, a "significant" result is disproportionately likely to be a noise spike inflated by chance (the *winner's curse*), and the researcher had many defensible ways to code, exclude, and analyze the data (*researcher degrees of freedom* / *garden of forking paths*) — so even without conscious misconduct, the published effect size is biased upward. Add publication bias (only significant results get published, the rest sit in the file drawer), and the literature ends up systematically overselling effects before any single researcher does anything wrong. This is the part "p-hacking" captures, and it's largely why preregistration and larger samples fix a lot of it.

**Layer 2 — incentives.** Careers were built on novel, surprising, publishable findings, not on replication or null results, for decades. That structure selects for exactly the kind of noisy, flashy, small-N result that layer 1 describes — it's not that individual researchers were unusually dishonest, it's that the whole field's reward function pointed at the same failure mode simultaneously (power posing, ego depletion, facial feedback all fit this).

**Layer 3 — the deeper one.** Even a scrupulously honest, adequately powered original study can fail to replicate because the underlying phenomenon is genuinely heterogeneous — it depends on population, culture, era, and unmeasured moderators in ways a single WEIRD-undergrad-sample study can't detect. Physical constants don't care what country or decade you measure them in; psychological effects often do. So a chunk of "failed" replications aren't debunking a false original result — they're revealing that the effect was real but conditional, and the field's single-study paradigm had no way to say so.

Verdict: p-hacking is real and was the first thing fixed (preregistration, Registered Reports, multi-lab replications like Many Labs have measurably improved things). But the harder, still-unresolved issue is that social science studies small, context-dependent effects with a publish-flashy-results incentive structure — a combination that manufactures false confidence even when no one cheats.
