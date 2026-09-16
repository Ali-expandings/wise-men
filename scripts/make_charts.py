#!/usr/bin/env python3
"""Regenerate the README charts from eval-data/parsed/*.yaml. Run: python3 scripts/make_charts.py
Outputs assets/*.svg (used by README) and assets/*.png (previews). Requires PyYAML + matplotlib."""
import glob, os, re, statistics as st, math
import yaml
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PARSED = os.path.join(ROOT, "eval-data", "parsed")
OUT = os.path.join(ROOT, "assets")
AXES = ["correctness", "insight", "practical", "risk", "dissent"]
ARMS = [("arm_c", "council (standard tier)", "#2f6f4f"), ("arm_b", "structured single prompt (solo tier)", "#c98a2b"), ("arm_a", "direct answer", "#8a8a8a")]

def load():
    rows = {}
    for f in sorted(glob.glob(os.path.join(PARSED, "Q*.yaml"))):
        if "tiebreaker" in f: continue
        txt = open(f).read(); d = yaml.safe_load(txt); q = d["question_id"]
        comp = {a: d["arms"][a]["composite_5axis"] for a, _, _ in ARMS}
        axes = {}
        if all(isinstance(d["arms"][a], dict) and "correctness" in d["arms"][a] for a, _, _ in ARMS):
            axes = {a: {x: d["arms"][a][x] for x in AXES} for a, _, _ in ARMS}
        else:
            m = re.search(r"blinding_map[^:]*:\s*([XYZ]=[ABC](?:,\s*[XYZ]=[ABC]){2})", txt)
            slot2arm = {s: "arm_" + a.lower() for s, a in (p.split("=") for p in m.group(1).replace(" ", "").split(","))}
            for s, arm in slot2arm.items():
                assert d["slots"][s]["composite_5axis"] == comp[arm], (q, s)
                axes[arm] = {x: d["slots"][s][x] for x in AXES}
        rows[q] = {"comp": comp, "axes": axes}
    assert len(rows) == 29, len(rows)
    return rows

def ci95(xs):
    n = len(xs); m = st.mean(xs); s = st.stdev(xs); t = 2.048  # t(0.975, 28)
    return m, t * s / math.sqrt(n)

def style(ax):
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(axis="x", color="#e5e5e5", lw=0.8); ax.set_axisbelow(True)

def chart_arms(rows):
    fig, ax = plt.subplots(figsize=(8, 3.2), dpi=150)
    ys = list(range(len(ARMS)))[::-1]
    for y, (arm, label, col) in zip(ys, ARMS):
        xs = [r["comp"][arm] for r in rows.values()]
        m, h = ci95(xs)
        ax.barh(y, m, color=col, height=0.55)
        ax.errorbar(m, y, xerr=h, fmt="none", ecolor="#222", capsize=4, lw=1.2)
        jit = [y + (i % 7 - 3) * 0.05 for i in range(len(xs))]
        ax.scatter(xs, jit, s=9, color="#111", alpha=0.35, zorder=3)
        ax.text(m + h + 0.3, y, f"{m:.1f}", va="center", fontsize=11, fontweight="bold")
    ax.set_yticks(ys); ax.set_yticklabels([l for _, l, _ in ARMS], fontsize=10)
    ax.set_xlim(0, 26); ax.set_xlabel("blind judge score, 5-axis rubric (max 25) — mean, 95% CI, one dot per question", fontsize=9)
    ax.set_title("Same 29 questions, three ways of answering", fontsize=12, loc="left")
    style(ax); fig.tight_layout()
    return fig

def chart_per_question(rows):
    items = sorted(rows.items(), key=lambda kv: kv[1]["comp"]["arm_c"] - kv[1]["comp"]["arm_b"])
    fig, ax = plt.subplots(figsize=(8, 7), dpi=150)
    for i, (q, r) in enumerate(items):
        b, c = r["comp"]["arm_b"], r["comp"]["arm_c"]
        ax.plot([b, c], [i, i], color="#bbb", lw=1.5, zorder=1)
        ax.scatter([b], [i], color=ARMS[1][2], s=28, zorder=2)
        ax.scatter([c], [i], color=ARMS[0][2], s=28, zorder=3)
        if c < b: ax.text(c - 0.4, i, "council lost", va="center", ha="right", fontsize=8, color="#a33")
    ax.set_yticks(range(len(items))); ax.set_yticklabels([q for q, _ in items], fontsize=7)
    ax.set_xlim(12, 26); ax.set_xlabel("score (max 25)", fontsize=9)
    ax.set_title("Council vs structured prompt, every question (sorted by gap)", fontsize=12, loc="left")
    ax.scatter([], [], color=ARMS[0][2], label="council"); ax.scatter([], [], color=ARMS[1][2], label="structured prompt")
    ax.legend(loc="lower left", frameon=False, fontsize=9)
    wins = sum(1 for _, r in items if r["comp"]["arm_c"] > r["comp"]["arm_b"])
    ax.text(12.2, len(items) - 0.5, f"council ahead on {wins}/29", fontsize=10, va="top")
    style(ax); fig.tight_layout()
    return fig

