# Q09 Arm C internals — 5 members + reviewers
# salvaged_from_context: false
# members: 5 sonnet-4.6 (Pragmatist, Skeptic, Architect, Maintainer, Devil's Advocate)
# validator: all 5 passed (5-section structure, non-empty)

## MEMBER: Pragmatist
ES not a storage pattern — commitment to never delete history. Schema migration one-way door (no door); projections rot (40 projections, unclear ownership, drift); eventual consistency surprises users+PMs; events-must-be-business-facts discipline impossible without senior review; debugging non-linear (state = f(all events)). Rec: don't adopt as default; surgical for audit/ledger/temporal; CDC log on relational = 70% benefit at 10% cost. Conf high. Weakest: both companies had typical web-app domains.

## MEMBER: Skeptic
Tutorials show write path, pretend read path trivial. Schema evolution brutal (OrderPlaced_v47, upcasting chains); projection rebuild ops tax (200M events = >1hr); eventual consistency infects UX contract; event granularity trap (coarse loses history, fine = noise); aggregate boundary mistakes compound; thin tooling (Kafka-as-event-store = category error). Rec: only adopt where audit/temporal IS core product req; CQRS alone = 70% benefit at 20% complexity. Conf high. Weakest: teams weren't event-native domain.

## MEMBER: Architect
ES conflates audit log + message bus + source of truth into one artifact = worse coupling than mutable state. Schema evolution without discipline; read-model proliferation without governance; eventual consistency surprise not decision; snapshots neglected until perf cliff; team cognitive load at scale. Rec: isolate event store as dependency not foundation + define schema-evolution contract day one; else CRUD + outbox = 80% benefit at 20% surface area. Conf high. Weakest: avoidable impl problems vs genuine domain mismatch.

## MEMBER: Maintainer
Teams adopt write model without committing to read model. Schema evolution without upcasting discipline; projection rebuild time at scale; temporal coupling in process managers/sagas (phantom dupes, stuck sagas); domain model instability (greenfield renames = migration nightmare); operational overhead without org buy-in. Rec: define versioning contract day 1, build rebuild pipeline before shipping, scope to stable subdomain first, sagas first-class, 6-month decision gate. Conf high. Weakest: abandonment technical vs organizational (knowledge concentration / team exodus).

## MEMBER: Devil's Advocate
Obvious answer blames ES itself — WRONG. Mess comes from one avoidable decision: coupling event log to query model + treating event store as shared DB across teams. Concrete failure: schema rot under silent consumers — Team A adds discountCode month 4, Team B fraud model replaying from position 0 silently drops undeserializable events, fraud scores stale, chargeback spike, root cause = replay 18mo through 3 undocumented schema versions. Secondary: snapshot neglect (rehydration at event 2M = 40s on Saturday traffic spike). Rec: ES only inside bounded context where you control all consumers; schema registry (Avro/Protobuf/JSON Schema + version envelope) before first event; if you can't name every consumer on a whiteboard, not ready. Conf high. Weakest: abandonment operational vs political (new architect/VP preference).
