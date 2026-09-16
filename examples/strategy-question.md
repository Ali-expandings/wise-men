# Example: strategy question — "Product Hunt or Reddit first?"

A worked end-to-end run for a non-engineering question. Shows domain adaptation.

## User input

> I'm launching Lumen (open-source AI chat shell). Should I post to Product Hunt or Reddit first? Only get one good first impression on each.

## Pre-flight

- Question: clear. Decision point: PH first vs Reddit first.
- Single question.
- Context: open-source, AI category, only-one-shot framing. Enough.
- Council-shaped: yes (real strategic decision, irreversible-ish first-impression framing).
- Domain: product / strategy (with marketing flavor).
- Tier: standard.
- Members: User Advocate + Business Analyst + Historian + Devil's Advocate + Designer (5).
- Expected calls: 8 (5 members + 3 reviewers).

Note: not using Pragmatist/Skeptic/Architect because this isn't a code question. Persona selection matched to domain.

## Stage 1 — outputs (compressed)

**User Advocate** (med conf): "Reddit users want substance + technical specificity. PH users want polish + product-market vibe. Lumen leans technical → Reddit audience will engage more meaningfully. PH first risks looking like 'another AI wrapper' to a fatigued audience. Confidence: medium. Weakest assumption: that Lumen's polish level matches Reddit's tolerance for 'just works' over 'beautiful demo'."

**Business Analyst** (med conf): "PH gives 1-day visibility spike + permanent searchable page. Reddit gives sub-specific traffic that compounds (search hits for the tool's niche compound for months). Reddit has higher cost-per-post (effort to match sub culture) but higher retention of qualified users. PH = quick burst; Reddit = compounding curve. For open-source with no monetization pressure, Reddit's curve wins. Confidence: medium."

**Historian** (high conf): "Pattern: 90% of dev-tool open-source projects that launched on PH and were under-engineered for the moment lost the chance permanently. Reddit (r/LocalLLaMA specifically) is the actual home of local-model users. Examples: ollama launched on r/MachineLearning first → built momentum → then crossposted. Open-source AI tools that PH-first without an existing community usually flop on PH (no votes from cold start). Confidence: high. Weakest assumption: that Lumen is comparable to those reference cases."

**Devil's Advocate** (med conf): "Counter-take: don't post to either yet. Both audiences smell hype. Lumen has two visible bugs (voice input broken on one browser; one model backend hangs). Launching now = first impression is a half-working tool. Wait two weeks, fix the visible bugs, write a real README, then pick one launch venue with confidence. The 'only one good first impression' framing is true — which means rushing it is the worst move. Confidence: medium. Weakest assumption: that user can wait two weeks (no time pressure mentioned, but...)."

**Designer** (low conf): "Visually: Lumen screenshots well in dark mode. Either platform will work visually. But: PH demands a video demo or it's invisible. Reddit doesn't. If you don't have a 30-sec demo recording, that's a Reddit signal, not PH. Confidence: low (haven't seen the actual screenshots/repo). Weakest assumption: that screenshot quality is decent."

## Stage 2 — peer review summary

Aggregated scores:

```
                 | Correct | Insight | Practical | Risk-aware | Avg
User Advocate    |   3     |   3     |    4      |    3       | 3.25
Business Analyst |   4     |   4     |    3      |    3       | 3.5
Historian        |   5     |   4     |    4      |    3       | 4.0
Devil's Advocate |   4     |   5     |    4      |    5       | 4.5
Designer         |   3     |   2     |    3      |    3       | 2.75
```

Top: Devil's Advocate (3 votes — "raises the strongest hidden assumption").
Bottom: Designer (low signal due to admitted low confidence).

Severe-disagreement flag (from one reviewer): "User Advocate and Devil's Advocate fundamentally disagree on whether to launch now."

## Stage 3 — skipped (standard tier)

The severe-disagreement flag and the User-Advocate-vs-DA split would have triggered a debate round at `deep` tier — at `standard`, debate is skipped by design and the split flows into the dissent section instead.

## Stage 4 — Chairman synthesis

```
Note: brief format upgraded to full because preserved dissent exceeded 3 sentences.

## Council answer

Reddit first — specifically r/LocalLLaMA — but only after a 1-week fix pass on the visible bugs.
Two-week wait isn't necessary. One week is.

Why Reddit:
- Audience is exactly the local-model users you need
- Compounding search traffic over weeks vs one-day PH burst
- Open-source AI tools historically struggle on PH without an existing community
- No video demo required (you don't have one)

Why the 1-week wait:
- Fix the voice-input bug or document it as a known issue
- Get the backend hang into a state where users won't hit it cold
- Write a 5-line README opener that's not generic-AI-tone

After Reddit lands, repost to PH 2-3 weeks later with "as seen on r/LocalLLaMA" social proof.
That sequence beats either-platform-first.

## Dissent worth keeping

The Devil's Advocate position is the most important dissent here: launching with visible bugs damages
the only-one-first-impression more than waiting damages momentum. If after 1 week the voice-input bug isn't
fixed and the backend is still flaky, push another week. The framing the user gave themselves ("only one good
first impression") is true — honor it.

The User Advocate's worry about Reddit's "just works" tolerance is also worth holding: if the bugs
aren't fixed, Reddit will be brutal in a way PH wouldn't be. Reddit-first only works if the bugs are
addressed.

### Severe-disagreement flags raised

> "User Advocate and Devil's Advocate fundamentally disagree on whether to launch now." (reviewer 3, verbatim)

## Confidence

Medium-high. Council converged on Reddit-first (4/5), and converged on "fix bugs first" (4/5).
Disagreed only on how long to wait (1 vs 2 weeks).

## Action items

1. Decide which bug to fix: voice input OR the backend hang. Probably the one easier to fix.
2. Rewrite README opener (5 lines, no marketing tone — see humanizer skill)
3. Draft r/LocalLLaMA post + drop link in first comment (avoids automod)
4. Set 7-day deadline for posting

## Open questions the council couldn't resolve

- Is the visual polish actually good enough? (Designer flagged low confidence due to not seeing it.)
  Would benefit from a separate UI review pass before launch.
```

## What to send to user

This run auto-upgraded to full format: the preserved dissent runs past 3 sentences and a severe-disagreement flag was raised, and dissent precedence forbids truncating either. On a run with short dissent and no flags, the brief format (Council answer + Dissent + Confidence) would go out instead.

## What was good about this run

- **Domain-matched personas**: User Advocate / Business Analyst / Historian / Designer instead of engineering personas. Without this, council would've answered the wrong question.
- **Historian provided concrete precedent reasoning** (ollama, dev-tool launch patterns) that elevated the answer beyond opinion.
- **Devil's Advocate caught the "don't launch yet" angle** that none of the others raised — and Chairman correctly preserved it as load-bearing dissent.
- **Designer's low-confidence answer wasn't punished** in aggregation — it just got noted. Allowing abstain/low-confidence prevents forcing bad signal.
- **Chairman didn't just say "Reddit"** — synthesized a sequenced plan that incorporated the dissent's core concern.

## Adaptive note

Same skill, completely different persona mix from the coding example. That's the design. Persona auto-selection by domain is what makes this skill work across cases, not just for engineering.
