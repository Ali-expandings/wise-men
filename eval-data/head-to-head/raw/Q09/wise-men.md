# arm: wise-men | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# skill: SKILL.md v3.9.2 (as written)
# subagent tokens: 165450 | tool uses: 15 | duration: 477s
# note: the orchestrator prefixed one status line ("All five members answered fully…") before the output; kept here, stripped at blinding as a status line.

All five members answered fully (no retries needed), all three reviewers returned well-formed rubric blocks (no exclusions, no severe-disagreement flags). Standard tier skips debate by design. No Stage 4.5 trigger (nothing excluded/abstained). Synthesizing as Chairman now.

---

*Note: brief format upgraded to full because the preserved dissent exceeds 3 sentences (dissent-precedence rule).*

## TL;DR

Tutorials hold three things constant that real systems can't — one aggregate, one event schema, one consumer — and event sourcing's cost is proportional to how much those three move. In production they move fast: schemas change, multiple teams build projections off the same stream, and event-store replay gets conflated with message-bus delivery. Underneath that, most adoptions were never justified by a real audit/temporal-replay requirement to begin with, so the first time the mechanics get expensive, there's no business case left to absorb the cost — which is exactly the mid-implementation abandonment window you're describing.

## Decision / Answer

Four of five members, reasoning down four independent paths (precedent, falsification, first-principles, base rates), converged on the same mechanism, which is a stronger signal than four people agreeing by default:

1. **Schema evolution is the wall nobody budgets for.** Events are immutable, so the first time a field needs to change shape, you're writing upcasters for every historical version, forever. Tutorials never hit this because no tutorial runs long enough to need it. Two members independently placed this at "month 4–9" — right in your mid-implementation window.
2. **Event store and message bus get conflated.** A store's replay is supposed to be safe and idempotent; a bus's isn't. Tutorials blur them because at toy scale it doesn't matter. In production, replaying the store to rebuild a projection re-fires non-idempotent consumers — duplicate emails, double charges. The Architect flagged this as the single most likely production-incident cause.
3. **Eventual consistency between write and read sides stops being a hidden implementation detail and becomes a live UX/organizational problem** once multiple teams own multiple projections off one stream with no single owner of what an event means.
4. **The adoption itself usually wasn't justified.** Nobody could name, in one sentence, the specific query a well-modeled CRUD table plus an audit log genuinely couldn't answer. Once that's true, any friction — and event sourcing produces friction early — is sufficient reason to bail, because there's no counterweight benefit to weigh it against.

The practical takeaway the four converge on: before adopting event sourcing (or before diagnosing why a past attempt failed), write down the one thing CRUD + an audit-log table can't do that this system needs. If you can't name it in a sentence, the postmortem on your two companies is "wrong tool," not "hard tool" — and scoping event sourcing to only the bounded context that actually needs it (not the whole domain) is the fix the tutorials never show because tutorials only ever show the one aggregate that needed it.

**Cost of being wrong:** treating this as a purely technical failure (buy better tooling, hire an ES consultant, try again with more discipline) is cheap to attempt but likely to repeat the outcome if the dissent below is actually what happened — because better tooling doesn't fix a credit/cost mismatch between who decided and who paid. The recovery path if the dissent is right: before a third attempt, check who benefits on what timeline and who pays on what timeline, not just whether the schema-versioning story is better this time.

## Confidence

**Medium** — capped deliberately. All five members, independently, named the same weakest assumption: none of them know what actually killed your two companies' implementations specifically — they're all reasoning from the general reference class of event-sourcing adoptions, not from your two cases. Five answers converging on one mechanism is a good signal about the *pattern*; it is not five confirmations of *your two companies*. Treat the mechanism above as the leading hypothesis, not a diagnosis.

## Where the council agreed

- Tutorials are clean because they fix three variables (aggregate count, schema stability, consumer count) that production can't hold still — this isn't a difficulty gap, it's a scope difference.
- Schema/event versioning is the standing tax nobody plans for, and it typically surfaces in the exact window ("mid-implementation," months 3–9) you described.
- Event-store/message-bus conflation (replay re-triggering non-idempotent side effects) is a real, specific, and underrated production-incident source.
- Most failed adoptions never had a requirement only event sourcing could satisfy — the pattern was chosen for being intellectually satisfying, not domain-necessary.

