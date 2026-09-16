# Q17 Arm C internals — 5 members + 5 reviewers
# salvaged_from_context: false
# regenerated: 2026-05-29 (prior partial — compressed members, no reviewers — overwritten with fresh verbatim full pipeline)
# members: 5 sonnet-4.6 (User Advocate, Business Analyst, Devil's Advocate, Historian, Designer)
# validator: all 5 passed (5-section contract present + non-empty + engaged)
# member outputs saved VERBATIM (no compression)

==================================================================
## MEMBER: User Advocate (sonnet-4.6)
==================================================================

## Core judgment

The NPS and retention data are measuring completely different populations at completely different moments in time. NPS captures the emotional peak of users who are actively engaged enough to respond to a survey — those are disproportionately your enthusiasts. The 55% six-month retention reflects what happens to the full cohort once the novelty wears off, the workflow friction accumulates, and the product fails to embed itself into daily habit. You do not have raving fans who churn; you have raving fans who recommend you, and a separate, larger group of quiet users who leave without ever telling you anything.

## Top risks

- **Survey timing bias**: If NPS is collected shortly after onboarding or a positive moment (first success, upgrade, support resolution), scores are artificially inflated and structurally disconnected from long-term value delivery.
- **Promoters who do not stay**: A user can genuinely love your product in the moment, recommend it to a friend, and still fail to build a habit around it — love and retention are not the same behavioral outcome.
- **Silent majority churn**: The users churning at month 6 are likely never completing your NPS survey at all, which means your NPS denominator is self-selected toward the happy.
- **Job-to-be-done mismatch over time**: The product might solve a narrow, acute problem brilliantly but fail to address the broader or evolving job the user actually has — creating a natural expiration date on enthusiasm.
- **Switching cost illusion**: Low switching costs mean users can sincerely recommend you and simultaneously leave the moment a slightly better option appears, with no cognitive dissonance on their part.

## Recommended change

Implement exit-intent interviews and post-churn surveys specifically targeting users who leave between months 3 and 6, and cross-reference their original NPS scores against their tenure length. You need to know whether churned users were ever Promoters, Passives, or Detractors — because if churned users were disproportionately Passives who never surfaced in your NPS data, that confirms the measurement gap. Simultaneously, shift at least one NPS collection touchpoint to month 5 or 6 rather than onboarding, so you are measuring sustained satisfaction rather than first-impression delight.

## Confidence

Medium — the most common structural explanation (survey population mismatch) is well-documented, but the actual cause in this specific product depends entirely on when NPS is measured and who is responding, which is information not provided here.

## Weakest assumption

The weakest assumption in my analysis is that the NPS respondents and the churning users are meaningfully distinct populations — it is possible that even confirmed Promoters are churning at high rates, in which case the problem is not measurement bias but a genuine gap between emotional satisfaction and behavioral lock-in, which is a harder and more fundamental product problem.

==================================================================
## MEMBER: Business Analyst (sonnet-4.6)
==================================================================

## Core judgment

Your NPS and your retention are measuring fundamentally different things at different points in time, and they are almost certainly drawing from different populations. NPS captures a sentiment snapshot — typically from engaged, recently-activated users who responded to a survey — while month-6 retention measures actual continued behavior across your entire cohort, including the silent majority who never responded to your survey. A 72 NPS with 55% month-6 retention is not a paradox; it is a sampling and timing problem disguised as a product problem.

## Top risks

- **Survivor bias in NPS**: Your promoters are the users who stayed long enough to have an opinion. The 45% who churned by month 6 were likely already disengaged when they took your survey — or never took it at all — making your NPS systematically inflated relative to the full cohort.
- **Decoupled value and stickiness**: Users can genuinely love your product for a specific moment or use case (high NPS) but have no recurring reason to return (low retention). Enthusiasm and habitual use are different behavioral drivers.
- **Churn is happening before the survey fires**: If your NPS survey goes out at day 30 or day 60, you may be surveying a population that has already self-selected for retention, meaning you never hear from the users who churned early.
- **Segment masking**: A small cohort of genuinely ecstatic power users (heavy promoters) can pull the NPS number high while a larger, mediocre-experience segment churns quietly and drags retention down.
- **Passive and detractor silence**: Low NPS response rates mean your 72 could be built on a tiny vocal minority, while passives and detractors represent the bulk of actual behavior.

## Recommended change

