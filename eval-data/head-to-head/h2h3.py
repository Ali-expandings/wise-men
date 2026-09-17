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

def save(transcript, arm, q, tokens, tools, seconds):
    txt = final_text(transcript); redacted = re.sub(r"\bAli\b", "the user", txt)
    head = f"# arm: {HEAD[arm]} | question: {q} | orchestrator: general-purpose/sonnet | run: 2026-09-17 (round 3, PREREG-3 rules)\n" + NOTE.get(arm, "")
    head += f"# subagent tokens: {tokens} | tool uses: {tools} | duration: {seconds}s\n"
    if redacted != txt: head += "# note: the author's first name (inherited from global config) redacted to \"the user\" per PREREG-3\n"
    os.makedirs(os.path.join(H, "raw", q), exist_ok=True)
    open(os.path.join(H, "raw", q, arm + ".md"), "w").write(head + "\n" + redacted + "\n")
    print("saved", q, arm, len(redacted.split()), "words", "(redacted)" if redacted != txt else "")

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

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "save": save(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    else: {"blind": blind, "parse": parse, "report": report}[cmd](*sys.argv[2:])