## Where the council split (preserved dissent)

The Devil's Advocate rejected the entire frame: *"'Tutorials are clean, reality is messy, what goes wrong?' presupposes that event sourcing is a technology with a difficulty gap... That's the comfortable answer, and it's the one that guarantees you watch a third company abandon it."* Its case, run through incentives rather than mechanics: the staff engineer who pitches event sourcing gets credited at the design-doc/demo stage — a legible "systems design" win — while the cost lands six to eight quarters later, on ICs with no authority to delete an event type and no credit for reducing one. Every maintenance action is therefore additive, never subtractive, and *"the mess you saw is not a technical artifact of event sourcing; it is the accumulated residue of a governance regime where addition is free and subtraction is forbidden."* It goes further: *"the real asymmetry isn't that ES fails more than CRUD. It's that ES fails visibly... organizations punish legible complexity while tolerating unlimited illegible complexity."* On this view, both companies may have made the *correct* call, just eighteen months later than a healthier feedback loop would have allowed — and the thing actually worth diagnosing is why detection took so long, not what was technically hard.

This isn't a hedge on the majority's mechanics — it's an argument that the mechanics are a downstream symptom, not the cause. It might be right specifically if the true trigger in your two companies was organizational (the champion left, budget got cut, nobody could kill a decision once made) rather than a hard technical ceiling (replay time, throughput) — which is exactly the kind of fact the whole council flagged it couldn't verify from here. Reviewers rated this answer weakest overall (lowest correctness and practical-usefulness scores — three independent graders called it the least actionable for a team mid-implementation) but *highest on insight* by all three — the normal Devil's Advocate pattern (weak on the scorecard, valuable as a check), not the inverted pattern where the contrarian view should lead.

## Open questions the council couldn't resolve

- **What actually triggered each of the two abandonments** — a hard technical ceiling (replay time, event-store throughput, an unshippable migration) versus an organizational one (turnover, a champion leaving, a governance failure to ever retire anything). This is the single highest-value fact to get, because it decides whether the majority's mechanics-focused fix or the Devil's Advocate's incentive-focused fix is the one that actually applies to your two cases.
- Whether either company ever had a written, specific requirement (compliance audit trail, true temporal queries, multiple independently-scaling read models) that justified adopting event sourcing in the first place, as opposed to a normal CRUD system with an audit-log table.

---

## Full audit

### Model routing used

```
Composite difficulty: 3/5 (depth=3, stakes=2, novelty=2)
Tier: standard

Member models:
- Pragmatist:        sonnet
- Skeptic:           sonnet
- Architect:         sonnet
- Maintainer:        sonnet
- Devil's Advocate:  opus   (per-role override, +1 tier)

Reviewer model: haiku × 3
Chairman: main thread (sonnet 5)

Validator: 0 retries triggered (all 5 members passed structure check on first pass;
           all 3 reviewers returned well-formed rubric blocks on first pass)
Stage 3 (debate): skipped — standard tier does not run debate regardless of variance
Stage 4.5 (synthesis checker): skipped — no exclusion/abstention/degradation to trigger it
Estimated cost: ~$0.05–0.07 (smart-routed standard: 4 sonnet members + 1 opus DA + 3 haiku reviewers)
```

### Rubric scores (reviewer averages, 1–5 scale)

| Member | Correctness | Insight | Practical | Risk | Overall |
|---|---|---|---|---|---|
| Architect | 4.67 | 4.33 | 5.00 | 5.00 | **4.75** |
| Maintainer | 4.00 | 3.00 | 4.00 | 4.00 | 3.75 |
| Skeptic | 4.00 | 4.00 | 3.33 | 4.00 | 3.83 |
| Pragmatist | 4.00 | 3.00 | 4.00 | 3.33 | 3.58 |
| Devil's Advocate | 3.00 | 4.67 | 2.67 | 3.00 | 3.33 |

Top pick: **Architect**, unanimous across all 3 reviewers. Bottom pick: **Devil's Advocate**, unanimous across all 3 reviewers (normal DA pattern — see dissent section). No severe-disagreement flags raised by any reviewer.

