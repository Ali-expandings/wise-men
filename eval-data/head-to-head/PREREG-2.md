# Head-to-head v2 — adding the two most-installed council skills (pre-registration)

Written and committed 2026-09-17, after v1 was published and before any v2 arm ran. Nothing below changes after this commit except through dated amendments; results go in `RESULTS-V2.md`. v1 (`PREREG.md`, `RESULTS.md`) stands as published.

## Why v2

The competitor scan (`COMPETITOR-SCAN.md`, 2026-09-17: skills.sh install counts, GitHub stars, community search) found that v1 covered the two most-used stress-test skills and the two best-known councils, but not the two most-installed general-purpose council skills. v2 adds them.

## Arms (8)

The six v1 arms, using their v1 outputs unchanged (`raw/<Q>/<arm>.md`), plus two new arms:

| arm | source | commit | license | how it is run |
|---|---|---|---|---|
| ecc-council | affaan-m/ECC `skills/council/SKILL.md` (repo 260,744★; 7,746 installs) | 8321021c54d6 | MIT | as written, with the no-human rule below |
| warp-council | warpdotdev/common-skills `.agents/skills/council/SKILL.md` (repo 579★; 24,515 installs) | 69b4753651ab | MIT | as written, with the adaptations below |

**Parity** — identical to v1 and its Amendment 1: a fresh `general-purpose` orchestrator on Sonnet 5 receives the skill file and the question verbatim; skills may spawn subagents, in the foreground; an arm may Read only its own skill file, never search the filesystem or notes; it returns only the finished output; an incomplete run is re-run once, and a second failure is recorded and scored as absent.

**Adaptations** (disclosed wherever v2 results appear):
- *ECC council*: where the skill would ask the user a clarifying question, it states the answer it assumes and continues — the same no-human rule v1 applied to brainstorming and grilling.
- *Warp council*: the skill is written for Warp's `run_agents` launcher and for model-diverse councils (an Opus-class, a GPT-class and an open-source model), and it asks the user to approve the member list before launching. Here members are launched with Claude Code's subagent tool on the models this harness offers (Claude models only) — the skill's own fallback rule allows the closest available models and asks for the substitution to be noted; the approval wait is skipped (no human), with the member plan kept in the output; members are read-only.

**Timing** — v1 outputs were produced on 2026-09-16/17; the two new arms are produced after v1's publication, with the same orchestrator model and rules.

## Questions

The same 8 as v1 — Q05, Q09, Q13, Q19, Q25, Q36, Q48, Q55 — text from `eval-data/questions.yaml`, unchanged.

## Blinding and judge

A new sealed order for eight slots per question (`blinding2.yaml`, seed 20260917, generated before any v2 arm ran). One fresh Opus judge per question sees all eight responses as A–H; `judge-prompt-8.txt` is word for word v1's prompt apart from the response count. Normalization is identical to v1 (`normalize()` in `h2h.py`; the two new arms get the same header and status-line stripping as the other council arms). Every arm is re-judged in v2, so v2 scores for the original six arms are a fresh judgment, not v1's numbers.

## Analysis (fixed)

As v1: per arm, mean composite (max 25) and per-axis means over the 8 questions; wins against the plain answer; wise-men's wins, ties and losses against each arm. No significance test (N=8). Reproduce with `H2H_STUDY=v2 python3 eval-data/head-to-head/h2h.py report`.

## Reporting

v2 is reported whatever it shows, next to v1, with both studies' caveats. If v2 changes the ordering, the README leads with v2.
