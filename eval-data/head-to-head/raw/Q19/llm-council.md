# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q19 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# subagent tokens: 116185 | tool uses: 12 | duration: 236s

## Council Verdict: Per-Seat vs Usage-Based API Pricing

### Where the Council Agrees

Pure per-seat is broken for this business. Every advisor independently rejected it: seats don't track value delivered when usage varies 10x, and "seat" is often a category error for an API product in the first place. The heaviest users are being subsidized by the lightest — that's not a pricing quirk, it's margin leaking out the door on your best accounts.

Pure usage-based is also rejected, unanimously. Unpredictable bills are the actual backlash trigger, not the pricing mechanism itself — finance teams can't approve what they can't forecast.

The convergent answer, reached independently via different reasoning paths, is **hybrid: base platform fee + usage-based overage/tiers**. One advisor calls it the fix for bill-shock optics, another cites Stripe/Twilio precedent, another arrives at it from a value-vs-capacity framing, another backs into it via committed-use tiers. Only the Contrarian stays agnostic on the model pending root-cause diagnosis — but even that objection isn't "hybrid is wrong," it's "don't pick any model until you know why usage varies 10x."

On migration: the risk is surprise and opacity, not the pricing mechanism itself. Grandfathering existing customers, showing them their actual number before it's real, and personal outreach over blanket announcements were proposed independently by multiple advisors.

### Where the Council Clashes

**Diagnose first vs. ship a plan now.** The Contrarian and First Principles Thinker both insist the 10x variance needs root-causing before any repricing — is it customer size (legitimate), integration maturity (temporary, punishing early adopters is wrong), or chatty/inefficient implementations (the Outsider's point — usage-based would be charging for bad code, not value received)? The Executor and Expansionist treat this as a distraction and move straight to a plan. Reasonable people disagree because they're optimizing for different failure modes — analysis paralysis vs. shipping a plan built on an unvalidated premise.

**Who's actually at risk in the migration.** The default worry is angering high-usage whales. The Contrarian inverts this: whales will renegotiate or complain loudly, which you can respond to. The low-usage long tail won't revolt — they'll just quietly not renew, and you won't see it coming. Multiple peer reviewers flagged this as the standout insight of the whole council. The Expansionist's line — "undercharging low-usage customers during transition is cheap insurance" — was independently called out by three separate reviewers as the weakest point in the entire council: it treats a real churn vector as a rounding error.

**Revenue-maximization vs. risk-management framing.** The Expansionist is unambiguously the outlier here. Every single reviewer flagged it as the weakest response, for the same reason: it's a sales pitch, not an analysis of the actual question (which explicitly includes migration risk as half the brief). Its individual ideas — commitment-based tiers, machine-driven consumption as a growth vector — aren't wrong, but they're additive to the hybrid plan, not a competing thesis.

### Blind Spots the Council Caught

Peer review surfaced misses no single advisor caught alone, clustering around two things:

**Contractual exposure** — flagged by four separate reviewers independently: existing contracts may lock in seat-based pricing for the term, have notice-period clauses constraining how fast you can reprice, or require renegotiation rather than a unilateral rollout. None of the five original responses mentioned this — it's a hard constraint on timing that could invalidate any clean execution plan.

**No validation before commitment.** Nobody proposed testing before committing — no willingness-to-pay study, no backtesting the new model against real historical invoices to see who actually gets hurt, no pilot/beta cohort before full rollout.

**Sales comp disruption** — caught by only one reviewer, but structurally important: reps paid on seat-based quotas or ARR definitions are a major internal source of revolt that nobody among the five advisors mentioned. A pricing change without a matching comp plan change creates an incentive-misaligned sales org during the exact window you need them selling confidently.

**Gaming incentive** — per-call billing invites customers to batch or cache calls to reduce their bill, quietly eroding the revenue base the switch was meant to capture. This is a reason the base-fee component isn't just an optics fix — it's a revenue floor.

### The Recommendation

**Hybrid pricing: base platform fee plus metered usage with tiers** — not pure per-seat, not pure usage-based. This is where four of five advisors converged independently, it matches how API companies that survive this transition actually price (Twilio, Stripe), and it directly solves both things that matter in the brief: capturing the 10x-usage customers' actual value, and avoiding the bill-shock unpredictability that causes revolt.

But don't skip the diagnosis the Contrarian and First Principles Thinker are pushing for. Spend one focused week finding out *why* usage varies 10x before finalizing tier breakpoints — company-size variance deserves to be priced in; integration-maturity or chattiness variance means usage-based punishes the wrong thing, and you fix the SDK/API design instead of the price sheet. This is a one-week gate that determines whether your usage metric (API calls) is even the right unit to bill on, or whether you need a different metric (data processed, transactions completed) that maps to value rather than implementation chattiness.

On migration: grandfather all existing customers at current effective rates for 12 months, show every existing customer their actual shadow invoice under the new model for 1-2 billing cycles before it's real, and put new pricing live for new signups immediately. Personally reach out — not an in-app banner — to the top usage quartile with their specific number. And explicitly instrument for the long-tail risk: track low-usage-tier renewal rates separately post-migration, because that's the group that won't complain, they'll just leave.

Before any of this touches a price sheet: pull existing contracts and check for repricing/notice-period clauses, and loop in whoever owns sales comp — a pricing model change without a comp plan change creates a sales org incentivized to fight the very change you're rolling out.

### The One Thing to Do First

Pull 6-12 months of actual per-customer usage data and segment the 10x variance by cause — company size, integration maturity, or implementation inefficiency — before writing a single number on a new price sheet. Everything else (which tiers, what base fee, who gets grandfathered, what the shadow invoice shows) is downstream of knowing what that variance actually represents.
