# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q13 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (re-run under Amendment 1; first run read the author's private notes and was discarded)
# adaptation: no-human — see PREREG.md
# subagent tokens: 82449 | tool uses: 1 | duration: 67s

# Market Entry Strategy vs. Dominant Player

**Classification: Architectural.** High-stakes, multi-part decision — affects positioning, product, pricing, go-to-market. Full process: questions, approaches, sectioned design.

## Clarifying Questions + Assumed Answers

*(No further context given — assumed most likely defaults based on framing of question)*

**Q1: High switching-cost market (contracts, lock-in, infrastructure) or low switching-cost (subscriptions, consumer, easy to try)?**
Assumed: low-to-moderate switching cost. Question doesn't mention contracts/renewals/lock-in — if it were high-lock-in enterprise, "go after unhappy customers" wouldn't even be on table (can't poach mid-contract). Low switching cost fits challenger-vs-incumbent framing given.

**Q2: Do we have a real wedge — some structural edge (cost, tech, speed, channel) — or just "we'll execute better"?**
Assumed: some edge exists, likely on a narrow dimension (speed, focus, service, or a specific use case), not across the board. 10x resource gap ruled out "win on breadth."

**Q3: Funding position — bootstrapped/scrappy or well-capitalized challenger?**
Assumed: resource-constrained relative to incumbent (stated directly: "10x their resources" on THEIR side implies we're the underdog, likely lean).

**Q4: B2B or B2C?**
Assumed: unspecified, treat as B2B-leaning — "dominant player," "strong brand," "10x resources" phrasing reads as enterprise/market-share language rather than consumer-brand language. Recommendation below holds either way.

**Q5: Timeline pressure — need revenue proof in ~12mo, or building for multi-year moat?**
Assumed: need traction proof within 12-18mo (typical startup runway constraint), not multi-year patience play.

## Three Approaches

**A. Go after unhappy customers.**
Pro: fast — angry customers convert quick, testimonials write themselves. Con: you're fighting on incumbent's home turf, on their weaknesses. Incumbent notices churn, patches weakness, out-resources you fixing it. Also: unhappy customers churn for many reasons — some are bad-fit customers who'll be unhappy with you too. Weak business, not a strategy on its own.

**B. Find ignored niche.**
Pro: no direct fire — incumbent's 10x resources don't matter if they're not pointed at you. Room to build beachhead, refine product-market fit without a bigger competitor watching. Con: risk of picking niche too small to matter, or niche stays ignored because it's genuinely unprofitable (test that assumption first).

**C. Something else — different axis entirely.**
Reframe category, different business model (usage-based vs seat-based, self-serve vs sales-led), different distribution channel incumbent can't easily copy without cannibalizing their own model. Highest upside, highest execution risk, hardest to validate cheaply.

## Recommendation: Hybrid — Niche Beachhead, Filtered by Unhappy Customers

Don't pick one of three in isolation. Combine B and A: find underserved niche where incumbent's weakness (the thing making some customers unhappy) is *structural* to how incumbent built their product — not a fixable bug. That's the real signal. Incumbent optimized for their core 80%, and structurally underserves an edge segment. Customers in that segment are unhappy *because* incumbent can't easily fix it without hurting their core business (classic disruption pattern — this is why they don't chase you back).

This is a judo strategy: use incumbent's size against them. Their strength in the core market becomes rigidity at the edge.

**Why not C first:** highest execution risk, no proof-of-life before big investment. Revisit C once beachhead (B+A) gives you data, revenue, and credibility.

**Why not A alone:** no defensibility. Any advantage from "we listen better" gets closed by incumbent shipping a fix. Need a segment where the *fix is expensive for them, cheap for you* (different tech stack, different pricing model, different cost structure) — that's what makes niche + unhappy-customer overlap defensible instead of just a feature race.

### Design

**Target segment:** intersection of (a) underserved by incumbent's core product, (b) vocal/switchable (not locked into contracts), (c) fix required is structural for incumbent, incidental for you. Find this by pulling churn/complaint data (review sites, forums, support communities) and asking: *why* unhappy — feature gap, or misfit product for their use case? Misfit = your niche.

**Go-to-market:** narrow positioning, not "better X for everyone" — "X built specifically for [segment]." Direct outreach to people already complaining publicly (reviews, Reddit, competitor's own support forums) — cheapest acquisition, highest intent.

**Risk / mitigation:** niche too small → validate market size before full build (10-20 customer interviews, not survey). Incumbent notices and reacts → likely late, since fixing structurally means rebuilding, not patching; monitor their release notes as early warning. Bad-fit unhappy customers (churn for reasons unrelated to your wedge) → filter hard in interviews, don't chase every complainer.

**Validation before full build:** talk to 15-20 people in target segment, confirm complaint is structural not cosmetic, get 3-5 to pre-commit (LOI, deposit, or beta signup) before writing more than an MVP.

**Milestones (12-18mo):** month 1-2 segment validation, month 3-6 MVP + first paying beachhead customers, month 6-12 prove retention/expansion within niche, month 12+ decide whether to expand niche-by-niche or pivot toward approach C with proof in hand.

**Bottom line:** don't choose "unhappy customers" or "niche" as competing options — the durable version is their overlap, entered small, validated cheap, expanded only after proof.
