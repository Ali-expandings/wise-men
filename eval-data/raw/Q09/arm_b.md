# Q09 Arm B raw output
# salvaged_from_context: false
# model: sonnet-4.6
# leakage_check: FAILED first call (agent tried to spawn real council, no visible answer) → RETRIED once → PASSED (clean 3-section + <thinking>)
# note: <thinking> block (5 internal persona positions) stripped during blinding.

[<thinking> block stripped during blinding — contained 5 persona internal positions: Pragmatist, Skeptic, Architect, Devil's Advocate, User Advocate + synthesis notes]

[VISIBLE OUTPUT — judge sees:]
## Answer

The gap between tutorial and production cleanliness comes from roughly six compounding failure modes that tutorials systematically hide:

**1. Schema evolution is the silent killer.** Tutorials show one version of `OrderPlaced`. Production has `OrderPlaced_v1` through `OrderPlaced_v7` because the domain changed, the field got renamed, a nested object got flattened. Now you need upcasters (code that transforms old events into the current shape) and a version registry, and those upcasters have to be correct forever because the old events are immutable. Get one wrong and your projections silently corrupt. Tutorials skip this entirely.

**2. Wrong aggregate boundaries cost everything.** In CRUD, discovering a wrong domain model means a refactor. In event sourcing, it means migrating the entire event history — possibly years of events — to a new shape. Teams often discover boundary mistakes only after going live, because requirements clarify under real load. The immutability that felt like a superpower becomes load-bearing concrete poured around a structural mistake.

**3. Projection rebuilds become an ops crisis.** Tutorial projections rebuild in milliseconds. Production event stores with 200M events take 16 hours to rebuild a projection. Now every schema change requires a maintenance window or a blue/green projection strategy. The "rebuild from source" superpower becomes a constraint that shapes every architectural decision downstream.

**4. GDPR and deletion break the immutability contract.** "Right to erasure" is legally mandated in most jurisdictions. The append-only log has no clean answer for this. You end up with crypto-erasure hacks (encrypt the data, delete the key), tombstone events with special handling, or admitting the event store is not actually the system of record — which undermines the whole premise.

**5. Eventual consistency UX is harder than anyone admits.** "Command accepted" followed by a stale read means users see their own writes disappear. Tutorials wave at this. Real fixes require read-your-writes guarantees, causality tokens, or client-side optimistic updates — none of which are trivial, all of which need to be maintained as projections multiply.

**6. Knowledge bus factor.** Event sourcing has a steep conceptual surface area. When the one person who understands the projection rebuild process, the upcaster chain, and the aggregate boundary decisions leaves, the system becomes a black box. CRUD systems are at least readable by any developer. Event sourcing creates expertise silos that feel fine at year one and become existential at year three.

The structural problem is the **point of no return**: two years of events in production means you cannot easily back out, and the cost of that lock-in only becomes visible after you're already locked in. CRUD doesn't have this asymmetry.

## Dissent worth keeping

Survivorship bias may be distorting the picture. Teams that succeed with event sourcing rarely publish post-mortems — they're shipping. The companies that abandon it do write the retrospectives. The pattern has legitimate success stories (Axon-based systems at scale, Kafka event logs in fintech) and the tooling has genuinely matured. The honest version of "two companies abandoned it" might be "two companies tried it without anyone who had done it before" — which is a team hiring problem, not an inherent pattern flaw. Event sourcing may be a power tool that injures novices, not a fundamentally broken tool.

## Confidence

High — the failure modes described are extensively documented across engineering literature (Udi Dahan, Greg Young, Martin Fowler's CQRS notes, and numerous public post-mortems) and the mechanisms are structurally sound, not anecdotal.
