# arm: wise-men | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# skill: SKILL.md v3.9.2 (as written); deep tier selected by the skill (6 members, 6 reviewers, checker)
# subagent tokens: 193026 | tool uses: 22 | duration: 564s
# note: the orchestrator prefixed process commentary (checker outcome) before the skill output — kept below verbatim, stripped at blinding as status text; one local scratchpad path in the audit footer replaced with <scratchpad>

Stage 4.5 checker returned 2 of 4 checks failing:

- **DISCLOSURE: FAIL** — legitimate catch. The draft never explicitly stated that the debate trigger didn't fire / no debate round ran. Fixing.
- **GROUNDING: FAIL** — checker flagged "Twilio, Stripe, MongoDB Atlas" as unsupported. I disagree with this one: checking back against the actual Stage 1 verbatim answers, Business Analyst wrote *"dominant pattern in API-product pricing (Twilio, Stripe, most usage-heavy SaaS)"* and Historian wrote *"made Twilio, Stripe, and AWS usage-based from day one... MongoDB Atlas has org access plus compute/storage metering."* The claim is grounded — the checker's FAIL is a false positive caused by the condensed member summary I sent it (which dropped those company citations), not an actual gap in the source material. Keeping the claim, disclosing the checker's objection per protocol rather than silently overriding it.

Finalizing the synthesis with the disclosure fix.

---

*Note: brief format upgraded to full because preserved dissent exceeded 3 sentences (dissent-precedence rule).*

## TL;DR

Don't treat this as a binary seat-vs-usage pick. The council rated the Devil's Advocate's reframe highest across every reviewer: before repricing anyone, find out whether your 10x usage variance is value (heavier users getting more from the product) or waste (inefficient integrations hitting your meters harder), because that determines which model is actually correct — then land on a hybrid model (base fee + metered usage overage), priced immediately for new customers and phased in for existing ones via grandfathering.

## Decision / Answer

Five of six members independently converged on the same destination: pure per-seat and pure per-usage both break under 10x variance. Seat pricing overcharges your light users and undercharges (or leaves money on the table with) your heaviest ones; pure usage pricing creates bill-shock, unpredictable revenue, and gives your most valuable accounts the strongest incentive to shop around or negotiate down. The fix converged on by Business Analyst, User Advocate, Historian, Skeptic, and Pricing Strategist is a hybrid: a base platform/access fee that covers your fixed cost-to-serve, plus metered usage above an included allotment, so revenue scales with consumption without customers losing all budget predictability. This is also the pattern named independently by two members as the dominant real-world shape for API/infrastructure products — Business Analyst cited Twilio and Stripe, Historian cited Twilio, Stripe, AWS, and MongoDB Atlas specifically (vs. Slack/Zoom/Salesforce for seat-fit collaboration tools).

But all six reviewers, independently and unanimously, rated the Devil's Advocate's answer highest on every axis (correctness, insight, practical usefulness, and risk awareness) — and the reason matters: DA is the only member who questioned whether the 10x variance itself means what the other five assume it means. Two other members, Historian and Pricing Strategist, independently flagged almost the identical weakest assumption in their own answers — "does the usage metric actually track cost-to-serve/value" — without realizing they'd converged on it. That means the entire hybrid consensus is standing on one unverified premise, named by three separate members through two different routes (one as an explicit dissent, two as self-reported weak points). If your 10x variance is heavy users getting proportionally more value, usage-based pricing is correct and undercharging them today is a real problem. If it's inefficient integrations (retries, polling, missing caching, sandbox traffic hitting production meters), usage pricing means invoicing customers for your own product's inefficiency — and the first competent engineer on their side who notices will cut your bill (and your revenue) sharply the moment they optimize it away.

