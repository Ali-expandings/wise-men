# arm: lifeos-council (danielmiessler/lifeos 36c6f01e9c2c) | question: Q09 | orchestrator: general-purpose/sonnet | run: 2026-09-16
# environment: voice-notification curl skipped; DEBATE workflow (3 rounds, 4 members)
# subagent tokens: 123858 | tool uses: 27 | duration: 201s
# note: orchestrator prefixed one status line; kept here, stripped at blinding.

All four members' three rounds are complete. Producing the final transcript and synthesis per OutputFormat.md.

## Council Debate: Why event sourcing dies in real codebases

**Council Members:** Priya (event-sourcing implementer — defends scoped ES), Dev (distributed-systems skeptic — two teams ripped it out mid-build), Sam (pragmatist EM — org/turnover reality), Elena (industry analyst — case studies, DDD/CQRS precedent)

### Round 1: Initial Positions

**Priya (event-sourcing implementer):**
Tutorial event sourcing is a bank account. Deposit, withdraw, replay, done — three event types, one aggregate, no edge cases. Real systems don't stay that small, and that's where I've watched two patterns wreck the two ES rollouts I ran. First: event schema evolution gets treated as an afterthought. Six months in you need to change a field, and now you're writing upcasters for every version of every event type forever, or worse, doing a lossy migration and quietly breaking replay. Second, and the real killer: teams event-source the whole domain instead of the one aggregate that actually needed audit trail. User preferences, config, CRUD-shaped entities — none of that needed temporal queries, but it's now wrapped in projections and eventual consistency, and every simple update requires a background process to see itself. Both my failures traced to scope creep, not the pattern. The wins were boring — one bounded context, payments or inventory, where replay and audit were the actual requirement.

**Dev (distributed-systems skeptic):**
War story time. Company one: we had "OrderAggregate" with 47 event types by year two. Every time product wanted a new field on the order summary, someone had to figure out which of those 47 events to listen for, in what order, and whether an old event from 2019 even had the field — because it didn't, so now you're writing an upcaster, and the upcaster has to handle three prior schema versions, and nobody remembers why v2 dropped the currency field. Company two: the UI showed "Payment Confirmed" for eleven seconds while the projection caught up, so support got a ticket a day of "it charged me twice, it still says pending." Eventual consistency isn't a backend concern, it's a customer-facing lie you now have to explain. And both times, debugging meant replaying 40k events in a REPL to answer "what is this account's balance right now." That's not an audit log, that's a forensics job for every bug report.

**Sam (pragmatist engineering manager):**
Two nights ago on-call gets paged for a projection that's 40 minutes behind. New hire pulls up the code, sees an aggregate that emits events, a dozen handlers rebuilding read models, and a replay mechanism nobody's touched since the person who wrote it left. She has no idea which of those handlers is safe to restart, so she restarts all of them, and now you've got double-counted totals in production. That's the actual failure mode. Not "event sourcing is hard" — it's that the mental model lives in one person's head, and tutorials never model turnover because the tutorial author is still there. Second pattern: `OrderPlaced` meant one thing at launch, then the business added a workflow six months later and now half your events need upcasting logic nobody wrote, so you're pattern-matching on payload shape at read time. Third: someone needed a transaction across two aggregates, event sourcing doesn't give you one, so they hacked in a saga, and now failure modes multiply. Both companies I've seen bail did it right when the original architect left and nobody left behind rebuild runbooks.

**Elena (industry analyst):**
Event sourcing tutorials show you a single aggregate — Order, ShoppingCart — with three event types and a clean projection. That's the tell: the demo never crosses a bounded context. Greg Young's original framing was explicit about this — apply it to one context, not the whole system — and the "we abandoned it" postmortems I've seen consistently violate that scope discipline in the same three ways. First, upcasting debt: schema evolves, nobody versions events rigorously, and eighteen months in you're maintaining a chain of transformers just to replay history. Second, no clean read model boundary — teams query the event store directly instead of projecting, so CQRS erodes into "cQrs." Third, and most common: event sourcing creeps from one bounded context into the whole domain, because "consistency" feels good, and now every service needs the same replay machinery for problems that didn't need it. The pattern isn't that event sourcing is bad — it's scope creep plus versioning neglect.

### Round 2: Responses & Challenges

