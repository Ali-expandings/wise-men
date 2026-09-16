# Q38 Arm C internals — 5 members + 5 reviewers
# salvaged_from_context: false
# members: 5 sonnet-4.6 (Editor, Audience Advocate, Rhetorician, Strategist, Devil's Advocate) — writing-domain personas
# validator: all 5 passed (5-section contract present + non-empty + engaged)
# reviewer framing: NEUTRAL grading frame (bug #6 fix)
# REAL split: Editor/AudienceAdvocate/Rhetorician → find the framing (weather forecast + contrast beat / paired metaphor + dead-reckoning); Strategist → reframe to DECISION-frame (what evidence licenses vs rules out), metaphor-hunt is wrong quest; DA → STOP searching for a metaphor (category error), use worked numbers + one plain sentence. 2 of 5 reject the metaphor premise (DA strongest).

==================================================================
## MEMBER: Editor (sonnet-4.6)
==================================================================
## Core judgment
The problem isn't your metaphors — you're treating uncertainty as a single thing. It has two faces: precision (how tight the estimate) and robustness (how much it shifts if assumptions change). Metaphors collapse these → either dismissive or falsely confident. Framing that works: weather forecast WITH A TRACK RECORD. "70% chance of rain" = a calibrated machine with a known error rate. You're not saying we know nothing; you're saying we know how well we know. Pair with one concrete number as a range not a point ("between 3.1 and 4.7, most likely 3.9").
## Top risks
1. Readers conflate "uncertain" with "unreliable" — say explicitly forecasters are MORE trustworthy because they quantify doubt. 2. If uncertainty is model-assumption not sampling, weather metaphor breaks (forecast uncertainty is about nature; assumption-based is about the model).
## Recommended change
Lead with the track record before the range: "We know how often estimates like this are wrong — that knowledge is the point." Then give the interval. Don't apologize for uncertainty; position it as what makes the finding credible.
## Confidence
High on diagnosis; medium on the forecast metaphor fitting the specific paper (depends frequentist sampling vs Bayesian/model uncertainty).
## Weakest assumption
That the audience reads "70% chance of rain" as calibrated expertise rather than vague hedging — skeptical audiences may need the medical-screening-test framing instead ("catches 94 of 100 cases; here's what the 6 misses look like").

==================================================================
## MEMBER: Audience Advocate (sonnet-4.6)
==================================================================
## Core judgment
Metaphors fail because most reach for SPATIAL analogies (range/window/zone) when statistical uncertainty is about CONFIDENCE IN A PROCESS, not a location. Readers hear "we're not sure" → "they don't know" (category error). Weather forecast works, but ONLY if you explain WHY: 70% chance of rain is the output of a well-calibrated system honest about limits → moves uncertainty from "epistemic failure" to "epistemic integrity."
## Top risks
1. Metaphor does the work but the follow-through reverts to "ranges/error bars" → mental model collapses; sustain the framing. 2. Lose readers at "confidence interval" regardless — false-cognate trap ("confident"); consider avoiding the term for general audience. 3. Overcorrection into relativism → reader concludes science is contested; need explicit counter-beat. 4. Expert reviewers push jargon back in; hold the line.
## Recommended change
Two-move structure: (1) process metaphor (forecast / carbon-dating margin / navigation dead-reckoning) establishes uncertainty as a feature of careful reasoning; (2) CONTRAST BEAT that explicitly names + dismisses the wrong interpretation ("doesn't mean scientists are guessing — means they're honest about what data can/can't show"). Most writers skip move 2; it's the one that inoculates against misreading. Dead-reckoning underused + powerful: navigator plots a growing circle, still acts on it.
## Confidence
High the two-move structure helps; moderate any single metaphor fully solves it — best communicators use multiple short metaphors in sequence.
## Weakest assumption
That readers have no prior model to displace — bad science journalism may have installed active distrust no in-text metaphor dissolves.

==================================================================
## MEMBER: Rhetorician (sonnet-4.6)
==================================================================
## Core judgment
You're reaching for ONE metaphor to carry two opposing cognitive loads: (1) we have real signal, (2) we don't know the exact answer. No lone analogy holds both without one dominating. Use a PAIRED metaphor with explicit contrast. Weather forecasting (culturally legible; audiences already hold useful+non-certain simultaneously), then NAME the structure: "statistical uncertainty works the same way — grounded in real data, genuinely informative, still a range not a point."
## Top risks
1. Lottery leak — "probability" without grounding maps to pure chance; weather forecloses this (physically caused). 2. "Just a model" dismissal — name the evidence base BEFORE the uncertainty range (uncertainty after evidence = honest; before = hedge). 3. Range anchoring — readers anchor on midpoint; say "both ends are real possibilities." 4. "Scientists agree there is uncertainty" sounds like scientists disagree — reframe "they agree on the range and that the range matters."
## Recommended change
Lead with forecast frame, then a SECOND image for the stakes dimension: navigation by dead reckoning (act on best inference, neither paralyzed nor pretending). Pair: forecast = uncertainty is normal/probabilistic; dead reckoning = uncertainty doesn't mean inaction.
## Confidence
High that weather is the most culturally pre-loaded option; moderate that dead-reckoning lands without explanation (maritime literacy uneven).
## Weakest assumption
That the audience's forecast experience is probabilistic rather than binary — many strip the probability ("probably raining"). If the paper needs readers to hold a distribution, supplement with frequency framing (imagine the forecast issued 100 times).

