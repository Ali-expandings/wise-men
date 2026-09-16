# arm: grilling (mattpocock/skills 85f83d3fde1d) | question: Q36 | orchestrator: general-purpose/sonnet | run: 2026-09-16 (Amendment 1 rules)
# adaptation: no-human — see PREREG.md
# subagent tokens: 75437 | tool uses: 1 | duration: 42s

❓ **Q1** - **What kind of "accountability" does your manager actually want?**: Blameless and accountable feel contradictory only if "accountability" means pinning fault on a person. It usually means something else: clear ownership of the fixes, and honesty about what actually broke (including leadership/process gaps), without a hunt for who to blame. Which is it — individual fault-finding, or ownership of remediation + honest surfacing of systemic gaps?

➡️ Assumed: organizational/systemic accountability — ownership of action items and honesty about contributing factors, not "who screwed up." This is the standard meaning in blameless-postmortem culture (Google SRE, Etsy) and the only reading that isn't actually contradictory with "blameless."

---

❓ **Q2** - **Who reads this document?**: Internal engineering only, or does it also go to executives and/or customers? This shapes how much narrative detail and what tone is safe to use.

➡️ Assumed: internal engineering + leadership as primary audience, with a shorter customer-facing summary derived from it separately if needed. (Full blameless postmortems with names/systems detail generally shouldn't go external as-is.)

---

❓ **Q3** - **Is the root cause already understood, or still being investigated while you draft?**: Determines whether you're writing a complete postmortem now or an interim one that will need a follow-up.

➡️ Assumed: root cause is understood — this is a standard post-resolution postmortem, not an interim status update.

---

❓ **Q4** - **In the timeline/narrative itself, do you name individuals ("Alex restarted the service") or use role/system language ("the on-call engineer restarted the service")?**: This is the actual mechanical decision that makes a doc feel blameless or not.

➡️ Assumed: role/system language in the narrative — no individual names attached to actions or mistakes in the timeline. Blamelessness lives here, in the prose.

---

❓ **Q5** - **Where does the "accountable" half live structurally?**: Woven into the narrative, or isolated in a dedicated Action Items section with named owners and deadlines?

➡️ Assumed: a dedicated "Action Items" section, separate from the timeline, where each item has one named owner (a person, not "the team") and a deadline. Accountability lives here, in ownership of fixes — not in the story of what happened.

---

❓ **Q6** - **Does accountability extend upward — to leadership/process decisions — or does it land only on the team closest to the incident?**: If the postmortem only ever finds fixes for the front-line team, "blameless" becomes a fig leaf that quietly blames the junior-most person anyway.

➡️ Assumed: it extends upward. If a contributing factor was "we had no alerting for this" or "we approved this deploy process," that's named as a systemic gap with its own owner and action item, not glossed over.

---

**Final recommendation**

The contradiction dissolves once you see "blameless" and "accountable" as operating on different layers of the same document, not competing goals:

- **Blameless = how you write the narrative.** Timeline and root-cause sections use system/role language, never "X person made a mistake." Assume good faith: given the information and pressure at the time, any competent person would likely have done the same. Focus on what let the failure happen (missing safeguard, ambiguous runbook, no alert) rather than who triggered it.

- **Accountable = how you write the action items.** Every contributing factor gets a corresponding action item with one named owner (a real person) and a real deadline, tracked to completion. This is where responsibility lives — not "whose fault," but "who owns making sure this can't happen the same way twice." Owners can and should include leadership when the gap is a process or resourcing decision, not just the engineer on call.

Concrete structure:
1. **Summary** — what happened, impact, duration, in one paragraph.
2. **Impact** — customers/systems affected, quantified.
3. **Timeline** — blameless, role/system-based, factual, timestamped.
4. **Root cause / contributing factors** — plural, systemic (a 5-whys that stops at systems and decisions, not at a person).
5. **What went well / what made it worse** — honest, includes process and leadership factors.
6. **Action items** — table: item, owner (named), deadline, status. This section is where "accountability" is visible and auditable.
7. **Lessons learned** — short, forward-looking.

The tell for whether you got the balance right: a reader should finish the doc unable to name who to blame, but able to name exactly who is responsible for what happens next.
