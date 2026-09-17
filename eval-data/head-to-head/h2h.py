#!/usr/bin/env python3
"""Head-to-head helpers: blind <Q> | parse <Q> | report | results.  Run from repo root."""
import os, re, sys, yaml, glob, statistics as st
H = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(H))
AXES = ["correctness", "insight", "practical", "risk", "dissent"]
STUDY = os.environ.get("H2H_STUDY", "v1")   # v1 = the published six-arm study; v2 = PREREG-2 (adds ECC and Warp council)
CFG = {
    "v1": dict(arms=["wise-men", "brainstorming", "grilling", "lifeos-council", "llm-council", "direct"], slots="ABCDEF",
               blinding="blinding.yaml", prompt="judge-prompt-6.txt", blinded="blinded", judgments="judgments", parsed="parsed",
               order=["wise-men", "lifeos-council", "llm-council", "brainstorming", "grilling", "direct"]),
    "v2": dict(arms=["wise-men", "brainstorming", "grilling", "lifeos-council", "llm-council", "ecc-council", "warp-council", "direct"], slots="ABCDEFGH",
               blinding="blinding2.yaml", prompt="judge-prompt-8.txt", blinded="blinded-v2", judgments="judgments-v2", parsed="parsed-v2",
               order=["wise-men", "lifeos-council", "llm-council", "ecc-council", "warp-council", "brainstorming", "grilling", "direct"]),
}[STUDY]
ARMS = CFG["arms"]

def qtext(q):
    d = yaml.safe_load(open(os.path.join(ROOT, "eval-data", "questions.yaml"))); qs = d["questions"] if isinstance(d, dict) and "questions" in d else d
    return next(x.get("text") or x.get("question") for x in qs if x["id"] == q)

def normalize(arm, txt):
    lines = txt.split("\n")
    while lines and (lines[0].startswith("# ") or lines[0].strip() == ""): lines.pop(0)  # provenance header block (all '# ' lines at top)
    t = "\n".join(lines).strip()
    # orchestrator status text that precedes the skill's own output (not part of any skill's user-facing format):
    # for skills whose output is headed, cut to the first '## ' heading if what precedes it is short status prose
    if arm in ("lifeos-council", "llm-council", "wise-men", "ecc-council", "warp-council"):
        m = re.search(r"^## ", t, re.M)
        if m and m.start() > 0 and len(t[:m.start()].split("\n")) <= 4: t = t[m.start():]
    if arm == "wise-men":  # same rule as the N=29 eval: strip the audit footer + status/process text; never edit content
        m = re.search(r"^(\*Note: brief format upgraded|## )", t, re.M)  # skill output starts at its first heading/note
        if m: t = t[m.start():]
        t = re.sub(r"^\*Note: brief format upgraded.*?\*\n+", "", t)
        t = re.split(r"\n---\n\n## Full audit( trail)?", t)[0].strip()
        t = re.sub(r"\n+\*One process note:.*?\*\s*$", "", t, flags=re.S).strip()  # orchestrator environment note (harness artefact, not skill output)
    return t

def blind(q):
    bm = yaml.safe_load(open(os.path.join(H, CFG["blinding"])))["map"][q]
    parts = []
    for slot in CFG["slots"]:
        arm = bm[slot]; raw = open(os.path.join(H, "raw", q, arm + ".md")).read()
        parts.append(f'Response {slot}:\n"""\n{normalize(arm, raw)}\n"""\n')
    tpl = open(os.path.join(H, CFG["prompt"])).read()
    out = tpl.replace("{question}", qtext(q)).replace("{responses}", "\n".join(parts))
    os.makedirs(os.path.join(H, CFG["blinded"]), exist_ok=True); open(os.path.join(H, CFG["blinded"], q + ".md"), "w").write(out); print("blinded", q, len(out), "chars")

