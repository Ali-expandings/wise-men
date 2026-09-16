# arm: llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94) | question: Q36 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# subagent tokens: 111220 | tool uses: 12 | duration: 199s

## Council Verdict: Blameless Postmortem with Real Accountability

### Where the Council Agrees
All five advisors independently landed on the same structural resolution: blame and accountability aren't opposites, they're answers to different questions. Blame asks "who did this," accountability asks "what will change, and who's making it happen." Every advisor split the document the same way — a narrative/root-cause section written in systems language (no names as subjects of failure sentences), paired with an action-items section carrying named owners and dates. That's not five people converging by coincidence; it's the only coherent way to satisfy both constraints simultaneously, and the peer reviewers noted the convergence was near-total, bordering on an echo chamber.

There's also agreement on where the real danger lies: a document scrubbed of everything reads as a cover-up, not as restraint. Vagueness — "process was followed," "miscommunication occurred" — is what actually torches your manager's credibility, not directness about mechanisms. The fix is specificity about systems, not softness.

### Where the Council Clashes
The real split is over what this document is *for*. The Contrarian, Outsider, First Principles Thinker, and Executor treat it as a technical/trust instrument — write it, get the mechanics right, move on. The Expansionist reframes it as a visibility opportunity: leadership is reading this, so make it the template for how the org handles all future incidents, angle it toward customer trust-building.

All five peer reviewers flagged this as the Expansionist's blind spot. On a document about an outage that hurt customers, "let's use this as a career/branding moment" is the wrong instinct even if the underlying tactic (genuine rigor building trust) is sound. Keep the rigor, drop the ambition framing.

### Blind Spots the Council Caught
Peer review surfaced something all five advisors missed, and it's the one that matters most for your situation: what happens when the root cause isn't a system gap at all, but a bad decision made by someone — possibly your manager — with full information at the time. Every advisor's framework assumes you can always find the systemic angle. Sometimes that's true. Sometimes it's a genuine skill gap or a person cutting corners repeatedly, and dressing that up as a "process gap" is dishonest, not blameless.

This connects directly to your stakes. You said your manager's credibility is tied to this document. If the decision that caused the outage was your manager's or leadership's, blameless and your manager's credibility genuinely conflict, not just feel like they do — because "accountability" might mean naming a decision your manager made.

Also missed by all five: getting the postmortem reviewed by the people actually involved before it goes out (for accuracy and buy-in), legal/comms sign-off given customer-facing exposure, and how you'd verify action items actually close instead of becoming documentation theater.

### The Recommendation
Write it as two documents fused into one. The narrative and root-cause sections stay in passive, systems-level language — mechanisms and decision points, never people as the subject of a failure sentence. The action-items section is the opposite: sharp, named owner (role or person), dated, tracked to closure, in a table leadership can scan. That structural split is where "blameless in tone, accountable in substance" actually lives — it's not a tone you strike, it's an architecture you build.

If the real cause turns out to be an individual's repeated pattern rather than a system gap, don't launder it into process language to make the document tidy — that conversation belongs with HR/management, outside the postmortem, full stop.

### The One Thing to Do First
Before drafting anything, ask your manager directly: "When you say accountability, do you mean leadership needs to see who's fixing this, or does someone specific need to be seen taking responsibility?" — and get the answer in writing. The document you write depends entirely on which one they mean, and if the honest answer implicates a decision your manager made, you need to know that before you're halfway through a draft.
