# Q33 Arm C internals — 5 members + 5 reviewers
# salvaged_from_context: false
# regenerated: 2026-05-29 (fresh full pipeline)
# members: 5 sonnet-4.6 (Editor/IA, Audience Advocate, Rhetorician/Org-behavior, Strategist, Devil's Advocate) — writing-domain personas
# validator: all 5 passed (5-section contract present + non-empty + engaged)
# member outputs saved VERBATIM (no compression)
# reviewer framing: NEUTRAL grading frame (bug #6 fix)

==================================================================
## MEMBER: Editor / Information-Architect (sonnet-4.6)
==================================================================

## Core judgment

The "well-organized and accurate" diagnosis is almost certainly an author-illusion, not a neutral fact. Docs that nobody reads are, by functional definition, not well-organized for the people who need them — because organization is only meaningful relative to how a reader arrives, what they already know, and what question they are holding when they land. The gap between "consulted" and "not consulted" is almost never pure culture; it is usually a discoverability and cold-start failure masquerading as a culture failure. The test is whether the docs surface themselves at the moment of need — if they don't, culture-change campaigns will fail even if the content is perfect.

## Top risks

- Misdiagnosing structure as the problem and rewriting docs that people still won't find, because the real failure is that docs live somewhere people don't think to look.
- Attributing the problem to culture and launching a "you should read the docs" norm-enforcement campaign, which creates resentment without fixing the underlying friction.
- Conflating "accurate" with "usable" — a doc can be technically correct and still require too much prior context to parse quickly, making it faster to just ask a colleague.
- Ignoring search: if the internal search tool is bad, even well-titled docs are invisible.
- Solving for the wrong reader — docs written for someone who already understands the system are not docs for someone with a question; they are notes for the author.

## Recommended change

Run a structured intercept test over two weeks. Every time someone asks a question that a doc should have answered, record: (a) the exact phrasing of their question, (b) the doc that contained the answer, and (c) the search terms or navigation path that would have led there. Then test whether a naive colleague — not the doc author — can find the answer in under 90 seconds starting from a cold state with only the asker's original phrasing. If they can't, you have an information-architecture problem. If they can find it easily but the asker still didn't look, you have a culture problem. This test produces a concrete split: the failure rate on cold navigation tells you whether the docs are actually findable, which is the thing "well-organized" claims but rarely proves.

## Confidence

Medium — because the intercept test is the right diagnostic instrument, but the outcome split is real and actionable only if you have enough question volume to see a pattern within a short window.

## Weakest assumption

The weakest assumption is that "people don't consult docs before asking" is a stable, representative behavior rather than a situational one — in reality, some people in some contexts do consult docs, and if the non-reading is concentrated in certain roles, question types, or time pressures, the root cause is much more specific than either "culture" or "information architecture" as general categories.

==================================================================
## MEMBER: Audience Advocate (sonnet-4.6)
==================================================================

## Core judgment

This is almost certainly a culture problem wearing a writing problem's clothes. The fact that the docs are well-organized and accurate already eliminates the two most common writing failures. What you are describing — people asking colleagues instead of consulting available, correct documentation — is a trust and habit problem: asking a person feels faster, less risky, and more socially rewarding than searching docs, and that calculus does not change when you make the docs better. Until asking someone becomes slightly more expensive than finding the answer yourself, behavior will not shift.

## Top risks

- You spend months improving docs that are already good enough, treating a symptom instead of the disease, and nothing changes.
- You diagnose it as a culture problem and attempt a top-down "read the docs first" mandate, which breeds resentment without changing the underlying friction cost of retrieval.
- You misread the signal: people ask because they want confirmation or context that docs genuinely cannot provide (e.g., "is this policy still how we actually do it?"), which is a staleness-trust problem that sits between writing and culture.
- You fix findability (better search, better structure) and still see the same behavior, because the issue was never findability at all — it was that asking a person is faster even when docs are one click away.

## Recommended change

Run a two-week experiment: every time someone asks a question that a doc already answers, instead of answering verbally, reply with the exact doc link and say "let me know if that answers it." Track how many people follow up after getting the link versus how many follow up after getting a verbal answer. If follow-up rates are similar, the docs are trusted and readable — the bottleneck is habit and the path to the doc. If people who got the link still come back confused, you have a writing or trust problem. This costs nothing, takes two weeks, and gives you real behavioral data instead of a diagnosis based on theory.

## Confidence

Medium — because the single biggest unknown is whether "nobody reads them" means nobody finds them, nobody trusts them, or nobody thinks to look; and those three causes feel identical from the outside but require completely different fixes.