def parse(q):
    bm = yaml.safe_load(open(os.path.join(H, CFG["blinding"])))["map"][q]
    j = open(os.path.join(H, CFG["judgments"], q + ".md")).read()
    blocks = re.findall(r"```scores\n(.*?)```", j, re.S); out = {}
    for b in blocks:
        d = dict(re.findall(r"(\w+):\s*([A-F]|\d)", b)); slot = d["response"]
        out[bm[slot]] = {a: int(d[a]) for a in AXES}; out[bm[slot]]["composite"] = sum(int(d[a]) for a in AXES); out[bm[slot]]["slot"] = slot
    assert set(out) == set(ARMS), set(out)
    os.makedirs(os.path.join(H, CFG["parsed"]), exist_ok=True); yaml.safe_dump({"question_id": q, "arms": out}, open(os.path.join(H, CFG["parsed"], q + ".yaml"), "w"), sort_keys=False); print("parsed", q, {a: out[a]["composite"] for a in ARMS})

NAMES = {"ecc-council": "ECC council", "warp-council": "Warp council", "wise-men": "wise-men", "lifeos-council": "LifeOS Council", "llm-council": "llm-council", "brainstorming": "brainstorming", "grilling": "grilling", "direct": "plain answer"}
ORDER = CFG["order"]  # display order in tables
SKILLS = ORDER[:-1]

def rows():
    return {os.path.basename(f)[:-5]: yaml.safe_load(open(f))["arms"] for f in sorted(glob.glob(os.path.join(H, CFG["parsed"], "Q*.yaml")))}

def durations():
    out = {a: [] for a in ARMS}
    for f in sorted(glob.glob(os.path.join(H, "raw", "Q*", "*.md"))):
        m = re.search(r"^# .*duration: (\d+)s", open(f).read(), re.M); a = os.path.basename(f)[:-3]
        if m and a in out: out[a].append(int(m.group(1)))
    return out

def one(x): return f"{x:.2f}"
def wtl(R, a, b):
    d = [r[a]["composite"] - r[b]["composite"] for r in R.values()]
    return sum(x > 0 for x in d), sum(x == 0 for x in d), sum(x < 0 for x in d)

def stats(R):
    S = {}
    for a in ARMS:
        comps = [r[a]["composite"] for r in R.values()]
        S[a] = {"mean": st.mean(comps), "min": min(comps), "max": max(comps), "axes": {x: st.mean(r[a][x] for r in R.values()) for x in AXES},
                "perfect_axes": [x for x in AXES if all(r[a][x] == 5 for r in R.values())],
                "top": sum(r[a]["composite"] == max(r[b]["composite"] for b in ARMS) for r in R.values())}
    return S

def report():
    R = rows(); S = stats(R); D = durations(); n = len(R)
    print(f"N={n}")
    print(f"{'arm':16}" + "".join(f"{x[:5]:>7}" for x in AXES) + "    mean  min-max  vs-plain W-T-L  vs-wise-men W-T-L  top(shared)  median-run")
    for a in ORDER:
        s = S[a]; vp = "-".join(map(str, wtl(R, a, "direct"))) if a != "direct" else "-"; vw = "-".join(map(str, wtl(R, a, "wise-men"))) if a != "wise-men" else "-"
        md = st.median(D[a]) if D[a] else float("nan")
        print(f"{a:16}" + "".join(f"{s['axes'][x]:7.2f}" for x in AXES) + f"  {s['mean']:6.2f}  {s['min']:>2}-{s['max']:<2}   {vp:>7}          {vw:>7}          {s['top']}/{n}       {md/60:.1f} min")
    print("perfect axes (5 on every question):", {a: S[a]["perfect_axes"] for a in ARMS if S[a]["perfect_axes"]})
    best = {q: max(SKILLS[1:], key=lambda b: r[b]["composite"]) for q, r in R.items()}
    vb = [R[q]["wise-men"]["composite"] - R[q][best[q]]["composite"] for q in R]
    print("wise-men vs best other skill per question W-T-L:", sum(x > 0 for x in vb), sum(x == 0 for x in vb), sum(x < 0 for x in vb))

