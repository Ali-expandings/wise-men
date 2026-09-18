#!/usr/bin/env python3
"""Regenerate the README charts as hand-authored SVG.

Run: python3 scripts/make_charts.py   (needs PyYAML only)

Every chart is written twice, <name>.svg for GitHub's light theme and <name>-dark.svg for dark; the README picks one
with <picture>. Head-to-head arm colours were checked for colour-blind separation in both themes (worst adjacent pair
dE 15.6 in OKLab x100 under protanopia/deuteranopia simulation; target >= 8). Text always uses neutral ink, never a
series colour: identity comes from the mark beside the text."""
import random, glob, math, os, statistics as st
from decimal import Decimal, ROUND_HALF_UP
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSED = os.path.join(ROOT, "eval-data", "parsed"); H2H = os.path.join(ROOT, "eval-data", "head-to-head", "parsed"); OUT = os.path.join(ROOT, "assets")
AXES = ["correctness", "insight", "practical", "risk", "dissent"]
AXIS_NAME = {"correctness": "Correctness", "insight": "Insight", "practical": "Practical use", "risk": "Risk awareness", "dissent": "Dissent quality"}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
THEMES = {
    "light": dict(ACCENT="#9e1b24", INK="#1f2328", TXT="#59636e", MUTE="#818b98", GRID="#d8dee4", SURF="#ffffff", PROMPT="#7d8ea5", DIRECT="#b9c2ce", PLAIN="#8c959f", OTHER="#8c959f", BAR2="#8c959f", AMBER="#d9a441",
                  ARM={"brainstorming": "#2a78d6", "grilling": "#eb6834", "lifeos-council": "#4a3aa7", "llm-council": "#eda100"}),
    "dark": dict(ACCENT="#b8323a", INK="#e6edf3", TXT="#9198a1", MUTE="#6e7681", GRID="#262c36", SURF="#0d1117", PROMPT="#7d8ea5", DIRECT="#4b535d", PLAIN="#656c76", OTHER="#6e7681", BAR2="#7d8590", AMBER="#d9a441",
                 ARM={"brainstorming": "#3987e5", "grilling": "#d95926", "lifeos-council": "#9085e9", "llm-council": "#c98500"}),
}
C = dict(THEMES["light"])  # active theme

# Head-to-head arms. Bar order = the validated colour order: plain answer first (the baseline), wise-men last.
H_ARMS = ["direct", "brainstorming", "grilling", "lifeos-council", "llm-council", "wise-men"]
H_NAME = {"direct": "plain answer", "brainstorming": "brainstorming", "grilling": "grilling", "lifeos-council": "LifeOS Council", "llm-council": "llm-council", "wise-men": "wise-men"}
H_SRC = {"direct": "no skill", "brainstorming": "obra/superpowers · 288k★ repo", "grilling": "mattpocock/skills · 264k★ repo",
         "lifeos-council": "danielmiessler/LifeOS · 19k★ repo", "llm-council": "aiwithremy · 2.1k★", "wise-men": "this repo"}
# Round 2 (PREREG-2): the six round-1 arms plus the two most-installed general-purpose council skills. Colour marks only wise-men; every bar is labelled.
H2H2 = os.path.join(ROOT, "eval-data", "head-to-head", "parsed-v2")
H2_ARMS = ["direct", "brainstorming", "grilling", "lifeos-council", "llm-council", "ecc-council", "warp-council", "wise-men"]
H_NAME.update({"ecc-council": "ECC council", "warp-council": "Warp council"})
H2_SRC = {"direct": "no skill", "brainstorming": "obra/superpowers · 366k installs", "grilling": "mattpocock/skills · 718k installs", "lifeos-council": "danielmiessler/LifeOS · 19k★",
          "llm-council": "aiwithremy · 1.0k installs", "ecc-council": "affaan-m/ECC · 7.7k installs", "warp-council": "warpdotdev · 24.5k installs", "wise-men": "this repo"}
TOPIC = {"Q05": "Monolith or microservices?", "Q09": "Why event sourcing gets messy", "Q13": "Entering a market with one giant", "Q19": "Per-seat or usage pricing?",
         "Q25": "Why replications fail", "Q36": "Blameless yet accountable postmortem", "Q48": "Colleagues underpaid, HR did nothing", "Q55": "A PhD at 35?"}

def num(v): return f"{v:.1f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)
def r1(x): return str(Decimal(str(x)).quantize(Decimal("0.1"), ROUND_HALF_UP))
def esc(s): return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
def svg(w, h, body, title): return f'<svg viewBox="0 0 {num(w)} {num(h)}" width="{num(w)}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">\n<title>{esc(title)}</title>\n{body}</svg>\n'
def t(x, y, s, size=12, fill=None, weight=400, anchor="start", extra=""):
    return f'<text x="{num(x)}" y="{num(y)}" font-size="{size}" font-weight="{weight}" fill="{fill or C["TXT"]}" text-anchor="{anchor}" {extra}>{esc(s)}</text>\n'
def line(x1, y1, x2, y2, col, w=1, extra=""): return f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" stroke="{col}" stroke-width="{w}" {extra}/>\n'
def hbar(x, y, w, h, fill, r=4):  # grows right from the baseline; rounded data end, square at the baseline
    if w <= 0: return ""
    r = min(r, w, h / 2)
    return f'<path d="M{num(x)},{num(y)}h{num(w - r)}a{num(r)},{num(r)} 0 0 1 {num(r)},{num(r)}v{num(h - 2 * r)}a{num(r)},{num(r)} 0 0 1 -{num(r)},{num(r)}h-{num(w - r)}z" fill="{fill}"/>\n'
def vbar(x, base, w, h, fill, r=4):  # grows up from the baseline; rounded top
    if h <= 0: return ""
    r = min(r, h, w / 2)
    return f'<path d="M{num(x)},{num(base)}v-{num(h - r)}a{num(r)},{num(r)} 0 0 1 {num(r)},-{num(r)}h{num(w - 2 * r)}a{num(r)},{num(r)} 0 0 1 {num(r)},{num(r)}v{num(h - r)}z" fill="{fill}"/>\n'
def dot(cx, cy, r, fill): return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{r}" fill="{fill}" stroke="{C["SURF"]}" stroke-width="2"/>\n'
def ring(cx, cy, r, col): return f'<circle cx="{num(cx)}" cy="{num(cy)}" r="{r}" fill="none" stroke="{col}" stroke-width="1.6"/>\n'
def swatch(x, y, fill): return f'<rect x="{num(x)}" y="{num(y)}" width="12" height="12" rx="3" fill="{fill}"/>\n'
def hbar_outline(x, y, w, h, col, r=4):  # the plain answer: same shape as hbar, outline only
    if w <= 0: return ""
    x, y, w, h = x + 0.75, y + 0.75, w - 1.5, h - 1.5; r = min(r, w, h / 2)
    return f'<path d="M{num(x)},{num(y)}h{num(w - r)}a{num(r)},{num(r)} 0 0 1 {num(r)},{num(r)}v{num(h - 2 * r)}a{num(r)},{num(r)} 0 0 1 -{num(r)},{num(r)}h-{num(w - r)}z" fill="none" stroke="{col}" stroke-width="1.5"/>\n'
def band(y, h): return f'<rect x="32" y="{num(y)}" width="816" height="{num(h)}" rx="6" fill="{C["ACCENT"]}" fill-opacity="0.08"/>\n'
def dashed(x1, y1, x2, y2): return line(x1, y1, x2, y2, C["INK"], 1, 'stroke-opacity="0.55" stroke-dasharray="4 3"')