def chart_axes(rows):
    fig, ax = plt.subplots(figsize=(8, 3.4), dpi=150)
    w = 0.26; sig = {"insight": "***", "practical": "***", "risk": "***", "dissent": "***", "correctness": "n.s."}
    for k, (arm, label, col) in enumerate(ARMS):
        means = [st.mean(r["axes"][arm][x] for r in rows.values()) for x in AXES]
        xs = [i + (k - 1) * w for i in range(len(AXES))]
        ax.bar(xs, means, width=w, color=col, label=label)
    for i, x in enumerate(AXES):
        ax.text(i, 5.15, sig[x], ha="center", fontsize=9, color="#444")
    ax.set_xticks(range(len(AXES))); ax.set_xticklabels(AXES, fontsize=10)
    ax.set_ylim(0, 5.6); ax.set_ylabel("mean score (1–5)", fontsize=9)
    ax.set_title("Where the gap comes from — per rubric axis (*** = council > prompt, Wilcoxon, Bonferroni α=0.01)", fontsize=10, loc="left")
    ax.legend(frameon=False, fontsize=8, loc="lower right", ncol=1)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    ax.grid(axis="y", color="#e5e5e5", lw=0.8); ax.set_axisbelow(True)
    fig.tight_layout()
    return fig

def chart_landscape():
    # Facts from resources/landscape.md (READMEs as read 2026-09-16). 2 = yes/strong, 1 = partial, 0 = absent/not mentioned.
    cols = ["wise-men", "llm-council skill\n(aiwithremy)", "llm-council-skill\n(tenfoldmarc)", "council-review\n(ngmeyer)", "agent-review-panel\n(wan-huiyan)", "karpathy\nllm-council"]
    feats = [
        ("Independent members, no API keys", [2, 2, 2, 2, 2, 0]),
        ("Rubric peer review, machine-parsed", [2, 1, 1, 1, 1, 1]),
        ("Debate on a mechanical trigger", [2, 0, 1, 2, 2, 0]),
        ("Dissent verbatim, cannot be truncated", [2, 1, 1, 2, 1, 0]),
        ("Independent check of the synthesis", [2, 0, 0, 0, 1, 0]),
        ("Members structurally unable to spawn/run", [2, 0, 0, 0, 1, 0]),
        ("Cost tiers + spend ceiling", [2, 0, 0, 1, 1, 0]),
        ("Deviations must be disclosed", [2, 0, 0, 0, 0, 0]),
        ("Eval data + script shipped in repo", [2, 0, 0, 1, 1, 0]),
    ]
    fig, ax = plt.subplots(figsize=(8.6, 4.6), dpi=150)
    colors = {2: "#2f6f4f", 1: "#c98a2b", 0: "#e8e8e8"}
    for i, (name, vals) in enumerate(feats):
        for j, v in enumerate(vals):
            ax.add_patch(plt.Rectangle((j, len(feats) - 1 - i), 0.92, 0.92, color=colors[v]))
    ax.set_xlim(0, len(cols)); ax.set_ylim(0, len(feats))
    ax.set_xticks([j + 0.46 for j in range(len(cols))]); ax.set_xticklabels(cols, fontsize=8)
    ax.set_yticks([len(feats) - 1 - i + 0.46 for i in range(len(feats))]); ax.set_yticklabels([f for f, _ in feats], fontsize=8.5)
    ax.tick_params(length=0); [s.set_visible(False) for s in ax.spines.values()]
    ax.set_title("Council skills for Claude Code — what each ships (from their READMEs, 2026-09-16)", fontsize=10, loc="left")
    for v, lab in ((2, "yes"), (1, "partial / unspecified"), (0, "absent")):
        ax.scatter([], [], marker="s", s=80, color=colors[v], label=lab)
    ax.legend(frameon=False, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3)
    fig.tight_layout()
    return fig

if __name__ == "__main__":
    rows = load()
    for name, fn in (("arms", chart_arms), ("per-question", chart_per_question), ("axes", chart_axes)):
        fig = fn(rows); fig.savefig(os.path.join(OUT, name + ".svg")); fig.savefig(os.path.join(OUT, name + ".png")); plt.close(fig)
    fig = chart_landscape(); fig.savefig(os.path.join(OUT, "landscape.svg")); fig.savefig(os.path.join(OUT, "landscape.png")); plt.close(fig)
    print("charts written to", OUT)
