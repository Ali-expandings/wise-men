#!/usr/bin/env python3
"""Deterministic helpers for the orchestrator (standard library only; optional — the protocol runs without them).

  council.py members  FILE...                       Stage 1 validator: five non-empty sections, or the abstention marker
  council.py aggregate --members "A,B,C" [--positions "x:3,y:2"] REVIEW...
                                                    Stage 2 validator + score aggregation + the three debate-trigger clauses

Exit status 0 = everything valid; 1 = at least one member answer or reviewer failed validation (details on stdout).
Nothing here calls a model or writes a file. The rules mirror SKILL.md and resources/prompts/peer-review.md."""
import re, sys, statistics as st

SECTIONS = ["## Core judgment", "## Top risks", "## Recommended change", "## Confidence", "## Weakest assumption"]
AXES = ["correctness", "insight", "practical", "risk"]
ABSTAIN = "OUT OF DOMAIN"

def member_status(text):
    """'answered', 'abstained', or ('invalid', reason). An abstention is valid on its own; an answer needs all five sections."""
    body = text.strip()
    if not body: return ("invalid", "empty output")
    if ABSTAIN in body and not any(h in body for h in SECTIONS): return "abstained"
    for i, h in enumerate(SECTIONS):
        if h not in body: return ("invalid", f"missing section: {h}")
        after = body.split(h, 1)[1]
        nxt = [after.find(o) for o in SECTIONS if o != h and o in after]
        content = after[:min(nxt)] if nxt else after
        if len(re.sub(r"[\s\-\*\[\]_.]", "", content)) < 12: return ("invalid", f"empty section: {h}")
    return "answered"

def parse_review(text, members):
    """One reviewer's rubric blocks -> {member: {axis: int} | None for an abstainer}. Raises ValueError on anything malformed:
    wrong member set, duplicate member, missing/extra key, a score that is not an integer 1-5."""
    out = {}
    for block in re.findall(r"```rubric\n(.*?)```", text, re.S):
        d = {}
        for line in (l.strip() for l in block.strip().splitlines() if l.strip()):
            m = re.fullmatch(r"(\w+):\s*(.+)", line)
            if not m or m[1] in d: raise ValueError(f"malformed or duplicate line: {line!r}")
            d[m[1]] = m[2].strip()
        name = d.get("member", "").replace("Member:", "").strip()
        if name not in members: raise ValueError(f"unknown member: {name!r}")
        if name in out: raise ValueError(f"duplicate block for {name}")
        if set(d) != {"member", "abstain", *AXES}: raise ValueError(f"{name}: keys {sorted(d)}")
        if d["abstain"].lower() == "true":
            if any(d[a].upper() != "N/A" for a in AXES): raise ValueError(f"{name}: an abstainer's axes must be N/A")
            out[name] = None; continue
        if d["abstain"].lower() != "false": raise ValueError(f"{name}: abstain must be true or false")
        if not all(re.fullmatch(r"[1-5]", d[a]) for a in AXES): raise ValueError(f"{name}: axis scores must be integers 1-5, got {[d[a] for a in AXES]}")
        out[name] = {a: int(d[a]) for a in AXES}
    if set(out) != set(members): raise ValueError(f"members missing from the review: {sorted(set(members) - set(out))}")
    return out

def aggregate(reviews, members):
    """reviews: {reviewer: parsed review}. Returns per-member axis means, overall mean and per-axis population variance.
    Abstainers (None in any valid review, or no scores at all) are left out of every average."""
    res = {}
    for m in members:
        rows = [r[m] for r in reviews.values() if r.get(m)]
        if not rows: res[m] = None; continue
        means = {a: st.mean(x[a] for x in rows) for a in AXES}
        res[m] = {"means": means, "overall": st.mean(means.values()), "variance": {a: st.pvariance([x[a] for x in rows]) if len(rows) > 1 else 0.0 for a in AXES}, "n": len(rows)}
    return res

def split_members(reviews, members, min_gap=2):
    """Clause 2 with explicit tie handling: a reviewer places a member top-2 (bottom-2) on an axis when fewer than two
    members scored strictly higher (lower) there. The clause fires only when some reviewer has the member top-2 and another
    has it bottom-2 AND those two scores differ by at least `min_gap` — a one-point gap among tied scores is grading noise."""
    hits = []
    for a in AXES:
        for m in members:
            tops, bots = [], []
            for rev in reviews.values():
                if not rev.get(m): continue
                vals = [rev[k][a] for k in members if rev.get(k)]
                if len(set(vals)) == 1: continue  # a flat tie says nothing about rank
                s = rev[m][a]
                if sum(v > s for v in vals) < 2: tops.append(s)
                if sum(v < s for v in vals) < 2: bots.append(s)
            if tops and bots and max(tops) - min(bots) >= min_gap: hits.append((m, a, max(tops), min(bots)))
    return hits

def trigger(reviews, members, positions=None):
    agg = aggregate(reviews, members); fired = []
    for m, r in agg.items():
        if r: fired += [f"clause 1: variance {r['variance'][a]:.2f} on {a} for {m}" for a in AXES if r["variance"][a] >= 1.5]
    fired += [f"clause 2: {m} is top-2 for one reviewer ({hi}) and bottom-2 for another ({lo}) on {a}" for m, a, hi, lo in split_members(reviews, members)]
    if positions:
        total = sum(positions.values())
        if total and max(positions.values()) * 2 <= total: fired.append(f"clause 3: no position holds a majority ({positions})")
    return agg, fired

def main(argv):
    if len(argv) < 2 or argv[1] not in ("members", "aggregate"): print(__doc__); return 2
    if argv[1] == "members":
        bad = 0
        for f in argv[2:]:
            s = member_status(open(f).read()); bad += isinstance(s, tuple)
            print(f"{f}: {s if isinstance(s, str) else 'INVALID — ' + s[1]}")
        return 1 if bad else 0
    args = argv[2:]; members, positions, files = None, None, []
    while args:
        x = args.pop(0)
        if x == "--members": members = [m.strip() for m in args.pop(0).split(",")]
        elif x == "--positions": positions = {k.strip(): int(v) for k, v in (p.rsplit(":", 1) for p in args.pop(0).split(","))}
        else: files.append(x)
    if not members or not files: print(__doc__); return 2
    reviews, bad = {}, 0
    for f in files:
        try: reviews[f] = parse_review(open(f).read(), members)
        except ValueError as e: bad += 1; print(f"{f}: EXCLUDED — {e}")
    if len(reviews) * 2 <= len(files): print("more than half the reviewers failed validation: the run is degraded — say so in the output")
    if not reviews: return 1
    agg, fired = trigger(reviews, members, positions)
    print(f"{'member':24}" + "".join(f"{a[:7]:>9}" for a in AXES) + "  overall   n")
    for m in sorted(members, key=lambda k: -(agg[k]["overall"] if agg[k] else -1)):
        r = agg[m]; print(f"{m:24}" + ("  abstained — left out of every average" if not r else "".join(f"{r['means'][a]:9.2f}" for a in AXES) + f"  {r['overall']:7.2f}  {r['n']:2}"))
    print("debate trigger: " + ("FIRES — " + "; ".join(fired) if fired else "does not fire" + ("" if positions else " on clauses 1-2 (pass --positions to check clause 3)")))
    return 1 if bad else 0

if __name__ == "__main__": sys.exit(main(sys.argv))
