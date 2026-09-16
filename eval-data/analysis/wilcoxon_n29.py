#!/usr/bin/env python3
"""Wilcoxon signed-rank analysis of the wise-men blind eval (N=29).

Reproduces every statistic quoted in README.md and RESULTS_N29.md:

    python3 eval-data/analysis/wilcoxon_n29.py

Requires only PyYAML. One-sided tests (C > B, C > A) on the 5-axis composites,
normal approximation with tie + continuity correction. Also runs the per-axis
check (spec section 8, condition 4) and a sensitivity analysis excluding the two
questions carrying the chairman-model parity flag.

Arms: A = direct answer, B = one structured prompt, C = full council.
"""
import glob
import math
import os
import re
from collections import Counter

import yaml

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "parsed")
AXES = ("correctness", "insight", "practical", "risk", "dissent")
ARMS = ("arm_a", "arm_b", "arm_c")
PARITY_FLAGGED = ("Q09", "Q11")  # chairman model not recorded; see HISTORY.md


def question_files():
    """Parsed question files. Q23_tiebreaker is a resolution artifact, not a question."""
    return [p for p in sorted(glob.glob(os.path.join(DATA, "Q*.yaml")))
            if "tiebreaker" not in os.path.basename(p)]


def load():
    """Return {qid: {arm: {axis: score, ..., 'composite': int}}}.

    Most files store per-axis scores under `arms`. Thirteen store them only under
    the blinded `slots` (X/Y/Z), with the unsealed mapping in a header comment —
    for those we reconstruct slot->arm and cross-check the composites.
    """
    rows = {}
    for path in question_files():
        raw = open(path, encoding="utf-8").read()
        doc = yaml.safe_load(raw)
        qid, arms = doc["question_id"], doc["arms"]
        entry = {}

        if "correctness" in arms["arm_c"]:
            for arm in ARMS:
                entry[arm] = {ax: arms[arm][ax] for ax in AXES}
        else:
            m = re.search(r"blinding_map[^:]*:\s*X=(\w),\s*Y=(\w),\s*Z=(\w)", raw)
            if not m:
                raise SystemExit(f"{qid}: per-axis scores are slot-only but no blinding map found")
            slot_to_arm = {slot: f"arm_{m.group(i).lower()}"
                           for i, slot in enumerate(("X", "Y", "Z"), start=1)}
            for slot, arm in slot_to_arm.items():
                entry[arm] = {ax: doc["slots"][slot][ax] for ax in AXES}
                if doc["slots"][slot]["composite_5axis"] != arms[arm]["composite_5axis"]:
                    raise SystemExit(f"{qid}: slot {slot} -> {arm} composite mismatch")

        for arm in ARMS:
            entry[arm]["composite"] = arms[arm]["composite_5axis"]
        rows[qid] = entry
    return rows


def wilcoxon_greater(x, y):
    """H1: median(x - y) > 0. Returns (W_plus, n_effective, z, one-sided p)."""
    diffs = [a - b for a, b in zip(x, y) if a != b]
    n = len(diffs)
    if n == 0:
        return 0.0, 0, float("nan"), 1.0

    ranked = sorted((abs(d), d) for d in diffs)
    ranks = [0.0] * n
    i = 0
    while i < n:                      # average ranks across ties in |d|
        j = i
        while j < n and ranked[j][0] == ranked[i][0]:
            j += 1
        for k in range(i, j):
            ranks[k] = (i + 1 + j) / 2.0
        i = j

    w_plus = sum(r for r, (_, d) in zip(ranks, ranked) if d > 0)
    mu = n * (n + 1) / 4.0
    tie_term = sum(t ** 3 - t for t in Counter(a for a, _ in ranked).values())
    sigma = math.sqrt(n * (n + 1) * (2 * n + 1) / 24.0 - tie_term / 48.0)
    z = (w_plus - mu - 0.5) / sigma   # continuity correction
    return w_plus, n, z, 0.5 * math.erfc(z / math.sqrt(2))


def median(v):
    s = sorted(v)
    mid = len(s) // 2
    return s[mid] if len(s) % 2 else (s[mid - 1] + s[mid]) / 2


def report(label, rows):
    qs = sorted(rows)
    a, b, c = ([rows[q][arm]["composite"] for q in qs] for arm in ARMS)
    n = len(qs)
    print(f"\n=== {label} (N={n}) ===")
    print(f"means   : C={sum(c)/n:.2f}  B={sum(b)/n:.2f}  A={sum(a)/n:.2f}")
    print(f"medians : C={median(c):.1f}  B={median(b):.1f}  A={median(a):.1f}")
    print(f"median gap C-B = {median([ci - bi for ci, bi in zip(c, b)]):.1f}"
          f" ; C beats B on {sum(1 for ci, bi in zip(c, b) if ci > bi)}/{n}")
    for name, x, y in (("C > B", c, b), ("C > A", c, a)):
        w, neff, z, p = wilcoxon_greater(x, y)
        print(f"Wilcoxon {name}: W+={w:.1f} n_eff={neff} z={z:.3f} p(one-sided)={p:.2e}")


def per_axis(rows):
    print("\n=== Per-axis C vs B (two-sided, Bonferroni alpha_eff=0.01)"
          " — spec section 8, condition 4 ===")
    qs = sorted(rows)
    for ax in AXES:
        c = [rows[q]["arm_c"][ax] for q in qs]
        b = [rows[q]["arm_b"][ax] for q in qs]
        w, neff, z, p_up = wilcoxon_greater(c, b)
        p_two = 2 * min(p_up, 1 - p_up) if neff else 1.0
        if p_two >= 0.01:
            verdict = "no significant difference"
        else:
            verdict = "C significantly BETTER" if z > 0 else "C significantly WORSE (gate fails)"
        print(f"{ax:12s}: n_eff={neff:2d} z={z:+.3f} p={p_two:.2e} -> {verdict}")


if __name__ == "__main__":
    rows = load()
    print(f"Loaded {len(rows)} questions from {os.path.normpath(DATA)}"
          " (slot->arm cross-checks passed)")
    report("FULL persisted set", rows)
    per_axis(rows)
    report(f"SENSITIVITY: excluding {'/'.join(PARITY_FLAGGED)} (chairman parity flag)",
           {q: v for q, v in rows.items() if q not in PARITY_FLAGGED})
