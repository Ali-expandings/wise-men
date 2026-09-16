# Contributing

- Run `scripts/check.sh` before every commit. It enforces the invariants the protocol depends on (trigger formula identical in three files, no `$`-digit in `SKILL.md`, agent file stamp, version consistency, PII sweep of the tree and git history, eval reproduction).
- `eval-data/` is a record, not code. Do not edit persisted arms, judgments, or parsed scores; add new runs under a new question id and log them in `eval-data/SESSION_LOG.md`.
- `SKILL.md` is auto-loaded whole on every invocation. Standing rule: changes must not add net lines to it; put detail in `resources/`.
- A protocol change needs either a live council run recorded with `resources/council-record.md` or eval evidence — not only reasoning.
- No attribution trailers in commits.
