# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q36 | orchestrator: general-purpose/sonnet | run: 2026-09-17 (v2, Amendment 1 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 113437 | tool uses: 4 | duration: 845s

*Council: 3 Claude subagents — no GPT/OSS model available in this harness, so model diversity fell back to perspective-only. Incident-review theory (opus), document mechanics (sonnet), contrarian red-team (opus).*

## Recommendation

Not a real contradiction — one word, "accountability," is doing two jobs. Split it: blameless protects **people** from punishment for decisions that were reasonable at the time; accountability targets **systems and commitments** — name the gap, name an owner, name a date. Write every sentence that way and both demands are satisfied at once. One catch: this only works if your manager means the forward-looking kind. Confirm that before you finish the draft.

## Why

- Dekker's *Just Culture* splits accountability into backward-looking (who pays) and forward-looking (who owns the fix). Blameless cancels only the first. Two of the three council members independently landed on this exact split without seeing each other's work — strong signal it's the standard, correct read, not a stretch.
- Etsy/Allspaw's original case for blameless postmortems: punish people for good-faith mistakes and they hide details next time, so the same failure recurs unseen. Blameless is what makes real accountability (the fix actually happening) possible — not what cancels it.
- Mechanically: never write "[person] + failed to / should have." Always write "[system or decision] + the gap it left + why it made sense at the time," paired with an owner and due date for the fix. Passive voice ("mistakes were made") fails *both* goals at once — it invites speculation about who, and it owns nothing.

## Example rewrites

- "The on-call engineer missed the alert for 40 minutes." → "The page routed to one phone with no auto-escalation after 15 min unacked. Owner: SRE lead, fix by Oct 3."
- "Someone pushed a bad config without testing it." → "A config change disabling the rate limiter shipped straight to prod — config-only changes skip the staging gate. Owner: Platform lead, fix by Sep 30."
- "QA should have caught this." → "The regression suite doesn't cover the checkout-discount path; coverage is tracked by file, not by user journey. Owner: QA lead, fix by Oct 15."

## Tradeoffs and risks

- Real risk, not hypothetical: if your manager actually means *personal* consequences — it shows up in a performance review, or a name gets said out loud in the meeting even though the doc reads clean — no wording fixes that. That's an org problem, not a writing problem. The council's contrarian pass flagged this as the single biggest way the advice above backfires.
- On a small team, "the on-call engineer" is still obviously one specific person internally. Omitting names isn't enough on its own if that's the only blameless mechanism you're using — the system-plus-gap framing is what actually does the work.
- Don't let vagueness pass as diplomacy. "Mistakes were made" protects no one and fixes nothing — it's the failure mode on both sides simultaneously.

## Final call

Before you finish the draft, ask your manager one direct question: "When you say accountability, do you mean named owners and deadlines on the fixes, or consequences for a person?" Get the answer in writing if you can — a recap email is enough. If it's the former (the normal case), structure the doc as: impact → timeline → contributing factors (system + gap + why it made sense, no names attached to blame) → corrective actions (owner, date, tracking link) → a follow-up date to confirm the actions actually happened. If your manager means the latter, that's a conversation to have before you write another word, not a phrasing problem — loop in your own manager or HR rather than trying to wordsmith around it.