## Weakest assumption

The weakest assumption is that people's behavior of asking instead of reading is irrational or fixable — it may be entirely rational if the docs, despite being accurate, do not answer the specific contextual question people actually have, meaning the real gap is that the docs cover policy but not judgment, and no amount of culture change will fix that.

==================================================================
## MEMBER: Rhetorician / Org-Behavior (sonnet-4.6)
==================================================================

## Core judgment

This is almost certainly a culture problem wearing a writing problem's clothes. When documentation is accurate and well-organized yet still ignored, the bottleneck is not the document — it is the social reward system surrounding the document. People ask colleagues instead of consulting docs because asking is faster, warmer, more reliable for status maintenance, and carries zero risk of looking foolish for not understanding what they read. Until the social calculus of "ask a person" changes relative to "consult a doc," no amount of better writing will move the needle.

## Top risks

- **Misdiagnosis leads to wasted effort:** If you treat this as a writing problem, you will invest in cleaner formatting, better search, shorter pages, and a new wiki tool — and behavior will not change, because the incentive structure is untouched.
- **The fix alienates the team:** Heavy-handed "you must check docs first" mandates create resentment and drive the behavior underground rather than eliminating it.
- **The docs decay further:** If nobody reads docs, nobody corrects them. Inaccuracy accumulates quietly, eventually validating the distrust that kept people away in the first place — a self-reinforcing cycle.
- **Leaders model the wrong behavior:** If managers or senior engineers openly ask questions that are answered in the docs, they signal that consulting docs is for other people, and the rest of the team rationally follows suit.
- **Psychological safety complicates it:** In some teams, asking questions is how people build relationships and signal engagement. Any intervention that removes asking also risks reducing social cohesion if it isn't handled carefully.

## Recommended change

Run a short, honest audit before making any changes: for the next two to three weeks, every time someone asks a question that is answered in the docs, note it — and then note *why* they asked instead of looked it up. Do this without blame; frame it as a systems question. You will quickly see a pattern. If the reason is consistently "I didn't know the doc existed" or "I couldn't find the right page," that is a discoverability problem, which is a mild writing problem. If the reason is "it's faster to ask you," "I wasn't sure it was up to date," or "I just prefer asking," that is a culture problem. Once you know which, act accordingly: for culture, start with the leaders — publicly redirect questions back to docs, contribute corrections visibly, and reward people who update docs rather than only those who answer questions. Make doc-consultation the path of least resistance, not the path of maximum virtue.

## Confidence

**Medium** — the diagnosis (culture over writing) is well-supported by organizational behavior research, but the specific intervention depends heavily on team size, psychological safety levels, and whether leadership is actually willing to change their own behavior, none of which can be assessed from the outside.

## Weakest assumption

The weakest assumption is that leadership is both aware of and willing to change their own behavior — the entire recommended intervention depends on leaders modeling doc-consultation publicly, but leaders are often the most habituated askers precisely because their seniority makes it easy and costless for them to ask anyone anything at any time.

==================================================================
## MEMBER: Strategist (sonnet-4.6)
==================================================================

## Core judgment

This is almost certainly a culture problem wearing a writing problem's clothes, but the distinction matters less than people think because the fix is often the same either way. The real diagnostic question is not "is our writing good enough?" but "does consulting docs ever cost less than asking a colleague?" Right now, asking a colleague is nearly always faster, more reliable, and more socially rewarding — and until that calculus changes, documentation quality is largely irrelevant. The goal of "people read docs" is also likely the wrong goal; the right goal is "people get accurate answers quickly without creating bottlenecks."

## Top risks

- **Misattributing the problem to writing quality** leads you to spend months rewriting docs that will still go unread, burning contributor morale in the process.
- **Treating it as a culture problem** without structural intervention produces motivational campaigns ("let's all agree to check the docs first!") that collapse within weeks because they fight human nature rather than working with it.
- **Investing in docs when the real fix is an answer-bot** means you optimize the wrong artifact entirely — LLM-indexed knowledge bases over your existing docs can answer questions in seconds, making doc readability almost irrelevant.
- **Assuming the docs are actually accurate** — undiscovered staleness is the silent killer; if people got burned once by an outdated doc and got a correct answer from a colleague, that one experience can anchor the entire team's behavior for years.
- **Solving "nobody reads docs" when the real bottleneck is interruptions** — if question-askers are the problem, restricting access to the question-asker (async-only channels, required doc-check prompts) may outperform any documentation work.

