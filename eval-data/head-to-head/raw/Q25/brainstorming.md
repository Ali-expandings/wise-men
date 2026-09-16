# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q25 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 81831 | tool uses: 1 | duration: 60s

# Brainstorming — Spike Classification

**Classification:** This is a **Spike** — a feasibility/understanding question ("why do X studies fail," "is it just Y or something deeper") whose output is an answer, not code kept around. No design doc, no plan file.

**Probe plan (as presented to user):** I'll pull apart the replication crisis into its distinct causal layers — publication/selection bias, researcher degrees of freedom (p-hacking broadly construed), statistical power problems, and structural features of how psychological theories are built and tested — then assess whether p-hacking alone explains the pattern or whether something more fundamental about the field's epistemics is doing real work. Sound right?

**Approval (assumed from context):** Yes — the question already frames the two candidate explanations ("just p-hacking" vs. "something deeper"), so the user wants exactly this comparison resolved, not a narrower sub-question.

---

## Findings / Recommendation

**Short answer: both, but the "deeper" part is doing more of the work than the p-hacking story alone gets credit for.**

**1. p-hacking is real but is really four overlapping problems, not one.**
Researcher degrees of freedom (optional stopping, flexible exclusion criteria, trying multiple DVs/covariates and reporting the one that worked), HARKing (writing the hypothesis after seeing the data), publication bias (journals selecting for significant, surprising results), and the file-drawer effect (null results never submitted) all compound. Simmons, Nelson & Simonsohn's "false-positive psychology" work showed you can push false-positive rates well above 5% just by exploiting normal, unremarked analytic flexibility — no fraud required. This alone predicts systematic overestimation of effects at publication time.

**2. Low power turns "significant" into "inflated," independent of any misconduct.**
Original psych studies routinely ran on n=20-40 per cell. Underpowered designs that clear p<.05 only do so by capturing an unusually large sample effect — regression to the mean guarantees replications (typically better-powered) come in smaller. This is the "winner's curse" / truth inflation problem: even a perfectly honest, non-p-hacked underpowered study systematically overstates true effect size. Combined with publication bias favoring the studies that got lucky, the published literature is a biased sample of a biased sample.

**3. Ioannidis's base-rate argument: this is a selection problem, not (only) a conduct problem.**
"Why Most Published Research Findings Are False" shows that when you combine low prior probability of a hypothesis being true, small sample sizes, flexible analysis, and publish-or-perish selection, the positive predictive value of a significant result can drop below 50% *even with everyone behaving honestly*. This is the mathematically deeper point: p-hacking is one lever among several that all push the same direction, and you don't need any of them to be egregious for the aggregate literature to be mostly noise dressed as signal.

**4. The genuinely deeper layer: weak theoretical structure.**
Paul Meehl's older critique ("soft psychology") argues most psychological theories are verbal, directional, and unfalsifiable in practice — "X will affect Y somehow" rather than a quantitative prediction. Almost any pattern in the data can be narrated as confirming a vague directional hypothesis. Physics theories forbid specific numbers; soft-psych theories forbid almost nothing. That means even a perfectly-run, adequately-powered, preregistered study can "succeed" on weak criteria the first time and still be measuring a fragile, context-bound pattern rather than a real causal mechanism.

**5. Effects are often genuinely context-dependent, not fake.**
The Many Labs projects and the 2015 Open Science Collaboration (~36% replication rate on 100 studies) found that even direct replications with large samples and preregistration still fail at meaningful rates — and follow-up work (moderator analyses, cross-cultural replications) often shows the original effect *does* exist but is smaller, sign-flipped in some populations, or conditional on unstated moderators (WEIRD-sample dependence, historical period, framing details treated as incidental that weren't). This is not p-hacking exposed retroactively — it's evidence that a lot of "robust" effects were never a fixed population parameter to begin with; they were local, culturally/temporally contingent regularities that got theorized as universal.

**6. Incentive structure ties it together.**
Careers reward novel, surprising, statistically significant findings over confirmatory or null ones. That doesn't just cause individual QRPs — it shapes which theories get built, which effects get chased, and which get canonized as "textbook" before anyone runs a high-powered direct replication. The incentive problem is upstream of the statistical problem.

**Bottom line:** p-hacking and publication bias are necessary parts of the explanation and probably account for the biggest chunk of inflated effect sizes. But the replication crisis persists even in studies with none of those defects, because psychological "effects" are frequently (a) statistically inflated by low power regardless of intent, (b) built on theories too loosely specified to be genuinely falsified the first time, and (c) more context/population-dependent than the field's universalist framing assumed. The field's response — preregistration, larger samples, direct replication requirements, registered reports — targets exactly these three deeper causes, not just QRP policing, which is itself evidence the field agrees the problem is structural, not just a hygiene issue.
