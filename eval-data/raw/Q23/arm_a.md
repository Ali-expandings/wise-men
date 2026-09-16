# Q23 Arm A raw output
# salvaged_from_context: false
# model: sonnet-4.6
# skill_suppression: applied
# contamination: none

The short answer: treat it with real caution, but not automatic dismissal. The quality depends on how the gray literature search was conducted and what you can verify. Here is what actually breaks down.

The core problem is that unpublished studies are not a random sample of all studies ever run. They skew heavily toward null or weak results that never cleared the publication bar, but the direction of the bias in a meta-analysis depends on *why* they were unpublished. If the gray literature consists of conference proceedings, government reports, and dissertations that were simply never submitted to journals, they are probably less biased than the published set and including them is methodologically sound. If they were located because a researcher emailed colleagues asking for "studies showing an effect of X," the sample is poisoned from the start.

The specific failure modes, in rough order of severity:

Selective reporting within the gray studies themselves. Unpublished work often only exists in summary form — a conference abstract or a report chapter — meaning you cannot verify whether the authors ran 10 outcomes and reported the two that worked. With published studies you can sometimes detect this via outcome switching registries. With gray lit you usually cannot.

The search is inherently non-reproducible. "Gray literature search" covers anything from a systematic database trawl (OpenGrey, ProQuest Dissertations, WHO IRIS) to emailing thirty colleagues. If the paper does not describe exactly where they searched, what search strings they used, and what the hit rate was, you cannot replicate it. This is not a theoretical concern — two researchers doing "gray literature searches" on the same topic routinely find completely different sets of studies.

Citation bias in how gray lit gets located. Gray studies are found partly through citation networks, which means well-known labs and English-language institutions are overrepresented. If the effect is heterogeneous by context or population, this biases the pooled estimate in ways that are hard to model.

Funnel plot asymmetry tests lose power. The standard tool for diagnosing publication bias (Egger's test, trim-and-fill) assumes that small studies with big effects are the missing ones. If half your studies are already nominally "from the file drawer," the funnel is contaminated and the diagnostic becomes unreliable. The meta-analysts may run the test, see no asymmetry, and conclude publication bias is not a problem — but that conclusion does not follow when the included sample is itself a mix of published and pre-selected unpublished work.

Version control problems. Gray studies are sometimes later published in modified form. If the meta-analysis includes both the gray version and the journal version of the same data, that study gets counted twice. Good meta-analyses catch this; many do not.

What to actually check before deciding how much weight to give this:

Look at the PRISMA flow diagram. Does it show how many gray sources were searched, how many records were identified from each, and what the yield was? A credible gray search identifies hundreds of records and includes a small fraction after screening. If they found 12 gray studies by emailing networks, that is a signal.

Check whether the effect size differs between the published and unpublished subsets. If the gray studies show systematically larger effects than the published ones, that is backwards from what you would expect if they are truly "file drawer" studies, and it suggests they were located because someone knew they showed the effect.

Check the heterogeneity statistic (I²). High heterogeneity alongside a pooled significant result often means the studies are not measuring the same thing, and the "significant" average is an artifact.

Look for a pre-registered protocol (PROSPERO). If the search strategy was pre-specified before data extraction began, the gray lit component is far more trustworthy.

The bottom line is that gray literature inclusion is, in principle, a methodological virtue — it combats publication bias. But it shifts the selection pressure from journal editors to whoever designed the search. That person is usually not blinded to the hypothesis, and the search is rarely as systematic as claimed. A significant effect from a meta-analysis where half the evidence is gray and the search is vaguely described should be treated the way you would treat any result with a plausible, uncontrolled confound: interesting, worth following up, not sufficient on its own to change practice or strong prior beliefs.
