#!/usr/bin/env python3
"""Regenerate README charts as hand-authored SVG from eval-data/parsed/*.yaml.
Run: python3 scripts/make_charts.py   (needs PyYAML only). Colours are chosen to read on GitHub light and dark themes."""
import glob, math, os, re, statistics as st
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSED = os.path.join(ROOT, "eval-data", "parsed"); OUT = os.path.join(ROOT, "assets")
AXES = ["correctness", "insight", "practical", "risk", "dissent"]
FONT = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"
TXT, MUTE, GRID = "#8b949e", "#6e7681", "rgba(139,148,158,0.22)"
ARMS = [("arm_c", "wise-men council", "#1a9e8a"), ("arm_b", "structured single prompt", "#7d8ea5"), ("arm_a", "direct answer", "#b9c2ce")]

def load():
    rows = {}
    for f in sorted(glob.glob(os.path.join(PARSED, "Q*.yaml"))):
        if "tiebreaker" in f: continue
        txt = open(f).read(); d = yaml.safe_load(txt); q = d["question_id"]
        comp = {a: d["arms"][a]["composite_5axis"] for a, _, _ in ARMS}
        if all(isinstance(d["arms"][a], dict) and "correctness" in d["arms"][a] for a, _, _ in ARMS):
            axes = {a: {x: d["arms"][a][x] for x in AXES} for a, _, _ in ARMS}
        else:
            m = re.search(r"blinding_map[^:]*:\s*([XYZ]=[ABC](?:,\s*[XYZ]=[ABC]){2})", txt)
            s2a = {s: "arm_" + a.lower() for s, a in (p.split("=") for p in m.group(1).replace(" ", "").split(","))}
            axes = {}
            for s, arm in s2a.items():
                assert d["slots"][s]["composite_5axis"] == comp[arm], (q, s)
                axes[arm] = {x: d["slots"][s][x] for x in AXES}
        rows[q] = {"comp": comp, "axes": axes}
    assert len(rows) == 29, len(rows); return rows

def ci95(xs): return st.mean(xs), 2.048 * st.stdev(xs) / math.sqrt(len(xs))
def svg(w, h, body, title): return f'<svg viewBox="0 0 {w} {h}" width="{w}" xmlns="http://www.w3.org/2000/svg" font-family="{FONT}">\n<title>{title}</title>\n{body}</svg>\n'
def t(x, y, s, size=12, fill=TXT, weight=400, anchor="start", extra=""): return f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>\n'

def chart_headline(rows):
    W, H = 860, 250; x0, x1 = 240, 800; sc = (x1 - x0) / 25
    b = t(x0, 30, "Same 29 questions, three ways of answering", 16, TXT, 600)
    b += t(x0, 50, "Blind judge · 5-axis rubric, max 25 · mean with 95% CI (dark tick)", 12, MUTE)
    for g in range(0, 26, 5):
        b += f'<line x1="{x0+g*sc}" y1="66" x2="{x0+g*sc}" y2="200" stroke="{GRID}"/>' + t(x0 + g * sc, 218, g, 11, MUTE, anchor="middle")
    for i, (arm, label, col) in enumerate(ARMS):
        y = 84 + i * 44; xs = [r["comp"][arm] for r in rows.values()]; m, h = ci95(xs)
        bold = 700 if arm == "arm_c" else 400
        b += t(x0 - 16, y + 17, label, 14, "#1a9e8a" if arm == "arm_c" else TXT, bold, "end")
        b += f'<rect x="{x0}" y="{y}" width="{m*sc:.1f}" height="26" rx="4" fill="{col}"/>\n'
        b += f'<line x1="{x0+(m-h)*sc:.1f}" y1="{y+13}" x2="{x0+(m+h)*sc:.1f}" y2="{y+13}" stroke="#0d1117" stroke-opacity="0.55" stroke-width="2"/>\n'
        b += t(x0 + (m + h) * sc + 12, y + 19, f"{m:.1f}", 18, col if arm != "arm_a" else MUTE, 700)
    b += t(x0, 240, "Council beat the structured prompt on 28 of 29 questions. Data: eval-data/parsed · script: scripts/make_charts.py", 11, MUTE)
    return svg(W, H, b, "Council 24.5 vs structured prompt 20.8 vs direct answer 16.3 on a 25-point blind rubric, N=29")