### Member answers (verbatim)

**Member: Pragmatist**

## Core judgment
Tutorials show event sourcing on one aggregate (a bank account, a cart) with events that map 1:1 to state transitions and no cross-aggregate concerns. Real codebases fail because of what the tutorial never has to deal with: event schema evolution, eventual consistency across aggregates, and the fact that projections/read models are a second system you now maintain forever.

Pattern I'd expect (and have seen on real projects) that precedes the abandonment: team adopts ES for an aggregate that didn't need it — usually something with moderate complexity but no real audit/replay requirement, adopted because it seemed "more correct" or someone read a good blog post. Six months in, they need to change an event's shape (add a field, split a field, fix a bug in how an event was interpreted). Now they're writing upcasters/migrations for every historical event version, forever, and every new engineer has to understand the full version history to touch that code. Meanwhile the read-side projections drift out of sync in production — a projector bug or an infra hiccup causes duplicate/missed events, and rebuilding projections from the full event log becomes an operational fire drill because nobody load-tested "replay 2 years of events" until they had to do it live. Debugging also gets harder, not easier: "what is the current state" is no longer a query, it's a computation, and when that computation is wrong, tracing it back to the offending event and reasoning about why the fold logic misbehaved is slower than reading a bug in a normal CRUD update. The teams that abandon it mid-implementation usually hit this in months 3-9: they never had a real requirement for full audit trail / temporal queries / replay-driven debugging that justified the complexity tax, and once the schema-evolution and projection-consistency pain shows up, there's no business case left to justify continuing to pay for it.

The tutorial setup differs from real projects in three load-bearing ways: single aggregate (no cross-aggregate consistency/sagas), events that never change shape (no versioning problem), and no operational requirement to rebuild/replay at scale under load.

## Top risks
- Adopting ES without an actual requirement (compliance audit trail, true temporal queries, or multiple independently-evolving read models) — solving a problem you don't have
- Event schema versioning/upcasting debt compounds silently until a change forces you to touch every historical version
- Projection rebuild-at-scale is never tested until it's needed in production, under pressure
- Team conflates "event sourcing" with "message bus / pub-sub" and builds both when only one was needed
- Sunk-cost drift: teams keep going past the point where the pain outweighs the benefit because nobody set an explicit "is this still worth it" checkpoint

## Recommended change
Before touching ES, write down the specific requirement (audit trail, replay, multiple read models) that CRUD + an audit log table genuinely can't satisfy — if you can't name one, don't adopt it.

## Confidence
medium — this matches common ES failure patterns I'd expect from real projects, but I don't have specifics on the two companies the user mentions, so I can't confirm their failure matched this exact shape.

## Weakest assumption
That the two companies' abandonment was driven by ES-specific complexity (schema evolution, projections) rather than something unrelated (team turnover, deadline pressure, org politics) that would have killed any sufficiently ambitious architecture choice.

---

**Member: Skeptic**

## Core judgment
Applying falsification: candidate explanations for the tutorial-clean/production-messy gap, tested against what would confirm or rule each out.

1. **Snapshot/replay performance decay** — ruled out as primary driver here. This bites *after* months of production event volume accumulate; it can't explain abandonment "mid-implementation," before real data existed to replay.
2. **Aggregate boundary mistakes forcing event migrations** — survives partially. Mid-implementation is exactly when teams discover their first aggregate boundary is wrong, and because events are immutable, fixing it means a data migration on a system that isn't even live yet.
3. **CQRS dual-model overhead outpacing perceived benefit** — survives. Teams feel the tax immediately, but the payoff only shows up much later or never, if the domain didn't need it.
4. **Team lacks eventual-consistency intuition** — survives. Developers reflexively want read-your-writes; every UI flow becomes a debate about consistency guarantees.
5. **Adopted without a genuine audit/temporal/multi-reader requirement (hype-driven adoption)** — survives and is likely the root cause underneath 2-4. If nobody can name the specific business need ES solves better than a well-modeled CRUD system with an audit log table, the complexity has no counterweight, and any friction becomes sufficient reason to bail.

