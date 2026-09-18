#!/usr/bin/env python3
"""Head-to-head round 3 (PREREG-3.md): save <agent-transcript> <arm> <Q> <tokens> <tools> <seconds> | blind <Q> | parse <Q> | report | results.
Run from the repo root. Rounds 1-2 live in h2h.py and are untouched."""
import os, re, sys, json, glob, random, statistics as st, yaml
from decimal import Decimal, ROUND_HALF_UP
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(H))
sys.path.insert(0, H)
from h2h import normalize, qtext  # the same normalization rules as rounds 1-2

AXES = ["correctness", "insight", "practical", "risk", "dissent"]
PART_A = ["Q05", "Q09", "Q13", "Q19", "Q25", "Q36", "Q48", "Q55"]
PART_B = ["Q23", "Q32", "Q43", "Q51"]
A_ARMS = ["wise-men-3.11", "wise-men", "warp-council", "llm-council", "lifeos-council", "ecc-council", "brainstorming", "grilling", "direct"]
B_ARMS = ["wise-men-3.11", "warp-council", "llm-council", "direct"]
JUDGES = ["j1", "j2", "j3"]
NAMES = {"wise-men-3.11": "wise-men 3.11.0", "wise-men": "wise-men 3.9.2", "warp-council": "Warp council", "llm-council": "llm-council", "lifeos-council": "LifeOS Council",
         "ecc-council": "ECC council", "brainstorming": "brainstorming", "grilling": "grilling", "direct": "plain answer"}
BLIND = yaml.safe_load(open(os.path.join(H, "blinding3.yaml")))["map"]

def arms_for(q): return A_ARMS if q in PART_A else B_ARMS
def r1(x): return str(Decimal(str(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))
def r2(x): return str(Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP))

def final_text(jsonl):
    rows = [json.loads(l) for l in open(jsonl)]
    last_user = max(i for i, r in enumerate(rows) if r.get("type") == "user")
    return "\n".join(c["text"] for r in rows[last_user + 1:] if r.get("type") == "assistant" for c in r["message"]["content"] if c.get("type") == "text").strip()

HEAD = {"wise-men-3.11": "wise-men-3.11 (SKILL.md v3.11.0, commit 1e32841)", "warp-council": "warp-council (warpdotdev/common-skills 69b4753651ab)",
        "llm-council": "llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94)", "direct": "direct (no skill)"}
NOTE = {"warp-council": "# adaptation: Claude Code subagents instead of run_agents; Claude models only; no approval wait — see PREREG-2.md\n"}

def transcript_stats(jsonl):
    from datetime import datetime
    rows = [json.loads(l) for l in open(jsonl)]; ts = [r["timestamp"] for r in rows if r.get("timestamp")]
    t0, t1 = (datetime.fromisoformat(x.replace("Z", "+00:00")) for x in (ts[0], ts[-1]))
    tools = sum(1 for r in rows if r.get("type") == "assistant" for c in r["message"]["content"] if c.get("type") == "tool_use")
    return tools, int((t1 - t0).total_seconds())

def save(transcript, arm, q, tokens, tools, seconds, note=""):
    if tools == "auto" or seconds == "auto": tools, seconds = transcript_stats(transcript)
    txt = final_text(transcript); redacted = re.sub(r"\bAli\b", "the user", txt)
    head = f"# arm: {HEAD[arm]} | question: {q} | orchestrator: general-purpose/sonnet | run: 2026-09-17 (round 3, PREREG-3 rules)\n" + NOTE.get(arm, "")
    head += f"# subagent tokens: {tokens} | tool uses: {tools} | duration: {seconds}s\n"
    if note: head += f"# note: {note}\n"
    if redacted != txt: head += "# note: the author's first name (inherited from global config) redacted to \"the user\" per PREREG-3\n"
    os.makedirs(os.path.join(H, "raw", q), exist_ok=True)
    open(os.path.join(H, "raw", q, arm + ".md"), "w").write(head + "\n" + redacted + "\n")
    print("saved", q, arm, len(redacted.split()), "words", "(redacted)" if redacted != txt else "")

