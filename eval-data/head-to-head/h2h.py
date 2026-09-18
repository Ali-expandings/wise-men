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

def score_blocks(text, letters):
    """Every fenced scores block in a judgment, parsed strictly: exactly one response letter and the five axes, each an
    integer 1-5 on its own line, no duplicate keys, no duplicate letters. A malformed block raises instead of being truncated."""
    out = {}
    for b in re.findall(r"```scores\n(.*?)```", text, re.S):
        d = {}
        for line in (l.strip() for l in b.strip().splitlines() if l.strip()):
            m = re.fullmatch(r"(\w+):\s*(\S+)", line)
            assert m and m[1] not in d, ("malformed or duplicate line in scores block", line)
            d[m[1]] = m[2]
        assert set(d) == {"response", *AXES}, ("scores block keys", sorted(d))
        assert d["response"] in letters and d["response"] not in out, ("response letter", d["response"])
        assert all(re.fullmatch(r"[1-5]", d[a]) for a in AXES), ("axis score must be an integer 1-5", d)
        out[d["response"]] = {a: int(d[a]) for a in AXES}
    return out

def parse(q):
    bm = yaml.safe_load(open(os.path.join(H, CFG["blinding"])))["map"][q]
    j = open(os.path.join(H, CFG["judgments"], q + ".md")).read(); out = {}
    for slot, sc in score_blocks(j, set(bm)).items():
        out[bm[slot]] = dict(sc); out[bm[slot]]["composite"] = sum(sc[a] for a in AXES); out[bm[slot]]["slot"] = slot
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
    if STUDY == "v2": return results_v2()
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

