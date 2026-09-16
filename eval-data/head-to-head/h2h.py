#!/usr/bin/env python3
"""Head-to-head helpers: blind <Q> | parse <Q> | report.  Run from repo root."""
import os, re, sys, yaml, glob, statistics as st
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(H))
AXES = ["correctness", "insight", "practical", "risk", "dissent"]
ARMS = ["wise-men", "brainstorming", "grilling", "lifeos-council", "llm-council", "direct"]

def qtext(q):
    d = yaml.safe_load(open(os.path.join(ROOT, "eval-data", "questions.yaml"))); qs = d["questions"] if isinstance(d, dict) and "questions" in d else d
    return next(x.get("text") or x.get("question") for x in qs if x["id"] == q)

def normalize(arm, txt):
    lines = [l for l in txt.split("\n") if not l.startswith("# arm:") and not l.startswith("# skill:") and not l.startswith("# subagent") and not l.startswith("# adaptation") and not l.startswith("# environment")]
    t = "\n".join(lines).strip()
    if arm == "wise-men":  # same rule as the N=29 eval: strip the audit footer + status line; never edit content
        t = re.sub(r"^\*Note: brief format upgraded.*?\*\n+", "", t)
        t = t.split("\n---\n\n## Full audit trail")[0].strip()
    return t

def blind(q):
    bm = yaml.safe_load(open(os.path.join(H, "blinding.yaml")))["map"][q]
    parts = []
    for slot in "ABCDEF":
        arm = bm[slot]; raw = open(os.path.join(H, "raw", q, arm + ".md")).read()
        parts.append(f'Response {slot}:\n"""\n{normalize(arm, raw)}\n"""\n')
    tpl = open(os.path.join(H, "judge-prompt-6.txt")).read()
    out = tpl.replace("{question}", qtext(q)).replace("{responses}", "\n".join(parts))
    open(os.path.join(H, "blinded", q + ".md"), "w").write(out); print("blinded", q, len(out), "chars")

def parse(q):
    bm = yaml.safe_load(open(os.path.join(H, "blinding.yaml")))["map"][q]
    j = open(os.path.join(H, "judgments", q + ".md")).read()
    blocks = re.findall(r"```scores\n(.*?)```", j, re.S); out = {}
    for b in blocks:
        d = dict(re.findall(r"(\w+):\s*([A-F]|\d)", b)); slot = d["response"]
        out[bm[slot]] = {a: int(d[a]) for a in AXES}; out[bm[slot]]["composite"] = sum(int(d[a]) for a in AXES); out[bm[slot]]["slot"] = slot
    assert set(out) == set(ARMS), set(out)
    yaml.safe_dump({"question_id": q, "arms": out}, open(os.path.join(H, "parsed", q + ".yaml"), "w"), sort_keys=False); print("parsed", q, {a: out[a]["composite"] for a in ARMS})

def report():
    rows = {os.path.basename(f)[:-5]: yaml.safe_load(open(f))["arms"] for f in sorted(glob.glob(os.path.join(H, "parsed", "Q*.yaml")))}
    print(f"N={len(rows)}"); print(f"{'arm':16}" + "".join(f"{a[:5]:>7}" for a in AXES) + "   comp   beats-direct  beats-wise-men")
    for a in ARMS:
        m = [st.mean(r[a][x] for r in rows.values()) for x in AXES]; c = st.mean(r[a]["composite"] for r in rows.values())
        bd = sum(r[a]["composite"] > r["direct"]["composite"] for r in rows.values()); bw = sum(r[a]["composite"] > r["wise-men"]["composite"] for r in rows.values())
        print(f"{a:16}" + "".join(f"{x:7.2f}" for x in m) + f"  {c:5.1f}   {bd}/{len(rows)}          {bw}/{len(rows)}")

if __name__ == "__main__":
    cmd = sys.argv[1]; (blind if cmd == "blind" else parse if cmd == "parse" else lambda *_: report())(*sys.argv[2:])