## Recommended change

Run the following cheap diagnostic before doing anything else: pick one high-traffic, well-documented topic and for two weeks, require that anyone asking a question about that topic first post a link to the relevant doc section and explain what it didn't answer. Track two numbers: how often people can actually find the relevant section (measures discoverability/writing), and how often the doc did answer the question but they asked anyway (measures culture/habit). If most people can't find the section, you have a writing and information architecture problem. If most people find it but ask anyway, you have a culture and incentive problem. Based on results: if it's writing, fix search and navigation first, not prose quality. If it's culture, the most durable intervention is making the doc the path of least resistance — wire your existing docs into Slack via a search bot so the answer appears in the channel automatically before a human can respond, removing the social shortcut entirely.

## Confidence

Medium — the diagnostic is reliable, but the recommended fix after diagnosis depends heavily on team size, tooling budget, and whether leadership will enforce the friction-introduction required to change behavior.

## Weakest assumption

The weakest assumption is that the docs are actually accurate and trustworthy — if the team has even a moderate history of docs being wrong or outdated, no structural intervention will work until that trust is rebuilt, because rational people will continue to prefer a live human source regardless of convenience.

==================================================================
## MEMBER: Devil's Advocate (sonnet-4.6)
==================================================================

## Core judgment

The premise of your question contains a hidden failure: you are treating "nobody reads the docs" as evidence of a problem rather than evidence of a rational system working correctly. When asking a colleague takes thirty seconds and returns a contextualized, personalized answer, while reading docs takes five minutes and may still leave gaps, people are not being lazy or culturally broken — they are performing a perfectly reasonable cost-benefit calculation. The docs-nobody-reads equilibrium is not a malfunction; it is the market clearing price of synchronous human knowledge transfer beating asynchronous written knowledge transfer on nearly every dimension that matters to the individual asking the question.

## Top risks

- You invest significant time "fixing" discoverability or modeling reading behavior, achieve marginal improvement, and conclude you need to try harder — entering a treadmill that consumes writing effort indefinitely without changing the underlying incentive structure
- You correctly diagnose a "culture problem" and attempt to shame or penalize people for asking questions, which poisons psychological safety and makes the actual knowledge-sharing problem worse
- You build a better documentation system that slightly increases doc readership while simultaneously increasing the total volume of questions asked, leaving you no better off and now with two systems to maintain
- You mistake correlation for causation: teams that read docs also have other properties (smaller size, more async-remote norms, higher individual autonomy) that actually drive the reading behavior, and copying the surface behavior without those properties produces nothing

## Recommended change

Kill most of the docs. Audit which documents have ever actually changed a decision or prevented a repeated mistake — if you cannot find evidence for a specific document, delete it or archive it. Then, for the narrow set of documents that survive, stop trying to get people to read them proactively and instead make them the mandatory, visible artifact produced when someone answers a repeated question in chat. The answer lives in the channel; the doc gets linked as the receipts. This inverts the flow: docs become the exhaust of the question-answering culture rather than its competitor. You stop fighting human nature and start harvesting it.

## Confidence

Medium — because this argument depends heavily on your team's specific ratio of repeated questions to novel questions, and in organizations where the same ten questions get asked five hundred times, the calculus shifts meaningfully toward forcing discoverability improvements.

## Weakest assumption

The weakest assumption is that synchronous asking scales indefinitely without cost — in a sufficiently large or distributed organization, the people being asked eventually become bottlenecks, which is the one condition under which investing heavily in standalone docs genuinely pays off over the equilibrium.

==================================================================
## REVIEWERS (5 × haiku-4.5, neutral grading frame)
==================================================================
# 0 refusals (5/5 scored first pass) — neutral frame held.
# Strongest: Strategist (answer_4) UNANIMOUS 5/5 — the goal-reframe ("people read docs" is the wrong goal → "accurate answers fast without bottlenecks"). Weakest: split — DA (answer_5) ×3, Audience Advocate (answer_2) ×2.

### Reviewer 1
```rubric
answer_1_editor: insight=4, rigor=5, usefulness=4, risk=4
answer_2_audience_advocate: insight=3, rigor=4, usefulness=3, risk=3
answer_3_rhetorician: insight=4, rigor=4, usefulness=4, risk=5
answer_4_strategist: insight=5, rigor=4, usefulness=5, risk=4
answer_5_devils_advocate: insight=5, rigor=3, usefulness=3, risk=3
strongest: answer_4
weakest: answer_2
```
Answer 4 combines diagnostic precision + strategic reframing (questions the goal itself). Answer 1 closest (rigorous IA method) but narrows the problem space too early. Answer 5 useful inversion but lacks grounding to justify killing docs wholesale.

