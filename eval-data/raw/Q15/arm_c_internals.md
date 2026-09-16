# Q15 Arm C internals — 5 members (sonnet-4.6) + validator
# salvaged_from_context: false
# tier: standard (eval-fixed); Opus-DA rule suspended (all members sonnet)
# domain: product → personas: User Advocate, Business Analyst, Devil's Advocate, Historian, Designer
# validator: all 5 members emitted full 5-section structure, non-empty → PASS, 0 retries

--- Member: User Advocate ---
## Core judgment
The product is rarely the problem. The failure mode is that the launch creates a burst of users who are actually just curious observers — people who showed up because of the press coverage, not because they had a burning problem the product solves. They try it once, get confused or bored, and leave. The team reads the initial signups as validation, builds more features, and never fixes the thing that made the first 500 users churn silently.

The real kill shot is the gap between "people think this sounds cool" and "people need this badly enough to change their behavior." Press coverage attracts the former. Products survive on the latter. When the launch noise fades, you're left with whoever genuinely had the problem — and if that group is too small, or if you never figured out how to reach them without the PR machine running, the numbers just slowly bleed out.

There's also a trust cliff. If someone signs up during the hype, has a mediocre first experience, and leaves — you've essentially used up your one shot with them. They will not come back when you fix the thing that confused them. They already decided. So a bad onboarding experience during launch week doesn't just lose those users, it poisons the well permanently with the exact audience the press sent you.

## Top risks
- First-time users hit a confusing moment and leave before seeing the value, and no one notices because signup numbers look fine
- Team celebrates press coverage as product-market fit, slows the hard retention conversations, loses 3-6 months
- Product solves a real problem but for a much smaller group than the hype implied; unit economics never work at that scale
- No one owns turning a curious visitor into a returning user — it falls between marketing and product
- Team burns out chasing the next spike instead of helping existing users succeed

## Recommended change
Before the next launch, define what a "successful user" looks like in behavioral terms (came back three times, completed one specific action, told someone else) and instrument that metric before you go live — not after.

## Confidence
High — this pattern repeats across categories and company sizes, and the mechanism (hype attracts the wrong users, team misreads signals) is consistent.

## Weakest assumption
The assumption that the product is genuinely good — if it only seems good to the founders but confuses real users from the first minute, the diagnosis shifts from "distribution problem" to "product problem."

--- Member: Business Analyst ---
## Core judgment
The failure mode is almost never product quality. It's the gap between acquisition economics and retention economics. A launch event is a one-time marketing spend that buys you a cohort of users whose behavior you haven't yet measured. Press coverage inflates early DAU/MAU, which flatters vanity dashboards, which delays the signal that Month 2 retention is 15% and LTV is $8 against a CAC of $40. By the time the math is undeniable, runway is 6 months and the team is in triage mode rather than fix mode.

The deeper structural problem: launch spend is front-loaded but revenue is back-loaded. Most products are priced and staffed for a growth curve that assumes compounding retention. When churn runs hot, you need more acquisition spend just to hold flat MAU, which accelerates burn. You're running a leaky bucket and pouring press releases into it. The "good product" framing is a trap — good for whom, measured how, at what point in the user journey?

The third layer: press coverage attracts the wrong cohort. Tech press readers and early adopters have different jobs-to-be-done than the mass market the unit economics require. The launch cohort churns fast, the team mistakes their feedback for signal, builds for them, and drifts further from the paying customer archetype that would sustain the business.

## Top risks
- Retention economics never modeled before launch — true LTV/CAC discovered at Month 4 when too late to restructure pricing
- Launch cohort systematically unrepresentative, poisoning roadmap with wrong-customer signal
- CAC payback exceeds runway, making growth capital-destructive at any spend level
- No owned distribution channel built during the hype window — when press fades, no low-CAC re-engagement
- Team confuses engagement metrics (sessions, page views) for retention metrics (D30/D90 return, expansion)

## Recommended change
Before launch, model the retention waterfall explicitly: project Month 1/3/6 cohort survival, multiply by ARPU, compare to blended CAC, and only proceed if payback period fits inside your funding horizon — kill or reprice if it doesn't.

## Confidence
High — this failure pattern is mechanically consistent across B2C and prosumer B2B; the math doesn't change based on industry.

## Weakest assumption
The assumption that retention economics are knowable and fixable before launch — some products have structurally low retention ceilings (seasonal, one-time jobs) no iteration will change.

--- Member: Devil's Advocate ---
## Core judgment
The "good product, bad retention" story is almost always a post-hoc rationalization told by people who never understood what problem they were actually solving. The real failure mode is not retention or activation — it is that founders and the press conspire to create a false measurement environment. Launch coverage selects for novelty-seekers, curious journalists, and early adopters who will try anything. These people are structurally incapable of representing the actual market, so the "initial traction" signal is garbage data dressed up as validation. The product did not fail after 18 months. It never had real traction to begin with — you just could not see the void because the noise was so loud.

The deeper issue is that "genuinely good" is doing enormous, unearned work in the question itself. Good by whose standard? The team built something they find elegant, reviewers found interesting, early adopters found novel. None of those people are the median user with a real workflow, real switching costs, and a genuine pain they need solved on a Tuesday afternoon under deadline pressure. The product was almost certainly solving a problem that felt urgent in a demo and vanished the moment real life intervened. That is a problem-definition failure that preceded the launch by 18 months.