Explanations 2-5 survive; explanation 1 is folklore in this context. The tutorial/production gap exists because tutorials fix the aggregate boundary correctly by construction and skip the "why do we even need this" justification — production forces both questions live, under deadline pressure, with a team that hasn't internalized eventual consistency.

The framing gap in the question: "what goes wrong with event sourcing" implicitly accepts ES as the baseline to defend. The sharper question is whether the domain had a real requirement ES uniquely satisfies — most CRUD-shaped problems get 90% of the audit-trail benefit from a simpler append-only log table bolted onto a normal transactional model.

## Top risks
- Wrong aggregate boundary chosen early → costly event-schema migration discovered mid-build, before any production value was realized.
- CQRS read-model lag surfaces immediately in UI/UX review → team bolts on synchronous reads, defeating the architecture.
- No documented business requirement for audit/temporal replay → complexity has no ROI counterweight.
- Team unfamiliar with eventual consistency → constant design debates and rework stall velocity.
- Immutable events conflict with "we need to correct a past mistake" → ad-hoc compensating-event hacks.

## Recommended change
Check whether either abandoned project ever had a written, specific requirement that only event sourcing satisfies — if not, the postmortem is "wrong tool," not "hard tool."

## Confidence
medium — reasoning is sound in general but I have zero verified facts about the two specific companies' actual failure sequence.

## Weakest assumption
That "abandoned mid-implementation" reliably signals a problem-solution mismatch rather than unrelated causes like team turnover or a champion leaving.

---

**Member: Architect**

## Core judgment
Tutorials are clean because they hold three variables constant that real systems can't: schema count (fixed, small), time horizon (zero), and consumer count (one). Event sourcing's core mechanics are cheap under those constraints and expensive the moment any of them moves.

Four mechanics account for almost all the pain:
1. **Schema evolution.** Events are immutable — every field rename/split/new-required-field creates a version every consumer must interpret forever. Standing tax most teams never budget for.
2. **Event store vs message bus conflation.** A store's replay should be safe/idempotent; a bus's isn't. Tutorials blur them. In production, replaying the store to rebuild a projection re-fires side-effecting consumers — duplicate emails, double charges. Likely the single most common cause of production incidents behind an abandoned implementation.
3. **Projection proliferation without ownership.** Multiple teams building multiple read models off the same stream means the event contract has no single owner, and interpretations drift.
4. **Replay cost at real volume.** Milliseconds in a tutorial, hours at production volume — requires snapshotting infrastructure most teams never engineered for.

The option missing from the framing: this isn't a binary of "ES done right" vs "ES turns into a mess." The alternative is scoping ES to only the bounded context(s) that genuinely need audit trail/temporal replay, and using plain CRUD + domain events everywhere else. Most systems that abandon ES mid-implementation adopted it as a whole-application architecture when only one subdomain needed it.

## Top risks
- Treating the failure as a tooling problem rather than a scope problem — the retry fails the same way.
- No upcasting/versioning strategy decided before the first event ships.
- Event store and message bus implemented as one pipeline — replay re-triggers non-idempotent side effects.
- No single owner of the event contract once multiple teams build projections off it.
- Snapshotting/replay infrastructure not budgeted until rebuild time is already measured in hours.

## Recommended change
Scope event sourcing to only the bounded context(s) with a real audit/temporal-replay requirement, decide schema-versioning and event-store-vs-message-bus boundaries up front, default everywhere else to CRUD with published domain events.

## Confidence
medium — the mechanics-based failure modes are well-established and I'd stake real work on them generalizing; but I have no visibility into what specifically killed the two implementations you saw.

## Weakest assumption
That the two abandonments were driven by ES mechanics at all — they could equally have been organizational or cost-driven.

---

**Member: Maintainer**

## Core judgment
Tutorials demo event sourcing at the scale of a single aggregate with three event types and no schema evolution. Base rate for this reference class (architectural pattern adopted from talks/tutorials, no prior production experience, multi-quarter rollout): this dies more often from the surrounding conditions than from the pattern being wrong. Most teams that adopt it don't have a real audit/temporal need — they adopted it because it's intellectually satisfying, not because their domain demanded it. That's the first-order cause of the two abandonments: solution in search of a problem, chosen by whoever ran the design review, not by whoever owns the on-call pager two years later.