def results_v2():
    # every sentence below is asserted against the data first, so a changed judgment breaks the writer instead of the prose
    from decimal import Decimal, ROUND_HALF_UP
    mins = lambda sec: str(Decimal(str(sec / 60)).quantize(Decimal("0.1"), ROUND_HALF_UP))
    R = rows(); S = stats(R); D = durations(); n = len(R); plain = S["direct"]["mean"]
    V1 = {os.path.basename(f)[:-5]: yaml.safe_load(open(f))["arms"] for f in sorted(glob.glob(os.path.join(H, "parsed", "Q*.yaml")))}
    src = {"warp-council": "warpdotdev/common-skills · 24.5k installs · 579★", "wise-men": "this repo",
           "llm-council": "aiwithremy/claude-skills-llm-council · 1.0k installs · 2.1k★", "lifeos-council": "danielmiessler/LifeOS · 19k★ repo",
           "ecc-council": "affaan-m/ECC · 7.7k installs · 261k★ repo", "brainstorming": "obra/superpowers · 366k installs · 288k★ repo",
           "grilling": "mattpocock/skills · 718k installs · 264k★ repo", "direct": "no skill"}
    srt = sorted(ARMS, key=lambda a: (-S[a]["mean"], ORDER.index(a)))
    councils = ["wise-men", "lifeos-council", "llm-council", "ecc-council", "warp-council"]
    ax = lambda a, x: S[a]["axes"][x]; best_on = lambda x: [a for a in ARMS if ax(a, x) == max(ax(b, x) for b in ARMS)]
    AXN = {"correctness": "correctness", "insight": "insight", "practical": "practical use", "risk": "risk awareness", "dissent": "dissent quality"}
    assert srt[:2] == ["warp-council", "wise-men"], srt
    warp_axes = [x for x in AXES if "warp-council" in best_on(x)]; assert warp_axes == ["correctness", "insight", "practical", "risk"], warp_axes
    assert best_on("dissent") == ["wise-men"]
    assert ax("wise-men", "correctness") < ax("direct", "correctness") and min(councils, key=lambda a: ax(a, "practical")) == "wise-men"
    six = [a for a in ARMS if a not in ("ecc-council", "warp-council")]
    m1 = {a: st.mean(r[a]["composite"] for r in V1.values()) for a in six}; drops = [m1[a] - S[a]["mean"] for a in six]
    o1 = sorted(six, key=lambda a: -m1[a]); o2 = sorted(six, key=lambda a: -S[a]["mean"]); sw = [a for a, b in zip(o1, o2) if a != b]
    assert all(d > 0 for d in drops) and sorted(sw) == ["lifeos-council", "llm-council"], (drops, o1, o2)
    spread = {a: S[a]["max"] - S[a]["min"] for a in councils}; assert max(spread, key=spread.get) == "ecc-council" and list(spread.values()).count(spread["ecc-council"]) == 1
    assert max(ARMS, key=lambda a: st.median(D[a])) == "warp-council"
    cut = {a: [q for q in R if normalize(a, open(os.path.join(H, "raw", q, a + ".md")).read()) != "\n".join(l for l in open(os.path.join(H, "raw", q, a + ".md")).read().split("\n") if not l.startswith("# ")).strip()] for a in ("ecc-council", "warp-council")}
    assert cut["ecc-council"] == [] and cut["warp-council"] == ["Q13", "Q36"], cut
    shape = [re.findall(r"^## (Recommendation|Why|Tradeoffs and risks|Final call)$", open(os.path.join(H, "raw", q, "warp-council.md")).read(), re.M) for q in R]
    assert all(x == ["Recommendation", "Why", "Tradeoffs and risks", "Final call"] for x in shape), shape
    ww, wt, wl = wtl(R, "wise-men", "warp-council"); v1_lead = st.mean(r["wise-men"]["composite"] for r in V1.values()) - st.mean(r["lifeos-council"]["composite"] for r in V1.values())
    L = ["# Head-to-head v2 results", "",
         "Generated by `H2H_STUDY=v2 python3 eval-data/head-to-head/h2h.py results` from `parsed-v2/` — the numbers here cannot drift from the data. Arms, questions, judge and analysis were fixed in [PREREG-2.md](PREREG-2.md), committed before either new arm ran and before any v2 judging (the six round-1 answers it reuses already existed). Installs from the skills.sh registry and stars from the GitHub API, both 2026-09-17 ([COMPETITOR-SCAN.md](COMPETITOR-SCAN.md)). v1 stands as published in [RESULTS.md](RESULTS.md).", "",
         "## Result", "",
         "| arm | source | mean /25 | vs plain | correctness | insight | practical | risk | dissent | lowest–highest | beat plain answer | top score (alone or shared) | wise-men vs it (W–T–L) |",
         "|---|---|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|--:|"]
    for a in srt:
        s = S[a]; d = s["mean"] - plain
        bp = f"{wtl(R, a, 'direct')[0]} of {n}" if a != "direct" else "—"
        vw = "–".join(map(str, wtl(R, "wise-men", a))) if a != "wise-men" else "—"
        name = f"**{NAMES[a]}**" if a == "wise-men" else NAMES[a]
        L.append(f"| {name} | {src[a]} | {one(s['mean'])} | {('+' if d >= 0 else '−') + one(abs(d)) if a != 'direct' else '—'} | " + " | ".join(one(s["axes"][x]) for x in AXES) + f" | {s['min']}–{s['max']} | {bp} | {s['top']} of {n} | {vw} |")
    L += ["", "Means over 8 questions are multiples of 0.125, so many land exactly on a half at two decimals; they are printed with Python's round-half-to-even (21.125 → 21.12). The README rounds to one decimal, half up (21.1).", "", "## Per question (total /25)", "", "| question | domain | " + " | ".join(NAMES[a] for a in srt) + " |", "|---|---|" + "--:|" * len(srt)]
    doms = {x["id"]: x["domain"] for x in (lambda d: d["questions"] if isinstance(d, dict) and "questions" in d else d)(yaml.safe_load(open(os.path.join(ROOT, "eval-data", "questions.yaml"))))}
    for q, r in R.items():
        top = max(r[a]["composite"] for a in ARMS)
        L.append(f"| {q} | {doms[q]} | " + " | ".join((f"**{r[a]['composite']}**" if r[a]["composite"] == top else str(r[a]["composite"])) for a in srt) + " |")
    L += ["", "Bold = top score on that question (ties bolded together).", "", "## What the numbers say — and what they don't", "",
          f"- **Warp's council had the highest mean** ({one(S['warp-council']['mean'])}) and the top score, alone or shared, on {S['warp-council']['top']} of {n} questions. It led on " + ", ".join(AXN[x] for x in warp_axes[:-1]) + f" and {AXN[warp_axes[-1]]}. wise-men was ahead of it on {ww} question{'s' if ww != 1 else ''}, tied on {wt} and behind on {wl}.",
          f"- **wise-men was second** ({one(S['wise-men']['mean'])}): ahead of " + (lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1])([f"{NAMES[a]} ({one(S[a]['mean'])})" for a in srt if a in councils and a not in ("warp-council", "wise-men")])
          + f". It beat the plain answer on {wtl(R, 'wise-men', 'direct')[0]} of {n} and had the highest dissent score of the eight arms ({one(ax('wise-men', 'dissent'))}).",
          f"- **Where wise-men lost ground.** Its correctness ({one(ax('wise-men', 'correctness'))}) was below the plain answer's ({one(ax('direct', 'correctness'))}), and its practical use ({one(ax('wise-men', 'practical'))}) was the lowest of the five councils. In 6 of 8 judgments (all but Q25 and Q36) the judge criticised process talk inside its answer — council meta, reviewer scores, model-routing notes — the same criticism as in v1 (7 of 8). All eight of Warp's answers share the same four core sections — recommendation, why, tradeoffs and risks, final call — and the judge called its member list noise on 4 of the 6 questions where the list was shown (Q09, Q19, Q25, Q55).",
          "- **Warp ran adapted, as pre-registered.** Its skill asks for a model-diverse council — an Opus-class, a GPT-class and an open-source model, launched by Warp's `run_agents` after the user approves the member list. Here every member was a Claude Code subagent on a Claude model, with no approval pause. Its intended setup could score differently, in either direction.",
          f"- **Every answer was re-judged.** The six v1 answers are byte-identical to v1's, yet the v2 judge, grading eight at a time, gave each of those six arms a lower mean than v1 did — by {min(drops):.1f} to {max(drops):.1f} points. Their order barely moved: only LifeOS Council and llm-council ({abs(S['llm-council']['mean'] - S['lifeos-council']['mean']):.2f} apart in v2) swapped places. Compare scores within a round, not across rounds.",
          f"- **ECC's council** tied LifeOS Council on the mean ({one(S['ecc-council']['mean'])}) and beat the plain answer on {wtl(R, 'ecc-council', 'direct')[0]} of {n}; its totals ranged from {S['ecc-council']['min']} to {S['ecc-council']['max']}, the widest spread of the five councils.",
          f"- **brainstorming and grilling** are built to interview the user before deciding; with nobody to answer they had to assume. They beat the plain answer on {wtl(R, 'brainstorming', 'direct')[0]} and {wtl(R, 'grilling', 'direct')[0]} of {n}. As in v1, this measures them on one-shot decisions, not on the interactive work they are designed for.",
          f"- **No significance test** — pre-registered: N={n}, one judge model, answers and judgments from the same model family. Warp's lead over wise-men (+{one(S['warp-council']['mean'] - S['wise-men']['mean'])}, ahead on {wl} of {n}) is larger than wise-men's v1 lead over the next council (+{one(v1_lead)}), but it is still one judge on eight questions.", "",
          "## Cost", "",
          "Wall-clock minutes per question, rounded half up. The six round-1 arms of a question ran at the same time, except the five round-1 re-runs (two at Q13, three at Q55), which ran separately; ECC and Warp ran four at a time (two questions, both councils). The load differed, so treat small gaps as noise:", "",
          "| arm | median | fastest | slowest |", "|---|--:|--:|--:|"]
    for a in srt:
        L.append(f"| {NAMES[a]} | {mins(st.median(D[a]))} | {mins(min(D[a]))} | {mins(max(D[a]))} |")
    L += ["", f"Warp's council was the slowest arm (median {mins(st.median(D['warp-council']))} minutes), then wise-men ({mins(st.median(D['wise-men']))}).", "",
          "## Deviations, all disclosed", "",
          "1. **Adaptations**, pre-registered in PREREG-2.md: Warp's council ran as described above; ECC's council stated the answer it assumed wherever it would have asked the user a question — the rule v1 applied to brainstorming and grilling. v1's own deviations (one amendment, five re-runs) are in RESULTS.md and carry over to the six reused answers.",
          f"2. **Normalization**, the same `normalize()` rules as v1: the `# ` provenance lines at the top, and a short passage before the first heading, are removed; nothing is reworded. Two effects to know about. (a) PREREG-2 says Warp's member plan stays in the output, but the status-line rule, also pre-registered, removed it on {' and '.join(cut['warp-council'])}, where the plan sat as a short paragraph before the first heading; on the other {n - len(cut['warp-council'])} it was a headed section and stayed. So the judge saw Warp's member list on {n - len(cut['warp-council'])} of {n} questions and called it noise on 4 of those {n - len(cut['warp-council'])}; if anything, the cut favoured Warp on {' and '.join(cut['warp-council'])}. (b) In both rounds the provenance rule also removed the one-line title brainstorming put at the top of its answers to Q13 and Q25 (a `# ` line directly under the header; on Q25 the title named the method). Nothing was removed from ECC's answers. The six v1 answers inside the v2 packets were checked byte for byte against the v1 packets.",
          "3. **Name redaction.** The author's first name, which subagents inherit from the author's global config, appeared in Warp's answer to Q09. It was redacted to \"the user\" in the raw file before blinding, so no judge saw it.",
          "4. **No re-runs.** All 16 new arm runs and all 8 judgments completed on the first attempt.",
          "5. **Parser fix.** `parse()` accepted response labels A–F only (v1 had six); it was widened to A–H before any v2 judgment was parsed. No v1 number changes, and `check.sh` verifies both rounds.",
          "6. **Provenance.** Every saved v2 answer and judgment was compared with the subagent transcript it came from; the only difference is the redaction in item 3.",
          "7. **Judge prompt vs PREREG.md** (applies to both rounds). PREREG.md describes the round-1 judge prompt as the N=29 eval's prompt extended from three to six slots. The five axes, the 1–5 scale and the summed total do match, but `judge-prompt-6.txt` also replaced the pairwise first pass with a ranking pass, dropped the per-score anchors (for example \"a response with no minority-view section caps at 2\" on dissent) and added \"Ignore length\". That prompt was committed a minute after PREREG.md, before the first judgment, and never changed; it was applied identically to every arm. `judge-prompt-8.txt` differs from it only in the response count, as PREREG-2 states.", "",
          "## Reproduce", "", "```bash", "H2H_STUDY=v2 python3 eval-data/head-to-head/h2h.py report    # the table above, in the terminal", "H2H_STUDY=v2 python3 eval-data/head-to-head/h2h.py results   # rewrites this file", "python3 scripts/make_charts.py                               # rewrites the charts in assets/", "```", ""]
    open(os.path.join(H, "RESULTS-V2.md"), "w").write("\n".join(L)); print("wrote RESULTS-V2.md")