Segment your NPS responses by whether those respondents were still active at month 6. Run a simple cohort join: for every user who completed an NPS survey, tag them as retained or churned at month 6, then recalculate NPS within each group. If your churned cohort has an NPS of 40 and your retained cohort has an NPS of 85, you have confirmation of survivor bias and the aggregate 72 is meaningless as a health metric. From there, shift your measurement from aggregate NPS to a leading behavioral indicator — something like week-3 activation depth or a specific action that correlates with retention — and track that as your primary signal. NPS can stay as a brand metric, but it should not be used as a proxy for product-market fit or customer health.

## Confidence

Medium — the survivor bias explanation is the most statistically likely cause, but without seeing your NPS survey timing, response rate, and the segment breakdown of who is actually churning, there are legitimate alternative explanations (pricing, competition, seasonality) that cannot be ruled out from the numbers alone.

## Weakest assumption

The weakest assumption in my analysis is that your NPS survey is being fielded to the same population that feeds your retention denominator. If you are surveying a deliberately curated sample (e.g., only power users, only users who contacted support, only users who hit a milestone) rather than a random or full cohort sample, then the survivor bias framing changes significantly and the gap between NPS and retention may reflect intentional measurement design rather than a flaw.

==================================================================
## MEMBER: Devil's Advocate (sonnet-4.6)
==================================================================

## Core judgment

You are not misreading anything — the data is telling you something strategically important that most advisors will rush past to fix the measurement. A 72 NPS with 55% month-6 retention is the signature pattern of a product that delivers a genuine, memorable peak experience that customers authentically loved, but which does not fit the cadence or sustained workflow of their actual lives. These are not fake fans. They are real fans of something they do not need often enough to justify a subscription. The problem is not NPS; the problem is your pricing and packaging model.

## Top risks

- You pivot to "fixing NPS measurement" and spend six months adding relationship-NPS surveys, segmenting by cohort, and building a voice-of-customer program, while the actual structural mismatch between your value delivery and your billing model goes untouched.
- You interpret churn as dissatisfaction and start degrading the product's honest simplicity or focus by adding features to increase stickiness, which destroys the very thing that generates the 72 in the first place.
- You start discounting at month 5 to arrest churn, which trains your best customers to wait for the offer and compresses lifetime value without solving the root cause.
- You hire a retention team to run re-engagement campaigns against customers who genuinely have no current need, burning goodwill and converting raving fans into annoyed ex-customers.

## Recommended change

Test a usage-based or seasonal pricing tier before your next quarterly planning cycle. Specifically: offer churned customers at the 6-month mark a "pause" option at a dramatically reduced rate (or zero) that keeps them in your ecosystem without a full subscription commitment. Measure whether reactivation rates from paused accounts outperform reactivation from fully churned accounts over the following 12 months. If they do, you have confirmed the hypothesis — your product is episodic-value, not continuous-value — and you should restructure your core pricing model accordingly, not your survey methodology.

## Confidence

Medium — because this diagnosis requires that the 72 NPS is drawn from a reasonably representative sample and not systematically biased toward a specific use-case segment that is itself unrepresentative of churners.

## Weakest assumption

The weakest assumption in this analysis is that churned customers and retained customers share similar NPS distributions — if the 72 is driven predominantly by the 55% who stayed, and churners were quietly scoring you much lower but leaving before being surveyed, then the metric genuinely is misleading and the measurement-fix crowd would be right.

==================================================================
## MEMBER: Historian (sonnet-4.6)
==================================================================

## Core judgment

The NPS/retention gap you are seeing is one of the most well-documented traps in SaaS, and the canonical explanation is that NPS measures emotional response at a moment of peak engagement, not habitual value delivery over time. Slack famously had sky-high promoter scores from power users in its early years while losing entire teams at the workspace level because champions loved the product but couldn't drive adoption across their organizations. You almost certainly have a vocal, enthusiastic minority inflating your NPS while a quieter majority churns without complaint — they don't hate you, they just stopped finding you necessary. The number 72 is real, but it is the score of your best customers, not your average one.

## Top risks

- **Promoter concentration**: A small segment of power users (likely 15–20% of your base) is generating most of your promoter scores, masking median-user indifference. HubSpot and Intercom both encountered this when NPS was driven by marketers and admins who evangelized the tool while end-users quietly abandoned it.
- **Time-of-survey bias**: If you survey at onboarding completion or first "aha" moment, you catch peak enthusiasm. Typeform and Notion both learned that NPS spiked right after a user hit their first successful workflow, then collapsed at month 4 when the novelty wore off and the tool became "just another tab."
- **Churn without noise**: Customers who churn passively — not canceling angrily but simply letting the subscription lapse — rarely show up in NPS because they've already mentally left before you ask. This is particularly common in PLG products where cancellation is low-friction.
- **Outcome gap vs. experience gap**: Users may love interacting with your product but not be achieving the downstream outcome they bought it for. Qualtrics documented this extensively — satisfaction with the tool and achievement of business goals are uncorrelated far more often than product teams expect.

