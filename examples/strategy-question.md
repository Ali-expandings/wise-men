# Example: strategy question — "Product Hunt or Reddit first?"

An illustrative scenario, not a captured run: the project, its bugs and the answers are constructed to show the flow for a non-engineering question. Every fact the members use is in the user's input or the context brief; anything else is marked unverified, as the protocol requires.

## User input

> I'm launching Lumen (open-source AI chat shell for local models). Should I post to Product Hunt or Reddit first? I only get one good first impression on each. Known state: two visible bugs (voice input is broken in one browser; one model backend hangs), and I have no demo video yet. No deadline.

## Pre-flight

- Question: clear. Decision point: PH first vs Reddit first.
- Single question.
- Context: open-source, AI category, one-shot framing, two known bugs, no video, no deadline. Enough.
- Council-shaped: yes (a real strategic decision with a hard-to-repeat first impression).
- Domain: product / strategy (with marketing flavor).
- Tier: standard (depth 3, stakes 3, novelty 2).
- Members: Practitioner (a developer-relations lead who has run open-source launches — the anchor, strong model) + User Advocate + Business Analyst + Historian + Devil's Advocate (5). The anchor replaced the Designer, the roster seat it overlapped most.
- Expected calls: 9 (5 members + 3 reviewers + 1 synthesis checker).

Note: not using Pragmatist/Skeptic/Architect because this isn't a code question. Persona selection matched to domain.

## Stage 0.5 — context brief (identical for every member)

Facts supplied by the user: open-source chat shell for local models; two visible bugs (voice input in one browser, one backend hang); no demo video; no deadline; wants one strong first impression per venue. Not known: current posting rules of any subreddit or of Product Hunt, the size of any existing community, how hard the bugs are. Nothing here was checked against an outside source.

## Stage 1 — outputs (compressed)

**Practitioner** (med conf): "Order of work: fix or hide the two bugs, write a five-line README opener, then post where the users already are. Must-check facts before acting: the target subreddit's self-promotion rules and whether Product Hunt still favours launches with a video (both unverified — rules change). The question also asks about Product Hunt: keep it, but second, once there is something to show. Weakest assumption: that the bugs take days, not weeks."

**User Advocate** (med conf): "Reddit readers want substance and technical detail; Product Hunt readers want polish. Lumen leans technical, so Reddit will engage more. Launching now is fine: open-source users file issues, they don't leave. Weakest assumption: that the bugs are tolerable on first contact."

**Business Analyst** (med conf): "PH is a one-day spike plus a permanent page; a Reddit thread in the right community keeps drawing search traffic (typical pattern, unverified). With no monetization pressure and no deadline, the slower curve costs nothing. Weakest assumption: that a fitting subreddit allows the post at all."

**Historian** (med conf): "Typical pattern, not a statistic I can cite (unverified): open-source tools that arrive on Product Hunt with no community behind them get few votes on day one, and the listing cannot be relaunched. Communities of local-model users exist on Reddit. Weakest assumption: that Lumen resembles those cases."

**Devil's Advocate** (med conf): "Don't post to either yet. The user's own framing — one good first impression — argues against launching a tool with two visible bugs and no video. Fix them, then choose a venue with evidence instead of a guess. Weakest assumption: that waiting costs nothing; no deadline was given, but momentum is real."

## Stage 2 — peer review summary (3 reviewers)

```
                 | Correct | Insight | Practical | Risk-aware | Avg
Practitioner     |   4.7   |   3.7   |    4.7    |    4.0     | 4.3
User Advocate    |   3.3   |   3.3   |    4.0    |    3.0     | 3.4
Business Analyst |   4.0   |   3.7   |    3.3    |    3.3     | 3.6
Historian        |   4.0   |   3.3   |    3.7    |    3.3     | 3.6
Devil's Advocate |   4.0   |   4.7   |    4.0    |    4.7     | 4.4
```

