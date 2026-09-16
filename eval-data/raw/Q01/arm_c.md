# Q01 Arm C Chairman synthesis
# salvaged_from_context: true
# Council: 5 sonnet-4.6 members (Pragmatist, Skeptic, Architect, Maintainer, Devil's Advocate)
# Reviewers: 5 haiku-4.5 (3 refused first call — retried successfully)
# Chairman: main thread sonnet-4.6
# Stage 2 aggregate (5 reviewers): Skeptic 17.2 top, Architect 16.6, DA 12.4 bottom (refusal-retry skewed but consensus held)

## Answer

Split it — but stage the work. The 1200-line file mixing auth, form state, and API calls has three different change velocities sharing one render cycle, one state tree, and zero isolation; the minimal tests turn every change into a trust-fall. Concretely, extract in this order: (1) API calls into a `useSubmitForm` or `useChat`-style custom hook — highest leverage, lowest blast radius; (2) form state into `useFormState`; (3) auth logic into `useAuth` last (most coupled). Target a final component body of ~150-200 lines that reads as composition, not implementation. Each hook becomes unit-testable in isolation, and adding tests stops requiring you to mount the full auth tree.

Sequencing matters. Write 2-3 integration tests for the golden paths (submit-with-fresh-token, submit-during-token-refresh, validation-then-submit) BEFORE the first extraction — that's how you catch the silent regressions during the refactor, and it doubles as the "test seams" the dissent wants you to find naturally. Watch how the first extraction feels for a week. If the codebase feels noisier after `useSubmitForm` is out, stop — that's your signal the seams aren't where you thought. Otherwise continue with the form-state extraction.

This is not a rewrite. It is three focused PRs over two to three weeks.

## Dissent worth keeping

Devil's Advocate, preserved: premature decomposition of a working monolith is one of the most common ways teams destroy velocity, and the coupling here may reflect genuine domain coupling (auth state feeds form validation feeds API authorization headers) rather than accidental complexity. Splitting blind, especially with minimal tests, risks producing a `useAuthFormApi` hook that's 800 lines of the same tangle plus three wrapper components passing refs and callbacks — you've traded one fat file for an opaque dependency graph. The safer-but-slower path is to write integration tests for the three behaviors first, let test seams show natural split points, and only then extract.

## Confidence

Medium-high — five members converged on "split with hooks" with only tactical differences on order; the load-bearing dissent (test-first to avoid wrong boundaries) is incorporated into the staged sequencing rather than overridden.