def savejudge(agent_transcript, q, j):
    os.makedirs(os.path.join(H, "judgments-v3"), exist_ok=True); t = final_text(agent_transcript)
    open(os.path.join(H, "judgments-v3", f"{q}-{j}.md"), "w").write(f"# judge: fresh opus subagent, no skills, Read-only | question: {q} | judge: {j} | run: 2026-09-17 (round 3)\n# blinded input: blinded-v3/{q}-{j}.md (slots per blinding3.yaml)\n\n{t}\n")
    got = {}
    for b in re.findall(r"```scores\n(.*?)```", t, re.S):
        d = dict(re.findall(r"(\w+):\s*([A-I]|\d)", b)); got[BLIND[q][j][d["response"]]] = sum(int(d[a]) for a in AXES)
    assert set(got) == set(arms_for(q)), (q, j, set(arms_for(q)) - set(got))
    print("judgment", q, j, dict(sorted(got.items(), key=lambda x: -x[1])))

def blind(q):
    tpl = open(os.path.join(H, "judge-prompt-9.txt" if q in PART_A else "judge-prompt-4.txt")).read()
    os.makedirs(os.path.join(H, "blinded-v3"), exist_ok=True)
    for j in JUDGES:
        parts = []
        for slot, arm in BLIND[q][j].items():
            raw = open(os.path.join(H, "raw", q, arm + ".md")).read()
            parts.append(f'Response {slot}:\n"""\n{normalize("wise-men" if arm.startswith("wise-men") else arm, raw)}\n"""\n')
        out = tpl.replace("{question}", qtext(q)).replace("{responses}", "\n".join(parts))
        open(os.path.join(H, "blinded-v3", f"{q}-{j}.md"), "w").write(out)
    print("blinded", q, "x3")

def parse(q):
    os.makedirs(os.path.join(H, "parsed-v3"), exist_ok=True); arms = arms_for(q); out = {}
    for j in JUDGES:
        text = open(os.path.join(H, "judgments-v3", f"{q}-{j}.md")).read(); got = {}
        for b in re.findall(r"```scores\n(.*?)```", text, re.S):
            d = dict(re.findall(r"(\w+):\s*([A-I]|\d)", b)); arm = BLIND[q][j][d["response"]]
            got[arm] = {a: int(d[a]) for a in AXES}; got[arm]["composite"] = sum(got[arm][a] for a in AXES)
        assert set(got) == set(arms), (q, j, set(arms) - set(got))
        out[j] = got
    yaml.safe_dump({"question_id": q, "judges": out}, open(os.path.join(H, "parsed-v3", q + ".yaml"), "w"), sort_keys=False)
    print("parsed", q, {a: r2(st.mean(out[j][a]["composite"] for j in JUDGES)) for a in arms})

def load():
    R = {}
    for f in sorted(glob.glob(os.path.join(H, "parsed-v3", "Q*.yaml"))):
        d = yaml.safe_load(open(f)); q = d["question_id"]
        R[q] = {a: {k: st.mean(d["judges"][j][a][k] for j in JUDGES) for k in AXES + ["composite"]} for a in arms_for(q)}
        R[q]["_sd"] = {a: st.pstdev([d["judges"][j][a]["composite"] for j in JUDGES]) for a in arms_for(q)}
    return R

def boot(diffs, seed=20260918, n=10000):
    rng = random.Random(seed); k = len(diffs)
    means = sorted(st.mean(rng.choice(diffs) for _ in range(k)) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]

def compare(R, qs, a, b="wise-men-3.11"):
    d = [R[q][b]["composite"] - R[q][a]["composite"] for q in qs]
    lo, hi = boot(d); w = sum(x > 0 for x in d); t = sum(x == 0 for x in d); l = sum(x < 0 for x in d)
    word = "clearly ahead" if lo > 0 else ("ahead" if st.mean(d) > 0 else ("level" if st.mean(d) == 0 else "behind"))
    return {"diff": st.mean(d), "lo": lo, "hi": hi, "w": w, "t": t, "l": l, "n": len(d), "word": word}

def table(R, qs, arms):
    return {a: {"mean": st.mean(R[q][a]["composite"] for q in qs), "axes": {x: st.mean(R[q][a][x] for q in qs) for x in AXES}} for a in arms}