def chart_axes(rows):
    W, H = 860, 364; y0, y1 = 96, 304; sc = (y1 - y0) / 5; sig = {"correctness": "no difference", "insight": "p &lt; 0.001", "practical": "p &lt; 0.001", "risk": "p &lt; 0.001", "dissent": "p &lt; 0.001"}
    b = t(40, 30, "Where the gap comes from — per rubric axis", 16, TXT, 600)
    b += t(40, 50, "Mean score 1–5 · council vs structured prompt, two-sided Wilcoxon, Bonferroni α = 0.01", 12, MUTE)
    lx = 40
    for arm, label, col in ARMS:
        b += f'<rect x="{lx}" y="62" width="12" height="12" rx="2" fill="{col}"/>' + t(lx + 17, 72, label, 12); lx += 17 + 6.6 * len(label) + 22
    for g in range(6):
        y = y1 - g * sc; b += f'<line x1="40" y1="{y}" x2="820" y2="{y}" stroke="{GRID}"/>' + t(32, y + 4, g, 11, MUTE, anchor="end")
    gw = 156; bw = 34
    for i, ax in enumerate(AXES):
        gx = 60 + i * gw
        for k, (arm, _, col) in enumerate(ARMS):
            m = st.mean(r["axes"][arm][ax] for r in rows.values()); x = gx + k * (bw + 6); y = y1 - m * sc
            b += f'<rect x="{x}" y="{y:.1f}" width="{bw}" height="{(y1-y):.1f}" rx="3" fill="{col}"/>'
            b += t(x + bw / 2, y - 6, f"{m:.1f}", 12, col if arm != "arm_a" else MUTE, 600, "middle")
        b += t(gx + (3 * bw + 12) / 2, y1 + 20, ax, 13, TXT, 500, "middle") + t(gx + (3 * bw + 12) / 2, y1 + 38, sig[ax], 11, "#1a9e8a" if sig[ax] != "no difference" else MUTE, 400, "middle")
    b += t(40, 354, "Correctness is a tie; the council's edge is insight, practical usefulness, risk awareness, and above all dissent.", 11, MUTE)
    return svg(W, H, b, "Per-axis means for council, structured prompt, and direct answer")

def chart_questions(rows):
    items = sorted(rows.items(), key=lambda kv: kv[1]["comp"]["arm_c"] - kv[1]["comp"]["arm_b"]); rh = 21
    W, H = 860, 96 + rh * len(items) + 40; x0, x1 = 120, 820; sc = (x1 - x0) / 13
    b = t(40, 30, "Every question, council vs structured prompt", 16, TXT, 600)
    b += t(40, 50, "Sorted by gap · score out of 25 · council ahead on 28 of 29", 12, MUTE)
    for g in range(12, 26, 2):
        x = x0 + (g - 12) * sc; b += f'<line x1="{x}" y1="70" x2="{x}" y2="{H-40}" stroke="{GRID}"/>' + t(x, H - 22, g, 11, MUTE, anchor="middle")
    for i, (q, r) in enumerate(items):
        y = 84 + i * rh; bx = x0 + (r["comp"]["arm_b"] - 12) * sc; cx = x0 + (r["comp"]["arm_c"] - 12) * sc
        b += t(x0 - 14, y + 4, q, 11, MUTE, anchor="end") + f'<line x1="{bx}" y1="{y}" x2="{cx}" y2="{y}" stroke="{TXT}" stroke-opacity="0.35" stroke-width="2"/>'
        b += f'<circle cx="{bx}" cy="{y}" r="5" fill="{ARMS[1][2]}"/><circle cx="{cx}" cy="{y}" r="5.5" fill="{ARMS[0][2]}"/>'
        if r["comp"]["arm_c"] < r["comp"]["arm_b"]: b += t(cx - 12, y + 4, "the one loss — dissent re-argued the majority", 11, "#d0665a", anchor="end")
    b += f'<circle cx="{x0+2}" cy="{H-8}" r="5" fill="{ARMS[0][2]}"/>' + t(x0 + 12, H - 4, "council", 11) + f'<circle cx="{x0+82}" cy="{H-8}" r="5" fill="{ARMS[1][2]}"/>' + t(x0 + 92, H - 4, "structured prompt", 11)
    return svg(W, H, b, "Council vs structured prompt on each of 29 questions")

