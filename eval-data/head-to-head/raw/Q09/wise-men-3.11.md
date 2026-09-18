# arm: wise-men-3.11 (SKILL.md v3.11.0, commit 1e32841) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (round 3, PREREG-3 rules)
# subagent tokens: 215625 | tool uses: 18 | duration: 1956s
# note: stopped by the account's usage limit mid-run and resumed from its own transcript after the reset; duration includes the pause

## Recommendation

The tutorial-to-production gap isn't mainly about event sourcing being fragile — tutorials show a single-aggregate, single-team, day-one slice of it, and real failures come from what gets bolted onto that: system-wide adoption, bundling it with a simultaneous CQRS/broker/microservices rewrite, retrofitting it onto a live CRUD app, and never deciding a scope boundary. Treat event sourcing as a per-subdomain storage choice — used only where someone can name, today, who actually reads the history — not an architecture for an entire system.

## Why

Tutorials pick domains that already think in past-tense facts (a bank account, a cart), with one aggregate, one writer, no legacy data, and no other consumer — every cost that actually hurts (schema evolution, cross-aggregate consistency, projection sprawl, replay safety, tooling) only appears with scale and time, which a demo never reaches.

Deaths that happen mid-implementation specifically are disproportionately driven by costs that show up in weeks to months, not the ones usually blamed in "event sourcing is hard" writing: events that just record a form diff (`CustomerUpdated`) rather than real intent, so the system pays ES's full cost for none of its benefit; a new read model needed for every screen or filter, which visibly slows every feature; users not seeing their own change immediately because projections update asynchronously — an eventual-consistency UX tax that's a choice, not something ES requires; and, whenever an existing app is being converted rather than built fresh, two live sources of truth running in parallel with no reconciliation story. Underneath this is an incentive problem: whoever decides to adopt event sourcing rarely pays its ongoing cost — the build team inherits a mandatory event-design decision on every trivial change, on-call inherits a system that's structurally harder to debug, and the business sees timelines slip with nothing shipped yet, since the audit-trail/replay payoff that's supposed to justify the cost arrives late, if ever. That combination — cost paid immediately and fully, benefit deferred and conditional — is enough on its own to explain a mid-build cancellation without needing a dramatic technical failure.

A real but harder-to-confirm alternative: once a system holds genuine personal data, an immutable, replayable event log collides with a right-to-erasure request, and teams that hit this late either bolt on expensive partial fixes (per-subject key deletion retrofitted after the fact) or quietly start mutating "immutable" events to comply — at which point the system has all of event sourcing's operational cost and none of its replay guarantee, a credibility collapse that can by itself end a project. This risk is real and underrated, but it typically needs real user data, volume, and time to surface — which cuts against it being the proximate cause of a project killed specifically mid-implementation, though it can't be ruled out without knowing whether either company had live user data and a real deletion or audit request before the project was cancelled.

## What to do

This is a diagnosis, not a live migration decision, so the useful move is a short triage, not an action plan:

1. Check scope and timing first: was event sourcing adopted system-wide and bundled with a simultaneous CQRS/broker/microservices rewrite, or retrofitted onto an already-live CRUD app with a dual-write period? Either one is a strong indicator that the early-operational/incentive explanation is primary — though check steps 2 and 6 before ruling out the alternatives.
2. Check whether either company had real production user data, meaningful traffic, and an actual deletion or compliance audit request before the project was killed. Little or no live data makes the compliance/erasure explanation unlikely to have been the proximate trigger; real data and a real request makes it a live contender.
3. Sample the event catalog: what fraction of event names are `Updated`/`Changed`/`Set`-style diffs versus real business events (`OrderShipped`, `PaymentCaptured`)? A high diff fraction is close to a smoking gun for paying ES's cost with none of its benefit, and it's checkable from the code in under a day (rough estimate).
4. Separate "my save didn't show up" complaints (an async-projection UX choice) from complaints about the event model itself (versioning, aggregate design) — the two get blamed on "event sourcing" together, but only one is intrinsic to it.
5. For any future adoption: scope it to one subdomain where a specific person or use case reads the history today, keep the read model used for "did my write succeed" in the same transaction as the event, and use a plain outbox — not event sourcing — if the actual goal is just reliable events for other services.
6. Check the store's concurrency guarantee (does it reject an append when the stream has moved on — optimistic concurrency / expected-version checking?) and whether a full replay is safe to run (do event handlers re-send emails, payments, or webhooks during a rebuild?). A store without append-time concurrency checks, or a rebuild whose handlers re-fire side effects, is a distinct, purely technical failure mode, separate from the scope/incentive story above and worth ruling out on its own.