# ---------- N=29 eval (council vs structured prompt vs direct) ----------
def arms29(): return [("arm_c", "wise-men council", C["ACCENT"]), ("arm_b", "structured single prompt", C["PROMPT"]), ("arm_a", "direct answer", C["DIRECT"])]
def load():
    rows = {}; keys = ["arm_c", "arm_b", "arm_a"]
    for f in sorted(glob.glob(os.path.join(PARSED, "Q*.yaml"))):
        if "tiebreaker" in f: continue
        txt = open(f).read(); d = yaml.safe_load(txt); q = d["question_id"]
        comp = {a: d["arms"][a]["composite_5axis"] for a in keys}
        if all(isinstance(d["arms"][a], dict) and "correctness" in d["arms"][a] for a in keys):
            axes = {a: {x: d["arms"][a][x] for x in AXES} for a in keys}
        else:
            import re
            m = re.search(r"blinding_map[^:]*:\s*([XYZ]=[ABC](?:,\s*[XYZ]=[ABC]){2})", txt)
            s2a = {s: "arm_" + a.lower() for s, a in (p.split("=") for p in m.group(1).replace(" ", "").split(","))}
            axes = {}
            for s, arm in s2a.items():
                assert d["slots"][s]["composite_5axis"] == comp[arm], (q, s)
                axes[arm] = {x: d["slots"][s][x] for x in AXES}
        rows[q] = {"comp": comp, "axes": axes}
    assert len(rows) == 29, len(rows); return rows

def ci95(xs): return st.mean(xs), 2.048 * st.stdev(xs) / math.sqrt(len(xs))

def chart_headline(rows):
    W, H = 860, 250; x0, x1 = 240, 800; sc = (x1 - x0) / 25
    b = t(x0, 30, "Same 29 questions, three ways of answering", 16, C["INK"], 600)
    b += t(x0, 50, "Blind judge · 5-axis rubric, max 25 · mean with 95% confidence interval", 12, C["TXT"])
    for g in range(0, 26, 5):
        b += line(x0 + g * sc, 66, x0 + g * sc, 200, C["GRID"]) + t(x0 + g * sc, 218, g, 11, C["MUTE"], anchor="middle")
    for i, (arm, label, col) in enumerate(arms29()):
        y = 84 + i * 44; m, h = ci95([r["comp"][arm] for r in rows.values()]); hero = arm == "arm_c"
        b += t(x0 - 16, y + 17, label, 14, C["INK"] if hero else C["TXT"], 700 if hero else 400, "end")
        b += hbar(x0, y, m * sc, 26, col)
        b += line(x0 + (m - h) * sc, y + 13, x0 + (m + h) * sc, y + 13, C["INK"], 2, 'stroke-opacity="0.6"')
        b += t(x0 + (m + h) * sc + 12, y + 19, f"{m:.1f}", 18, C["INK"] if arm != "arm_a" else C["TXT"], 700)
    b += t(x0, 240, "Council beat the structured prompt on 28 of 29 questions. Data: eval-data/parsed · script: scripts/make_charts.py", 11, C["MUTE"])
    return svg(W, H, b, "Council 24.5 vs structured prompt 20.8 vs direct answer 16.3 on a 25-point blind rubric, N=29")

def chart_axes(rows):
    W, H = 860, 364; y0, y1 = 96, 304; sc = (y1 - y0) / 5
    sig = {"correctness": "no difference", "insight": "p < 0.001", "practical": "p < 0.001", "risk": "p < 0.001", "dissent": "p < 0.001"}
    b = t(40, 30, "Where the gap comes from — per rubric axis", 16, C["INK"], 600)
    b += t(40, 50, "Mean score 1–5 · council vs structured prompt, two-sided Wilcoxon, Bonferroni α = 0.01", 12, C["TXT"])
    lx = 40
    for arm, label, col in arms29():
        b += swatch(lx, 62, col) + t(lx + 17, 72, label, 12, C["TXT"]); lx += 17 + 6.6 * len(label) + 22
    for g in range(6):
        y = y1 - g * sc; b += line(40, y, 820, y, C["GRID"]) + t(32, y + 4, g, 11, C["MUTE"], anchor="end")
    gw = 156; bw = 34
    for i, ax in enumerate(AXES):
        gx = 60 + i * gw
        for k, (arm, _, col) in enumerate(arms29()):
            m = st.mean(r["axes"][arm][ax] for r in rows.values()); x = gx + k * (bw + 6)
            b += vbar(x, y1, bw, m * sc, col) + t(x + bw / 2, y1 - m * sc - 6, f"{m:.1f}", 12, C["INK"] if arm == "arm_c" else C["TXT"], 600, "middle")
        cx = gx + (3 * bw + 12) / 2
        b += t(cx, y1 + 20, ax, 13, C["INK"], 500, "middle") + t(cx, y1 + 38, sig[ax], 11, C["INK"] if sig[ax] != "no difference" else C["MUTE"], 400, "middle")
    b += t(40, 354, "Correctness is a tie; the council's edge is insight, practical usefulness, risk awareness, and above all dissent.", 11, C["MUTE"])
    return svg(W, H, b, "Per-axis means for council, structured prompt, and direct answer")

def chart_questions(rows):
    items = sorted(rows.items(), key=lambda kv: kv[1]["comp"]["arm_c"] - kv[1]["comp"]["arm_b"]); rh = 21
    W, H = 860, 96 + rh * len(items) + 40; x0, x1 = 120, 820; sc = (x1 - x0) / 13; A = arms29()
    b = t(40, 30, "Every question, council vs structured prompt", 16, C["INK"], 600)
    b += t(40, 50, "Sorted by gap · score out of 25 · council ahead on 28 of 29", 12, C["TXT"])
    for g in range(12, 26, 2):
        x = x0 + (g - 12) * sc; b += line(x, 70, x, H - 40, C["GRID"]) + t(x, H - 22, g, 11, C["MUTE"], anchor="middle")
    for i, (q, r) in enumerate(items):
        y = 84 + i * rh; bx = x0 + (r["comp"]["arm_b"] - 12) * sc; cx = x0 + (r["comp"]["arm_c"] - 12) * sc
        b += t(x0 - 14, y + 4, q, 11, C["MUTE"], anchor="end") + line(bx, y, cx, y, C["TXT"], 2, 'stroke-opacity="0.35"')
        b += dot(bx, y, 5, A[1][2]) + dot(cx, y, 5.5, A[0][2])
        if r["comp"]["arm_c"] < r["comp"]["arm_b"]: b += t(cx - 12, y + 4, "the one loss — dissent re-argued the majority", 11, C["INK"], anchor="end")
    b += dot(x0 + 2, H - 8, 5, A[0][2]) + t(x0 + 12, H - 4, "council", 11) + dot(x0 + 82, H - 8, 5, A[1][2]) + t(x0 + 92, H - 4, "structured prompt", 11)
    return svg(W, H, b, "Council vs structured prompt on each of 29 questions")

def label_lines(nm):  # column header: one line if short, else split at the space or at the hyphen that balances the two lines
    if len(nm) <= 9: return [nm]
    if " " in nm: i = nm.find(" "); return [nm[:i], nm[i + 1:]]
    k = min((k for k, ch in enumerate(nm) if ch == "-"), key=lambda k: max(k + 1, len(nm) - k - 1)); return [nm[:k + 1], nm[k + 1:]]
