# Security

This is markdown executed by an LLM; the attack surface is prompt injection, not code execution.

Guarded surfaces: the user's question (wrapped as data in every member and reviewer prompt), member answers entering the grading packet, and file content members Read. Members run as `wise-member` — Read/Grep/Glob only — so a hostile file cannot make a member run commands, write, or spawn. The spend ceiling in the runbook limits cost amplification from a crafted "high-stakes" question.

Report a bypass by opening an issue with the minimal prompt or file that triggers it.