The 18-month timeline is also suspect. It implies the product had a meaningful run and then declined. More often, the decay begins at week three, founders paper over it with "we're still iterating," runway runs out, and the post-mortem lands at month 18. The splash was a mirage. The quiet death was always the trajectory.

## Top risks
- Founding team optimizes for press coverage as a proxy for PMF, which are anti-correlated signals in most categories
- The problem is real but seasonal/situational/low-frequency — even satisfied users don't need it enough to become habitual
- Distribution mistaken for demand: surge of installs looks like pull but is push from social proof and FOMO
- Assumed moat is product quality; actual moat requirement is switching-cost creation, never built
- Investor timelines force a growth phase before PMF is confirmed, burning credibility on users who'd never retain

## Recommended change
Kill the public launch entirely and spend the first 12 months in a closed, paid pilot with ten customers who are paying with budget that already exists and screaming about the problem before you showed up.

## Confidence
Medium — the counter-argument is itself a generalization that will be wrong for categories where press coverage genuinely drives durable distribution (some developer tools, security, enterprise where coverage credibility is the purchase driver).

## Weakest assumption
The assumption that "genuinely good" is meaningless — if a product is objectively superior on dimensions that matter to a large addressable population with high switching readiness, the failure really is distribution/retention mechanics, not problem definition, and the argument collapses.

--- Member: Historian ---
## Core judgment
The actual failure mode is almost never product quality. It's the gap between acquisition and retention, specifically that launch press creates a spike of curiosity-driven signups from people who were never going to become habitual users. The team looks at the spike, mistakes it for validation, hires to scale, and then discovers that the cohort that came in during launch week churns at 80-90% by week 8. The product works, but it works for a narrower audience than the press moment implied.

The named version is the "TechCrunch bump" — documented repeatedly from roughly 2009 onward as a real but misleading signal. Products like Yo (2014), Ello (2014), Peach (2016), and Clubhouse (2020-2021) all showed this pattern: massive launch attention, genuine early enthusiasm, then a trough when the curiosity audience exhausted itself and the product hadn't built enough habitual use among the core to sustain organic word-of-mouth. Clubhouse is the clearest recent case — 10 million users in early 2021, then a collapse near-total by mid-2022, not because the product broke but because the core use case (serendipitous live audio) required a density of users the trough destroyed.

Products that survive typically share one trait: they found the small group of people who were actually changing behavior before the launch spike hit, and treated that group as the real signal. Notion had years of quiet growth before it became "hot." Figma was the same. The launch splash for both was a lagging indicator of real retention, not the cause of it. Products that die treat the spike as the beginning; products that survive treat it as a test to see if anyone stays.

## Top risks
- Mistaking launch cohort size for PMF — curiosity audience and habitual-use audience are almost never the same people
- Post-launch hiring that raises burn before retention is proven, compressing runway to find real ICP
- Metric selection that hides churn: tracking MAU/signups while weekly retention collapses underneath
- No re-engagement loop for early churned users, so they're gone permanently even if the product later improves
- Team morale structured around the spike — the trough feels like failure even when the core cohort is healthy, causing premature pivots

## Recommended change
Before the launch event, identify the 50-100 users who have already changed a real behavior because of the product, study them obsessively, and use their retention curve (not the launch spike) as the only metric governing headcount and spend for the next 12 months.

## Confidence
High — this pattern is well-documented across multiple product cycles; the underlying mechanism (curiosity-driven acquisition vs habit-driven retention) is structurally consistent.

## Weakest assumption
The assumption that the core habitual-use audience exists and is large enough to sustain a business — some products die because the real retained audience is too small to be commercially viable.

--- Member: Designer ---
## Core judgment
The failure mode is almost never the product. It's the gap between a user's first session and their third. Launch buzz creates a surge of curious, low-intent users who try the product once under artificial conditions — motivated by novelty, not need. The product feels good in that moment. Then they leave. They don't come back because nothing happened to make coming back feel necessary. No habit loop formed. No moment of irreversibility occurred. The product never crossed from "interesting thing I tried" to "thing I reach for."

The deeper problem is that teams optimize for the metric launch rewards: signups, press mentions, Product Hunt ranking. Those metrics peak on day one and become irrelevant. But retention doesn't surface until week two or three, by which point the team has moved on to the next launch push. The gap between "impressive demo" and "daily utility" is where products die, and most teams never design for that gap specifically.

What makes this insidious is that a "genuinely good" product can still fail here. Good means technically capable. It does not mean the user understood what to do next, felt a reason to return, or built any mental model of when to reach for it. Those are design problems, not engineering problems, and they live entirely in the first-week experience.

## Top risks
- No defined "aha moment" — the product never delivers a single undeniable proof of value the user can remember and repeat
- Week-two vacuum — no re-engagement trigger (habit cue, email, social nudge) pulls the user back after novelty wears off
- Onboarding optimized for completion, not comprehension — users finish setup without understanding the core loop
- Feature bloat at launch — too many things to try means the user never goes deep enough on one to feel real value
- Team attention shifts post-launch — nobody watches day-7 and day-14 retention because the launch sprint is over

## Recommended change
Identify the single action that predicts retention (the "aha moment"), then redesign the entire first session around getting every new user to that action within 10 minutes.

## Confidence
High — this pattern (launch spike, retention cliff) is structurally consistent across categories and well-documented in growth data.

## Weakest assumption
The assumption that there is a single identifiable aha moment — some products have diffuse value that accumulates slowly, and forcing a single proof moment into session one would misrepresent the product.
