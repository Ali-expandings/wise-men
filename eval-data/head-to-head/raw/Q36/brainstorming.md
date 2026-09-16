# arm: brainstorming (obra/superpowers b36e0829c6d0) | question: Q36 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 81757 | tool uses: 1 | duration: 60s

**Classification: Spike.** This is a conceptual question needing a recommendation, not a document I write for you — treating it as: state the tension, probe assumptions, deliver the answer.

**Question + probe (assumed answers, since no reply available this run):**
- Is the tension about the document's language, or about downstream consequences (reviews, discipline)? → Assumed: the document itself — how to write it so both readings hold.
- Audience — eng-only, or exec/customer-facing too? → Assumed: internal eng + leadership; a separate customer-facing summary if needed.
- Specific incident in hand, or general framework? → Assumed: specific incident, general framework applies directly.

**The recommendation:**

Blameless and accountable aren't opposites — they're solving different problems. Blameless answers "why did this happen" without judging character or competence. Accountable answers "who owns fixing it, and will they" — forward-looking, always answerable. Confusing the two is what makes them feel contradictory.

The split to write into the document:

**1. Narrative (blameless zone) — what happened**
- Timeline of actions and decisions, described in context: "the deploy ran without the new canary check, which had been disabled the prior week for an unrelated migration" — not "Alex forgot to check X."
- No individual is the subject of a judgment sentence. People appear as actors executing a process, not as culprits.
- Root cause section goes past the first person who touched the system, to the conditions that let it happen (missing guardrail, unclear runbook, alert fatigue, understaffed on-call). If the first draft's root cause is a person's action, keep asking why until it's a system gap.

**2. Action items (accountability zone) — what happens next**
- Every action item has one named owner (not a team), a due date, and a tracking ticket.
- Owners commit to prevention work, not confession. "Alex owns re-enabling the canary check and adding a CI guard so it can't be silently disabled — due Sept 30" is accountability. It carries a name and a deadline without carrying blame.
- Close the loop: a follow-up review (2-4 weeks out) checks which action items actually landed. This is where most "blameless" processes quietly lose their teeth — and it's the single highest-leverage thing to add if your manager wants accountability to be real, not just a section header.

**3. Meeting conduct matches the doc**
Run the review itself blameless — assume good intent, ask "what made this seem reasonable at the time," don't let it become a hot-seat. Save ownership talk for the action-items portion, where it belongs.

**One-line answer for your manager, if useful:** "Blameless" governs how we talk about what happened; "accountable" governs who owns what happens next. The doc keeps those in separate sections so neither gets diluted by the other.
