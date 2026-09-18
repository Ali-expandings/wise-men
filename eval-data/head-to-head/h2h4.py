#!/usr/bin/env python3
"""Head-to-head round 4 (PREREG-4.md): fresh questions, five arms, three judges, measured time and cost.
  save <agent-transcript.jsonl> <arm> <Q> [note] | savejudge <transcript> <Q> <j> | blind <Q> | parse <Q> | report | results | readme
Run from the repo root. Rounds 1-3 live in h2h.py and h2h3.py and are untouched."""
import os, re, sys, json, glob, random, statistics as st, yaml
from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H)
from h2h import normalize, score_blocks

AXES = ["correctness", "insight", "practical", "risk", "dissent"]
ARMS = ["wise-men-3.13", "wise-men-3.13-fast", "warp-council", "llm-council", "direct"]
RIVALS = ["warp-council", "llm-council", "direct"]; COUNCILS = ["warp-council", "llm-council"]; WM = ARMS[:2]
JUDGES = ["j1", "j2", "j3"]
NAMES = {"wise-men-3.13": "wise-men 3.13.0 (default)", "wise-men-3.13-fast": "wise-men 3.13.0 `--fast`", "warp-council": "Warp council", "llm-council": "llm-council", "direct": "plain answer"}
HEAD = {"wise-men-3.13": "wise-men-3.13 (SKILL.md v3.13.0, default tier selection)", "wise-men-3.13-fast": "wise-men-3.13-fast (SKILL.md v3.13.0, invoked with --fast)",
        "warp-council": "warp-council (warpdotdev/common-skills 69b4753651ab; adapted as in PREREG-2)", "llm-council": "llm-council (aiwithremy/claude-skills-llm-council 1162f272ab94)", "direct": "direct (no skill)"}
QS = {q["id"]: q for q in yaml.safe_load(open(os.path.join(H, "questions-r4.yaml")))}
BLIND = yaml.safe_load(open(os.path.join(H, "blinding4.yaml")))["map"] if os.path.exists(os.path.join(H, "blinding4.yaml")) else {}
PRICE = {"haiku": (1, 5), "sonnet": (3, 15), "opus": (5, 25), "fable": (10, 50)}  # USD per million input/output tokens (2026-07 list); cache read 0.1x input, 5-minute cache write 1.25x input

