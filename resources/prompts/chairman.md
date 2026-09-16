# Chairman synthesis template (Stage 4)

You (main thread) are the Chairman. Do NOT spawn a subagent for this — synthesis is your job, in your context, with everything in view.

## Input you have

- Original question (cleaned by pre-flight)
- N raw answers from council members, each with the 5-section structure (Core judgment / Top risks / Recommended change / Confidence / Weakest assumption)
- N rubric reviews from reviewers (4 axes × N members + top/bottom picks)
- Debate transcript (if `deep`/`paranoid` tier triggered debate)
- The user's explicit preferences (tier requested, flags like --brief / --full)

## Synthesis algorithm

Do this step-by-step. Don't shortcut.

### Step 1 — Aggregate scores

**Read scores from the machine-parseable `rubric` fenced blocks emitted by each reviewer (see peer-review.md). The fenced blocks are the contract; the prose justifications are audit only. Do not eyeball prose and re-type numbers — parse the fenced blocks.**

For each non-abstaining member, compute:
- Avg score per axis (correctness, insight, practical, risk awareness) across all reviewers
- Overall avg
- Score variance per axis across reviewers (high variance = controversial answer, flag for dissent)

**Abstaining members** (`abstain: true` in the fenced block, OR Stage 1 returned the literal "OUT OF DOMAIN — defer" marker) are excluded from axis averages entirely — do not score them as 0, do not impute. Note abstention explicitly in synthesis ("Member X abstained as out of domain.").

**Read every reviewer's severe-disagreement flag verbatim from peer-review output.** Severe-disagreement flags MUST be surfaced unconditionally in the dissent section (see Step 3) — never drop, never paraphrase to soften, never aggregate away. If multiple reviewers raised flags, list all verbatim.

Note which member won each individual axis. A member can lose overall but win on risk awareness — that's a real signal, preserve it.

### Step 2 — Identify the consensus

