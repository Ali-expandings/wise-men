# Q33 Arm B raw output
# salvaged_from_context: false
# model: sonnet-4.6
# leakage_check: CLEAN — hardened anti-spawn wrapper held; STEP 1 stayed inside <thinking>; visible output = exactly 3 sections (Answer/Dissent/Confidence). No retry, no contamination. (subagent reported tool_uses internally but emitted no tool calls in output; visible text clean.)
# note: <thinking> block preserved here in raw; stripped during blinding.
# regenerated: 2026-05-29 (fresh full pipeline)

<thinking>
Let me work through the five perspectives carefully before synthesizing.

---

**Pragmatist:**
The simplest diagnostic is to run a single test: the next time someone asks a question that's answered in the docs, stop and ask them "Did you check the docs first?" If they say yes and couldn't find it, that's a writing/discoverability problem. If they say no or "I didn't think to," that's culture. You don't need a survey or a culture audit. You need to intercept five live incidents and categorize the reason. That's the fastest signal available. The solution that works quickest is also simple: for every question asked that has a doc answer, respond with the link before answering the question. Do this consistently for a few weeks. If question volume drops, the docs were fine and the habit just didn't exist. If people still ask despite being pointed there repeatedly, the docs may be genuinely hard to use even when you get there.

---

**Skeptic:**
The premise that the docs are "well-organized and accurate" is unverified. The person asking this question is almost certainly the person who wrote or manages the docs — they have an insider's map and can't see the docs the way a newcomer does. What feels well-organized to the author often fails the "cold start" test: can someone who doesn't already know the answer navigate to it without already knowing where to look? The framing of "writing vs culture" is also a false binary — it's probably both, and separating them may be a way to avoid confronting one uncomfortable possibility: that the docs are harder to use than the author believes. The real test is to ask a new team member to find the answer to a specific question using only the docs, while you watch silently. Don't help. See how long it takes. That's the truth.

---

**Architect:**
Long-term, the distinction matters enormously because the interventions are entirely different. If it's a writing problem (discoverability, search, structure, cold-start UX), you solve it with information architecture work: better titles, better search, contextual linking from tools/Slack/code to docs, and progressive disclosure. If it's a culture problem (learned helplessness, it's faster to ask a person, nobody modeled the behavior, docs aren't trusted to be current), you solve it with social and process changes: leadership modeling, onboarding requirements, making "ask without checking" mildly friction-ful. The reason to diagnose correctly is that applying the wrong fix wastes significant effort. Teams often improve the docs endlessly when the real problem is culture, which means the docs get better and usage stays flat. The structural signal to look for: if people don't consult docs even when the doc is linked directly in the Slack thread, it's culture. If they try but fail to find things, it's writing.

---

**Devil's Advocate:**
The obvious answer here is "it's a culture problem, fix the culture," but that's wrong — or at least it's almost always used as a way to blame the users rather than the system. The blunt truth is: internal documentation almost always fails because it's optimized for the writer, not the reader. "Well-organized and accurate" describes a filing cabinet, not a communication tool. People don't consult docs because docs don't meet people where they are. They require context-switching, knowing what to search for, and trusting that the answer is actually there. The fact that it's "accurate and organized" and still ignored is strong evidence that the format, discoverability, and integration into actual workflow are broken. Calling this a culture problem lets the docs off the hook. Nobody has a culture problem reading Stack Overflow answers that directly solve their problem. The bar for internal docs is just lower quality than alternatives, so people rationally route around them.

---

**User Advocate:**
From the actual end user's perspective, the real question is: what does it cost me to consult the docs vs. to ask a person? If the honest answer is "asking a person is faster, more reliable, and more pleasant," then the docs are failing on user experience grounds regardless of their quality. Users aren't irrational — they're optimizing for the outcome they need. If the docs are indexed poorly in Slack search, if opening them requires leaving the flow of work, if the last time they tried the docs were stale, they built a mental model of "docs aren't reliable" and updated it rarely. The emotional dimension matters too: asking a person feels collaborative and low-risk; consulting docs alone can feel like you might miss something or go down a wrong path. To diagnose this, you need to ask users directly: "Why didn't you check the docs?" — not in an accusatory way, but genuinely, and the answer will tell you whether it's a trust problem, a discoverability problem, or a habit problem. Those are three different things.
</thinking>

## Answer

It is almost certainly both, but the interventions are completely different, so you need to distinguish them rather than treat them as equivalent.

The fastest diagnostic is to intercept live incidents rather than theorize. The next time someone asks a question that has a documented answer, stop and ask them directly: "Did you check the docs first?" Their answer sorts the problem immediately. If they say yes and couldn't find it — or found something outdated — that is a writing, structure, or discoverability problem. If they say no, or "I didn't think to," or "it's faster to just ask," that is a culture and workflow-integration problem.

Run that on five or ten incidents and you will have your answer more reliably than any survey.

A second diagnostic is a cold-start usability test: ask a team member who didn't write the docs to find the answer to a specific question using only the documentation, while you watch silently. Don't help. Time them. Note where they get confused or give up. This surfaces whether "well-organized and accurate" is true from a reader's perspective, or only from the author's. These often diverge significantly — what feels organized to someone who knows the answer is frequently unnavigable to someone who doesn't.

The structural tells to watch for:
- If people are pointed directly to a doc link in Slack and still don't read it before replying with follow-up questions, that is culture — the doc was accessible and they still skipped it.
- If people try the docs but search fails them, or they land on the right page and still can't find the answer, that is an information architecture and writing problem.
- If the docs are rarely opened even during onboarding, when new people have the strongest incentive to self-serve, that is a trust and integration problem — people learned early that asking is more reliable.

The culture fix (if needed) is primarily social: every time a question is answered that has a doc, respond with the link before or alongside the answer, consistently, without shaming. After a few weeks of that, if volume drops, the docs were fine and the habit just hadn't formed. If volume stays flat despite everyone being pointed to docs regularly, either the docs aren't actually solving the user's need when they get there, or the workflow cost of leaving Slack to read them is too high.

The writing fix (if needed) is integration and discoverability, not reorganization: contextual links from Slack, from the codebase, from onboarding checklists; better search titles; shorter answers at the top with detail below. The problem with most internal docs that go unread is not that they lack information, it is that they require the reader to already know what to look for.

## Dissent worth keeping

Calling this a culture problem lets the docs off the hook. Nobody has a culture problem reading Stack Overflow answers that directly solve their problem. The bar for internal docs is just that they are lower quality than the alternatives — less reliable, harder to navigate, requiring more effort for the same outcome — so people rationally route around them. "Well-organized and accurate" is the author's assessment, not the user's, and those almost never agree. Fix the product before blaming the users.

## Confidence

Medium — the five perspectives agreed strongly on the diagnostic method and on the false-binary framing, but diverged meaningfully on whether writing quality or culture deserves more weight as the root cause, which reflects a genuine empirical uncertainty that only your specific team's data can resolve.
