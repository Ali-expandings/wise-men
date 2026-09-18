# arm: warp-council (warpdotdev/common-skills 69b4753651ab) | question: Q51 | orchestrator: general-purpose/sonnet | run: 2026-09-18 (round 3, PREREG-3 rules)
# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md
# subagent tokens: 110240 | tool uses: 5 | duration: 488s
# note: the orchestrator wrote its output in the compressed register that the author's global config asks of every agent (an environment condition shared by every arm in all three rounds); kept as produced, since the run was complete

## Council

3 models avail this harness = Claude only (opus/sonnet/haiku). No GPT, no OSS. Per skill's own fallback rule: Sonnet subs for GPT-practitioner slot, Haiku subs for OSS-contrarian slot. Substitution noted per skill instructions.

- Opus / Strategist — long-horizon career capital, IC vs EM ladder economics, optionality
- Sonnet / Practitioner — year-1 lived reality, switching-cost vs internal-risk read (GPT sub)
- Haiku / Contrarian — attacks question's framing, surfaces missing facts, red-teams "manager = strategic" (OSS sub)

All 3 read-only. No filesystem/vault/web search — question self-contained by design. Reasoned from question text + general IC/EM career-track knowledge only, independently, no cross-talk.

## Recommendation

3/3 lean same way: **take senior IC offer.** Not unconditional though — each flags own swing-fact that'd flip it to manager track. Check Tradeoffs before locking in.

## Why

- "Should be more strategic" = a *should*, not a *want*. 2 of 3 flag this as status-anxiety/obligation signal, not real desire — known predictor of poor first-time-manager fit.
- Optionality favors IC hard, across all 3. IC → manager stays open, gets *easier* w/ seniority (staff ICs get mgmt offers routinely). Manager → IC reversal: visible, often costs a level, awkward re-entry same company.
- IC offer = validated — outside market already paying for that skill. Manager track = speculative, first attempt, unproven.
- Staff/senior IC work often *already is* "strategic" work — architecture calls, tech direction, hiring bar. Premise that mgmt = strategic, IC = not, is false at that level.
- Stated preference (code > meetings) matches evidence: real EM week = 1:1s, calibration, hiring loops, roadmap syncs. Coding time → near-zero in 2-3 quarters, even "player-coach" setups.

## Tradeoffs and risks

- Swing fact #1: does current company have staff/principal IC ladder above senior? If no — IC-elsewhere wins clean (Haiku: high confidence). Does new company's "senior" sit below a real ladder, or is it terminal title? If terminal — manager track edges back ahead (Opus).
- Swing fact #2: is internal mgmt opening rare/closing (reorg, one-time nod) or will it recur? If rare + curiosity re: leading people genuine (not anxiety-driven) — worth the one-time shot (Sonnet).
- "Smaller company" = real tail risk (funding/stability), independent of IC/manager axis, cuts both ways — none of 3 members had funding/runway facts to weigh it properly.
- Comp/equity delta: unknown, not in question, matters a lot, unweighed by all 3.
- Manager path = cheapest place to fail (existing trust/context cushion absorbs mistakes). IC path = costs 3-6mo ramp + resets trust clock at new co.

## Final call

Get 3 facts before deciding:
1. Staff/principal IC ladder exist at current company — yes/no.
2. New company's funding runway / stability.
3. Internal mgmt opening — one-time window or recurring.

Default lean absent new facts: **take senior IC offer** — matches stated preference, validated market signal, better optionality, 3/3 council convergence.

Exception: if current co has zero IC ladder above senior, use offer as leverage first — ask for staff/tech-lead counter before deciding either way.

Skip manager track if driven by "should," not "want." Per 2 of 3 reports, that's a flagged failure predictor, not a minor detail.
