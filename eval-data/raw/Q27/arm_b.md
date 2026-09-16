# Q27 Arm B raw output
# salvaged_from_context: false
# model: sonnet-4.6
# leakage_check: CLEAN — hardened anti-spawn wrapper held; STEP 1 stayed inside <thinking>; visible output = exactly 3 sections (Answer/Dissent/Confidence). No retry, no contamination.
# note: <thinking> block preserved here in raw; stripped during blinding.
# regenerated: 2026-05-29 (fresh full pipeline)

<thinking>
Let me work through five distinct perspectives on this question about benchmark contamination and credibility.

**Pragmatist perspective:**
The benchmark is contaminated enough to be meaningless as-is, but not necessarily fraudulent. The contamination comes from two main selection effects: (1) they chose the 14 tasks, meaning they almost certainly cherry-picked where their model shines, and (2) they funded the study, meaning there was pressure — conscious or not — to find favorable results. The practical question is: does any useful signal survive? Probably some. If their model genuinely outperforms on those 14 tasks, that's real performance. The problem is we have no base rate — we don't know how many tasks they tested total. If they tested 100 and published the 14 where they won, that's very different from if they tested 15. The simplest fix: require them to publish all task results and disclose the full experimental design up front, before running it.

**Skeptic perspective:**
This evidence is nearly worthless in its current form. "They chose the benchmark" is the original sin of AI evaluation. It's survivorship bias baked in by design. The Goodhart's Law problem applies at the meta level: once you're allowed to choose your own evaluation criteria, you're not measuring capability, you're measuring the ability to find favorable evaluation criteria. The funding bias compounds this — there's substantial literature on how industry-funded studies show systematically more favorable results than independent studies (a phenomenon documented extensively in pharma, and increasingly in AI). The 14-task framing obscures crucial information: what was the full task set? What's the confidence interval on each task? Were there any tasks where GPT-4 won? Without this, the benchmark is closer to marketing than science.

**Architect perspective:**
The structural problem here is that the entire ecosystem of AI benchmarking is broken in a way that makes individual contaminated benchmarks almost irrelevant — they're symptoms of a systemic failure. The real issue is that there's no separation of concerns between model developers and model evaluators. In clinical trials, we solved this with pre-registration, independent IRBs, and mandatory disclosure of negative results. AI needs equivalent institutions. A single company's benchmark is contaminated by design, not just by this particular company's choices. What would make it credible structurally: pre-registration of the benchmark before model development concludes (so they can't tune the model to the benchmark), third-party replication with access to the same model weights, and ideally participation in a neutral benchmark suite like HELM or BIG-bench rather than a proprietary one. The long-term fix is institutional: we need an independent AI evaluation body analogous to the FDA's advisory committees.

**Devil's Advocate perspective:**
The obvious answer is that this benchmark is heavily contaminated and unreliable. But let's argue the opposite: the benchmark might actually be more informative than a "neutral" one. Here's why. If a company knows their model inside out, they're better positioned to design tasks that reveal real capability differences — an external evaluator might design tasks that miss the actual capabilities entirely. The fact that they chose the benchmark is a feature if they chose it because they genuinely understand what their model is good at, and if their model's actual use cases align with those tasks. Cherry-picking is only a problem if the cherry-picked tasks don't correspond to real-world use. If the 14 tasks happen to be the tasks that matter most in practice, then outperforming on them is exactly the signal we want. The adversarial framing assumes bad faith; good faith self-evaluation with domain expertise can be more accurate than naive third-party testing. The question "what would make it credible" might have the answer: nothing, because credibility requires independence — but the practical question of usefulness is different from credibility.

**User Advocate perspective:**
As an actual user trying to decide which AI to use, this benchmark is close to useless and potentially harmful. The contamination isn't the main problem for me — the main problem is that the 14 tasks probably don't correspond to what I actually need to do. Even if the company ran this study perfectly, the fact that their model wins at "their" 14 tasks tells me almost nothing about whether it'll be better for my specific workflow. What I actually want is: performance on tasks I specifically care about (which means I need to be able to specify them), cost per task, latency, reliability, safety alignment, and whether the model's failure modes are tolerable. A contaminated benchmark that's also irrelevant to my use case is doubly useless. What would make it credible for me specifically: let me run my own evaluation on a sample of my actual tasks. The best thing companies could do is provide evaluation APIs and let users run their own benchmarks. The company-level benchmark is a marketing artifact regardless of methodology — users need personal benchmarking tools.
</thinking>

## Answer

The evidence is severely contaminated — enough that no confident comparative claim about general model quality can be drawn from it. Contamination operates on two axes simultaneously.

**Task selection bias** is the primary problem. "They chose the benchmark" hides a crucial unknown: the denominator. If the company tested 14 tasks and published 14, that is a different situation from testing 100 tasks and publishing the 14 where they won. Without the full experimental record, you cannot distinguish genuine capability from selection effects. This is survivorship bias baked in by design — the moment you allow a party to choose its own evaluation criteria, you are measuring their ability to find favorable criteria at least as much as you are measuring model quality.

**Funding bias** compounds this. The literature on industry-funded research in pharma, nutrition, and increasingly AI is consistent: funded studies produce systematically more favorable results, not necessarily through fraud, but through thousands of small decisions — what to control for, how to define success, what to report — that accumulate in the funder's favor. The bias is often not conscious.

A third contamination layer is **benchmark overfitting**: if the model was tuned or evaluated internally against similar tasks during development, the benchmark is not measuring held-out generalization, it is measuring in-distribution performance — which tells you almost nothing about real-world deployment.

What would make it credible, in order of importance:

1. **Pre-registration** of the full benchmark specification before model training or fine-tuning concludes — so the model cannot be tuned to the benchmark.
2. **Full disclosure of all tasks tested**, not just the wins. If they tested 14 tasks and all 14 are in the paper, that is stated explicitly. If they tested more, all results must be published.
3. **Third-party independent replication** with full API access or model weights, run by researchers with no financial stake.
4. **Neutral multi-model benchmarks** (HELM, BIG-Bench Hard, MMLU variants administered by independent parties) run in parallel so the results can be contextualized against a shared reference.
5. **Dataset contamination audits** confirming the test set does not overlap with the model's training data.
6. Confidence intervals on each of the 14 tasks, not just win/loss framing.

The absence of any of these does not prove fraud. It proves the evidence cannot carry the weight being placed on it.

---

## Dissent worth keeping

*"The independence requirement here might actually be counterproductive. A company that knows their model inside out is better positioned to design tasks that reveal real capability differences than a neutral external party who designs tasks that systematically miss what the model actually does well. Cherry-picking is only harmful if the cherry-picked tasks don't correspond to real-world use — but if those 14 tasks happen to be the tasks that genuinely matter in practice, outperforming on them is exactly the signal you want. The adversarial framing of self-evaluation assumes bad faith; domain-expert self-evaluation can be more accurate than naive third-party testing. We should be asking whether the tasks are ecologically valid, not just who designed them."*

---

## Confidence

**Medium.** The five perspectives converged strongly on "high contamination," but diverged meaningfully on whether any useful signal survives and on whether the remedy is primarily institutional (independent evaluation bodies) or task-level (ecological validity of the chosen tasks) — which leaves the prescription less settled than the diagnosis.