def readme():
    # prints the README table for this round; check.sh verifies every line is present in README.md
    from decimal import Decimal, ROUND_HALF_UP
    r1 = lambda x: str(Decimal(str(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))
    R = rows(); S = stats(R); n = len(R); plain = S["direct"]["mean"]
    label = {"v1": {"wise-men": "**wise-men**", "lifeos-council": "[LifeOS Council](https://github.com/danielmiessler/LifeOS) 19k★", "llm-council": "[llm-council](https://github.com/aiwithremy/claude-skills-llm-council) 2.1k★",
                    "brainstorming": "[superpowers](https://github.com/obra/superpowers) brainstorming 288k★", "grilling": "[mattpocock](https://github.com/mattpocock/skills) grilling 264k★", "direct": "plain answer"},
             "v2": {"wise-men": "**wise-men**", "warp-council": "[Warp council](https://github.com/warpdotdev/common-skills) 24.5k installs", "llm-council": "[llm-council](https://github.com/aiwithremy/claude-skills-llm-council) 1.0k installs",
                    "lifeos-council": "[LifeOS Council](https://github.com/danielmiessler/LifeOS) 19k★", "ecc-council": "[ECC council](https://github.com/affaan-m/ECC) 7.7k installs",
                    "brainstorming": "[superpowers](https://github.com/obra/superpowers) brainstorming 366k installs", "grilling": "[mattpocock](https://github.com/mattpocock/skills) grilling 718k installs", "direct": "plain answer"}}[STUDY]
    order = ORDER if STUDY == "v1" else sorted(ARMS, key=lambda a: (-S[a]["mean"], ORDER.index(a)))
    val = lambda a, c: S[a]["mean"] if c == "total" else S[a]["axes"][c]
    best = {c: max(val(a, c) for a in ARMS) for c in ["total"] + AXES}
    bold = lambda txt, on: f"**{txt}**" if on else txt
    print("| vs plain answer | total /25 | correct | insight | practical | risk | dissent | beat plain |" if STUDY == "v1" else "| round 2 | total /25 (vs plain) | correct | insight | practical | risk | dissent | beat plain |")
    print("|---|--:|--:|--:|--:|--:|--:|--:|")
    for a in order:
        d = S[a]["mean"] - plain; tot = bold(r1(S[a]["mean"]), S[a]["mean"] == best["total"]) + ("" if a == "direct" else f" ({'+' if d >= 0 else '−'}{r1(abs(d))})")
        w = wtl(R, a, "direct")[0]; bp = "—" if a == "direct" else bold(f"{w} of {n}", w == n)
        print(f"| {label[a]} | {tot} | " + " | ".join(bold(r1(val(a, x)), val(a, x) == best[x]) for x in AXES) + f" | {bp} |")

if __name__ == "__main__":
    cmd = sys.argv[1]; {"blind": blind, "parse": parse, "report": report, "results": results, "readme": readme}[cmd](*sys.argv[2:])