==================================================================
## MEMBER: Strategist (sonnet-4.6)
==================================================================
## Core judgment
Category error in the communication GOAL. You're treating statistical uncertainty as a fact to convey when it's a RELATIONSHIP to establish between reader and evidence. The undersell/oversell oscillation is the symptom: metaphors describe a static state, but readers need a dynamic cognitive posture. The framing that works is not a metaphor — it's a DECISION FRAME. Show what the reader would DO differently along the uncertainty spectrum. Weather works because "70% → bring umbrella" connects to an action. Reframe: instead of what uncertainty IS, show what the evidence LICENSES vs does NOT license. "Strong enough to act on X, not strong enough to conclude Y."
## Top risks
1. Solve the metaphor problem, leave the structure problem — vivid image, still don't know what to do with it. 2. Decision-frame needs the audience's actual decision context, which varies; general audience has no single lever. 3. Over-correcting toward actionability → prescriptive, violates research-writing genre norms.
## Recommended change
Pair every uncertainty statement with a two-sided bound: what the evidence confidently rules IN, what it confidently rules OUT, uncertain zone named in the middle. Drop the single-metaphor search. Use a recurring "what this means / what this doesn't mean" callout that trains readers to hold uncertainty as a bounded range, not a binary.
## Confidence
High on diagnosis (metaphor-hunt is the wrong quest); medium on the two-sided-bound device (depends on topic + audience literacy).
## Weakest assumption
That the audience is uncertainty-naive — if policy-adjacent / scientifically literate, the real obstacle is TRUST not comprehension, and the fix is method transparency not a framing device.

==================================================================
## MEMBER: Devil's Advocate (sonnet-4.6)
==================================================================
## Core judgment
The premise is flawed — stop searching for a metaphor. "Undersells OR sounds like we know nothing" is not a metaphor-quality problem; it's a fundamental property of metaphor applied to probabilistic reasoning. Every metaphor maps uncertainty onto a familiar domain (weather/gambling/archery) with DIFFERENT epistemic structure than your statistical claim → reader imports wrong intuitions → you spend the paper correcting the baggage. Not one clever framing away — chasing a category error.
## Top risks
Concrete failure mode: the weather-forecast metaphor (most popular) trains readers that uncertainty is a prediction interval for a single event with a clear resolution date. Statistical uncertainty in research is often parameter estimation / model assumptions / sampling distributions — none resolve cleanly like "did it rain?". A reader who absorbs the weather metaphor asks "so when will we know for sure?" — possibly permanently unanswerable. You've made comprehension WORSE by introducing a false resolution expectation.
## Recommended change
Use worked numbers instead of a metaphor. One concrete case: "In a sample of 1,000 we estimated X. If we repeated this 100 times with different samples, about 95 of those studies would produce an estimate between A and B." Harder for two seconds but doesn't lie. Pair with ONE sentence of plain English — not a metaphor, a direct statement of what you do and don't know.
## Confidence
High. The evidence is in the question: multiple metaphors each fail in a different direction — that's the signal the tool is wrong, not the instances.
## Weakest assumption
That general-audience readers can't handle numerical explanation without metaphorical scaffolding — readers who engage with research papers typically can; if they truly can't, a metaphor gives them a comfortable wrong model instead of an honest gap.

==================================================================
## REVIEWERS (5 × haiku-4.5, NEUTRAL grading frame) — 0 refusals
==================================================================
# Per-member mean across 5 reviewers (C/I/P/R → total /20):
#   Devil's Advocate  4.8 / 4.6 / 3.8 / 4.8 = 18.0  (CLEAR TOP — every reviewer ranked DA top or co-top)
#   Audience Advocate 4.0 / 4.2 / 3.2 / 3.8 = 15.2
#   Editor            4.0 / 3.0 / 4.0 / 3.0 = 14.0
#   Rhetorician       3.8 / 3.8 / 3.2 / 3.0 = 13.8
#   Strategist        3.4 / 4.2 / 2.2 / 3.6 = 13.4  (BOTTOM — insight high but practical 2.2: abstraction without a surface sentence)
#
# Per-reviewer raw (C/I/P/R):
#   R1: Editor 4/3/4/3 | AudAdv 4/4/3/4 | Rhet 4/3/3/3 | Strat 4/4/2/3 | DA 5/5/4/5  | top DA, bottom Strategist
#   R2: Editor 4/3/4/3 | AudAdv 4/5/3/4 | Rhet 4/4/3/3 | Strat 3/4/2/4 | DA 5/4/4/5  | top DA, bottom Strategist
#   R3: Editor 4/3/4/3 | AudAdv 4/4/3/3 | Rhet 4/4/4/3 | Strat 4/5/2/4 | DA 5/4/3/5  | top DA+Strategist(insight), bottom Editor
#   R4: Editor 4/3/4/3 | AudAdv 4/4/4/4 | Rhet 4/4/3/4 | Strat 3/4/3/4 | DA 4/5/4/5  | top DA, bottom Strategist
#   R5: Editor 4/3/4/3 | AudAdv 4/4/3/4 | Rhet 3/4/3/3 | Strat 3/4/2/3 | DA 5/5/4/4  | top DA, bottom Strategist
#
# SEVERE-DISAGREEMENT FLAG raised by all 5 reviewers: Devil's Advocate vs the other four on whether metaphor is
# SALVAGEABLE. Editor/AudienceAdvocate/Rhetorician (+ partly Strategist) assume the right framing/pairing works;
# DA rejects the premise — the under/oversell oscillation is fundamental to metaphor applied to probabilistic
# reasoning; weather implies clean dated resolution that parameter/model uncertainty lacks → comprehension worse.
# UNUSUAL: the DA (contrarian-by-design, normally peer-weakest) was peer-rated the STRONGEST member here (18.0).
# Reviewers judged the contrarian read to be the correct one. Standard tier → NO debate round; DA preserved as
# load-bearing dissent (and arguably the lead). Cross-arm note: Arm B's own dissent independently raised the same
# "skip the metaphor, give an operational sentence" point — convergent signal.