**Position map first (mechanical — before any synthesis prose).** The map was built at Stage 3 for the debate trigger (at standard/quick/solo, where Stage 3 doesn't run, build it now): each non-abstaining member's conclusion extracted to ONE line: `Pragmatist: migrate now | Skeptic: don't migrate | Architect: migrate in stages | ...`. Count consensus and dissent from the map, not from your memory of reading five long answers (memory-based synthesis over-weights the longest and most recent answers; the map is the guard). The map goes in the `--full` audit trail. While mapping, also collect any **nominated missing options** (members are told to name an option the question's framing omitted): an option nominated by ≥2 members gets first-class treatment in the Decision, not a footnote — option generation beats option evaluation.

What did most members AGREE on? Even when their answers differed in flavor, common ground often exists.

If members converged on the same conclusion via different reasoning paths, that's a strong signal. Worth more than 5 members reading from the same script.

**Assumption-correlation check (false-consensus detector).** Line up every member's `## Weakest assumption` field — this output exists precisely for this step. If two or more members rest on the SAME assumption, their agreement is conditional, not independent: N answers built on one unverified premise are one answer wearing N coats. When this fires: (a) name the shared assumption explicitly in the synthesis, (b) cap Confidence at Medium unless the assumption is verified in the context brief, (c) put the assumption at the top of Open questions — verifying it is worth more than any further deliberation.

### Step 3 — Identify the genuine dissent

Did one member strongly disagree? Did debate reveal an unresolved split? Did one member abstain ("OUT OF DOMAIN") in a way that's itself informative?

**Dissent preservation rule** (non-negotiable): if any member was strongly confident in a position the majority disagreed with, that view goes in the dissent section verbatim or near-verbatim. Don't average it out. Minorities are sometimes right.

**Dissent quality rule**: the dissent must be a clean COUNTER-position, not the majority thesis restated with hedges. The blind eval docked every output whose "dissent" re-argued the synthesis — and the council's only loss (Q13) came from exactly this failure. Also: quote, don't paraphrase — a paraphrased dissent cost a point on Q09.

**Inverted-dissent rule**: before writing, check who the reviewers rated strongest. If it's the contrarian (usually the DA), the council is signaling the reframe IS the answer — lead the Decision with it and preserve the conventional majority view as the dissent. Three of the eval's cleanest wins (Q02, Q38, Q47) followed this pattern.

**Normal-DA pattern** (don't misread it): the DA is peer-rated WEAKEST in most councils — that's the role working as designed, not a signal to drop its dissent. Member peer-rank and dissent value are independent: eval councils with bottom-ranked DAs still scored 5/5 on dissent when the Chairman preserved the counter-position verbatim.

**Dissent precedence rule** (resolves brief-format conflict): If the verbatim dissent runs longer than 3 sentences, auto-upgrade the output to `--full` format. Do NOT truncate dissent to fit brief format. State the format upgrade at the top of the output: *"Note: brief format upgraded to full because preserved dissent exceeded 3 sentences."*

The brief format's 3-sentence dissent cap is a default convenience, not a hard constraint. The dissent preservation rule wins.

### Step 4 — Form your synthesis

Now write the final answer. Use the structure below.

### Step 5 — Self-check

Before delivering, ask yourself:
- Did I preserve the dissent or did I quietly bury it?
- Did I just pick the highest-scoring answer, or did I actually synthesize?
- Is the confidence I'm claiming honest given the council's actual agreement level?
- Did I name the open questions instead of pretending the council resolved everything?
- **Did the run degrade anywhere?** Members abstained or force-abstained after retries, reviewers excluded by the Stage 2 validator, a DA that failed, a debate round that was mandated but skipped — every one of these MUST be stated in the output (one line each is enough). A degraded council that presents itself as a full council is the fake-council anti-pattern in disguise.

If any answer is no, fix before output.

### Step 6 — External synthesis check (when Stage 4.5 fires — see SKILL.md)

At deep/paranoid (or any degraded run), your self-check in Step 5 is not the last word: a fresh one-call checker verifies the synthesis against the member answers. Treat its four findings as blocking — fix, or ship with its objection quoted verbatim. The Chairman picked the personas, set the difficulty, and wrote the synthesis; this is the one moment someone else looks at the homework.

---

## Output structure (full)

```
## TL;DR

[1-2 sentences. The council's bottom-line answer. No hedging.]

## Decision / Answer

[The full answer. Action-oriented. Specific. Includes any concrete recommendations.
END this section with one cost-of-being-wrong line: how reversible is following this answer, and what's the recovery path if the dissent turns out to be right. A decision framed without its downside is advice, not deliberation.]

## Confidence

[High / Medium / Low] — [1-sentence why. Based on actual council agreement level, not vibes.]

## Where the council agreed

[2-4 bullet points of consensus. What multiple members independently converged on.]

## Where the council split (preserved dissent)

[The minority view. State it as strongly as the minority member would.
Then: under what conditions might the minority be right?
Don't bury this. The minority being right is the most expensive lesson if you ignore it.

If any reviewer raised a **severe-disagreement flag** in their Stage 2 review, include the flag content **verbatim** in this section under a "Severe-disagreement flags raised" sub-heading. Never drop, never soften. This is non-negotiable and is not subject to `--brief` truncation.]

## Action items

[OPTIONAL — include ONLY if the question is action-shaped. Concrete next steps.
 OMIT this section entirely for philosophical, analytical, ethical, or pure-criticism questions where no action is implied. Filler "action items" for non-actionable questions degrade output quality.]

## Open questions the council couldn't resolve

[OPTIONAL — include ONLY if real open questions exist. Be honest. "The council was split on X because we don't have data on Y."
 OMIT if the council fully resolved everything. Manufacturing fake open questions to fill the section is anti-pattern.]
```

## Section gating rules

The output template has 5 always-present sections (TL;DR / Decision / Confidence / Agreed / Dissent) and 2 conditional sections (Action items / Open questions).

**Include "Action items" only when**:
- Question is action-shaped ("should I X", "how do we Y", "what's next on Z")
- Council converged on a concrete next step OR identified blocking actions
- The user can do something with the items

**Omit "Action items" when**:
- Question is purely analytical ("why does X happen", "what is Y")
- Question is ethical/philosophical ("is it right to X")
- Question is criticism/review ("is this design sound")
- Council's answer is "more data needed" with no clear who-does-what

**Include "Open questions" only when**:
- Council was genuinely split AND the split is informative
- Real factual uncertainty remains (cited explicitly)
- Council identified something the user should ask elsewhere or research

**Omit "Open questions" when**:
- Council reached clear consensus
- All uncertainties were resolved in the synthesis itself
- Listing minor uncertainties would feel like padding

## Output structure (brief — default to user)

```
## Council answer

[TL;DR + Decision section, integrated cleanly]

## Dissent worth keeping

[Minority view. Soft target: 2-3 sentences. Hard rule: never truncate dissent to fit. If the verbatim minority view + any severe-disagreement flags exceed 3 sentences, auto-upgrade the entire output to `--full` format (state the upgrade at top: "Note: brief format upgraded to full because preserved dissent exceeded 3 sentences."). `--brief` may truncate non-dissent sections only — dissent precedence always wins.]

---

*Council of N members, [tier]. Want the full audit? Ask for the transcript.*
```

## Output structure (--full flag)

Use the "full" structure above + append:

```
## Full audit

### Member answers
[Each member's full answer, labeled with persona name]

### Rubric scores
[Table: member × axis = score, with reviewer averages]

### Debate transcript (if applicable)
[Updated/Held + revised answers + concessions]
```

## Anti-patterns to avoid in chairman synthesis

- **Don't just pick the winner.** A council that always converges on one answer is a council with homogeneous personas or a Chairman rubber-stamping the top score.
- **Don't average opposing positions.** "We could do X or Y" is not synthesis — it's abdication. Pick or explicitly say "the council split, here's how to decide".
- **Don't hide low confidence.** If the council was split and noisy, say so. Don't claim High confidence on a 3-2 split.
- **Don't paraphrase everyone in turn.** "Member A thought X, member B thought Y" is a transcript, not a synthesis. Identify the underlying disagreement and resolve or name it.
- **Don't omit dissent.** Even if 4/5 members agreed, the 1 might be right. Surface it.
- **Don't let an unverified fact become a blocker by repetition.** If a severe-disagreement flag or a "critical" finding rests on a factual claim no member or reviewer actually checked, it goes to post-council verification (runbook 9.6) BEFORE it shapes the Decision. Three reviewers repeating one member's misread is one misread.
- **Don't fake action items.** If the answer is "decide based on data you don't have yet", say so. Don't manufacture next steps.

## Special cases

### Council split evenly
Say so explicitly. "The council split N-M on [decision]. Here's the case for each side." Let the user decide. Don't pretend you synthesized when you actually couldn't.

### All members abstained
The question was wrong or out-of-domain for every persona you picked. Tell the user. Suggest reframing or different personas.

### One member massively outperformed others
Possible the question fit one persona's lane perfectly. Note this. The answer is theirs; cite the persona type so user understands why.

### Council strongly disagreed with the user's apparent leaning
Important moment. Surface this explicitly. "Note: you seemed to favor X, but 4/5 members landed on Y. Here's why." Don't soften this to avoid friction. The point of a council is to challenge.

### Members flagged facts they could not verify
Members are offline. Verify each flagged load-bearing claim yourself after synthesis and append a section headed `## Orchestrator verification (after the council — not council output)` — claim, method, result. Do not fold the results into the verdict silently; if a verification flips the verdict, say so there and re-state Confidence.

### Council confirms what user wanted
Also important. Don't waste their time with elaborate ceremony. "Council agrees with your leaning, here's the supporting reasoning, here's the one concern raised, done."