def report():
    R = load(); A = [q for q in PART_A if q in R]; B = [q for q in PART_B if q in R]; AB = A + B
    for label, qs, arms in (("Part A (round-2 questions)", A, A_ARMS), ("Part B (held-out questions)", B, B_ARMS), ("All 12 (arms in both parts)", AB, B_ARMS)):
        if not qs: continue
        T = table(R, qs, arms); print(f"\n{label}: N={len(qs)}")
        print(f"{'arm':16}" + "".join(f"{x[:5]:>7}" for x in AXES) + "   total")
        for a in sorted(arms, key=lambda a: -T[a]["mean"]):
            print(f"{a:16}" + "".join(f"{T[a]['axes'][x]:7.2f}" for x in AXES) + f"  {T[a]['mean']:6.2f}")
    print("\nwise-men 3.11.0 vs each arm (widest shared question set):")
    for a in A_ARMS[1:]:
        qs = AB if a in B_ARMS else A; qs = [q for q in qs if q in R]
        if not qs: continue
        c = compare(R, qs, a)
        print(f"  vs {a:15} N={c['n']:2}  diff {c['diff']:+.2f}  95% [{c['lo']:+.2f}, {c['hi']:+.2f}]  W-T-L {c['w']}-{c['t']}-{c['l']}  -> {c['word']}")
    sds = [R[q]["_sd"][a] for q in R for a in arms_for(q)]
    print(f"\njudge agreement: mean SD of the three judges' totals = {st.mean(sds):.2f}")

RIVALS = [a for a in A_ARMS if not a.startswith("wise-men")]
def sg(x): return ("+" if x >= 0 else "") + r1(x)
def sg2(x): return ("+" if x >= 0 else "") + r2(x)
def done_sets(R): return [q for q in PART_A if q in R], [q for q in PART_B if q in R], [q for q in PART_A + PART_B if q not in R]
def shared(a, A, B): return A + B if a in B_ARMS else A

def rawhead(q, arm):
    p = os.path.join(H, "raw", q, arm + ".md")
    return [l[2:] for l in open(p).read().split("\n\n", 1)[0].splitlines() if l.startswith("# ")] if os.path.exists(p) else []