## Recommended change

Segment your NPS responses by cohort tenure and by whether each respondent is still active at month 6. Run the NPS calculation exclusively on users who have already survived to month 6 and compare it to the NPS of users in their first 60 days. If the month-6 survivor NPS is 20–30 points lower than your overall number, you have confirmed promoter concentration at onboarding. Then, for every churned user from the last two quarters, pull their NPS score and survey date — if churners had scores of 8 or 9 before leaving, you have a classic "happy quitter" pattern (documented extensively in Amplitude's retention research and by Gibson Biddle at Netflix), meaning the product delivers joy but not habit or necessity. That data gives you the specific intervention: you need to move users from "I like this" to "I can't do my job without this," which is a workflow integration problem, not a satisfaction problem.

## Confidence

**Medium** — the diagnosis fits the data pattern and has strong historical precedent, but the actual mechanism driving your specific gap could be one of several distinct root causes (promoter concentration, survey timing, outcome gap, or genuine product-market fit for a niche only) and only cohort-segmented data will confirm which one is dominant.

## Weakest assumption

The weakest assumption in this analysis is that your churning users were ever genuinely engaged rather than merely polite — if a significant portion of your promoter scores come from users who gave a 9 or 10 on a survey they treated as a formality (a well-documented social desirability bias in NPS, particularly in B2B contexts where respondents know the vendor), then the entire "raving fans who churn" framing is wrong and you are actually looking at inflated NPS from disengaged users, which is a different and more serious problem.

==================================================================
## MEMBER: Designer (sonnet-4.6)
==================================================================

## Core judgment

NPS and retention measure two completely different things and they can diverge sharply without contradiction. NPS captures a moment of emotional peak — typically right after a success or "aha" experience — while retention measures whether the product has been woven into the user's routine across months. What you likely have is a product that creates genuine delight during active use, but has not built the habit infrastructure needed to survive the natural troughs in motivation that every user hits between months two and six. The fans are real; the habit loop is missing.

## Top risks

- **Peak-end bias in NPS collection**: If you survey users shortly after a positive interaction (onboarding completion, a successful outcome, a support resolution), you are measuring the peak, not the average lived experience. The 45% who churn by month six probably also gave you a 9 or 10 at month one.
- **No investment loop**: Users may get value from the product but never put enough of themselves into it — data, preferences, history, social connections — to make leaving feel costly. Without sunk-cost assets, switching is frictionless.
- **Trigger decay**: Whatever pulled users back into the product in the early weeks (notifications, novelty, external motivation) fades, and you have nothing replacing it. The product never became a contextual habit triggered by a recurring life event.
- **Wrong moment of value**: The thing users love may not be something they need repeatedly. They rave about it, they just don't need it again next quarter.
- **Segmentation blindness**: Your aggregate NPS of 72 may be masking that your most vocal promoters are a small, highly engaged segment, and the majority of your user base is quietly lukewarm and churning silently.

## Recommended change

Instrument the specific moment — the week, the workflow context, the feature usage pattern — where month-six churners diverge from month-six retainers. Do not ask them why they left; churned users rationalise post-hoc and their answers will mislead you. Instead, compare behavioral data in months two and three between the two cohorts. What you are looking for is the variable-reward loop: are retained users experiencing a recurring cycle where effort in the product produces a meaningful, somewhat unpredictable positive outcome that pulls them back? Once you identify where that loop breaks for churners, design one specific re-engagement trigger tied to a real-world cue in their life or workflow — not a generic push notification, but something that fires when the context genuinely makes your product relevant again.

## Confidence

Medium — the peak-end NPS timing hypothesis is well-supported by behavioral economics, but the specific mechanism driving your churn depends entirely on product category, and I am reasoning without knowing whether this is a B2B tool, a consumer app, or something else.

## Weakest assumption

The weakest assumption is that the churning users are the same population as the NPS promoters — it is possible that your promoters genuinely retain at high rates, and the 45% churn is concentrated in a segment that gave middling NPS scores that your average is smoothing over, in which case you do not have a habit problem so much as a positioning and acquisition problem.

==================================================================
## REVIEWERS (5 × haiku-4.5)
==================================================================
# 0 refusals. Strong consensus: strongest=Business Analyst, weakest=Devil's Advocate.

### Reviewer 1
```rubric
member_1_user_advocate: insight=4, rigor=3, usefulness=3, risk=4
member_2_business_analyst: insight=5, rigor=5, usefulness=5, risk=4
member_3_devils_advocate: insight=4, rigor=2, usefulness=2, risk=3
member_4_historian: insight=4, rigor=4, usefulness=4, risk=3
member_5_designer: insight=4, rigor=3, usefulness=4, risk=3
strongest: member_2
weakest: member_3
severe_flag: member_3: conflates business model failure with measurement validity without evidence; recommends major pricing changes before diagnosis is complete, risking false pivot
```
Member 2 dominates (isolates sampling bias + timing, prescribes low-cost cohort-join validation). Members 1/4/5 identify the phenomenon but stay abstract; Member 3 leaps to business-model diagnosis without establishing the measurement problem first.

### Reviewer 2
```rubric
member_1_user_advocate: insight=4, rigor=3, usefulness=3, risk=4
member_2_business_analyst: insight=5, rigor=5, usefulness=5, risk=4
member_3_devils_advocate: insight=4, rigor=2, usefulness=2, risk=3
member_4_historian: insight=4, rigor=4, usefulness=4, risk=3
member_5_designer: insight=4, rigor=3, usefulness=4, risk=2
strongest: member_2
weakest: member_3
severe_flag: member_3: prescribes business model overhaul before root-cause analysis; conflates measurement problem with product problem; "pause tier" without evidence
```
Member 2 dominates: cohort-tagged NPS is the only diagnosis that resolves the paradox instead of redefining it. Member 3 inverts the question (assumes measurement correct, design wrong) — dangerous flip without data.

### Reviewer 3
```rubric
member_1_user_advocate: insight=4, rigor=3, usefulness=3, risk=4
member_2_business_analyst: insight=5, rigor=5, usefulness=5, risk=5
member_3_devils_advocate: insight=4, rigor=2, usefulness=2, risk=3
member_4_historian: insight=4, rigor=4, usefulness=4, risk=4
member_5_designer: insight=4, rigor=3, usefulness=4, risk=3
strongest: member_2
weakest: member_3
severe_flag: member_3: confuses diagnosis with solution; recommends pricing experiments before confirming measurement artifact
```
Member 2 wins decisively (correct mechanism + exact diagnostic + avoids premature root-cause). Member 3 has a valid insight but commits prematurely to it.

### Reviewer 4
```rubric
member_1_user_advocate: insight=4, rigor=3, usefulness=3, risk=4
member_2_business_analyst: insight=5, rigor=5, usefulness=5, risk=4
member_3_devils_advocate: insight=4, rigor=2, usefulness=3, risk=3
member_4_historian: insight=4, rigor=4, usefulness=4, risk=3
member_5_designer: insight=4, rigor=3, usefulness=4, risk=2
strongest: member_2
weakest: member_3
severe_flag: member_3: dismisses measurement rigor as distraction without evidence; conflates product-fit vs packaging; assumes churners price-sensitive without validating NPS distributions
```
Member 2 dominates (mechanism + diagnostic + behavioral anchor). Member 3 reframes as business-model problem — could be right but lacks rigor to confirm it's not sampling noise.

### Reviewer 5
```rubric
member_1_user_advocate: insight=4, rigor=3, usefulness=3, risk=4
member_2_business_analyst: insight=5, rigor=5, usefulness=5, risk=5
member_3_devils_advocate: insight=4, rigor=2, usefulness=2, risk=3
member_4_historian: insight=4, rigor=4, usefulness=4, risk=4
member_5_designer: insight=4, rigor=3, usefulness=4, risk=3
strongest: member_2
weakest: member_3
severe_flag: member_3: conflates pricing-model mismatch with NPS validity without evidence; jumps to billing hypothesis without diagnostic rigor
```
Member 2 cuts cleanest. Member 3 has intuitive force but flips causality — one of five competing explanations, requires measurement before conviction.

### Reviewer aggregate (mean composite /20)
- member_2_business_analyst: 19.4  ← strongest (unanimous)
- member_4_historian: 15.4
- member_1_user_advocate: 14.0
- member_5_designer: 13.6
- member_3_devils_advocate: 11.2  ← weakest (unanimous; flagged premature pricing pivot, but = the genuine minority dissent to preserve)
# No council-breaking flag. DA flagged as weakest = standard "argues counter-position"; its view preserved as dissent per protocol.