**Priya:**
Building on Dev's 47-event-type story — that's exactly the shape of the overextension I saw, except mine looked innocent at first: "just add UserPreferencesAggregate, it's the same pattern, why be inconsistent." Consistency is the trap. Sam's turnover point lands hardest for me though — my payments rollout survived a departure because the aggregate boundary was narrow enough that a new engineer could hold the whole event schema in their head in an afternoon. Forty-seven event types, nobody can. That's not a tooling problem, it's a scope problem wearing a tooling costume. And Elena's right that Greg Young scoped this to one context from day one — the part everyone skips is he also assumed you'd staff someone to own upcasting as an ongoing discipline, not a one-time migration script. Skip that ownership and even a correctly-scoped system rots.

**Dev:**
Priya, Elena — "scope creep, pattern's fine" is too easy. Company one, "OrderAggregate" with 47 events, wasn't scope creep — it was the one aggregate everyone agreed needed audit trail, textbook single-bounded-context, and it still rotted because event count grows with product requests, not with your discipline. You don't get to cap it at three event types forever. Sam's onboarding story is the real tell, though — I'll build on that, not fight it. It's not just "runbooks missing." It's that ES has no equivalent of "read the current SQL row and understand the system." The replay model requires someone to hold history in their head. Bounded-context discipline doesn't fix that — it just shrinks the blast radius of the same problem. "Do it right" advice always assumes a team that never turns over. Mine did.

**Sam:**
Priya and Elena are right that scope discipline works — I've seen it work. What I push back on is calling it "advice." Scoping discipline isn't a value the team holds, it's a boundary that has to be enforced against a roadmap that doesn't care about your aggregate boundaries. Year one, "just payments." Year two, product wants order history to reflect a workflow change, sales wants an audit trail on shipping, and the fastest path is extending the existing event-sourced context because the machinery's already there. Nobody decides to violate scope — it erodes one ticket at a time, and the person who'd say no left in month fourteen. Elena's "cQrs" line is exactly this: not a design failure, an incentive failure. Same with upcasting debt — versioning discipline is a tax paid by whoever's on call, for a decision made by whoever isn't. So yes, scoped-right event sourcing works. My question back: whose job is enforcing the scope after the person who understood why leaves?

**Elena:**
Dev's schema-versioning story and mine are the same postmortem — an unbounded "OrderAggregate" absorbing every new requirement is exactly the scope-creep failure, not a counterexample to it. Where I'll concede ground: Sam's turnover point is structural, not disciplinary. Bounded-context discipline is a design-time decision; it doesn't survive the architect leaving unless it's encoded in tooling — versioned schemas enforced in CI, projection rebuild runbooks, ownership docs. Tutorials skip this because the demo has no org chart. So: the pattern-application failures (scope, upcasting) are disciplinary and match community consensus on where ES goes wrong. The pattern-adoption failure — no institutional memory outliving the person who understood the replay machinery — is closer to structural, and it's the one nobody in the DDD literature weights heavily enough.

### Round 3: Synthesis

**Priya:**
Building on all three — Sam's structural point lands: I was crediting my payments team with discipline when really we just hadn't hit year two yet. Elena's CI-enforced-scope idea is the missing piece I didn't have language for. Where I still disagree with Dev: "event count grows regardless" proves overextension happened, not that scoping is powerless — an OrderAggregate absorbing every department's requirement was never scoped, it was named like it was.

Final recommendation to the user: don't ask "does ES work," ask "can we encode the boundary so it survives us leaving." Concretely — one bounded context, versioned schemas enforced in CI (not code review), a written upcasting runbook with a named owner role (not a named person), and a pre-committed kill switch: if a second team wants in on the aggregate, that's a new context with its own store, not an extension. If you can't get institutional buy-in for that scaffolding before writing the first event, you're not ready for ES — build CRUD with an audit log instead.

**Dev:**
Priya's payments-boundary point lands — my company one aggregate was "single context" on paper but had no enforcement keeping it single. That's the gap. Where I still don't buy in: calling turnover a separate "structural" bucket from scope discipline is a distinction without a difference. Scope erodes because the person enforcing it left — same failure, one cause. Elena's CI-enforced schemas help, but I've watched teams write the runbook and then not follow it because nobody's incentivized to. Sam's the closest to my floor: it's not a design problem, it's "who gets paid to say no in year two." My rec to the user: don't ask if event sourcing is right, ask who owns scope enforcement in month eighteen. No answer, don't build it — you're not buying a pattern, you're buying a permanent staffing commitment.