Concrete path: (1) instrument usage now and, for existing customers, show the hypothetical usage-based cost on invoices without changing what they're actually billed — roughly two quarters of "shadow metering." This tells you whether the variance is value or waste, and it builds the metering/billing infrastructure a usage component requires anyway. (2) Price every new customer on the hybrid model (base fee + metered overage) starting immediately — new logos have no prior price to revolt against, so there's no reason to wait on them. (3) Fix sales compensation in parallel — if reps are still paid on seat-count bookings when the pricing conversation reaches existing customers, the org will reconstruct seat economics informally regardless of what the price sheet says. (4) Once shadow data confirms the variance is meaningfully value-driven (the base-rate-likely outcome for most API businesses, per Historian's cross-industry pattern), migrate existing customers with grandfathering: lock in current effective pricing for at least one renewal cycle (estimates across members ranged 90 days to 12 months), ship a side-by-side bill-comparison tool before the first new invoice, and offer an opt-in early-migration incentive rather than an imposed flip date. Before finalizing tier breakpoints under either path, pull actual usage percentiles (P50/P90/P99) and per-account gross margin — guessing at thresholds either gives away margin or throttles your best customers on day one.

Cost of being wrong: choosing to skip the diagnostic step and going straight to hybrid-with-grandfathering (the five-member majority's answer) is not reckless — hybrid is very likely the correct destination either way, and grandfathering is real protection. What's harder to recover from is billing existing customers for usage variance that turns out to be your own product's inefficiency rather than their value — that's the scenario that turns a defensible pricing decision into a trust and press problem (see the Mailchimp 2019 and HubSpot 2023 precedents below), and it's much harder to walk back publicly than a two-quarter delay is to justify internally.

## Confidence

**Medium** — six of six reviewers rated the reframe highest and the hybrid destination is well-converged (5 of 6 members, consistent with named industry precedent), but confidence is capped at Medium because two members independently named the same unverified premise (whether usage tracks cost-to-serve/value) as their single weakest assumption, and that premise is load-bearing for the entire recommendation. No member had data to resolve it, because the question came with no usage or margin data attached — this council was run "none needed" on context brief, i.e. purely from the question as stated.

## Where the council agreed

- Pure per-seat and pure per-usage both fail under 10x variance; some hybrid shape (base fee + metered usage) is right, not a binary pick between the two options named in the question.
- Migrating existing customers without grandfathering is the single highest revolt-risk move, regardless of which model you land on — Historian named two real, checkable precedents: Mailchimp's 2019 "Audience" pricing change and HubSpot's 2023 marketing-contacts pricing change, both of which triggered public backlash after insufficient notice and no grandfathering. (Reviewers independently corroborated these as real, documented events.)
- New customers can be priced on the new model immediately with no revolt risk at all — the entire risk is concentrated in repricing the existing base.
- Sales compensation and internal incentives must be realigned alongside the pricing change, or the sales org will informally rebuild seat pricing regardless of the new price sheet.

## Where the council split (preserved dissent)

The Devil's Advocate's reframe — verify value-vs-waste first via shadow metering, reprice only new logos in the meantime — is rated highest across the board and leads the Decision above. The clean counter-position, held by the other five members (Business Analyst, User Advocate, Historian, Skeptic, Pricing Strategist), is: **skip the diagnostic phase**. You already have enough signal — 10x variance under equal seat pricing is de facto evidence of unequal value capture — to commit to hybrid pricing now, using a generously-sized included usage allotment plus grandfathering as the sole risk mitigation, rather than spending a full product cycle instrumenting before acting. Under this view, the value-vs-waste ambiguity DA raises is real but second-order: a well-designed included allotment already absorbs normal variance, and two quarters of delay has its own cost — continued margin bleed on whale accounts today, and the real risk of a competitor reaching value-aligned pricing first. This view is more likely right if the business is already losing money on its highest-usage accounts (DA's own named weakest assumption) or if competitive pressure makes the two-quarter wait itself the more dangerous move — in either case, the council's majority says move straight to hybrid-plus-grandfathering rather than wait.

Severe-disagreement flags raised: none. One non-severe credibility flag, raised independently by 4 of 6 reviewers: the Skeptic's specific statistics ("20-40% MRR variance increase," "5-15% churn from change-aversion") are unsourced and read as fabricated precision — treat them as illustrative, not as numbers to plan a forecast around.

## Action items

1. Pull your actual usage distribution (P50/P90/P99) and per-account gross margin now — needed under either path in the dissent above.
2. Start shadow-metering existing accounts (or skip straight to committing, per your own risk tolerance and the dissent) for one to two quarters: instrument usage, show hypothetical usage-based cost on invoices, keep current billing unchanged.
3. Price all new customers on the hybrid model (base fee + metered overage) immediately.
4. Realign sales compensation toward usage/expansion, not pure seat count, before the pricing conversation reaches existing customers.
5. When migrating existing customers, grandfather current effective pricing for at least one full renewal cycle (90 days minimum; 2-3 cycles is safer), ship a bill-comparison/usage-visibility tool before the first differently-priced invoice, and offer an opt-in early-migration incentive rather than a forced flip date.

## Open questions the council couldn't resolve

- Whether the 10x usage variance reflects genuine value differences or integration inefficiency — this single fact would most change the answer, and no member had the data to resolve it.
- How much competitive or runway pressure the business is actually under, which determines whether the DA's "wait two quarters" path or the majority's "commit now" path is the better bet — this depends on facts (cash runway, competitive threats, whether whale accounts are margin-positive today) that no context brief was provided for.

---

## Full audit

### Member answers
All 6 verbatim member answers, all 6 verbatim reviewer rubrics, and the grading packet are preserved in `<scratchpad>/pricing-council-grading-packet.md` (Business Analyst, User Advocate, Historian, Skeptic, Pricing Strategist, Devil's Advocate — full 5-section outputs).

### Rubric scores (reviewer means, 6 reviewers, 1-5 scale)

| Member | Correctness | Insight | Practical | Risk | Overall |
|---|---|---|---|---|---|
| Business Analyst | 4.17 | 3.00 | 4.00 | 4.00 | 3.79 |
| User Advocate | 3.50 | 2.00 | 3.67 | 3.17 | 3.08 |
| Historian | 4.83 | 4.00 | 4.00 | 4.00 | 4.21 |
| Skeptic | 3.17 | 3.67 | 3.67 | 5.00 | 3.88 |
| Pricing Strategist | 4.17 | 4.17 | 4.00 | 4.00 | 4.08 |
| Devil's Advocate | 4.17 | 5.00 | 4.33 | 5.00 | **4.63** |

Top pick: Devil's Advocate, unanimous 6/6. Bottom pick: User Advocate, unanimous 6/6.

### Debate transcript
Not run. Canonical trigger checked after Stage 2: no rubric axis had variance ≥1.5 across reviewers for any member; no member was ranked top-2 by some reviewers and bottom-2 by others on the same axis; the position map showed "hybrid + grandfather" holding a 5/6 majority. All three clauses required to skip were satisfied, so deep tier's conditional debate round did not fire — this is disclosed per Stage 4.5's DISCLOSURE check, which caught its absence from the first draft.

### Synthesis checker (Stage 4.5) findings
DISSENT: PASS. CONFIDENCE: PASS. DISCLOSURE: FAIL (fixed — added the explicit debate-trigger-did-not-fire statement above). GROUNDING: FAIL, disputed — checker flagged the Twilio/Stripe/MongoDB Atlas claim as unsupported, but this was an artifact of a condensed member-answer summary I sent it rather than the full verbatim text; Business Analyst's and Historian's actual Stage 1 answers do name those companies. Kept the claim, disclosing the checker's objection here rather than silently overriding it.

### Protocol notes
Composite difficulty 4/5 (depth=4, stakes=4, novelty=2) → deep tier. 6 members (5 domain personas + mandatory Devil's Advocate), models: Business Analyst/Historian/Skeptic/Pricing Strategist/Devil's Advocate on Sonnet 5, Devil's Advocate on Opus 5 (per-role +1 tier override), User Advocate on Haiku 4.5 (haiku-tolerant override). 6 reviewers (deep tier: reviewers = member count) on Sonnet 5. No Stage 1 or Stage 2 validator retries — all 6 members and all 6 reviewers passed on first attempt. Chairman: main thread. Stage 4.5 checker: 1 call, Sonnet 5, findings above. No context brief was gathered (question is self-contained, per this run's scope); this caps Confidence at Medium as noted. No project/vault record was written for this run — this invocation was scoped to answer the question directly with no filesystem or vault access.

---

*Council of 6 members, deep tier, 6 reviewers, no debate round, 1 synthesis-checker pass. Want the raw grading packet? It's at the scratchpad path above.*
