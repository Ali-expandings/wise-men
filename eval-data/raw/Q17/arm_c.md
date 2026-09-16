# Q17 Arm C — Chairman synthesis
# salvaged_from_context: false
# regenerated: 2026-05-29 (fresh full pipeline)
# CHAIRMAN MODEL: sonnet-4.6 (spawned as sonnet subagent for model parity — main thread was opus-4-8)
# members: 5 × sonnet-4.6 | reviewers: 5 × haiku-4.5 | chairman: 1 × sonnet-4.6 subagent
# eval tier: standard | Opus-DA rule SUSPENDED (model parity) | no flags
# dissent precedence: DA dissent >3 sentences → preserved as full dissent block

## Council answer

The short answer is that you are almost certainly reading two different populations with two different instruments, and the gap between them is doing the interpretive work you are attributing to a paradox.

NPS is a sentiment snapshot drawn from whoever responded to your survey at a particular moment in time. Retention is a behavioral count across your entire original cohort. Those two groups are not the same group, and until you prove they are, the 72 and the 55% are not in tension — they are measuring different things about different people at different times.

The most likely mechanism is survivor bias compounded by timing. By the time your NPS survey fires, the customers who were going to churn early have already gone. They never answered. The people who responded are disproportionately the engaged, the curious, the power users — the people who are, in fact, doing well with your product. Their enthusiasm is real. It just does not represent the full cohort that started month one with you. A small ecstatic segment can push a company-level NPS score into the seventies while a silent majority leaves quietly, politely, and without leaving a data trail.

The cheapest decisive diagnostic you can run right now costs almost nothing: join your NPS response table to your retention table by user ID. Tag every NPS respondent as either retained-at-month-6 or churned-at-month-6, then recalculate NPS separately within each group. If you find that churned users gave you scores of 8 or 9 before they left — the "happy quitter" signature documented at Amplitude, Slack, Notion, and Typeform — you have confirmed survivor bias and you have also learned something more important: your product is genuinely liked but not genuinely needed at the frequency your billing model requires. If instead you find that churned users gave you scores of 4 or 5, you have a different problem entirely — your NPS is inflated by non-representative responders and the product is failing a large segment silently.

Move one NPS touchpoint to month 5 or 6, before the churn decision is made rather than after. This alone will degrade your headline score, but the score you get will be honest.

While you are waiting for that data, instrument behavioral divergence. Do not ask churned users why they left — post-hoc rationalization produces answers that feel true and are often useless. Instead, look at what churners were doing differently from retainers in months 2 and 3. Where did their session depth drop? Which features did they touch once and never return to? Where did the habit loop break? The historical pattern across SaaS companies with this signature — high NPS, mid-50s six-month retention — is that the product creates a genuine peak experience, often around a specific aha moment, but lacks the infrastructure to survive motivation troughs: no variable-reward loop that pulls users back, no investment loop that makes the product increasingly personal and costly to abandon, no trigger tied to a real-world cue that recurs on the user's schedule rather than the product's.

The diagnostic sequence is therefore: (1) cohort-join NPS to retention this week, (2) shift one survey touchpoint to month 5-6, (3) identify the behavioral fork between retainers and churners at months 2-3, (4) design one re-engagement trigger tied to a real-world recurring cue. Do those four things before touching pricing, packaging, or retention campaigns.

Confidence: high that the diagnosis is measurement plus habit infrastructure, and that the cohort-join will resolve which component dominates. The confidence is tempered only by the possibility that the pricing model is itself the root cause — see dissent below.

## Dissent worth keeping

The Devil's Advocate position, stated plainly: you are not misreading anything. A 72 NPS with 55% six-month retention is not a measurement artifact — it is the signature of a product that delivers a real, memorable peak experience that users authentically loved but that does not fit the cadence of their lives. Real fans of something they do not need often enough to justify a recurring subscription will churn, and they will churn happily. They are not confused; they are rational. The problem is not your survey timing or your sampling methodology. The problem is that you are selling a subscription to episodic value. Spending six months fixing your measurement while the billing-model mismatch persists is six months of compounding churn. Test usage-based or seasonal pricing. Offer churned users a low-cost pause tier and measure reactivation rates from paused accounts versus fully churned accounts. The answer may be that your product is worth $9 four times a year, not $29 every month — and no amount of habit-loop engineering will change that if the underlying usage pattern is inherently episodic.
