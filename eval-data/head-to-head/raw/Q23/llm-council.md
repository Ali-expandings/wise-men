# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q23 | orchestrator: general-purpose/sonnet | run: 2026-09-18 (round 3, PREREG-3 rules)
# subagent tokens: 131877 | tool uses: 12 | duration: 1065s

## Council Verdict: Trusting a Gray-Literature-Heavy Meta-Analysis

### Where the Council Agrees
Four of five advisors — the Contrarian, the First Principles Thinker, the Outsider, and the Executor — independently arrived at the same concrete test without seeing each other's work: split the pooled estimate by publication status and compare the peer-reviewed-only subset against the unpublished-only subset. Four independent arrivals at the same check is the strongest signal from this exercise.

Three of those four also converge on the same mechanism: "unpublished data obtained by contacting authors directly" is not a neutral fix for publication bias — it's a new selection filter. Whoever is reachable, still has the file, and is willing to send it is not a random draw from everyone who ran the study, and willingness-to-share plausibly correlates with not being embarrassed by the result. The Contrarian frames it as trading journal-editor gatekeeping for author-goodwill gatekeeping with no record of who declined; the Outsider calls it a favor, not a search; the Executor calls it a network sample, not a systematic one. Same diagnosis, three vocabularies, zero coordination.

The peer-review layer converged even harder: all five reviewers independently flagged the same advisor (the Expansionist) as weakest, and four of five named the same advisor (the Contrarian) as strongest.

### Where the Council Clashes
The fault line: does loading a meta-analysis with unpublished studies make a significant result *harder* to fake, because unpublished work trends toward null and drags against significance (the Expansionist) — or does the specific retrieval channel here, cold-contacting authors for unpublished data, introduce a fresh selection filter just as capable of inflating the result as deflating it (the other four)?

The Expansionist's strongest case: there's a documented pattern where a study's thesis version shows a smaller or null effect than its own later published version, because pressure to land on something clean operates at the publication stage. If that holds here, a significant effect that survived dilution by null-leaning material is the harder result to produce.

The rest of the council's answer: that argument proves something more general than what this meta-analysis needs proven. "Gray literature in general trends toward null" isn't the same claim as "gray literature obtained by emailing authors and asking if they have anything lying around trends toward null" — the second is the actual mechanism here, and reluctant authors sitting on a disappointing result are more likely to just not reply. Industry/NGO reports folded into the same bucket cut against the Expansionist's case further, since those are sometimes produced by parties with a stated interest in the conclusion. Neither side is arguing in bad faith — thesis-deflation is real, so is reluctant-author non-response — they're different mechanisms that can each dominate in different corners of what's being lumped together as one "gray literature" number.

### Blind Spots the Council Caught
Four things surfaced only through peer review, absent from all five original responses:

No one named the actual statistical toolkit for this exact problem — funnel plots, Egger's regression, trim-and-fill, PET-PEESE, Copas selection models, p-curve. All five peer reviewers independently caught that the four skeptical advisors reinvented an informal version (the published-vs-unpublished split) without noting that sharper, formal versions already exist.

Nobody flagged double-counting: a single underlying study can enter the pool more than once — as a thesis, then a conference abstract from the same data, then an eventual journal article — breaking the independence assumption the pooled variance depends on and manufacturing significance out of one result counted twice.

Weighting corrects for precision, not quality: inverse-variance weighting rewards a study for a small variance (typically just a large sample), not for being well-conducted. One large, low-quality unpublished study can dominate the pooled estimate regardless of what share of study *count* is gray literature.

The council's own consensus test has a hole: dropping the unpublished half doesn't just remove potential bias, it roughly halves the sample, which mechanically widens the confidence interval. A significance flip is consistent with real bias — but equally consistent with simple power loss, true effect unchanged. The Executor and First Principles Thinker both stated their version of this check as if a significance flip settles the matter outright, with no such caveat.

### The Recommendation
Don't trust the topline finding yet, and don't dismiss it either. Treat it as unverified pending one specific, cheap check, and put the burden of proof on whoever wants you to act on it now.

The case for trusting it immediately (the Expansionist's position) was the one every peer reviewer independently rated weakest: it generalizes a real pattern to a retrieval mechanism it was never shown to apply to, and proposes no way to check itself against this dataset — the exact over-trust failure mode the question flagged. But nobody on the council argued for reflexive dismissal either; even the most skeptical advisors built an explicit path to trusting the result, conditional on a named check. A good-faith gray-literature search is not automatically a red flag. The real problem is narrower: direct-author-solicitation is an under-scrutinized channel with a plausible bias toward flattering results, sitting on top of an analysis process — data pulled and computed on the spot for the meta-analyst — with no pre-registration and no independent check.

One caveat survives even a clean check: independent teams doing honest gray-literature searches on the same question are documented to surface substantially different, barely-overlapping study sets. This result is somewhat contingent on which theses and conference programs this particular team happened to find, in a way the published-only check doesn't fully retire. A clean result earns trust. It doesn't buy certainty.

### The One Thing to Do First
Get the study-level data behind the forest plot, split it into peer-reviewed vs. unpublished, and compute the effect size and confidence interval for each half side by side — not just whether the peer-reviewed half alone still clears p<0.05, which conflates losing half the sample's power with actually removing bias. If the unpublished-only estimate runs materially larger than the peer-reviewed-only estimate, the finding is most likely inflated by relocated selection bias and isn't ready to act on. If the two estimates land close together, or the unpublished half is smaller, the finding has earned its significance and the gray-literature search did the job it was supposed to do.