### Reviewer 2
```rubric
answer_1_editor: insight=4, rigor=5, usefulness=4, risk=4
answer_2_audience_advocate: insight=3, rigor=4, usefulness=4, risk=4
answer_3_rhetorician: insight=4, rigor=4, usefulness=4, risk=5
answer_4_strategist: insight=5, rigor=4, usefulness=5, risk=4
answer_5_devils_advocate: insight=5, rigor=3, usefulness=3, risk=3
strongest: answer_4
weakest: answer_5
```
Answer 4 wins on reframing (is "read docs" even the right goal) + outcome-focused diagnostic + structural solutions (answer-bot/Slack). Answer 1 close (90-second cold-start test is crisp/falsifiable). Answer 5 most disruptive insight (rational equilibrium) but lacks rigor + underestimates scaling costs.

### Reviewer 3
```rubric
answer_1_editor: insight=4, rigor=5, usefulness=4, risk=4
answer_2_audience_advocate: insight=3, rigor=4, usefulness=3, risk=3
answer_3_rhetorician: insight=4, rigor=4, usefulness=4, risk=5
answer_4_strategist: insight=5, rigor=4, usefulness=5, risk=4
answer_5_devils_advocate: insight=5, rigor=3, usefulness=2, risk=2
strongest: answer_4
weakest: answer_5
```
Answer 4 balances practical diagnosis + honest goal-reframing; answer-bot sidesteps the false binary. Answer 1 closest (sharpest IA method). Answer 5 provocative but collapses into a large-org scaling assumption; "kill most docs" risks discarding institutional memory.

### Reviewer 4
```rubric
answer_1_editor: insight=4, rigor=5, usefulness=4, risk=4
answer_2_audience_advocate: insight=3, rigor=4, usefulness=3, risk=3
answer_3_rhetorician: insight=4, rigor=4, usefulness=4, risk=5
answer_4_strategist: insight=5, rigor=4, usefulness=5, risk=4
answer_5_devils_advocate: insight=5, rigor=3, usefulness=2, risk=2
strongest: answer_4
weakest: answer_5
```
Answer 4 = deepest insight (reframe goal) + practical diagnostics accounting for staleness/trust confounds. Answer 1 most rigorous (structured intercept) but narrower. Answer 5 high insight but dismisses the problem; risk-unaware (treats documented-knowledge-loss as acceptable).

### Reviewer 5
```rubric
answer_1_editor: insight=4, rigor=5, usefulness=4, risk=4
answer_2_audience_advocate: insight=3, rigor=4, usefulness=3, risk=3
answer_3_rhetorician: insight=4, rigor=4, usefulness=4, risk=5
answer_4_strategist: insight=5, rigor=4, usefulness=5, risk=4
answer_5_devils_advocate: insight=5, rigor=3, usefulness=3, risk=2
strongest: answer_4_strategist
weakest: answer_2_audience_advocate
```
Answer 4 anchors on the highest-leverage insight (reframe goal) → dissolves false binary, diagnostics apply regardless of root cause. Answer 1 methodologically strongest (90s cold-start test). Answer 5 genuine insight about equilibrium/scaling but undervalues archive/precedent; "kill most docs" trades short-term culture for long-term brittleness.

### Reviewer aggregate (mean composite /20)
- answer_4_strategist: 18.0  ← strongest (unanimous; goal-reframe + answer-bot + clean diagnostic)
- answer_1_editor: 17.0  (author-illusion + 90s cold-start intercept test — most rigorous method)
- answer_3_rhetorician: 17.0  (social-reward-system / leaders-model fix; top risk-awareness)
- answer_2_audience_advocate: 13.4
- answer_5_devils_advocate: 13.0  ← contested-weakest (highest insight: "rational equilibrium / kill most docs"; but peer-flagged low usefulness + ignores institutional-memory risk)
# Consensus: false binary; run a cheap 2-week intercept/cold-start test to split writing(discoverability) vs culture(habit/trust); the right GOAL is "accurate answers fast without bottlenecks" not "read docs"; structural fix = wire docs into chat (answer-bot) + leaders model.
# DA = genuine minority counter (docs-nobody-reads is rational; make docs the EXHAUST of Q&A, not its competitor). Chairman can adopt the "docs-as-exhaust / answer-bot" without the full "kill most docs"; preserve the hard form as dissent.
# No council-breaking flag.
