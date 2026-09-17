# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 120259 | tool uses: 4 | duration: 648s

## Council

Three members, launched in parallel, read-only, independent (no cross-visibility between reports). This harness only exposes Claude models — GPT and open-source options from the skill's default roster aren't available here, so the roster substitutes across Claude's three tiers to preserve the intended angle split:

- **Opus** — architecture/correctness angle (native fit for the skill's "strongest reasoning model" slot): does the pricing metric actually map to cost-to-serve and value for an API product.
- **Sonnet** — implementation/feasibility angle (substitute for the skill's GPT/implementation-review slot): metering infra, contracts, phased rollout mechanics.
- **Haiku** — contrarian/red-team angle (substitute for the skill's open-source/contrarian slot): pressure-test the obvious "just go usage-based" answer.

All three independently converged on the same shape of answer.

## Recommendation

Don't go pure per-seat, and don't go pure linear usage-based either — go **hybrid**: a base platform fee per account (not per seat) that bundles an included usage allowance, plus metered overage beyond it, with a committed-use/annual option for your heaviest accounts.

## Why

- **Per-seat doesn't track cost or value for an API product.** "Seats" barely map to machine-to-machine traffic, and at 10x usage variance, flat per-seat means your heaviest accounts can run at or below your cost to serve them while light accounts effectively overpay for what they consume. Worked example from the architect review: two accounts, same 5 seats — the light one runs ~70% gross margin, the heavy one runs *negative* margin, under identical per-seat pricing.
- **Pure usage-based fixes that but creates a new problem: it taxes success.** The contrarian review's strongest point: if bills scale linearly with volume, customers who grow get punished with a bigger invoice, which pushes them to throttle usage or engineer around the meter — the opposite of what you want. It also stalls B2B sales cycles, since procurement resists signing against an open-ended number.
- **Hybrid keeps most of your base predictable while still capturing the tail.** The allowance covers the majority of accounts with a flat, forecastable bill; overage and committed-use capture the value of the 10x cohort without making every customer's bill volatile. This is also the pattern usage-heavy B2B platforms (Snowflake/Datadog-style) generally land on, per the implementation review.
- **Get the billable unit right, or the pricing change won't hold.** If the 10x is driven by more calls per customer, bill on a unit that resists gaming — records, tokens, or compute-units rather than raw request count, or customers just batch calls and your revenue drops while your cost doesn't. If it's driven by more end-entities per account, price per entity instead. None of the three reviews could resolve which one applies — that depends on data only you have.

## Tradeoffs and risks

- **The top-usage decile is both your best logos and your highest migration risk.** All three reviews independently flagged this group for white-glove handling — a named contact, a phased increase (e.g., 25/50/75/100% of the delta over several quarters), and the committed-use discount framed as "here's how to pay less," not a form email announcing an increase.
- **Metering has to be invoice-grade before you bill on it.** Decide up front whether retries, errors, or timeouts count as billable, make ingestion idempotent, and give customers a usage dashboard fed by the same pipeline as the invoice. Mismatches between what customers see and what they're billed are what actually trigger disputes — more than the price change itself.
- **Check existing contracts before announcing anything.** Any multi-year or fixed-term deal needs a legal read for repricing/amendment clauses; don't let a pricing announcement get ahead of what you're actually allowed to change mid-contract.
- **Hybrid doesn't fully dissolve the contrarian's objection, it just contains it.** There's still variability at the margin (overage), so some procurement friction and "am I being punished for growing" psychology survives — just scoped to the tail instead of your whole base.
- **This is a real build, not a pricing-page edit.** Budget for it: roughly 4–6 months to first migrated customer using a billing vendor (Orb, Metronome, Lago, Stripe Billing) for the rating/invoicing layer, materially longer if built in-house. Team involved: 1–2 backend engineers, someone from finance/RevOps to set rates off real usage data, support for the dashboard and alerting, and sales/legal for new contract templates.
- **Confidence is medium-high, not certain.** All three reviews flagged the same gap: nobody has your actual usage distribution (p50/p90/p99), what specifically drives the 10x spread, or current per-account margins. Exact tier sizes and overage rates shouldn't be locked without that.

## Final call

1. Shadow-meter the hybrid model against real traffic for 1–2 full billing cycles and re-price every existing account against it before announcing anything. If most accounts land flat or lower and increases concentrate in the accounts that are margin-negative today, that's your defensible story.
2. Ship the new pricing to new signups first. Zero risk to existing revenue, and it proves the meter works under real load.
3. Segment existing accounts by bill impact: early light-touch migration for anyone whose bill goes down; standard notice period for small increases; named-human, glide-path treatment for the top usage decile. Anything on a signed fixed-term contract stays on current pricing until renewal.
4. Give 60–90 days' notice, show every account a "what you'd have paid last quarter" calculator before their bill actually changes, and turn on spend alerts/caps from day one.
5. Before finalizing exact rates, pull your own usage-distribution data — where the 10x actually comes from, and revenue concentration in the top decile. Every council member named this as the single biggest open unknown, and it decides both the billing unit and how aggressive the overage pricing can be.