## Risks of this plan

Diagnosing the two companies as pure early-operational/incentive failure when it was really a compliance/erasure-driven credibility collapse (or the reverse) means fixing the wrong layer — for example, adding adoption governance to a problem that was actually "PII is baked into every projection and a deletion request can't be honored." Steps 1-2 above exist to catch this before committing to either story.

Treating "two companies abandoned it mid-build" as proof that event sourcing itself is the problem risks ruling it out for the domains it actually fits well — ledgers, claims, regulated audit trails — where the fallback is usually a hand-built, driftier audit log bolted onto CRUD tables, which carries its own ongoing reconciliation cost, just a less visible one. The opposite overcorrection — concluding it was purely bad execution and the pattern itself is blameless — risks a second attempt that repeats the exact mistake (system-wide scope, bundled rewrite, undecided boundary) that sits underneath both explanations above as the more basic cause, regardless of which one turns out to be right.

Cost of being wrong here is low: this is a read on what already happened, not a commitment, so acting on the wrong diagnosis mainly costs the time spent fixing the wrong layer before someone notices. The expensive mistake is the one both companies already appear to have made — committing to unscoped, bundled, retrofit-style adoption without ever naming a boundary — and the recoverable way to avoid repeating it is to pilot any future event sourcing scoped to a single subdomain for a few weeks before it touches the rest of the system.

## Strongest counter-position

The case that the immutable-log-vs-right-to-erasure conflict, not incentive or scope failure, was the real driver: personal data ends up spread through event payloads, and once a real deletion or audit request arrives, teams either bolt on expensive, partial fixes after the fact, or start quietly mutating events that were sold as immutable — at which point the system carries all of event sourcing's operational cost with none of its replay guarantee. That credibility collapse — "we said append-only and immutable, and now it isn't" — can be a more common trigger for abandonment than any single discrete security incident.

This wins if either company had accumulated real user data and faced an actual deletion, audit, or legal request before the project was cancelled. It loses force against a project killed specifically mid-implementation, since compliance exposure of this kind generally needs months of live traffic and real requests to surface at all — but that argument is about typical timing, not about these two cases specifically, and neither has been confirmed.

## Confidence

High — tutorials cover only a single-aggregate, single-team, day-one slice: this follows directly from how the pattern's costs scale (schema evolution, cross-aggregate consistency, projection maintenance, and replay safety are all functions of elapsed time, data volume, and team count, none of which a short demo has) and from what a tutorial needs to stay short and convincing. This isn't seriously in dispute.

High — scoping event sourcing to a named subdomain instead of the whole system is the single highest-leverage fix: every failure mode identified here — CRUD-shaped events, cross-service contract sprawl, dual sources of truth during a retrofit, PII spread through payloads, aggregate bloat — either doesn't arise or stays contained once a boundary is actually chosen, and gets worse the more of a system runs through one undifferentiated event model.

Medium — that early operational/incentive collapse, rather than compliance/erasure, was the primary driver for these two specific companies: favored by the "mid-implementation" detail in the question, but nothing here is verified against what actually happened inside either company.

Low — any implied frequency ("this is usually what happens"): every such claim behind this memo is explicitly reasoned from typical patterns, not measured.

Material unknowns, in order of how much they'd resolve the diagnosis: (1) whether either company bundled event sourcing with a simultaneous architecture rewrite or retrofitted it onto a live system; (2) whether either had real user data and a live deletion/compliance request before cancellation; (3) what specifically triggered the cancellation decision — a technical incident, a departure, or a budget/deadline call.
