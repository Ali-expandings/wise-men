# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 81108 | tool uses: 1 | duration: 53s

**Classification: Bounded** — this is a single, well-scoped decision (one pricing model change) with a clear existing state (a pricing model already in place) to move from, not a multi-system buildout. Short design in chat, no spec doc.

**Clarifying questions (answered from the question's own context, since no reply is available):**

1. *What's your current model?* — Not stated directly, but "switch... without a revolt" implies an existing paying base on a model they'd resent losing. Most likely: **per-seat today** (the classic starting point for B2B SaaS-turned-API products).
2. *Does usage correlate with your infra/compute cost, or mainly with customer value?* — For an API product, usage (calls/compute) is almost always the direct cost driver. Assumed: **yes, usage tracks cost**.
3. *Is the 10x spread a few outlier whales vs. a smooth continuum?* — "Varies wildly" reads as a continuum, not two clean buckets. Assumed: **continuum**, which rules out simple two-tier segmentation.

---

## Design

**Recommendation: hybrid — platform/seat base fee + metered usage on top, not pure per-seat and not pure pay-as-you-go.**

Why not the extremes:
- **Pure per-seat** breaks under a 10x usage spread — light users subsidize heavy ones, heavy users get a windfall (and keep growing usage at zero marginal price to you, which hurts if usage drives your costs), and you're leaving revenue on the table from your best accounts.
- **Pure usage-based** aligns price to cost/value but creates bill unpredictability, which finance/procurement teams resist — it also makes revenue lumpy and forecasting harder for you.

**The hybrid shape:**
- Base platform fee (small, seat- or tier-based) covering access + a bundled usage allowance.
- Metered overage beyond the allowance, billed per unit (calls/tokens/whatever your natural usage unit is — pick one dimension, not several).
- Volume discounts / committed-use tiers for your heaviest accounts (pay-upfront-for-a-block-at-a-discount, à la AWS/Snowflake/Twilio) — this is what actually captures the value from the 10x-usage customers instead of losing them to a competitor with better volume pricing.

This is the standard shape for API products with wide usage variance because it gives predictability at the low end (a base fee, a bill floor) and captures upside at the high end (metered overage + committed tiers), without pure-usage's bill-shock problem.

---

## Migration plan — avoiding the revolt

1. **Grandfather, don't flip a switch.** Existing customers keep current pricing for a defined window (6–12 months) or get a "you will not pay more than today" guarantee during transition.
2. **Preview before you charge.** Run the new model in shadow/dashboard mode for 1–2 billing cycles so customers see what they'd owe under the new plan before it's real. Removes surprise as the source of anger.
3. **Segment the comms, lead with winners.** Split customers into "pays less," "roughly flat," and "pays more" under the new model. Reach the "pays less" group first — they become your social proof / case studies. Handle "pays more" individually, not via a mass email.
4. **Ramp, don't cliff, for increases.** Customers facing a real increase get a phased step (e.g., 25/50/75/100% of the delta over 3 months) instead of an immediate jump.
5. **New customers go straight to the new model.** Only existing customers get the transition path — this bounds your complexity and cost.
6. **Give 60–90 days notice**, a clear FAQ, a pricing calculator, and a named contact for anyone above a revenue threshold.
7. **New customers get simple, visible usage alerts** (soft caps, "you're at 80% of allowance") so nobody gets blindsided on the new model either — this is the ongoing anti-revolt mechanism, not just a migration-week one.

**Net:** per-usage-with-a-base (hybrid, tiered/committed) is the right target model for 10x usage variance; the switch is de-risked by grandfathering, preview billing, segmented outreach led by the customers who win, and ramped (not cliff) increases for the ones who don't.