def chart_landscape():
    cols = [("wise-men", ""), ("llm-council skill", "aiwithremy"), ("llm-council-skill", "tenfoldmarc"), ("council-review", "ngmeyer"), ("agent-review-panel", "wan-huiyan"), ("Warp council", "warpdotdev"), ("ECC council", "affaan-m"), ("llm-council", "karpathy")]
    feats = [("Independent members, no API keys", [2, 2, 2, 2, 2, 2, 2, 0]), ("Rubric peer review, machine-parsed", [2, 1, 1, 1, 1, 0, 0, 1]), ("Debate on a mechanical trigger", [2, 0, 1, 2, 2, 1, 1, 0]),
             ("Dissent verbatim, cannot be truncated", [2, 1, 1, 2, 1, 1, 1, 0]), ("Independent check of the synthesis", [2, 0, 0, 0, 1, 0, 0, 0]), ("Members structurally unable to spawn or run", [2, 0, 0, 0, 1, 1, 0, 0]),
             ("Cost tiers + spend ceiling", [2, 0, 0, 1, 1, 0, 0, 0]), ("Every deviation disclosed in output", [2, 0, 0, 0, 0, 1, 0, 0]), ("Eval data + script shipped in repo", [2, 0, 0, 1, 1, 0, 0, 0])]
    W = 860; rh = 34; x0 = 300; cw = (W - x0 - 20) / len(cols); H = 120 + rh * len(feats) + 40
    b = t(40, 30, "Council skills for Claude Code — what each one ships", 16, C["INK"], 600) + t(40, 50, "From each project's README or skill file, 2026-09-16/17 · full table with sources in resources/landscape.md", 12, C["TXT"])
    for j, (nm, o) in enumerate(cols):
        cx = x0 + cw * (j + 0.5); parts = label_lines(nm)
        for li, part in enumerate(parts): b += t(cx, 78 + li * 13, part, 10.5, C["INK"] if j == 0 else C["TXT"], 700 if j == 0 else 500, "middle")
        if o: b += t(cx, 78 + len(parts) * 13, o, 10, C["MUTE"], anchor="middle")
    b += f'<rect x="{num(x0)}" y="62" width="{num(cw)}" height="{rh * len(feats) + 58}" rx="8" fill="{C["ACCENT"]}" fill-opacity="0.10"/>\n'
    for i, (name, vals) in enumerate(feats):
        y = 120 + i * rh + rh / 2; b += t(x0 - 16, y + 4, name, 12, C["INK"], anchor="end") + line(40, y + rh / 2, W - 20, y + rh / 2, C["GRID"])
        for j, v in enumerate(vals):
            cx = x0 + cw * (j + 0.5)
            b += {2: f'<circle cx="{num(cx)}" cy="{num(y)}" r="7" fill="{C["ACCENT"]}"/>', 1: f'<circle cx="{num(cx)}" cy="{num(y)}" r="7" fill="{C["AMBER"]}"/>', 0: ring(cx, y, 6, C["MUTE"])}[v]
    ly = H - 16
    b += f'<circle cx="46" cy="{ly - 4}" r="6" fill="{C["ACCENT"]}"/>' + t(58, ly, "yes", 11) + f'<circle cx="106" cy="{ly - 4}" r="6" fill="{C["AMBER"]}"/>' + t(118, ly, "partial or unspecified", 11) + ring(256, ly - 4, 5.5, C["MUTE"]) + t(268, ly, "absent", 11)
    return svg(W, H, b, "Feature matrix of council skills for Claude Code")

# ---------- head-to-head (8 questions, 6 arms) ----------
def load_h2h():
    rows = {os.path.basename(f)[:-5]: yaml.safe_load(open(f))["arms"] for f in sorted(glob.glob(os.path.join(H2H, "Q*.yaml")))}
    assert len(rows) == 8 and all(set(r) == set(H_ARMS) for r in rows.values()), len(rows); return rows
def hmean(rows, a, key="composite"): return st.mean(r[a][key] for r in rows.values())
def colour(a): return C["ACCENT"] if a == "wise-men" else C["PLAIN"] if a == "direct" else C["ARM"][a]