def results():
    R = load(); A, B, todo = done_sets(R); AB = A + B
    L = ["# Head-to-head round 3 results", ""]
    if todo:
        L += [f"**Interim.** {len(AB)} of the 12 pre-registered questions are fully judged ({', '.join(AB)}); still to come: {', '.join(todo)}. "
              "This file is regenerated from `parsed-v3/` as questions complete, so its numbers and wording can change; the pre-registered analysis covers all 12 ([`PREREG-3.md`](PREREG-3.md)).", ""]
    L += ["Three blind Opus judges per question, each with its own sealed answer order ([`blinding3.yaml`](blinding3.yaml)); an arm's score on a question is the mean of the three judges; totals are out of 25 (five axes scored 1–5). "
          "Part A re-judges round 2's answers from eight arms next to fresh wise-men 3.11.0 answers to the same eight questions (judge prompt: [`judge-prompt-9.txt`](judge-prompt-9.txt), nine answers labelled A–I); Part B asks four held-out questions no head-to-head has used, with four arms ([`judge-prompt-4.txt`](judge-prompt-4.txt)). Answers are normalized as in rounds 1–2 (`normalize()` in `h2h.py`).", ""]
    for label, qs, arms in (("Part A: round-2 questions", A, A_ARMS), ("Part B: held-out questions", B, B_ARMS), ("All judged questions: the four arms in both parts", AB if B else [], B_ARMS)):
        if not qs: continue
        T = table(R, qs, arms)
        L += [f"## {label} (N={len(qs)})", "", "| arm | total /25 | correctness | insight | practical | risk | dissent |", "|---|--:|--:|--:|--:|--:|--:|"]
        L += [f"| {NAMES[a]} | {r2(T[a]['mean'])} | " + " | ".join(r2(T[a]["axes"][x]) for x in AXES) + " |" for a in sorted(arms, key=lambda a: -T[a]["mean"])] + [""]
    L += ["## Per question (mean of three judges, total /25)", ""]
    for qs, arms in ((A, A_ARMS), (B, B_ARMS)):
        if not qs: continue
        L += ["| question | " + " | ".join(NAMES[a] for a in arms) + " |", "|---|" + "--:|" * len(arms)]
        L += [f"| {q} | " + " | ".join(r2(R[q][a]["composite"]) for a in arms) + " |" for q in qs] + [""]
    L += ["## wise-men 3.11.0 against each arm", "",
          "Mean per-question difference in total score, with a 95% percentile bootstrap interval over questions (10,000 resamples, seed 20260918), on the widest question set both arms share. "
          "Wording per PREREG-3: *clearly ahead* only when the interval's lower bound is above zero, *ahead* when only the mean difference is.", "",
          "| against | N | difference | 95% interval | W–T–L | wording |", "|---|--:|--:|--:|--:|---|"]
    lows = {}
    for a in A_ARMS[1:]:
        qs = shared(a, A, B)
        if not qs: continue
        c = compare(R, qs, a); lows[a] = c["lo"]
        L += [f"| {NAMES[a]} | {c['n']} | {sg2(c['diff'])} | [{sg2(c['lo'])}, {sg2(c['hi'])}] | {c['w']}–{c['t']}–{c['l']} | {c['word']} |"]
    every = all(lows.get(a, -1) > 0 for a in RIVALS)
    L += ["", f"Clearly ahead of every rival skill and the plain answer on the questions judged so far: **{'yes' if every else 'no'}**" + (" (interim; the pre-registered claim needs all 12 questions)." if todo else "."), ""]
    L += ["## What the numbers say, and what they don't", "",
          "- Part A's questions, and round 2's judgments of them, are the evidence versions 3.10.0 and 3.11.0 were built on, so Part A can reward fitting those judgments. Part B's held-out questions test that" + ("; they have not been judged yet." if not B else "."),
          "- Scores are relative within a round. The eight reused answers are the same files as in round 2, judged here next to a ninth answer by three judges instead of one; compare arms inside this round, not against round 2's numbers.",
          "- Every answer and every judge is a Claude model. Judges see letters, not arm names, but a distinctive answer format can still be recognizable.",
          "- The intervals resample questions, not judges, and the number of questions is small.", ""]
    sds = [R[q]["_sd"][a] for q in R for a in arms_for(q)]
    L += ["## Judge agreement", "", f"Mean standard deviation of the three judges' totals, over every arm and question: {r2(st.mean(sds))} points out of 25.", ""]
    L += ["## Cost of the new runs", "", "| question | arm | subagent tokens | tool uses | duration |", "|---|---|--:|--:|--:|"]
    notes, redacted = [], []
    for q in PART_A + PART_B:
        for a in (["wise-men-3.11"] if q in PART_A else B_ARMS):
            h = rawhead(q, a); m = re.search(r"subagent tokens: (\d+) \| tool uses: (\d+) \| duration: (\d+)s", "\n".join(h))
            if not m: continue
            L += [f"| {q} | {NAMES[a]} | {int(m[1]):,} | {m[2]} | {(Decimal(m[3]) / 60).quantize(Decimal('1'), ROUND_HALF_UP)} min |"]
            for l in h:
                if l.startswith("note: ") and "first name" in l: redacted.append(f"{q} {NAMES[a]}")
                elif l.startswith("note: "): notes.append(f"{q}, {NAMES[a]}: {l[6:]}")
    L += ["", "## Deviations and disclosures", ""] + [f"- {n}" for n in notes]
    if redacted: L += [f"- The author's first name, which subagents inherit from the author's global config, was redacted to \"the user\" before blinding, as pre-registered, in: {', '.join(redacted)}."]
    if not notes and not redacted: L += ["- None so far."]
    L += ["", "## Reproduce", "", "`python3 eval-data/head-to-head/h2h3.py report` prints these numbers, `results` rewrites this file, and `readme` prints the README table. Raw answers: `raw/<question>/`; blinded packets: `blinded-v3/`; judgments: `judgments-v3/`; parsed scores: `parsed-v3/`.", ""]
    if os.environ.get("H2H3_STDOUT"): sys.stdout.write("\n".join(L)); return
    open(os.path.join(H, "RESULTS-V3.md"), "w").write("\n".join(L))
    print("wrote RESULTS-V3.md:", len(AB), "questions; clearly ahead of every rival so far:", every)

def readme():
    R = load(); A, B, todo = done_sets(R); T = table(R, A, A_ARMS)
    print(f"| round 3, Part A ({len(A)} of 8 questions) | total /25 | correct | insight | practical | risk | dissent | wise-men 3.11.0 ahead by [95%] | W–T–L |")
    print("|---|--:|--:|--:|--:|--:|--:|--:|--:|")
    for a in sorted(A_ARMS, key=lambda a: -T[a]["mean"]):
        c = None if a == "wise-men-3.11" else compare(R, A, a)
        gap, wtl = ("—", "—") if c is None else (f"{sg(c['diff'])} [{sg(c['lo'])}, {sg(c['hi'])}]", f"{c['w']}–{c['t']}–{c['l']}")
        print(f"| {'**' + NAMES[a] + '**' if c is None else NAMES[a]} | {r1(T[a]['mean'])} | " + " | ".join(r1(T[a]["axes"][x]) for x in AXES) + f" | {gap} | {wtl} |")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "save": save(*sys.argv[2:9])
    else: {"blind": blind, "parse": parse, "report": report, "savejudge": savejudge, "results": results, "readme": readme}[cmd](*sys.argv[2:])