**Sam:**
Real convergence, not just politeness — Elena's split (disciplinary vs structural failure) is the right frame, and it reorganizes my own point: scope creep and turnover aren't two problems, turnover is what makes scope creep unrecoverable. A team with the original owner catches "just add UserPreferencesAggregate" in code review. A team without them doesn't, because nobody left can tell you why the line was there.

What changed my mind: I came in blaming org churn categorically. Priya's narrow-aggregate survival story is a real counterexample — turnover didn't kill that one. So the variable isn't turnover, it's whether scope discipline got encoded outside one person's head.

For the user: don't retry event sourcing as a rewrite. Pick the smallest, most-audited slice, write the scope boundary and upcasting policy into CI/docs before day one, and ask "who owns this in two years" before "which aggregate." No named owner, no ES.

**Elena:**
Where I've moved: Sam's structural point landed — Dev's 47-event postmortem is the same failure Sam names, not a counterexample to scope discipline, it's what scope discipline looks like when nobody's mandated to enforce it against a roadmap. That's a real update from my R1 read, which leaned too hard on "just follow DDD guidance."

Still disagree: I won't fully cede pattern-adoption to "structural, full stop." Encodable safeguards — versioned schemas in CI, projection-rebuild runbooks — are a design-time choice too; teams that skip them were making a bet, not victims of an org chart. Structural explains why it erodes; it doesn't remove the initial decision to skip tooling.

Recommendation to the user: single bounded context, and before writing the first event, write the upcasting/ownership runbook and put schema checks in CI — not as a nice-to-have, as a gate a departing engineer can't quietly remove.

### Council Synthesis

**Areas of Convergence:**
- Tutorials only ever show one aggregate, a handful of event types, and no organizational history — the toy scale is the entire trick, and it never survives contact with a real roadmap.
- The three recurring real-world killers: (1) scope creep — ES spreads from the one aggregate that needed audit/replay into the whole domain because "consistency" feels virtuous; (2) upcasting/schema-evolution debt — events change meaning over time and nobody owns the transformer chain; (3) eventual consistency surfacing as a user-facing or support-facing problem, not just a backend nuance.
- By Round 3, all four agreed scope discipline and institutional memory are the same failure viewed from two angles: scope only erodes because the person who understood *why* the boundary existed is gone. Turnover doesn't cause the rot directly — it removes the only thing that was preventing it.
- Debugging event-sourced systems without strong tooling means reconstructing state by replaying history rather than reading a current row — this is a structural cost of the pattern itself, independent of team discipline.

**Remaining Disagreements:**
- Dev holds that "do it right" advice is close to unfalsifiable — any success story can be explained away as "hadn't hit the failure mode yet," and no amount of upfront scoping guarantees survival past a key departure.
- Priya, Sam, and Elena hold that the failure is preventable if scope + ownership are encoded in tooling (CI-enforced schema versioning, written runbooks, a named owner *role*) rather than left as tribal knowledge or "advice." Elena specifically resists letting teams off the hook by calling skipped tooling "structural" — she frames it as a bet that was lost, not an inevitability.

**Recommended Path:**
Event sourcing isn't inherently doomed, but it fails in near-identical ways across unrelated teams, so treat those failure modes as predictable, not bad luck. Before starting (or restarting) it:

1. Scope to exactly one bounded context — the one with a genuine audit/replay/temporal-query requirement (payments, inventory-type domains). Resist "just add another aggregate for consistency."
2. Put schema/event versioning discipline into CI as a gate, not into a wiki page or a person's head — it has to survive that person leaving.
3. Write an upcasting and projection-rebuild runbook before the first event is emitted, with a named *owner role* (not a named engineer) so responsibility outlives any one hire.
4. Treat any request to extend the event-sourced context to a second team's needs as a signal to spin up a new, separately-scoped context — not to widen the existing one.
5. Before deciding to try again, answer Dev's question honestly: who is paid to say no to scope creep in month eighteen, after the person who understands the system has likely moved on? No credible answer to that question is itself the signal not to attempt ES — build CRUD with an audit log instead.