def chart_landscape():
    cols = [("wise-men", ""), ("llm-council skill", "aiwithremy"), ("llm-council-skill", "tenfoldmarc"), ("council-review", "ngmeyer"), ("agent-review-panel", "wan-huiyan"), ("llm-council", "karpathy")]
    feats = [("Independent members, no API keys", [2, 2, 2, 2, 2, 0]), ("Rubric peer review, machine-parsed", [2, 1, 1, 1, 1, 1]), ("Debate on a mechanical trigger", [2, 0, 1, 2, 2, 0]),
             ("Dissent verbatim, cannot be truncated", [2, 1, 1, 2, 1, 0]), ("Independent check of the synthesis", [2, 0, 0, 0, 1, 0]), ("Members structurally unable to spawn or run", [2, 0, 0, 0, 1, 0]),
             ("Cost tiers + spend ceiling", [2, 0, 0, 1, 1, 0]), ("Every deviation disclosed in output", [2, 0, 0, 0, 0, 0]), ("Eval data + script shipped in repo", [2, 0, 0, 1, 1, 0])]
    W = 860; rh = 34; x0 = 300; cw = (W - x0 - 20) / len(cols); H = 120 + rh * len(feats) + 40
    b = t(40, 30, "Council skills for Claude Code — what each one ships", 16, TXT, 600) + t(40, 50, "From each project's README, 2026-09-16 · full table with sources in resources/landscape.md", 12, MUTE)
    for j, (n, o) in enumerate(cols):
        cx = x0 + cw * (j + 0.5); parts = [n] if len(n) <= 13 else ([n[:n.find(" ")], n[n.find(" ") + 1:]] if " " in n else [n[:n.rfind("-") + 1], n[n.rfind("-") + 1:]])
        for li, part in enumerate(parts): b += t(cx, 78 + li * 13, part, 11, "#1a9e8a" if j == 0 else TXT, 700 if j == 0 else 500, "middle")
        if o: b += t(cx, 78 + len(parts) * 13, o, 10, MUTE, anchor="middle")
    b += f'<rect x="{x0}" y="62" width="{cw}" height="{rh*len(feats)+58}" rx="8" fill="#1a9e8a" fill-opacity="0.08"/>'
    for i, (name, vals) in enumerate(feats):
        y = 120 + i * rh + rh / 2; b += t(x0 - 16, y + 4, name, 12, TXT, anchor="end") + f'<line x1="40" y1="{y+rh/2}" x2="{W-20}" y2="{y+rh/2}" stroke="{GRID}"/>'
        for j, v in enumerate(vals):
            cx = x0 + cw * (j + 0.5)
            b += {2: f'<circle cx="{cx}" cy="{y}" r="7" fill="#1a9e8a"/>', 1: f'<circle cx="{cx}" cy="{y}" r="7" fill="#d9a441"/>', 0: f'<circle cx="{cx}" cy="{y}" r="6" fill="none" stroke="{TXT}" stroke-opacity="0.45" stroke-width="1.5"/>'}[v]
    ly = H - 16
    b += f'<circle cx="46" cy="{ly-4}" r="6" fill="#1a9e8a"/>' + t(58, ly, "yes", 11) + f'<circle cx="106" cy="{ly-4}" r="6" fill="#d9a441"/>' + t(118, ly, "partial or unspecified", 11) + f'<circle cx="256" cy="{ly-4}" r="5.5" fill="none" stroke="{TXT}" stroke-opacity="0.45" stroke-width="1.5"/>' + t(268, ly, "absent", 11)
    return svg(W, H, b, "Feature matrix of council skills for Claude Code")

def banner():
    W, H = 860, 190
    b = f'<rect width="{W}" height="{H}" rx="14" fill="#0b0f14"/>\n'
    for k, (cx, cy) in enumerate([(88, 96), (114, 70), (146, 62), (178, 70), (204, 96)]):
        b += f'<circle cx="{cx}" cy="{cy}" r="9" fill="{"#1a9e8a" if k == 3 else "#e6edf3"}"/>'
    b += f'<path d="M 88 96 Q 146 150 204 96" fill="none" stroke="#e6edf3" stroke-opacity="0.35" stroke-width="2"/>'
    b += t(250, 92, "wise-men", 52, "#e6edf3", 700, extra='letter-spacing="-1"')
    b += t(252, 126, "A council of Claude subagents that argue, grade each other,", 16, "#8b949e")
    b += t(252, 148, "and hand you one answer with the dissent kept intact.", 16, "#8b949e")
    return svg(W, H, b, "wise-men")

if __name__ == "__main__":
    rows = load(); os.makedirs(OUT, exist_ok=True)
    for name, s in (("headline", chart_headline(rows)), ("axes", chart_axes(rows)), ("questions", chart_questions(rows)), ("landscape", chart_landscape()), ("banner", banner())):
        open(os.path.join(OUT, name + ".svg"), "w").write(s)
    print("wrote", ", ".join(("headline", "axes", "questions", "landscape", "banner")))
