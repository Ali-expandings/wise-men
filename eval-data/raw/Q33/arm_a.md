# Q33 Arm A raw output
# salvaged_from_context: false
# model: sonnet-4.6
# skill_suppression: applied
# contamination: none
# regenerated: 2026-05-29 (fresh full pipeline)

This is almost certainly a culture problem wearing a writing problem's clothes, but the distinction matters less than most people think — and the way to tell is by running a small experiment rather than by analyzing the docs themselves.

Here's the core diagnostic: take your three most frequently asked questions from the past month, find the doc that answers each one, and measure how many clicks it takes a new person to get from "I have this question" to "I found the answer." If the answer is more than two clicks, or if the person would need to already know what the doc is called in order to find it, you have a discoverability problem, which is a writing/structure problem. If the answer is one click and the doc is clearly written but people still ask the question, that's a culture problem.

The reason most people misdiagnose this is that they evaluate docs by how good they look when you already know where they are. That's not the user experience. The actual user experience starts with a vague feeling of uncertainty, a quick mental check of "where would I even look for this," and then a decision about whether asking a person is faster than searching. If asking a person has ever worked and taken under thirty seconds, that pathway is reinforced, and no amount of documentation quality changes the calculus.

The honest signs that it's primarily a culture problem: people who wrote the docs also don't consult them and go straight to asking; senior people on your team visibly model the behavior of answering questions from memory rather than linking to docs; there's mild social reward for being the person who knows things, and no social friction for asking questions that are already documented. These are behavioral norms, and they don't respond to better writing.

The honest signs it's primarily a writing/structure problem: your docs are organized around how your team thinks about the system rather than how someone with a question thinks about it; docs are titled with internal jargon that doesn't match how people phrase questions; there's no single obvious starting point, so people face a whole wiki with no clear entry path; and search returns too many results or the wrong ones.

In practice, most teams have both, in roughly this proportion: 30% writing and 40% culture and 30% discoverability. The discoverability piece often gets ignored because it falls between the two — it's not exactly a writing quality issue and it's not exactly a norms issue, but it's actually the cheapest to fix. A well-placed link in a Slack channel description, a pinned message, a simple search alias, or a bot that auto-responds to common questions with doc links can move the needle on discoverability in a day.

The culture piece takes longer and requires modeling from whoever has the most social authority on the team. That person needs to start responding to questions with "great question, the answer is in [link]" rather than just answering, and they need to do it without being condescending about it, which is genuinely hard. Over a few months, people learn that consulting docs is the faster path.

So: look at discoverability first because it's the easiest to fix and will give you a quick signal. If fixing discoverability doesn't move behavior after three or four weeks, you're looking at culture, and you need to change what gets modeled and socially rewarded rather than what gets written.
