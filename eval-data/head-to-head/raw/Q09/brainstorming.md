# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# adaptation: no-human — see PREREG.md
# subagent tokens: 81077 | tool uses: 1 | duration: 52s

**Classification: Spike.** This is a "why does X happen" question — output is an analysis/recommendation, not code. No design doc, no build.

**Probe I'd propose:** "Want a breakdown of the 6-8 most common failure patterns that kill event sourcing mid-project, or focus tight on what likely sank your two specific companies?" Most likely answer given the phrasing ("what actually goes wrong") — broad breakdown, general patterns. Assumed yes, proceeding.

---

## What actually goes wrong

Tutorials show one aggregate, ten events, in-memory store. Real system hits none of tutorial's constraints. Gap shows up in these spots:

**1. Event schema rot.**
Tutorial: events never change. Real world: business rules shift monthly. Old events still sit in log, must still deserialize. Team bolts on upcasters, version fields, migration scripts — schema debt compounds faster than regular DB migrations because you can't just ALTER the past.

**2. Wrong aggregate boundaries.**
Tutorial picks one clean entity (ShoppingCart, BankAccount). Real domain: boundaries fuzzy, need cross-aggregate consistency. Team reaches for sagas/process managers to fake transactions across aggregates. Sagas are hard to get right, harder to debug, and most teams building their first event-sourced system have never built one before.

**3. Projection sprawl.**
Every new UI need → new projection. Projections drift out of sync with source of truth (bugs in projection code, replay ordering issues). Once one projection shows stale/wrong data, team stops trusting the pattern — trust, once lost here, doesn't come back.

**4. Replay cost.**
Log grows to millions of events. Rebuilding state or a projection from scratch gets slow. Snapshotting fixes speed, adds another layer of versioning complexity (snapshot schema now also needs migration alongside event schema).

**5. No tooling for "what's true right now."**
SQL lets support/ops just look at a row. Event-sourced system needs specialized tooling to answer "what does this account look like today" — that tooling usually doesn't exist yet, gets built ad hoc, badly. Support team can't self-serve, escalates everything to the 2-3 engineers who understand the event store. Bus factor problem shows up fast.

**6. Team thinks in CRUD, not intent.**
Events end up named `FieldXUpdated` instead of `CustomerRelocated` — state-mutation events wearing an event-sourcing costume. Kills the actual value (audit trail, intent capture) while keeping all the overhead. Common when team adopts the pattern without deep buy-in — half the codebase does it right, half fakes it.

**7. Fixing bad historical data.**
Bug emits wrong events into an immutable log. Correct fix is a compensating event. Under deadline pressure, someone edits the event store directly "just this once." Now log's core invariant (immutable, append-only, source of truth) is broken, and nobody fully trusts replay again.

**8. Applied everywhere, not where it pays.**
Event sourcing earns its cost where audit trail / temporal queries / complex domain history matter. Teams often apply it uniformly across the whole system including simple CRUD-shaped entities — all the overhead, none of the offsetting value, everywhere.

**9. Infra tutorials skip.**
Dual-write consistency between event store and read-model DB, message ordering guarantees, idempotent consumers, retry/dead-letter handling — this is most of the real engineering effort and basically doesn't exist in a tutorial's single-process demo.

---

## Why it dies mid-implementation specifically

Pattern in both failure types you'd expect: team ships the "core" aggregate fine (matches tutorial shape), then hits the second or third aggregate needing cross-boundary consistency (#2) or a projection going stale under load (#3) — that's the moment velocity craters and trust breaks. Sunk cost buys a few more months, then someone asks "what are we actually getting for this" and the answer isn't compelling enough to justify #4/#5/#9's ongoing tax. Abandonment usually isn't one big blowup — it's a slow bleed where every story takes 3x longer than a CRUD equivalent, projection bugs erode confidence, and eventually someone routes around it with a plain table.

**Mitigation, if this comes up again:** scope event sourcing to the one or two aggregates where audit/history genuinely matters, keep everything else CRUD, invest in replay/projection tooling before the second aggregate, and write down the compensating-event procedure before the first bad event ships — not after.