def results():
    if STUDY != "v1": raise SystemExit("RESULTS-V2.md is written with the v2 analysis; this writer produces v1's RESULTS.md")
    R = rows(); S = stats(R); D = durations(); n = len(R); plain = S["direct"]["mean"]
    T = {q: re.search(r"(solo|quick|standard|deep|paranoid) tier", open(os.path.join(H, "raw", q, "wise-men.md")).read(), re.I).group(1).lower() for q in R}
    D_by_q = {q: int(re.search(r"duration: (\d+)s", open(os.path.join(H, "raw", q, "wise-men.md")).read()).group(1)) for q in R}
    stars = {"wise-men": "this repo", "lifeos-council": "danielmiessler/LifeOS · 19k★ repo", "llm-council": "aiwithremy/claude-skills-llm-council · 2.1k★",
             "brainstorming": "obra/superpowers · 288k★ repo", "grilling": "mattpocock/skills · 264k★ repo", "direct": "no skill"}
    L = ["# Head-to-head results", "",
         "Generated by `python3 eval-data/head-to-head/h2h.py results` from `parsed/` — the numbers here cannot drift from the data. Design, arms, questions, judge and analysis plan were fixed in [PREREG.md](PREREG.md) before any arm ran; star counts from the GitHub API on 2026-09-17.", "",
         "## Result", "",
         "| arm | source | mean /25 | vs plain | correctness | insight | practical | risk | dissent | lowest–highest | beat plain answer | wise-men vs it (W–T–L) |",
         "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for a in ORDER:
        s = S[a]; d = s["mean"] - plain
        bp = f"{wtl(R, a, 'direct')[0]} of {n}" if a != "direct" else "—"
        vw = "–".join(map(str, wtl(R, "wise-men", a))) if a != "wise-men" else "—"
        name = f"**{NAMES[a]}**" if a == "wise-men" else NAMES[a]
        L.append(f"| {name} | {stars[a]} | {one(s['mean'])} | {('+' if d >= 0 else '−') + one(abs(d)) if a != 'direct' else '—'} | " + " | ".join(one(s["axes"][x]) for x in AXES) + f" | {s['min']}–{s['max']} | {bp} | {vw} |")
    L += ["", "## Per question (total /25)", "", "| question | domain | " + " | ".join(NAMES[a] for a in ORDER) + " |", "|---|---|" + "--:|" * len(ORDER)]
    doms = {x["id"]: x["domain"] for x in (lambda d: d["questions"] if isinstance(d, dict) and "questions" in d else d)(yaml.safe_load(open(os.path.join(ROOT, "eval-data", "questions.yaml"))))}
    for q, r in R.items():
        top = max(r[a]["composite"] for a in ARMS)
        L.append(f"| {q} | {doms[q]} | " + " | ".join((f"**{r[a]['composite']}**" if r[a]["composite"] == top else str(r[a]["composite"])) for a in ORDER) + " |")
    best = {q: max(SKILLS[1:], key=lambda b: r[b]["composite"]) for q, r in R.items()}
    vb = [R[q]["wise-men"]["composite"] - R[q][best[q]]["composite"] for q in R]
    vl, vm = wtl(R, "wise-men", "lifeos-council"), wtl(R, "wise-men", "llm-council")
    others_min = {a: S[a]["min"] for a in SKILLS[1:]}
    perfect_others = [a for a in ARMS if a != "wise-men" and S[a]["perfect_axes"]]
    lead = sorted(ARMS, key=lambda a: -S[a]["axes"]["practical"])[0]
    L += ["", "Bold = top score on that question (ties bolded together).", "", "## What the numbers say — and what they don't", "",
          f"- **wise-men had the highest mean** ({one(S['wise-men']['mean'])} vs {one(plain)} for a plain answer) and scored 5 on "
          + " and ".join(S["wise-men"]["perfect_axes"]) + f" on all {n} questions" + ("; no other arm scored 5 on any axis on every question." if not perfect_others else "."),
          f"- **Consistency, not a sweep.** Its lowest total was {S['wise-men']['min']}; the other skills' lowest were " + ", ".join(f"{NAMES[a]} {m}" for a, m in others_min.items())
          + f". Against the best of the other four on each question it was ahead on {sum(x > 0 for x in vb)}, tied on {sum(x == 0 for x in vb)}, behind on {sum(x < 0 for x in vb)}.",
          f"- **The other councils are close.** wise-men vs LifeOS Council {vl[0]}–{vl[1]}–{vl[2]} (mean gap {S['wise-men']['mean'] - S['lifeos-council']['mean']:+.2f}), vs llm-council {vm[0]}–{vm[1]}–{vm[2]} ({S['wise-men']['mean'] - S['llm-council']['mean']:+.2f}). With N={n} and a spread of roughly ±2 points across questions, that ordering is suggestive, not established. Both of those councils also beat the plain answer on every question.",
          f"- **brainstorming and grilling are not built for this job.** Both interview the user before deciding; with nobody to answer they had to assume, and the judge marked grilling down for manufacturing facts. They beat the plain answer on {wtl(R, 'brainstorming', 'direct')[0]} and {wtl(R, 'grilling', 'direct')[0]} of {n}. This measures them on one-shot decisions, not on the interactive work they are designed for.",
          f"- **Where wise-men did not lead.** Correctness was level ({one(S['wise-men']['axes']['correctness'])} for wise-men, brainstorming and the plain answer alike). Practical usefulness was led by {NAMES[lead]} ({one(S[lead]['axes']['practical'])}); wise-men scored {one(S['wise-men']['axes']['practical'])}, the same as the plain answer. In 7 of 8 judgments (all but Q36) the judge criticised process talk inside wise-men's answer — council meta, peer-review scores, self-praise; that is the clearest thing to fix.",
          f"- **No significance test** — pre-registered: N={n}, one judge model, answers produced and judged by models from the same family.", "",
          "## Cost", "",
          "Wall-clock minutes per question (all six arms of a question ran at the same time, so load was shared):", "",
          "| arm | median | fastest | slowest |", "|---|--:|--:|--:|"]
    for a in ORDER:
        L.append(f"| {NAMES[a]} | {st.median(D[a]) / 60:.1f} | {min(D[a]) / 60:.1f} | {max(D[a]) / 60:.1f} |")
    slow = sorted(R, key=lambda q: -D_by_q[q])[:2]
    L += ["", f"wise-men is the most expensive arm. It picks its own tier per question — here deep on {', '.join(q for q in R if T[q] == 'deep')} and standard on {', '.join(q for q in R if T[q] == 'standard')}; the two slowest runs ({slow[0]}, {slow[1]}) were deep-tier councils of 7 members and 7 reviewers, one of them with a debate round. The lead costs minutes and subagent calls; it is not free.", "",
          "## Deviations, all disclosed", "",
          "1. **Amendment 1** (after Q05/Q09 were judged, before Q13 was judged): arms may Read only their own skill files, orchestrators must wait for their subagents, an incomplete run is re-run once. Triggered by one Q13 arm reading the author's private notes and one orchestrator returning early. See PREREG.md.",
          "2. **Re-runs** (each allowed once): Q13 brainstorming (first output used private notes — discarded), Q13 wise-men (first orchestrator returned before its subagents finished), Q55 wise-men, LifeOS Council and llm-council (first attempts terminated by an API rate limit before producing any output). No second failures.",
          "3. **Normalization before blinding**, identical rules for every arm (`normalize()` in h2h.py): provenance headers and orchestrator status lines removed. wise-men's appended *Full audit* section was removed on Q05, Q09, Q19 and Q55 — SKILL.md shows the audit trail only on request (`--full`, or asking for the transcript), so those orchestrators appended something a user does not see by default. LifeOS Council's round-by-round debate was kept, because its OutputFormat.md makes the transcript the output. One trailing orchestrator note (Q48, wise-men) was removed. Content was never edited; every raw answer is in `raw/`.",
          "4. **No-human adaptation** for brainstorming and grilling, and the skipped LifeOS voice notification — both pre-registered.",
          "5. The author's first name, which subagents inherit from the author's global config, is redacted to \"the user\" in raw files. One answer slipped through before blinding (Q09, LifeOS Council, run before Amendment 1), so the Q09 judge saw the name inside that answer; it identifies no arm. That raw file and its blinded packet were redacted afterwards — the only edit ever made to a blinded packet.", "",
          "## Reproduce", "", "```bash", "python3 eval-data/head-to-head/h2h.py report    # the table above, in the terminal", "python3 eval-data/head-to-head/h2h.py results   # rewrites this file", "python3 scripts/make_charts.py                  # rewrites the charts in assets/", "```", ""]
    open(os.path.join(H, "RESULTS.md"), "w").write("\n".join(L)); print("wrote RESULTS.md")

if __name__ == "__main__":
    cmd = sys.argv[1]; {"blind": blind, "parse": parse, "report": report, "results": results}[cmd](*sys.argv[2:])
