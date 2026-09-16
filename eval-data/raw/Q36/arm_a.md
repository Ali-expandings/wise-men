# Q36 Arm A raw output
# salvaged_from_context: false
# model: sonnet-4.6
# skill_suppression: applied
# contamination: none
# regenerated: 2026-05-29 (fresh full pipeline)

These two goals feel contradictory because people often conflate "blame" with "accountability," but they're actually describing different things. Once you separate them cleanly, the postmortem writes itself.

Blame is about finding a person to fault. It's retrospective, punitive, and personal. It answers the question "whose fault was this?" Accountability is about understanding what happened and ensuring someone owns the path forward. It's forward-looking, constructive, and systemic. A blameless postmortem isn't accountability-free — it shifts accountability from individuals to systems, processes, and decisions, while still naming who is responsible for fixing each thing.

The practical way to do this is to distinguish between the "what happened" section and the "what we're doing about it" section. In the narrative, you describe actions without assigning personal culpability. You write "a configuration change was deployed at 14:32" not "Dave deployed a bad config at 14:32." You write "the monitoring threshold was set too high to catch gradual degradation" not "the team set up monitoring incorrectly." This isn't dishonesty or euphemism — it's precision. The configuration change is a fact. Dave's intent, competence, or culpability is an interpretation, and a postmortem is not the right forum for that interpretation.

The reason blameless language matters here is deeply practical: if engineers fear being named in postmortems, they'll stop writing honest ones. They'll under-report near-misses. They'll avoid owning incidents. The entire value of the postmortem culture collapses. Blameless language protects the information flow that makes postmortems worth writing.

Accountability comes back in the action items. Every action item needs an owner — a specific named person — and a due date. "The on-call rotation process will be revised by June 15, owned by Priya." That's accountability. Priya's name is there. She has a deadline. Her manager can follow up. This is where your manager's concern is actually satisfied, and it's completely compatible with the blameless narrative section. You're not saying no one is responsible for fixing things; you're saying the postmortem isn't the place to prosecute anyone for causing them.

There's also a useful framing device called the "five whys" that naturally pushes you away from individual blame. When you keep asking why, you almost always end up at systemic causes — insufficient testing infrastructure, unclear ownership boundaries, missing runbooks, inadequate alerting. Real outages are almost never caused by one person doing one stupid thing. They're caused by a chain of conditions that made the bad outcome possible and the error easy to make. Writing that story — the whole chain — is more accurate than assigning blame, and it produces better action items because you're fixing the actual causes rather than just punishing someone.

One more thing that helps: write the postmortem as if the person who made the triggering mistake is a perfectly competent, well-intentioned engineer who was set up by their environment to make that mistake. Because almost always, that's true. If a senior engineer with ten years of experience deployed a breaking change without catching it, the real questions are: why did the tooling allow that? Why didn't review catch it? Why didn't staging mirror production closely enough? Why was the rollback procedure slow? Those questions produce action items. "Dave screwed up" produces nothing except a chilling effect on your team's willingness to be honest.

Your manager wants accountability because they want to see follow-through and improvement — they want to be able to point to the postmortem and say "we learned from this." That's entirely achievable. Give every action item a name, a date, and a mechanism for tracking it. Have someone present postmortem progress in a future team meeting. Blamelessness and accountability, properly understood, aren't in tension at all. They're just operating on different parts of the document.