Second-order cause: event schema evolution is the load-bearing wall nobody budgets for. Teams build the happy path, ship it, and hit the "we need to change an event shape" wall around month 4-6 — which matches "abandoned mid-implementation" almost exactly.

## Top risks
- Domain didn't need it: picked for architectural elegance, not because the business had requirements that justified the complexity tax.
- No event versioning/upcasting strategy designed before the first breaking schema change.
- Projection rebuild time becomes a production incident: nobody load-tested replaying the full event log until it took hours during an outage.
- Team turnover: the 2-3 people who understood the event store internals leave, and the pattern becomes archaeology.
- Eventual consistency between write-side and read-side gets discovered by support tickets instead of being designed for upfront.

## Recommended change
Before greenlighting event sourcing, write down the specific query or requirement that a normal CRUD table plus an audit log literally cannot satisfy — if you can't name one in a sentence, don't do it.

## Confidence
medium — the domain-fit and versioning failure modes are well-established, but I'd want to know the specific reasons the two companies actually cited for abandoning.

## Weakest assumption
That your two observed abandonments are representative of the general failure mode rather than both being instances of the same local cause.

---

**Member: Devil's Advocate**

## Core judgment
The frame is wrong, and the frame is the actual problem. "Tutorials are clean, reality is messy, what goes wrong?" presupposes that event sourcing is a technology with a difficulty gap that better docs, better tooling, or a better-informed engineer would close. Run the incentive ledger instead: the staff engineer pitching it gets paid at design-doc-plus-first-demo time — ES is unusually legible as "systems design leadership." Payoff lands in two quarters; cost lands in eight. The implementers get paid in greenfield: ES is a politically legitimate excuse to rewrite. The ICs two years out are pure payers: no authority to delete an event type, zero credit for reducing event count. So every maintenance action is additive. The mess is not a technical artifact of event sourcing; it is the accumulated residue of a governance regime where addition is free and subtraction is forbidden. Management bought an unfalsifiable good — "auditability" — and unfalsifiable goods have no completion criterion, so the only detectable failure signal is velocity collapse, which arrives late and gets attributed to the team rather than the architecture.

The contrarian core: tutorials are not lying. A tutorial author's incentive is to be re-cited — being wrong about a demo gets caught fast. The real asymmetry isn't that ES fails more than CRUD — it's that ES fails *visibly*. A CRUD system of equal accidental complexity survives because the complexity is hidden in stored procedures, nullable columns, cron jobs, and tribal knowledge. ES converts implicit complexity into explicit artifacts with names, and organizations punish legible complexity while tolerating unlimited illegible complexity. Both abandonments may have been correct decisions made for wrong reasons — the missing option in the framing is that abandonment isn't necessarily a failure state; it may be the fastest healthy feedback loop those companies had, and the thing worth diagnosing is why it took eighteen months to fire.

## Top risks
- The "ES is just hard" answer makes you the person who knows the pitfalls, which qualifies you to green-light attempt three.
- Fixing the technology leaves the credit/cost asymmetry fully intact, so the next big-noun architecture fails identically.
- Treating abandonment as the failure hides the real defect: the 18-month detection latency on an unfalsifiable business case.
- Concluding "use CRUD, it's simpler" trades legible complexity for illegible complexity and buys survivability, not simplicity.
- The audit/compliance justification is frequently retrofitted post-hoc; taking it at face value makes deletion policy unnegotiable forever.

## Recommended change
Write a one-page ledger naming who collects credit on what date versus who pays on what date, and refuse any proposal where the payers aren't in the room — then make the first milestone retiring an event type end-to-end, not adding one.

## Confidence
Medium — I'd want the proximate trigger of each abandonment verified before staking a week on it.

## Weakest assumption
That both abandonments were driven by incentive and governance dynamics rather than a genuine technical wall.

---

*Council of 5 members + Devil's Advocate, standard tier, 3 reviewers. Protocol deviations: none — full standard-tier run, no retries, no exclusions, no debate (not applicable at this tier).*
