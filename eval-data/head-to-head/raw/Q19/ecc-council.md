# arm: ecc-council (affaan-m/ECC 8321021c54d6) | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: no-human (a clarifying question becomes a stated assumption) — see PREREG-2.md
# subagent tokens: 97233 | tool uses: 4 | duration: 330s

## Council: Per-seat vs per-usage pricing for an API product

**Architect:** Move off pure per-seat to a hybrid — base fee plus a usage component — because cost-to-serve and customer value both scale with API calls, not seats.
A 10x usage spread means one seat price is always wrong for someone: too expensive for light accounts, a giveaway for heavy ones.

**Skeptic:** Don't jump straight to per-call metering — replace seats with 5-6 flat-priced usage tiers, each with a generous included allowance, not fine-grained metering.
Metering taxes the exact behavior you want more of: customers ration, cache, and negotiate around a meter; tiers let usage grow without feeling like a toll.

**Pragmatist:** Hybrid (base fee + metered overage) is right, but ship it by renewal cohort with a time-boxed grandfather period, and don't announce anything until every account's usage has been run against the new price book.
The model debate is the easy part — the rollout lives or dies on whether billing/metering is accurate and visible before the first new invoice goes out.

**Critic:** Structurally, hybrid is correct, but your 10x accounts are almost certainly your best customers — the switch hits them hardest, right when renewal gives them the most leverage to push back.
"Revenue-neutral in aggregate" hides brutal account-level variance; the losers escalate loudly and the winners barely notice, so aggregate math won't save you from a revolt.

### Verdict
- **Consensus:** Per-seat can't survive a 10x usage spread — all four voices agree. The real danger is the migration, not the model: undefined or opaque usage metering is what actually triggers a revolt, and three voices converged on that independently.
- **Strongest dissent:** Skeptic rejects fine-grained per-call metering in favor of coarse volume tiers — metering infrastructure is costly to build and support, and it taxes the usage growth you're trying to encourage. This materially shifted the recommendation below rather than being overruled.
- **Premise check:** Yes. Skeptic reframed "seat vs. usage vs. hybrid" as really a question of metering granularity — that reframe survives into the recommendation.
- **Recommendation:** Base fee + a small number of usage tiers (not per-call metering), generous allowance per tier, soft overage rate only past the top tier for true outliers. Before announcing anything:
  - Model every existing account's real usage against the new price book; flag accounts by percent moved, not just aggregate impact.
  - White-glove your heaviest-usage accounts individually — they're your best customers, and the ones hit hardest at exactly the moment (renewal) they have the most leverage.
  - Roll out by renewal cohort, not flag-day; put a written, contractual sunset date on any grandfathering — no open-ended two-tier pricing.
  - Define what counts as a billable unit (retries, errors, webhooks, batches, cache hits) with worked examples, and give customers a live usage dashboard before the first new invoice — not after the first dispute.
  - Check existing contracts for price-lock or fixed-term clauses before promising anyone a timeline.
