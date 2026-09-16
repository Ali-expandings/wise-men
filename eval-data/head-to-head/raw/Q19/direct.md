# arm: direct (no skill) | question: Q19 | general-purpose/sonnet | run: 2026-09-16
# subagent tokens: 69343 | tool uses: 0 | duration: 15s

Per-seat vs usage isn't really the question when usage varies 10x across customers — flat per-seat either overcharges your light users (they churn) or underprices your heavy users (you lose margin on your best accounts). That variance is itself the signal to price on usage.

**What actually fits here**

Pure usage-based (pay per API call/token/whatever your unit is) aligns price with value and handles the 10x spread naturally. Downsides: revenue becomes unpredictable for you, and customers hate unpredictable bills — it creates budget anxiety and finance-team pushback at renewal.

The pattern most API companies converge on (Stripe, Twilio, OpenAI, Snowflake) is **hybrid: platform/seat fee + usage on top**, or **tiered usage with committed minimums**. Concretely:

- Base platform fee (covers access, support, seats for the humans hitting a dashboard) — keeps revenue floor predictable.
- Usage-based metering above included allotment, with per-unit price dropping at higher tiers (rewards your biggest accounts instead of penalizing them).
- Optional: let customers pre-commit to a usage tier at a discount (annual commit) for budget predictability on their side.

This directly solves your 10x problem: your smallest customer pays near the base fee, your biggest pays 10x more but at a marginally better rate, and nobody feels either ripped off or like they're subsidizing someone else.

**How to switch without a revolt**

1. **Grandfather, don't force.** Existing customers keep current pricing for a defined window (6–12 months) or permanently if they're small enough not to matter. New pricing applies to new signups immediately.
2. **Give 60-90 days notice**, in writing, individually — not a blog post. Heavy users especially need runway to budget.
3. **Model each existing customer's bill under the new scheme before announcing anything.** Anyone who'd pay meaningfully more is a targeted conversation, not a mass email — offer them a longer transition or negotiated rate.
4. **Frame it as "pay for what you use," not "price increase."** If some of your light-usage customers would pay *less* under the new model, lead with that publicly — it buys credibility for the change overall.
5. **Ship usage dashboards before the switch**, not after. Nobody accepts metered billing they can't see coming.
6. **Never let a bill surprise someone.** Usage alerts, soft caps, or at minimum a "you're trending toward $X this month" notice.

The revolts happen when companies change the *rules* and the *price* at the same time with no warning (see: recent backlash any time a dev-tool API repriced usage overnight). Separate the announcement from the effective date, model your existing book first, and protect your smallest/newest customers from the biggest relative shock.

If you want, tell me your actual usage distribution (rough range, average, what the unit of usage is) and I can sketch actual tier breakpoints.