def r1(x): return str(Decimal(str(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))
def r2(x): return str(Decimal(str(x)).quantize(Decimal("0.01"), ROUND_HALF_UP))
def sg(x): return ("+" if x >= 0 else "") + r1(x)
def rows_of(f): return [json.loads(l) for l in open(f)]
def tier(model): return next((k for k in PRICE if k in (model or "")), "sonnet")
def first_prompt(rows):
    r = next((r for r in rows if r.get("type") == "user"), None)
    if not r: return ""
    c = r["message"]["content"]; return c if isinstance(c, str) else "\n".join(x.get("text", "") for x in c if x.get("type") == "text")
def final_text(rows):
    last = max(i for i, r in enumerate(rows) if r.get("type") == "user")
    return "\n".join(c["text"] for r in rows[last + 1:] if r.get("type") == "assistant" for c in r["message"]["content"] if c.get("type") == "text").strip()

def usage(rows):
    """Tokens by billing category and list-price USD for one transcript. Streamed messages repeat their id: keep the largest figure per field."""
    per = {}
    for r in rows:
        if r.get("type") != "assistant": continue
        m = r["message"]; x = m.get("usage") or {}; d = per.setdefault(m.get("id"), {"model": m.get("model"), "in": 0, "out": 0, "cr": 0, "cw": 0})
        for k, f in (("in", "input_tokens"), ("out", "output_tokens"), ("cr", "cache_read_input_tokens"), ("cw", "cache_creation_input_tokens")): d[k] = max(d[k], x.get(f, 0) or 0)
    u = {"in": 0, "out": 0, "cr": 0, "cw": 0, "usd": 0.0}
    for d in per.values():
        pi, po = PRICE[tier(d["model"])]
        for k in ("in", "out", "cr", "cw"): u[k] += d[k]
        u["usd"] += (d["in"] * pi + d["out"] * po + d["cr"] * pi * 0.1 + d["cw"] * pi * 1.25) / 1e6
    return u

def run_cost(transcript):
    """The orchestrator plus every subagent it spawned (matched by the exact prompt it sent), so a council's children are counted."""
    rows = rows_of(transcript); ts = [r["timestamp"] for r in rows if r.get("timestamp")]
    t0, t1 = (datetime.fromisoformat(x.replace("Z", "+00:00")) for x in (ts[0], ts[-1]))
    index = {}
    for f in glob.glob(os.path.join(os.path.dirname(transcript), "agent-*.jsonl")):
        try: index.setdefault(first_prompt(rows_of(f))[:3000], []).append(f)
        except Exception: pass
    tot = usage(rows); calls = 0; used = set()
    for r in rows:
        if r.get("type") != "assistant": continue
        for c in r["message"]["content"]:
            if c.get("type") == "tool_use" and c["name"] in ("Agent", "Task"):
                calls += 1
                for f in index.get((c["input"].get("prompt") or "")[:3000], []):
                    if f in used: continue
                    used.add(f); ku = usage(rows_of(f))
                    for k in tot: tot[k] += ku[k]
                    break
    return {"minutes": (t1 - t0).total_seconds() / 60, "calls": calls, "matched": len(used), **tot}

def save(transcript, arm, q, note=""):
    rows = rows_of(transcript); txt = final_text(rows); red = re.sub(r"\bAli\b", "the user", txt); c = run_cost(transcript)
    head = f"# arm: {HEAD[arm]} | question: {q} | orchestrator: general-purpose/sonnet | run: {rows[0]['timestamp'][:10]} (round 4, PREREG-4 rules)\n"
    head += f"# minutes: {c['minutes']:.1f} | subagent calls: {c['calls']} (transcripts matched: {c['matched']}) | tokens in/out/cache-read/cache-write: {c['in']}/{c['out']}/{c['cr']}/{c['cw']} | list-price USD: {c['usd']:.2f}\n"
    if note: head += f"# note: {note}\n"
    if red != txt: head += "# note: the author's first name (inherited from global config) redacted to \"the user\"\n"
    os.makedirs(os.path.join(H, "raw", q), exist_ok=True); open(os.path.join(H, "raw", q, arm + ".md"), "w").write(head + "\n" + red + "\n")
    print("saved", q, arm, len(red.split()), "words |", f"{c['minutes']:.1f} min, {c['calls']} calls, ${c['usd']:.2f}")

def blind(q):
    tpl = open(os.path.join(H, "judge-prompt-5.txt")).read(); os.makedirs(os.path.join(H, "blinded-v4"), exist_ok=True)
    for j in JUDGES:
        parts = [f'Response {slot}:\n"""\n{normalize("wise-men" if arm.startswith("wise-men") else arm, open(os.path.join(H, "raw", q, arm + ".md")).read())}\n"""\n' for slot, arm in BLIND[q][j].items()]
        open(os.path.join(H, "blinded-v4", f"{q}-{j}.md"), "w").write(tpl.replace("{question}", QS[q]["text"]).replace("{responses}", "\n".join(parts)))
    print("blinded", q, "x3")

def savejudge(transcript, q, j):
    rows = rows_of(transcript); t = final_text(rows); os.makedirs(os.path.join(H, "judgments-v4"), exist_ok=True)
    open(os.path.join(H, "judgments-v4", f"{q}-{j}.md"), "w").write(f"# judge: fresh opus subagent, no skills, Read-only | question: {q} | judge: {j} | run: {rows[0]['timestamp'][:10]} (round 4)\n# blinded input: blinded-v4/{q}-{j}.md (slots per blinding4.yaml)\n\n{t}\n")
    got = {BLIND[q][j][s]: sum(v.values()) for s, v in score_blocks(t, set(BLIND[q][j])).items()}; assert set(got) == set(ARMS), (q, j, set(ARMS) - set(got))
    print("judgment", q, j, dict(sorted(got.items(), key=lambda x: -x[1])))

def parse(q):
    os.makedirs(os.path.join(H, "parsed-v4"), exist_ok=True); out = {}
    for j in JUDGES:
        got = {}
        for slot, sc in score_blocks(open(os.path.join(H, "judgments-v4", f"{q}-{j}.md")).read(), set(BLIND[q][j])).items():
            a = BLIND[q][j][slot]; got[a] = dict(sc); got[a]["composite"] = sum(sc.values())
        assert set(got) == set(ARMS), (q, j); out[j] = got
    yaml.safe_dump({"question_id": q, "judges": out}, open(os.path.join(H, "parsed-v4", q + ".yaml"), "w"), sort_keys=False)
    print("parsed", q, {a: r2(st.mean(out[j][a]["composite"] for j in JUDGES)) for a in ARMS})

def load():
    R = {}
    for f in sorted(glob.glob(os.path.join(H, "parsed-v4", "R*.yaml"))):
        d = yaml.safe_load(open(f)); R[d["question_id"]] = {a: {k: st.mean(d["judges"][j][a][k] for j in JUDGES) for k in AXES + ["composite"]} for a in ARMS}
        R[d["question_id"]]["_sd"] = {a: st.pstdev([d["judges"][j][a]["composite"] for j in JUDGES]) for a in ARMS}
    return R

def costs():
    """Per arm: minutes, calls and USD read back from the raw headers; runs whose note says they were interrupted are left out of the time figures only."""
    C = {a: {"min": [], "usd": [], "calls": []} for a in ARMS}
    for q in QS:
        for a in ARMS:
            p = os.path.join(H, "raw", q, a + ".md")
            if not os.path.exists(p): continue
            h = open(p).read().split("\n\n", 1)[0]; m = re.search(r"minutes: ([\d.]+) \| subagent calls: (\d+).*list-price USD: ([\d.]+)", h)
            if not m: continue
            C[a]["usd"].append(float(m[3])); C[a]["calls"].append(int(m[2]))
            if "interrupted" not in h: C[a]["min"].append(float(m[1]))
    return C

def boot(d, seed=20260919, n=10000):
    rng = random.Random(seed); k = len(d); means = sorted(st.mean(rng.choice(d) for _ in range(k)) for _ in range(n)); return means[int(0.025 * n)], means[int(0.975 * n) - 1]
def compare(R, a, b):
    d = [R[q][b]["composite"] - R[q][a]["composite"] for q in R]; lo, hi = boot(d)
    word = "clearly ahead" if lo > 0 else "ahead" if st.mean(d) > 0 else "level" if st.mean(d) == 0 else ("clearly behind" if hi < 0 else "behind")
    return {"diff": st.mean(d), "lo": lo, "hi": hi, "w": sum(x > 0 for x in d), "t": sum(x == 0 for x in d), "l": sum(x < 0 for x in d), "word": word}
def table(R): return {a: {"mean": st.mean(R[q][a]["composite"] for q in R), "axes": {x: st.mean(R[q][a][x] for q in R) for x in AXES}} for a in ARMS}

def lines():
    R = load(); n = len(R); T = table(R); C = costs(); L = []
    med = lambda v: st.median(v) if v else float("nan")
    L += [f"| round 4 ({n} of {len(QS)} questions) | total /25 | correct | insight | practical | risk | dissent | median minutes | median calls | median list-price USD |", "|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for a in sorted(ARMS, key=lambda a: -T[a]["mean"]):
        L += [f"| {NAMES[a]} | {r1(T[a]['mean'])} | " + " | ".join(r1(T[a]["axes"][x]) for x in AXES) + f" | {r1(med(C[a]['min']))} | {r1(med(C[a]['calls']))} | {r2(med(C[a]['usd']))} |"]
    L += [""]
    for w in WM:
        for a in ARMS:
            if a == w or (a in WM and w == WM[1]): continue
            c = compare(R, a, w); L += [f"- {NAMES[w]} against {NAMES[a]}: {sg(c['diff'])} [{sg(c['lo'])}, {sg(c['hi'])}], W–T–L {c['w']}–{c['t']}–{c['l']} — {c['word']}."]
    L += [""]
    for w in WM:
        best = {x: max(ARMS, key=lambda a: T[a]["axes"][x]) for x in AXES}
        L += [f"- {NAMES[w]}: highest mean on {sum(best[x] == w for x in AXES)} of 5 axes; faster than " + (", ".join(NAMES[a] for a in COUNCILS if med(C[w]["min"]) < med(C[a]["min"])) or "neither rival council") +
              "; cheaper than " + (", ".join(NAMES[a] for a in COUNCILS if med(C[w]["usd"]) < med(C[a]["usd"])) or "neither rival council") + "."]
    sds = [R[q]["_sd"][a] for q in R for a in ARMS]; L += ["", f"Judge agreement: mean SD of the three judges' totals {r2(st.mean(sds))}."]
    return L

def report(): print("\n".join(lines()))
def results():
    R = load(); todo = [q for q in QS if q not in R]
    L = ["# Head-to-head round 4 results", ""] + ([f"**Interim.** {len(R)} of {len(QS)} questions judged; still to come: {', '.join(todo)}. Regenerated from `parsed-v4/` and the raw headers as questions complete.", ""] if todo else [])
    L += ["Eight questions written for this round by an author that knew nothing about the arms ([`PREREG-4.md`](PREREG-4.md), [`questions-r4.yaml`](questions-r4.yaml)); five arms; three blind Opus judges per question with sealed orders ([`blinding4.yaml`](blinding4.yaml)) and an error-first judge prompt ([`judge-prompt-5.txt`](judge-prompt-5.txt)). "
          "Minutes are the orchestrator's first-to-last transcript timestamp; calls are its subagent spawns; USD prices every token the run used — the orchestrator's and every spawned agent's, input, output, cache reads and cache writes — at the 2026-07 list rates in `resources/model-routing.md`. No council can be faster or cheaper than the plain answer; the pre-registered time and cost comparisons are against the rival councils.", ""] + lines()
    L += ["", "## Per question (mean of three judges, total /25)", "", "| question | " + " | ".join(NAMES[a] for a in ARMS) + " |", "|---|" + "--:|" * len(ARMS)] + [f"| {q} ({QS[q]['domain']}, {QS[q]['shape']}) | " + " | ".join(r2(R[q][a]["composite"]) for a in ARMS) + " |" for q in R]
    notes = [f"- {q}, {NAMES[a]}: {l[8:]}" for q in QS for a in ARMS if os.path.exists(os.path.join(H, "raw", q, a + ".md")) for l in open(os.path.join(H, "raw", q, a + ".md")).read().split("\n\n", 1)[0].splitlines() if l.startswith("# note: ")]
    L += ["", "## Deviations and disclosures", ""] + (notes or ["- None."]) + ["", "## Reproduce", "", "`python3 eval-data/head-to-head/h2h4.py report` prints the table and comparisons; `results` rewrites this file. Time and cost were computed from local agent transcripts when each answer was saved and are stored in the raw file headers; the transcripts themselves are not in the repository.", ""]
    out = "\n".join(L)
    if os.environ.get("H2H4_STDOUT"): sys.stdout.write(out); return
    open(os.path.join(H, "RESULTS-V4.md"), "w").write(out); print("wrote RESULTS-V4.md:", len(R), "questions")

if __name__ == "__main__":
    cmd = sys.argv[1]; {"save": save, "savejudge": savejudge, "blind": blind, "parse": parse, "report": report, "results": results, "readme": report}[cmd](*sys.argv[2:])
