# Competitor scan — are we testing against the skills people actually use?

Scanned 2026-09-17. Usage = all-time installs from the skills.sh registry API (`skills.sh/api/search`, 40 keywords, 3,511 skills); awareness = GitHub stars (GitHub API) and community reach (X, YouTube, Instagram, Reddit and Hacker News search results). Reddit pages could not be fetched directly (blocked for scrapers), so Reddit evidence is limited to thread titles and snippets from search results.

**The job:** take a hard question or decision and stress-test it — adversarial challenge or several perspectives — before recommending.

## Skills that do this job, by usage

| Skill | Installs (skills.sh) | Repo stars | Kind | In head-to-head v1 |
|---|--:|--:|---|---|
| `grill-me` / `grilling` — mattpocock/skills | 1,160,865 / 717,927 | 263,960 | one-agent interview that stress-tests a plan | **yes** (`grilling`; `grill-me` delegates to it) |
| `brainstorming` — obra/superpowers | 365,683 | 287,855 | one-agent design dialogue | **yes** |
| `council` — warpdotdev/common-skills | 24,515 | 579 | model-diverse subagent council (+ `cross-critique`, 18,709) | **no** |
| `council` — affaan-m/ECC | 7,746 | 260,744 | four-voice council: in-context voice + Skeptic, Pragmatist, Critic subagents | **no** |
| `council` — boshu2/agentops | 2,983 | 441 | council | no |
| `llm-council` — aiwithremy (Ole Lehmann's "LLM Council") | 1,001 | 2,110 | 5 advisors + peer review + chairman; viral on X, YouTube, Instagram | **yes** |
| Council — danielmiessler/LifeOS | not listed (ships inside LifeOS) | 19,039 | 3-round debate | **yes** |
| War Council — zapier/wade-skills (Zapier CEO) | not listed | 89 | persona advisors; widely shared by its author | no |

Out of scope, and why: `marketing-council` (29,835 installs) is marketing-only; `decision-mapping` (mattpocock, 44,875) is a multi-session planning tracker; `pre-mortem` (9,615) and `strategy-red-team` (8,620, phuryn/pm-skills) are single-pass PM templates; `think` (tw93/Waza, 13,816) turns an idea into a build plan; karpathy/llm-council (24,883★) is a web app that needs an OpenRouter key, not a skill.

## Verdict

v1 covers the two most-used stress-test skills (grilling, brainstorming) and the two best-known councils (Ole Lehmann's LLM Council, LifeOS Council). It does **not** include the two most-installed general-purpose council skills: **ECC `council`** (from one of the most-starred Claude Code repos) and **Warp `council`**. Warp's skill is written for model-diverse councils (Opus + GPT + an open-source model via Warp's `run_agents`); inside Claude Code it would run on Claude models only, which must be disclosed if it is tested.

## Follow-up (2026-09-17)

Both gaps were closed by head-to-head v2 ([PREREG-2.md](PREREG-2.md), [RESULTS-V2.md](RESULTS-V2.md)): ECC `council` and Warp `council` were run on the same 8 questions and all eight arms were re-judged blind. Warp's council ran on Claude models only, as disclosed. The table above is left as scanned.