def chart_h2h(rows):
    x0, sc, top, rh, n = 250, 15.6, 112, 46, len(rows)
    arms = sorted(H_ARMS, key=lambda a: -hmean(rows, a)); plain = hmean(rows, "direct"); bottom = top + rh * len(arms) - 6
    b = t(40, 32, f"Round 1: total score vs a plain answer — {n} hard questions, one blind judge", 16, C["INK"], 600)
    b += t(40, 52, "Sum of 5 rubric axes (1–5 each, max 25), averaged over the 8 questions. In brackets: the gap to the plain answer.", 12, C["TXT"])
    b += t(40, 68, "The other four are popular skills people already use to think a decision through.", 12, C["TXT"])
    b += t(840, top - 12, "beat the plain answer", 11, C["MUTE"], anchor="end")
    for g in range(0, 26, 5):
        x = x0 + g * sc; b += line(x, top - 4, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    for i, a in enumerate(arms):
        y = top + i * rh; m = hmean(rows, a); hero = a == "wise-men"
        b += t(x0 - 14, y + 15, H_NAME[a], 13, C["INK"], 700 if hero else 500, "end") + t(x0 - 14, y + 30, H_SRC[a], 11, C["MUTE"], anchor="end")
        b += hbar(x0, y + 6, m * sc, 22, colour(a))
        vx = x0 + m * sc + 8; b += t(vx, y + 22, r1(m), 13, C["INK"], 700 if hero else 500)
        if a == "direct":
            b += t(840, y + 22, "—", 12, C["MUTE"], anchor="end"); continue
        d = m - plain; b += t(vx + 32, y + 22, f"({'+' if d >= 0 else '−'}{r1(abs(d))})", 11, C["TXT"])
        wins = sum(r[a]["composite"] > r["direct"]["composite"] for r in rows.values())
        b += t(840, y + 22, f"{wins} of {n}", 12, C["INK"] if wins == n else C["TXT"], 600 if wins == n else 400, "end")
    px = x0 + plain * sc; b += dashed(px, top - 4, px, bottom) + t(px, top - 12, f"plain answer {r1(plain)}", 11, C["MUTE"], anchor="middle")
    fy = bottom + 42
    b += t(40, fy, "brainstorming and grilling are built to interview you first; with nobody to answer, they had to assume (pre-registered, disclosed).", 11, C["MUTE"])
    b += t(40, fy + 16, f"N = {n}, no significance claimed · one top-level model ran every arm · the judge saw answers as A–F in a sealed order · raw data: eval-data/head-to-head", 11, C["MUTE"])
    return svg(860, fy + 30, b, "Round 1 mean total score out of 25 on 8 blind-judged questions: " + ", ".join(f"{H_NAME[a]} {r1(hmean(rows, a))}" for a in arms))

def chart_h2h_axes(rows):
    y1, sc, n = 340, 40, len(rows)
    b = t(40, 32, "Round 1: where the gap comes from — each rubric axis", 16, C["INK"], 600)
    b += t(40, 52, f"Mean score per axis, 1–5, over the same {n} questions · dashed line = the plain answer on that axis", 12, C["TXT"])
    lx = 40
    for a in H_ARMS:
        hero = a == "wise-men"; b += swatch(lx, 72, colour(a)) + t(lx + 17, 82, H_NAME[a], 12, C["INK"] if hero else C["TXT"], 700 if hero else 400); lx += 17 + 6.8 * len(H_NAME[a]) + 22
    for g in range(6):
        y = y1 - g * sc; b += line(56, y, 840, y, C["GRID"]) + t(46, y + 4, g, 11, C["MUTE"], anchor="end")
    bw, gap = 16, 3; gw = len(H_ARMS) * bw + (len(H_ARMS) - 1) * gap; pitch = (840 - 64) / len(AXES)
    for i, ax in enumerate(AXES):
        gx = 64 + i * pitch + (pitch - gw) / 2; m = {a: hmean(rows, a, ax) for a in H_ARMS}
        for k, a in enumerate(H_ARMS): b += vbar(gx + k * (bw + gap), y1, bw, m[a] * sc, colour(a))
        py = y1 - m["direct"] * sc; b += dashed(gx - 5, py, gx + gw + 5, py) + t(gx + bw / 2, py - 6, r1(m["direct"]), 10, C["MUTE"], anchor="middle")
        b += t(gx + gw - bw / 2, y1 - m["wise-men"] * sc - 6, r1(m["wise-men"]), 11, C["INK"], 700, "middle")
        d = m["wise-men"] - m["direct"]
        b += t(gx + gw / 2, y1 + 22, AXIS_NAME[ax], 13, C["INK"], 600, "middle")
        b += t(gx + gw / 2, y1 + 39, "wise-men level with plain" if abs(d) < 0.05 else f"wise-men +{r1(d)} over plain", 11, C["TXT"], anchor="middle")
    perfect = [AXIS_NAME[x].lower() for x in AXES if all(r["wise-men"][x] == 5 for r in rows.values())]
    others_perfect = any(all(r[a][x] == 5 for r in rows.values()) for a in H_ARMS if a != "wise-men" for x in AXES)
    top_c = [H_NAME[a] for a in H_ARMS if hmean(rows, a, "correctness") == max(hmean(rows, z, "correctness") for z in H_ARMS)]
    lead_p = max(H_ARMS, key=lambda a: hmean(rows, a, "practical"))
    b += t(40, y1 + 72, f"wise-men scored 5 on {' and '.join(perfect)} on all {n} questions" + ("; no other arm did that on any axis." if not others_perfect else "."), 11, C["MUTE"])
    b += t(40, y1 + 88, f"It did not lead everywhere: correctness was a tie ({', '.join(top_c)}), and {H_NAME[lead_p]} was rated most practical ({r1(hmean(rows, lead_p, 'practical'))} vs wise-men {r1(hmean(rows, 'wise-men', 'practical'))}).", 11, C["MUTE"])
    return svg(860, y1 + 104, b, "Round 1 per-axis mean scores for six arms: " + "; ".join(f"{AXIS_NAME[x]}: " + ", ".join(f"{H_NAME[a]} {r1(hmean(rows, a, x))}" for a in H_ARMS) for x in AXES))

def chart_h2h_questions(rows):
    x0, x1, lo, hi = 300, 640, 13, 25; sc = (x1 - x0) / (hi - lo); top, rh = 112, 32; qs = sorted(rows); n = len(qs)
    others = ["brainstorming", "grilling", "lifeos-council", "llm-council"]
    short = {"brainstorming": "brainstorming", "grilling": "grilling", "lifeos-council": "LifeOS", "llm-council": "llm-council"}
    wm_min = min(r["wise-men"]["composite"] for r in rows.values()); bottom = top + rh * (n - 1) + 16
    b = t(40, 32, f"Round 1, question by question — wise-men never scored below {wm_min} of 25", 16, C["INK"], 600)
    b += t(40, 52, "Each row: wise-men, the four other skills and the plain answer, as scored by the blind judge (max 25)", 12, C["TXT"])
    b += t(660, top - 22, "vs the best other skill", 11, C["MUTE"])
    for g in (15, 20, 25):
        x = x0 + (g - lo) * sc; b += line(x, top - 16, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    won = tied = lost = 0
    for i, q in enumerate(qs):
        y = top + i * rh; r = rows[q]; vals = [r[a]["composite"] for a in H_ARMS]; wm = r["wise-men"]["composite"]
        b += t(40, y + 4, q, 11, C["MUTE"]) + t(76, y + 4, TOPIC[q], 12, C["INK"])
        b += line(x0 + (min(vals) - lo) * sc, y, x0 + (max(vals) - lo) * sc, y, C["GRID"], 2)
        b += ring(x0 + (r["direct"]["composite"] - lo) * sc, y, 7, C["TXT"])
        for a in others: b += dot(x0 + (r[a]["composite"] - lo) * sc, y, 4.5, C["OTHER"])
        b += dot(x0 + (wm - lo) * sc, y, 6.5, C["ACCENT"])
        bv = max(r[a]["composite"] for a in others); best = [short[a] for a in others if r[a]["composite"] == bv]
        rel = "ahead" if wm > bv else "tied" if wm == bv else "behind"; won += wm > bv; tied += wm == bv; lost += wm < bv
        b += t(660, y + 4, rel, 12, C["INK"]) + t(712, y + 4, f"{', '.join(best)} {bv}", 11, C["MUTE"])
    ly = bottom + 44
    b += dot(46, ly - 4, 6.5, C["ACCENT"]) + t(58, ly, "wise-men", 11) + dot(136, ly - 4, 4.5, C["OTHER"]) + t(146, ly, "the other four skills", 11) + ring(284, ly - 4, 7, C["TXT"]) + t(296, ly, "plain answer", 11)
    mins = [min(r[a]["composite"] for r in rows.values()) for a in others]
    b += t(40, ly + 22, f"Against the best of the other four on each question: ahead {won}, tied {tied}, behind {lost}. Their lowest scores were {min(mins)}–{max(mins)}; wise-men's was {wm_min}.", 11, C["MUTE"])
    return svg(860, ly + 38, b, f"Round 1 per-question scores: wise-men lowest {wm_min} of 25; versus the best other skill ahead {won}, tied {tied}, behind {lost}")

def load_h2h2():
    rows = {os.path.basename(f)[:-5]: yaml.safe_load(open(f))["arms"] for f in sorted(glob.glob(os.path.join(H2H2, "Q*.yaml")))}
    assert len(rows) == 8 and all(set(r) == set(H2_ARMS) for r in rows.values()), len(rows); return rows
def by_total(rows): return sorted(H2_ARMS, key=lambda a: (-hmean(rows, a), H2_ARMS.index(a)))
def bar2(a, x, y, w, h, r=4): return hbar_outline(x, y, w, h, C["TXT"], r) if a == "direct" else hbar(x, y, w, h, C["ACCENT"] if a == "wise-men" else C["BAR2"], r)

def chart_h2h_v2(rows):
    x0, sc, top, rh, n = 250, 15.6, 112, 46, len(rows)
    arms = by_total(rows); plain = hmean(rows, "direct"); bottom = top + rh * len(arms) - 6
    b = t(40, 32, f"Round 2: total score vs a plain answer — {n} hard questions, one blind judge", 16, C["INK"], 600)
    b += t(40, 52, "Sum of 5 rubric axes (1–5 each, max 25), averaged over the 8 questions. In brackets: the gap to the plain answer.", 12, C["TXT"])
    b += t(40, 68, "Round 2 added the two most-installed general-purpose council skills, Warp's and ECC's, and re-judged every answer.", 12, C["TXT"])
    b += t(840, top - 12, "beat the plain answer", 11, C["MUTE"], anchor="end")
    for g in range(0, 26, 5):
        x = x0 + g * sc; b += line(x, top - 4, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    for i, a in enumerate(arms):
        y = top + i * rh; m = hmean(rows, a); hero = a == "wise-men"
        if hero: b += band(y - 3, rh - 2)
        b += t(x0 - 14, y + 15, H_NAME[a], 13, C["INK"], 700 if hero else 500, "end") + t(x0 - 14, y + 30, H2_SRC[a], 11, C["MUTE"], anchor="end")
        b += bar2(a, x0, y + 6, m * sc, 22)
        vx = x0 + m * sc + 8; b += t(vx, y + 22, r1(m), 13, C["INK"], 700 if hero else 500)
        if a == "direct":
            b += t(840, y + 22, "—", 12, C["MUTE"], anchor="end"); continue
        d = m - plain; b += t(vx + 32, y + 22, f"({'+' if d >= 0 else '−'}{r1(abs(d))})", 11, C["TXT"])
        wins = sum(r[a]["composite"] > r["direct"]["composite"] for r in rows.values())
        b += t(840, y + 22, f"{wins} of {n}", 12, C["INK"] if wins == n else C["TXT"], 600 if wins == n else 400, "end")
    px = x0 + plain * sc; b += dashed(px, top - 4, px, bottom) + t(px, top - 12, f"plain answer {r1(plain)}", 11, C["MUTE"], anchor="middle")
    fy = bottom + 42
    b += t(40, fy, "Warp's council ran on Claude models only; its skill asks for a model-diverse council (pre-registered, disclosed).", 11, C["MUTE"])
    b += t(40, fy + 16, "brainstorming and grilling are built to interview you first; with nobody to answer, they had to assume.", 11, C["MUTE"])
    b += t(40, fy + 32, f"N = {n}, no significance claimed · one top-level model ran every arm · the judge saw answers as A–H in a sealed order · raw data: eval-data/head-to-head", 11, C["MUTE"])
    return svg(860, fy + 46, b, "Round 2 mean total score out of 25 on 8 blind-judged questions: " + ", ".join(f"{H_NAME[a]} {r1(hmean(rows, a))}" for a in arms))

def chart_h2h_v2_axes(rows):
    n = len(rows); arms = by_total(rows); top, rh = 118, 34
    cols = [("composite", "Total /25", 25, 222, 80)] + [(x, AXIS_NAME[x], 5, 364 + k * 94, 46) for k, x in enumerate(AXES)]
    b = t(40, 32, "Round 2 scoreboard — the total and each rubric axis", 16, C["INK"], 600)
    b += t(40, 52, f"Mean over the same {n} questions · total out of 25, each axis 1–5 · sorted by total · the plain answer is the outlined bar", 12, C["TXT"])
    for key, title, mx, x, w in cols: b += t(x, top - 14, title, 11, C["INK"], 600)
    best = {key: max(hmean(rows, a, key) for a in arms) for key, *_ in cols}
    for i, a in enumerate(arms):
        y = top + i * rh; yc = y + rh / 2; hero = a == "wise-men"
        if hero: b += band(y + 2, rh - 4)
        b += t(206, yc + 4, H_NAME[a], 13, C["INK"], 700 if hero else 500, "end")
        for key, title, mx, x, w in cols:
            v = hmean(rows, a, key); top_v = abs(v - best[key]) < 1e-9
            b += f'<rect x="{num(x)}" y="{num(yc - 5)}" width="{num(w)}" height="10" rx="3" fill="{C["GRID"]}" fill-opacity="0.6"/>\n'
            b += bar2(a, x, yc - 5, v / mx * w, 10, 3)
            b += t(x + w + 8, yc + 4, r1(v), 12, C["INK"] if top_v else C["TXT"], 700 if top_v else 400)
    leaders = {key: [H_NAME[a] for a in arms if abs(hmean(rows, a, key) - best[key]) < 1e-9] for key, *_ in cols}
    wm_lead = [AXIS_NAME[x].lower() for x in AXES if "wise-men" in leaders[x]]
    top_arm = arms[0]; top_lead = [AXIS_NAME[x].lower() for x in AXES if H_NAME[top_arm] in leaders[x]]
    fy = top + rh * len(arms) + 28
    b += t(40, fy, f"Bold = highest in the column (ties bolded together). wise-men had the top score on {' and '.join(wm_lead) or 'no axis'}; "
                   f"{H_NAME[top_arm]} led the total and {len(top_lead)} of the 5 axes.", 11, C["MUTE"])
    b += t(40, fy + 16, f"Warp's council ran on Claude models only; its skill asks for a model-diverse council. N = {n}, one blind judge per question, no significance claimed.", 11, C["MUTE"])
    return svg(860, fy + 30, b, "Round 2 scoreboard, means over 8 questions: " + "; ".join(f"{H_NAME[a]}: total {r1(hmean(rows, a))}, " + ", ".join(f"{AXIS_NAME[x].lower()} {r1(hmean(rows, a, x))}" for x in AXES) for a in arms))

def chart_h2h_v2_questions(rows):
    x0, x1, lo, hi = 300, 640, 10, 25; sc = (x1 - x0) / (hi - lo); top, rh = 112, 32; qs = sorted(rows); n = len(qs)
    others = [a for a in H2_ARMS if a not in ("direct", "wise-men")]
    short = {"brainstorming": "brainstorming", "grilling": "grilling", "lifeos-council": "LifeOS", "llm-council": "llm-council", "ecc-council": "ECC", "warp-council": "Warp"}
    bottom = top + rh * (n - 1) + 16
    b = t(40, 32, "Round 2, question by question", 16, C["INK"], 600)
    b += t(40, 52, "Each row: the blind judge's total (max 25) for wise-men, the six other skills and the plain answer", 12, C["TXT"])
    b += t(660, top - 22, "wise-men vs the best other skill", 11, C["MUTE"])
    for g in (10, 15, 20, 25):
        x = x0 + (g - lo) * sc; b += line(x, top - 16, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    won = tied = lost = 0
    for i, q in enumerate(qs):
        y = top + i * rh; r = rows[q]; vals = [r[a]["composite"] for a in H2_ARMS]; wm = r["wise-men"]["composite"]
        b += t(40, y + 4, q, 11, C["MUTE"]) + t(76, y + 4, TOPIC[q], 12, C["INK"])
        b += line(x0 + (min(vals) - lo) * sc, y, x0 + (max(vals) - lo) * sc, y, C["GRID"], 2)
        b += ring(x0 + (r["direct"]["composite"] - lo) * sc, y, 7, C["TXT"])
        for a in others: b += dot(x0 + (r[a]["composite"] - lo) * sc, y, 4.5, C["OTHER"])
        b += dot(x0 + (wm - lo) * sc, y, 6.5, C["ACCENT"])
        bv = max(r[a]["composite"] for a in others); best = [short[a] for a in others if r[a]["composite"] == bv]
        rel = "ahead" if wm > bv else "tied" if wm == bv else "behind"; won += wm > bv; tied += wm == bv; lost += wm < bv
        b += t(660, y + 4, rel, 12, C["INK"]) + t(712, y + 4, f"{', '.join(best)} {bv}", 11, C["MUTE"])
    ly = bottom + 44
    b += dot(46, ly - 4, 6.5, C["ACCENT"]) + t(58, ly, "wise-men", 11) + dot(136, ly - 4, 4.5, C["OTHER"]) + t(146, ly, "the other six skills", 11) + ring(276, ly - 4, 7, C["TXT"]) + t(288, ly, "plain answer", 11)
    top_w = sum(r["warp-council"]["composite"] == max(r[a]["composite"] for a in H2_ARMS) for r in rows.values())
    b += t(40, ly + 22, f"Against the best of the other six on each question: ahead {won}, tied {tied}, behind {lost}. Warp's council had the top score, alone or shared, on {top_w} of {n}.", 11, C["MUTE"])
    return svg(860, ly + 38, b, f"Round 2 per-question scores: wise-men versus the best other skill ahead {won}, tied {tied}, behind {lost}; Warp's council top on {top_w} of {n}")

# ---------- banner: the council in pixel art, one 5 px grid, three-tone shading per material, dark-red theme ----------
BU, B_OUTLINE = 5, "#120b09"
B_RAMP = {  # material: highlight, base, shadow
    "O": ("#e89272", "#d97757", "#a6563b"), "L": ("#a6563b", "#8c4730", "#6e3624"), "C": ("#474d57", "#30353d", "#1f2329"),
    "D": ("#2c3037", "#1b1e23", "#101215"), "R": ("#b3303a", "#8e1b24", "#5e1117"), "G": ("#a1a8b0", "#747b84", "#4d535b"),
    "A": ("#e5b04e", "#c48a22", "#8a5e12"), "F": ("#3a2a22", "#2a1d17", "#1a110d")}
B_FIXED = {"k": "#16100e", "W": "#e8e3dd", "l": "#4a505a", "m": "#2f343c", "r": "#8e1b24", "x": "#5e1117", "Y": "#d4a72c", "B": "#f4f1ec", "b": "#c8c2ba", "N": "#9fb0c2"}
LEGS = ["..L.L..L.L..", "..L.L..L.L.."]
FACE, BLANK = ".OOOOOOOOOO.", "............"
def _at(ch, *cells): return {rc: ch for rc in cells}
COUNCIL = {  # grid of materials + painted details
    "devils-advocate": ([".R........R.", ".RR......RR.", "..RR....RR..", FACE, FACE, FACE, FACE, "RRRRRRRRRRRR", "RRRRRRRRRRRR", ".RRRRRRRRRR.", *LEGS],
                        {**_at("k", (3, 2), (3, 3), (4, 4), (3, 9), (3, 8), (4, 7), (5, 3), (6, 3), (5, 8), (6, 8)), **_at("x", (7, 5), (7, 6))}),
    "engineer": (["...AAAAAA...", "..AAAAAAAA..", "AAAAAAAAAAAA", FACE, FACE, FACE, FACE, "CCCCCCCCCCCC", "CCCCCCCCCCCC", ".CCCCCCCCCC.", *LEGS],
                 {**_at("k", (3, 2), (3, 3), (3, 4), (3, 7), (3, 8), (3, 9), (5, 3), (6, 3), (5, 8), (6, 8)), **_at("Y", (8, 1), (8, 10))}),
    "analyst": ([BLANK, BLANK, BLANK, FACE, FACE, FACE, FACE, "CCCCCCCCCCCC", "CCCCCCCCCCCC", ".CCCCCCCCCC.", *LEGS],
                {**_at("k", (4, 2), (4, 3), (4, 4), (4, 7), (4, 8), (4, 9), (5, 2), (5, 4), (5, 5), (5, 6), (5, 7), (5, 9), (6, 2), (6, 3), (6, 4), (6, 7), (6, 8), (6, 9)),
                 **_at("N", (5, 3), (5, 8)), **_at("l", (7, 4), (8, 4), (7, 7), (8, 7)), **_at("x", (7, 5), (7, 6)), **_at("r", (8, 5), (8, 6), (9, 5), (9, 6))}),
    "elder": (["....GGGG....", "...GGGGGG...", "..GGGGGGGG..", *[".GOOOOOOOOG."] * 4, "GGGGGGGGGGGG", "GGGGGGGGGGGG", ".GGGGGGGGGG.", *LEGS],
              {**_at("B", (3, 3), (3, 4), (3, 7), (3, 8), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (8, 5), (8, 6), (9, 5), (9, 6)),
               **_at("k", (4, 3), (5, 3), (4, 8), (5, 8)), **_at("b", (8, 4), (8, 7))}),
    "chairman": ([*[".OOOOOOOOOOOO."] * 5, "DDDDDDDDDDDDDD", "DDDDDDDDDDDDDD", ".DDDDDDDDDDDD.", ".DDDDDDDDDDDD.", "..L.L....L.L..", "..L.L....L.L.."],
                 {**_at("k", (1, 2), (1, 3), (1, 4), (1, 9), (1, 10), (1, 11), (2, 3), (3, 3), (2, 10), (3, 10)), **_at("m", (5, 5), (5, 8)), **_at("l", (6, 5), (7, 5), (6, 8), (7, 8)), **_at("x", (5, 6), (5, 7)), **_at("r", (6, 6), (6, 7), (7, 6), (7, 7), (8, 6), (8, 7))}),
    "chair": (["......FFFFFFFF......", "....FFFRRRRRRFFF....", "..FFRRRRRRRRRRRRFF..", *[".FRRRRRRRRRRRRRRRRF."] * 15,
               "FFFRRRRRRRRRRRRRRFFF", "FFFRRRRRRRRRRRRRRFFF", "FFFFFFFFFFFFFFFFFFFF", ".FF..............FF."],
              _at("x", (4, 5), (4, 9), (4, 13), (7, 7), (7, 11), (10, 5), (10, 9), (10, 13), (13, 7), (13, 11), (16, 5), (16, 9), (16, 13))),
}

def _sprite(name, x0, y0):
    grid, marks = COUNCIL[name]
    g = [list(row) for row in grid]
    for (r, c), ch in marks.items(): g[r][c] = ch
    h, w = len(g), len(g[0])
    solid = lambda r, c: 0 <= r < h and 0 <= c < w and g[r][c] != "."
    px = lambda r, c, col: f'<rect x="{x0 + c * BU}" y="{y0 + r * BU}" width="{BU}" height="{BU}" fill="{col}"/>'
    out = [px(r, c, B_OUTLINE) for r in range(-1, h + 1) for c in range(-1, w + 1)
           if not solid(r, c) and any(solid(r + a, c + b) for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
    for r in range(h):
        for c in range(w):
            m = g[r][c]
            if m == ".": continue
            if m in B_RAMP:
                hi, base, sh = B_RAMP[m]
                col = hi if not solid(r - 1, c) or not solid(r, c - 1) else sh if not solid(r + 1, c) or not solid(r, c + 1) else base
            else:
                col = B_FIXED[m]
            out.append(px(r, c, col))
    return "".join(out)

def banner():
    mw, chw, gap, x0 = 12 * BU, 20 * BU, 6, 20
    xs = [x0, x0 + mw + gap, x0 + 2 * (mw + gap), x0 + 2 * (mw + gap) + chw + gap, x0 + 3 * (mw + gap) + chw + gap]
    tier_top = [158, 144, 130]
    b = '<rect width="860" height="190" rx="14" fill="#0d1117"/>\n'
    for tier, left, right in ((0, xs[0] - 10, xs[4] + mw + 10), (1, xs[1] - 8, xs[3] + mw + 8), (2, xs[2] - 6, xs[2] + chw + 6)):
        b += (f'<rect x="{left}" y="{tier_top[tier]}" width="{right - left}" height="{178 - tier_top[tier]}" fill="#161b22"/>'
              f'<rect x="{left}" y="{tier_top[tier]}" width="{right - left}" height="3" fill="{"#8e1b24" if tier == 2 else "#262c34"}"/>\n')
    chair_y = tier_top[2] - 22 * BU
    b += '<g shape-rendering="crispEdges">' + _sprite("chair", xs[2], chair_y) + _sprite("chairman", xs[2] + 3 * BU, chair_y + 11 * BU)
    for i, name, tier in ((0, "devils-advocate", 0), (1, "engineer", 1), (3, "analyst", 1), (4, "elder", 0)):
        b += _sprite(name, xs[i], tier_top[tier] - 12 * BU)
    b += "</g>\n"
    tx = xs[4] + mw + 30
    b += f'<rect x="{tx + 2}" y="50" width="14" height="4" fill="#8e1b24"/>'
    b += t(tx + 24, 56, "MULTI-AGENT COUNCIL", 11, "#8b949e", 700, extra='letter-spacing="3"')
    b += t(tx, 106, "wise-men", 54, "#f0f6fc", 800, extra='letter-spacing="-1.5"')
    b += t(tx + 2, 134, "A council of Claude subagents that argue, grade each other,", 15, "#9198a1")
    b += t(tx + 2, 154, "and hand you one answer with the dissent kept intact.", 15, "#9198a1")
    return svg(860, 190, b, "wise-men: a pixel-art council, a Devil's Advocate, an engineer, the chairman in a high-backed chair, an analyst and an elder")

# ---------- round 3 (PREREG-3): three judges per question, fresh 3.11.0 answers next to round 2's, then four held-out questions ----------
H2H3 = os.path.join(ROOT, "eval-data", "head-to-head", "parsed-v3")
H3_A = ["direct", "brainstorming", "grilling", "lifeos-council", "llm-council", "ecc-council", "warp-council", "wise-men", "wise-men-3.11"]
H3_B = ["direct", "llm-council", "warp-council", "wise-men-3.11"]
H3_PART_A, H3_PART_B = ["Q05", "Q09", "Q13", "Q19", "Q25", "Q36", "Q48", "Q55"], ["Q23", "Q32", "Q43", "Q51"]
H_NAME.update({"wise-men-3.11": "wise-men 3.11.0"}); H3_NAME = dict(H_NAME, **{"wise-men": "wise-men 3.9.2"})
H3_SRC = dict(H2_SRC, **{"wise-men": "this repo · round-2 answers", "wise-men-3.11": "this repo · new answers"})
TOPIC.update({"Q23": "A meta-analysis built on gray literature", "Q32": "A cold email to a VP", "Q43": "A report who is quietly job hunting", "Q51": "Senior IC or the manager track?"})

def load_h2h3():
    rows = {}
    for f in sorted(glob.glob(os.path.join(H2H3, "Q*.yaml"))):
        d = yaml.safe_load(open(f)); q = d["question_id"]; js = list(d["judges"].values()); arms = H3_A if q in H3_PART_A else H3_B
        rows[q] = {a: {k: st.mean(j[a][k] for j in js) for k in AXES + ["composite"]} for a in arms}
    return rows
def h3_boot(diffs, seed=20260918, n=10000):  # the same percentile bootstrap as h2h3.py
    rng = random.Random(seed); k = len(diffs); means = sorted(st.mean(rng.choice(diffs) for _ in range(k)) for _ in range(n))
    return means[int(0.025 * n)], means[int(0.975 * n) - 1]
def h3_gap(rows, a):
    d = [r["wise-men-3.11"]["composite"] - r[a]["composite"] for r in rows.values()]; lo, hi = h3_boot(d); return st.mean(d), lo, hi
def bar3(a, x, y, w, h, r=4): return hbar_outline(x, y, w, h, C["TXT"], r) if a == "direct" else hbar(x, y, w, h, C["ACCENT"] if a == "wise-men-3.11" else C["BAR2"], r)
def sgn(v): return f"{'+' if v >= 0 else '−'}{r1(abs(v))}"

def chart_h2h_v3(rows):
    rows = {q: r for q, r in rows.items() if q in H3_PART_A}; n = len(rows); interim = n < len(H3_PART_A)
    x0, sc, top, rh = 250, 15.6, 112, 46; arms = sorted(H3_A, key=lambda a: (-hmean(rows, a), H3_A.index(a))); bottom = top + rh * len(arms) - 6
    b = t(40, 32, f"Round 3{', in progress' if interim else ''}: total score on the round-2 questions — {n} of 8 judged, three blind judges each" if interim else "Round 3: total score on the round-2 questions — 8 questions, three blind judges each", 16, C["INK"], 600)
    b += t(40, 52, "Sum of 5 rubric axes (1–5 each, max 25), mean of 3 judges, averaged over the questions. Right: 3.11.0's lead, 95% bootstrap interval.", 12, C["TXT"])
    b += t(40, 68, "Fresh wise-men 3.11.0 answers, judged next to the eight round-2 answers unchanged; each judge saw its own sealed order of letters.", 12, C["TXT"])
    b += t(840, top - 12, "3.11.0 ahead by [95%]", 11, C["MUTE"], anchor="end")
    for g in range(0, 26, 5):
        x = x0 + g * sc; b += line(x, top - 4, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    for i, a in enumerate(arms):
        y = top + i * rh; m = hmean(rows, a); hero = a == "wise-men-3.11"
        if hero: b += band(y - 3, rh - 2)
        b += t(x0 - 14, y + 15, H3_NAME[a], 13, C["INK"], 700 if hero else 500, "end") + t(x0 - 14, y + 30, H3_SRC[a], 11, C["MUTE"], anchor="end")
        b += bar3(a, x0, y + 6, m * sc, 22) + t(x0 + m * sc + 8, y + 22, r1(m), 13, C["INK"], 700 if hero else 500)
        if hero: b += t(840, y + 22, "—", 12, C["MUTE"], anchor="end"); continue
        d, lo, hi = h3_gap(rows, a); b += t(840, y + 22, f"{sgn(d)}  [{sgn(lo)}, {sgn(hi)}]", 12, C["INK"] if lo > 0 else C["TXT"], 600 if lo > 0 else 400, "end")
    fy = bottom + 42; clear = sum(h3_gap(rows, a)[1] > 0 for a in arms if a != "wise-men-3.11")
    b += t(40, fy, f"An interval above zero is the pre-registered bar for \"clearly ahead\": met against {clear} of {len(arms) - 1} arms{' on the questions judged so far' if interim else ''}.", 11, C["MUTE"])
    b += t(40, fy + 16, "Intervals resample questions (10,000 draws), not judges. Round 2's judgments of these questions shaped versions 3.10.0 and 3.11.0;", 11, C["MUTE"])
    b += t(40, fy + 32, "the four held-out questions (per-question chart) are the check on that. Warp's council ran on Claude models only (pre-registered, disclosed).", 11, C["MUTE"])
    b += t(40, fy + 48, f"N = {n} · one top-level model ran every arm · three fresh Opus judges per question, letters A–I · PREREG-3.md · raw data: eval-data/head-to-head", 11, C["MUTE"])
    return svg(860, fy + 62, b, f"Round 3{' (in progress)' if interim else ''} mean total score out of 25 on {n} round-2 questions, three blind judges each: " + ", ".join(f"{H3_NAME[a]} {r1(hmean(rows, a))}" for a in arms))

def chart_h2h_v3_questions(rows):
    qs = [q for q in H3_PART_A + H3_PART_B if q in rows]; n = len(qs); interim = n < 12
    lo = min(10, int(min(r[a]["composite"] for r in rows.values() for a in r)))
    x0, x1, hi = 300, 640, 25; sc = (x1 - x0) / (hi - lo); top, rh = 112, 32; gap = 18 if any(q in H3_PART_B for q in qs) else 0; bottom = top + rh * (n - 1) + gap + 16
    short = {"brainstorming": "brainstorming", "grilling": "grilling", "lifeos-council": "LifeOS", "llm-council": "llm-council", "ecc-council": "ECC", "warp-council": "Warp", "wise-men": "wise-men 3.9.2"}
    b = t(40, 32, f"Round 3{', in progress' if interim else ''}, question by question", 16, C["INK"], 600)
    b += t(40, 52, "Each row: the mean of three blind judges' totals (max 25) for wise-men 3.11.0, every other arm and the plain answer", 12, C["TXT"])
    b += t(660, top - 22, "3.11.0 vs the best other arm", 11, C["MUTE"])
    for g in range(lo, 26, 5):
        x = x0 + (g - lo) * sc; b += line(x, top - 16, x, bottom, C["GRID"]) + t(x, bottom + 16, g, 11, C["MUTE"], anchor="middle")
    won = tied = lost = 0; part_b_at = None
    for i, q in enumerate(qs):
        y = top + i * rh + (gap if q in H3_PART_B else 0); r = rows[q]; arms = [a for a in (H3_A if q in H3_PART_A else H3_B)]; others = [a for a in arms if a not in ("direct", "wise-men-3.11")]
        if q in H3_PART_B and part_b_at is None: part_b_at = y; b += t(40, y - 14, "held-out questions (four arms)", 10, C["MUTE"], 600)
        wm = r["wise-men-3.11"]["composite"]; vals = [r[a]["composite"] for a in arms]
        b += t(40, y + 4, q, 11, C["MUTE"]) + t(76, y + 4, TOPIC[q], 12, C["INK"])
        b += line(x0 + (min(vals) - lo) * sc, y, x0 + (max(vals) - lo) * sc, y, C["GRID"], 2) + ring(x0 + (r["direct"]["composite"] - lo) * sc, y, 7, C["TXT"])
        for a in others: b += dot(x0 + (r[a]["composite"] - lo) * sc, y, 4.5, C["OTHER"])
        if "wise-men" in r: b += ring(x0 + (r["wise-men"]["composite"] - lo) * sc, y, 6, C["ACCENT"])
        b += dot(x0 + (wm - lo) * sc, y, 6.5, C["ACCENT"])
        bv = max(r[a]["composite"] for a in others); best = [short[a] for a in others if abs(r[a]["composite"] - bv) < 1e-9]
        rel = "ahead" if wm > bv + 1e-9 else "tied" if abs(wm - bv) < 1e-9 else "behind"; won += rel == "ahead"; tied += rel == "tied"; lost += rel == "behind"
        b += t(660, y + 4, rel, 12, C["INK"]) + t(712, y + 4, f"{', '.join(best)} {r1(bv)}", 11, C["MUTE"])
    ly = bottom + 44
    b += dot(46, ly - 4, 6.5, C["ACCENT"]) + t(58, ly, "wise-men 3.11.0", 11) + ring(176, ly - 4, 6, C["ACCENT"]) + t(188, ly, "wise-men 3.9.2 (round-2 answer)", 11) + dot(376, ly - 4, 4.5, C["OTHER"]) + t(386, ly, "the other skills", 11) + ring(496, ly - 4, 7, C["TXT"]) + t(508, ly, "plain answer", 11)
    b += t(40, ly + 22, f"Against the best other arm on each question: ahead {won}, tied {tied}, behind {lost}{' (of the ' + str(n) + ' questions judged so far)' if interim else ''}.", 11, C["MUTE"])
    b += t(40, ly + 38, "The first rows are the round-2 questions; the held-out rows were never used in an earlier round. Three fresh Opus judges per question.", 11, C["MUTE"])
    return svg(860, ly + 54, b, f"Round 3{' (in progress)' if interim else ''} per-question scores over {n} questions: wise-men 3.11.0 versus the best other arm ahead {won}, tied {tied}, behind {lost}")

def chart_h2h_v3_axes(rows):
    rows = {q: r for q, r in rows.items() if q in H3_PART_A}; n = len(rows); interim = n < len(H3_PART_A); arms = sorted(H3_A, key=lambda a: (-hmean(rows, a), H3_A.index(a))); top, rh = 118, 34
    cols = [("composite", "Total /25", 25, 222, 80)] + [(x, AXIS_NAME[x], 5, 364 + k * 94, 46) for k, x in enumerate(AXES)]
    b = t(40, 32, f"Round 3 scoreboard{', in progress' if interim else ''} — the total and each rubric axis", 16, C["INK"], 600)
    b += t(40, 52, f"Mean of three judges over the same {n} round-2 questions · total out of 25, each axis 1–5 · sorted by total · the plain answer is the outlined bar", 12, C["TXT"])
    for key, title, mx, x, w in cols: b += t(x, top - 14, title, 11, C["INK"], 600)
    best = {key: max(hmean(rows, a, key) for a in arms) for key, *_ in cols}
    for i, a in enumerate(arms):
        y = top + i * rh; yc = y + rh / 2; hero = a == "wise-men-3.11"
        if hero: b += band(y + 2, rh - 4)
        b += t(206, yc + 4, H3_NAME[a], 13, C["INK"], 700 if hero else 500, "end")
        for key, title, mx, x, w in cols:
            v = hmean(rows, a, key); top_v = abs(v - best[key]) < 1e-9
            b += f'<rect x="{num(x)}" y="{num(yc - 5)}" width="{num(w)}" height="10" rx="3" fill="{C["GRID"]}" fill-opacity="0.6"/>\n' + bar3(a, x, yc - 5, v / mx * w, 10, 3)
            b += t(x + w + 8, yc + 4, r1(v), 12, C["INK"] if top_v else C["TXT"], 700 if top_v else 400)
    leaders = {key: [a for a in arms if abs(hmean(rows, a, key) - best[key]) < 1e-9] for key, *_ in cols}
    wm_lead = [AXIS_NAME[x].lower() for x in AXES if "wise-men-3.11" in leaders[x]]; shared = [AXIS_NAME[x].lower() for x in AXES if "wise-men-3.11" in leaders[x] and len(leaders[x]) > 1]
    fy = top + rh * len(arms) + 28
    b += t(40, fy, f"Bold = highest in the column (ties bolded together). wise-men 3.11.0 had the top score on {len(wm_lead)} of the 5 axes" + (f" (shared on {', '.join(shared)})" if shared else "") + f"{' on the questions judged so far' if interim else ''}.", 11, C["MUTE"])
    b += t(40, fy + 16, f"Warp's council ran on Claude models only (its skill asks for a model-diverse council). N = {n}, three blind judges per question, means shown.", 11, C["MUTE"])
    return svg(860, fy + 30, b, f"Round 3{' (in progress)' if interim else ''} scoreboard, means over {n} questions: " + "; ".join(f"{H3_NAME[a]}: total {r1(hmean(rows, a))}, " + ", ".join(f"{AXIS_NAME[x].lower()} {r1(hmean(rows, a, x))}" for x in AXES) for a in arms))

if __name__ == "__main__":
    rows, h2h, h2h2, h2h3 = load(), load_h2h(), load_h2h2(), load_h2h3(); os.makedirs(OUT, exist_ok=True); wrote = []
    charts = [("headline", lambda: chart_headline(rows)), ("axes", lambda: chart_axes(rows)), ("questions", lambda: chart_questions(rows)), ("landscape", chart_landscape),
              ("h2h", lambda: chart_h2h(h2h)), ("h2h-axes", lambda: chart_h2h_axes(h2h)), ("h2h-questions", lambda: chart_h2h_questions(h2h)),
              ("h2h-v2", lambda: chart_h2h_v2(h2h2)), ("h2h-v2-axes", lambda: chart_h2h_v2_axes(h2h2)), ("h2h-v2-questions", lambda: chart_h2h_v2_questions(h2h2)),
              ("h2h-v3", lambda: chart_h2h_v3(h2h3)), ("h2h-v3-axes", lambda: chart_h2h_v3_axes(h2h3)), ("h2h-v3-questions", lambda: chart_h2h_v3_questions(h2h3))]
    for theme, suffix in (("light", ""), ("dark", "-dark")):
        C.clear(); C.update(THEMES[theme])
        for name, fn in charts:
            open(os.path.join(OUT, name + suffix + ".svg"), "w").write(fn()); wrote.append(name + suffix)
    open(os.path.join(OUT, "banner.svg"), "w").write(banner()); wrote.append("banner")
    print("wrote", ", ".join(wrote))