Severe-disagreement flag (from one reviewer): "User Advocate and Devil's Advocate fundamentally disagree on whether to launch now."

## Stage 3 — skipped (standard tier)

The User-Advocate-vs-DA split would have triggered a debate round at `deep` tier — at `standard`, debate is skipped by design and the split goes into the counter-position instead.

## Stage 4 — Chairman synthesis (first draft), then Stage 4.5

The checker returned five PASS and one FAIL — CLAIMS: the draft said "put the link in the first comment so automod doesn't catch it", a claim about a community's rules that is in no brief and carried no unverified mark. Fixed: replaced by "check the subreddit's posting rules first". The memo below is the checked version.

```
## Recommendation

Fix the two visible bugs first (give it one week), then launch on Reddit, in the community where local-model users already are; take it to Product Hunt afterwards, once there is a demo video and some traction to show.

## Why

- You said you get one good first impression per venue, and you described two bugs a first-time user would hit. Those two facts together decide the order.
- A technical audience rewards substance over polish, which suits an open-source tool without a video.
- Product Hunt listings can't be relaunched, and tools arriving there with no community behind them tend to get few votes (typical pattern, unverified — check recent launches in your category).
- There is no deadline, so a week costs little.

## What to do

1. This week: fix or disable the two broken paths (voice input in that browser, the hanging backend). If one proves hard, ship with it switched off and say so in the README.
2. Rewrite the README opener: five lines, what it does, how to run it.
3. Before posting, read the target subreddit's self-promotion rules (unverified here — they change) and follow them.
4. Post within 7 days of the fix. Stop and rethink if the bugs take more than two weeks: at that point the question is scope, not venue.
5. Product Hunt: after the video exists and the Reddit thread has shown what people ask about.

## Risks of this plan

- A week can become a month; the step-4 limit exists for that.
- Technical communities are harsh on tools that don't work on first run: launching with the bugs live would cost more there than on Product Hunt.
- The subreddit may not allow the post; step 3 finds that out before it matters.
- Severe-disagreement flag: "the case for launching now and the case for fixing first fundamentally disagree on whether to launch now."
- Cost of being wrong: moderate and mostly one-way — a bad first thread is hard to repeat, which is why the fix week comes first. If the counter-position is right, you lose a week.

## Strongest counter-position

The case for launching now: "Open-source users file issues, they don't leave." A week of polish is a guess about what strangers will care about; the fastest way to learn which bug matters is to let them hit it, and a maintainer who answers issues within hours makes a better first impression than a silent, polished repo. This wins if the bugs sit in paths most users never touch (voice input, one backend) — check your own usage before deciding.

## Confidence

High that Reddit comes before Product Hunt given no video and no community yet — it follows from your own constraints. Medium that fixing first beats launching now: it turns on how visible the two bugs are, which only you can see. Low on anything about either venue's current rules or algorithms: nothing here was checked against them.
```

## What to send to user

The memo above. A long counter-position never changes the format, and the reviewer's severe-disagreement flag sits under Risks with the member names replaced by the positions they hold; the verbatim flag, the scores, the member answers and the checker's finding stay in the council record.

## What was good about this run

- **Domain-matched personas**: a launch practitioner, User Advocate, Business Analyst and Historian instead of engineering personas. Without this, the council would have answered the wrong question.
- **No invented facts**: the bugs and the missing video came from the user; the Historian offered its precedent as a typical pattern marked unverified rather than a statistic, and the checker caught the one unmarked claim before the user saw it.
- **The counter-position argues against the recommendation** (launch now), instead of restating "fix first" with hedges.
- **The practitioner anchor supplied the must-check facts** (posting rules, video expectations) that turned a venue opinion into a plan.
- **The Chairman didn't just say "Reddit"** — it sequenced both venues and set a stop condition.

## Adaptive note

Same skill, completely different persona mix from the coding example. That's the design. Persona auto-selection by domain is what makes this skill work across cases, not just for engineering.
