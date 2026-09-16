# arm: grilling (mattpocock/skills 85f83d3fde1d) | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 79650 | tool uses: 1 | duration: 84s

❓ **Q1** - **Does usage correlate with value delivered?**: The core question for usage vs. seat pricing is whether a customer calling your API 10x more is also getting roughly 10x more value (more automation run, more workflows completed, more revenue enabled) — or whether high usage is partly noise (inefficient integration, retries, polling) that would make usage-based pricing feel punitive rather than fair.

➡️ For an API product, usage is a reasonable value proxy — more calls/tokens/jobs generally means more real work happening for the customer, not just inefficiency.

**Assumed:** Usage ≈ value delivered (with some noise from inefficient callers worth normalizing later).

---

❓ **Q2** - **Does your cost (COGS) scale with usage?**: If infrastructure, compute, storage, or downstream API costs scale roughly with call volume, flat per-seat pricing leaves you exposed — heavy users (10x) erode margin while light users overpay relative to what they actually draw on your infra.

➡️ Assume yes. API products almost always carry usage-correlated marginal cost. This is the strongest argument against pure per-seat.

**Assumed:** Costs scale with usage; per-seat alone creates margin risk on the heavy tail.

---

❓ **Q3** - **Do customers need predictable, budget-lockable bills?**: Enterprise buyers and procurement teams often resist pure usage-based pricing because it's hard to budget against; smaller/startup customers are usually more usage-tolerant, especially if it's cheaper at low volume. A 10x usage spread implies a long tail of small accounts plus a handful of power users, possibly including larger enterprise buyers.

➡️ Assume a mixed base with real predictability needs at the top end.

**Assumed:** Mixed predictability needs → a hybrid model is safer than pure usage-based.

---

❓ **Q4** - **What's the current pricing model, and are there existing commitments?**: Whether you're migrating off pure per-seat, off flat/unlimited, or pricing something for the first time changes the switch strategy. Framing the question as "deciding between" while worrying about "revolt" implies an existing base already paying under one model.

➡️ Assume you're currently on (or close to) per-seat/flat pricing, moving toward usage-sensitivity — this is the standard trigger for this exact question.

**Assumed:** Existing customers are on per-seat/flat pricing today, mostly short-term (monthly/annual, not multi-year locked) contracts.

---

❓ **Q5** - **Pure usage, pure seat, or hybrid?**: Given usage tracks value (Q1), costs scale with usage (Q2), but real predictability needs exist at the top of the customer base (Q3) — which shape wins?

➡️ Hybrid: a base/platform fee plus metered usage on top, rather than either pure extreme.

**Assumed:** Hybrid pricing model selected.

---

❓ **Q6** - **What does the base fee attach to — seats, tiers, or a flat platform fee?**: This is an API product; consumers are often services and integrations, not named humans logging in. "Seats" may not be a natural axis at all.

➡️ Anchor the base fee to a plan tier (e.g., Starter / Growth / Enterprise), not headcount, with an included usage allowance per tier and metered overage above it.

**Assumed:** Tiered base plans (not per-seat) + included usage allowance + metered overage beyond it.

---

❓ **Q7** - **Overage mechanics — hard cutoff, automatic billing, or pooled credits?**: With 10x usage variance, a hard cutoff breaks production systems for your heaviest (often most valuable) customers; unbounded silent overage billing risks bill-shock complaints instead.

➡️ Soft cap with automatic metered overage (never a hard service cutoff for paying customers), usage alerts at 50/80/100% of allowance, and volume-discounted overage tiers so unit price drops as usage grows — rewarding scale instead of punishing it.

**Assumed:** Metered overage with alerts and volume-discount tiers; no hard cutoffs.

---

❓ **Q8** - **Grandfather existing customers, or force-migrate everyone at once?**: A forced, immediate switch on a base of accounts already anchored to today's price is the single biggest revolt risk.

➡️ Grandfather existing customers on current pricing for a defined window (2-3 billing cycles, or until next renewal), with an opt-in incentive (discount) for anyone who'd actually benefit from switching early.

**Assumed:** Time-boxed grandfathering + opt-in early-migration discount.

---

❓ **Q9** - **Notice period and communication approach?**: How the change is communicated determines whether it reads as a partnership move or an ambush.

➡️ Minimum 60-90 days written notice before any billing change takes effect; a personalized calculator showing "here's what your last 3 months would have cost under the new plan"; and direct, human outreach (not just an email blast) to the top 10-20% of accounts by spend.

**Assumed:** 60-90 day notice, personalized before/after calculators, high-touch outreach to top accounts.

---

❓ **Q10** - **Guardrails for customers who'd see a big increase?**: Some current per-seat customers with low usage will look cheap under the new model, but some low-seat/high-usage customers will spike hard — those are the revolt risk.

➡️ Cap any individual account's bill increase (e.g., no more than +20-30% year-over-year) during a transition period, even if their true usage-based price would be higher — absorb the gap temporarily rather than sending shock invoices.

**Assumed:** Increase caps during the transition window to prevent bill shock.

---

❓ **Q11** - **Bundle the change with new value, or present it as pure repricing?**: A price change alone reads as extraction; a price change paired with something new reads as evolution.

➡️ Ship something the new model enables — higher rate limits, priority throughput, new endpoints, better SLAs for heavy users — in the same announcement, so it lands as "more value, priced fairly" rather than "we're charging you more for the same thing."

**Assumed:** Pricing change bundled with a tangible product improvement in the same announcement.

---

**Final recommendation**

Move to a **hybrid tiered-plus-usage model**, not pure per-seat and not pure usage-based:

- **Structure:** Plan tiers (Starter / Growth / Enterprise) each carrying a base fee, an included usage allowance, and metered overage beyond it, with overage unit price stepping *down* at higher volume tiers. Tiers are sized by plan/feature access, not seat count — seats aren't the natural unit for an API product.
- **Guardrails:** No hard usage cutoffs for paying customers; proactive alerts at 50/80/100% of allowance; automatic (not surprise) overage billing.
- **Migration:** Grandfather existing accounts on current pricing for 2-3 billing cycles or until renewal; offer an opt-in discount to switch early for anyone who benefits; cap year-over-year bill increases (e.g., +20-30% max) through the transition window so no one gets a shock invoice.
- **Communication:** 60-90 days' written notice, a personalized "what this would have cost you" calculator per account, and direct human outreach to the top 10-20% of accounts by spend — don't let your biggest customers learn about this from an email blast.
- **Framing:** Bundle the switch with a real product improvement (higher limits, priority throughput, better SLAs for heavy users) so it ships as added value, not a bare price hike.

This keeps revenue aligned with both cost-to-serve and value delivered (fixing the margin risk from 10x usage variance), while the grandfathering, caps, and advance notice are what specifically prevent the "revolt" — nobody gets billed differently with less than two to three months' warning, and nobody's bill jumps more than a capped amount in year one.
