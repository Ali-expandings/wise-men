# Q05 Arm A raw output
# salvaged_from_context: true
# salvage_note: Skill-suppression preamble used. Clean prose, no contamination.
# model: sonnet-4.6

Yes, and it's called a modular monolith — and for an 8-person team it's almost certainly the right answer.

The core idea: keep a single deployable unit, but enforce hard internal boundaries between modules. Each module owns its data, its logic, and its public interface. Other modules can only talk to it through that interface, never by reaching into its internals or its database tables. You get the deployment simplicity of a monolith with most of the organizational clarity of microservices.

The deployment coordination problem you're describing is almost never actually caused by having one binary. It's caused by having tangled code where a change in one area unpredictably affects another area, which forces everyone to sync before shipping. That's a coupling problem, not a deployment topology problem. Microservices solve coupling problems by making the blast radius physical — you literally can't reach into another service's database. But you can get 80% of that benefit with in-process module boundaries enforced through code review, linter rules, or language-level access controls, without paying the distributed systems tax.

The distributed systems tax is real and severe at your size. You now need service discovery, network failure handling, distributed tracing, eventual consistency in places that used to be a simple transaction, separate CI/CD pipelines per service, and someone who understands all the failure modes of the whole mesh. Eight engineers is not a lot of people to absorb that overhead while still shipping product.

The middle ground that actually works in practice: identify the 3-5 natural seams in your monolith — the places where teams already mentally think of the system as divided. Draw clear module boundaries there. Enforce that modules only talk through explicit interfaces (function calls, internal events, whatever fits your language). Make sure each module owns its own database schema or at minimum its own tables, and no other module queries them directly. Now your deployment problem is mostly solved because changes are localized, and you've built the conceptual groundwork to actually extract a service later if one module genuinely needs independent scaling or has a wildly different operational profile.

Extract to a real separate service only when you have a concrete, specific reason: this module needs to deploy 20 times a day while everything else deploys once a week, or it needs to run in a completely different language, or it has security requirements that demand true isolation. "The team working on this module wants autonomy" is a reasonable reason too, but only once you have enough people that the coordination overhead of a service is cheaper than the coordination overhead of shared code — and for most teams that's somewhere north of 15-20 engineers.

The honest failure mode of the modular monolith is discipline erosion. The boundaries are logical, not physical, so when someone is in a hurry they reach across them and nobody notices for months. You need lightweight enforcement: a linter rule, a CI check, an architecture fitness function, or just a culture of flagging it in code review. Without that, you drift back to a big ball of mud and the problem returns.

But compared to premature microservices — where you get all the coordination pain plus the distributed systems tax plus the operational complexity — a well-disciplined modular monolith is dramatically less pain for a team your size.
