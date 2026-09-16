# For agents other than Claude Code

This repository is a Claude Code plugin/skill. The protocol is `SKILL.md`; stage prompts are in `resources/prompts/`; personas and model routing in `resources/`. Any agent that can spawn parallel sub-tasks can follow the protocol as written. Two things are Claude-Code-specific:

- **The tool-restricted member** (`agents/wise-member.md`, Read/Grep/Glob only) is what makes council recursion structurally impossible. In another runtime, reproduce it with whatever sandboxing you have; without it, members are only *asked* not to spawn.
- **Argument placeholders**: `SKILL.md` avoids `$`+digit sequences because Claude Code substitutes them; nothing else in the file depends on the host.

The eval in `eval-data/` and the checks in `scripts/check.sh` are runtime-independent.
