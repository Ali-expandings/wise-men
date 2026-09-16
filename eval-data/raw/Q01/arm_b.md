# Q01 Arm B raw output
# salvaged_from_context: true
# salvage_note: Output had preamble before <thinking> block ("Good, I have enough context..."); stripped during blinding per § 6. Plus <thinking> block also stripped.
# model: sonnet-4.6
# leakage_check: STEP 1 perspectives stayed inside <thinking>; no retry required.

[PREAMBLE — stripped during blinding:]
Good, I have enough context. The component is `App.tsx` at 1179 lines, handling store state, settings, model selection, streaming, scroll logic, and will clearly contain settings UI, chat UI, and API call logic all inline. Let me now give the structured answer.

[<thinking> block — stripped during blinding:]
Pragmatist: "It's working, tests are minimal anyway, splitting won't automatically add tests. Pick the two most painful extraction wins — the auth logic and the API call layer — extract those as hooks/services. Don't boil the ocean. A 600-line component is still big but manageable if the logic is out."
Skeptic: "1200 lines is already a bug farm. You said tests are minimal — that's the real problem. Re-renders are probably catastrophic because everything shares the same state."
Architect: "Three distinct concerns in one file violates SRP at every level. The correct shape is: service layer + custom hooks + leaf components. App.tsx should be <100 lines of composition."
Devil's Advocate: "Stop. The instinct to split is itself the problem. Premature abstraction creates prop drilling, context spaghetti, or over-engineered abstractions you don't need."
User Advocate: "I don't care about file size. I care about the app being fast, correct, and not breaking when you add a feature."

[VISIBLE OUTPUT — what judge sees:]
## Answer

Split it — but be surgical, not wholesale. The file is already past the threshold where the cognitive overhead is real. More importantly, the combination of auth, form state, and API calls in a single component means every state change potentially re-renders all three concerns, and adding tests is nearly impossible because you can't isolate any one piece.

The right extraction order, by value:

1. **API calls → a service module or custom hook (`useChat`, `useStream`).** This is the highest-leverage move. It decouples network logic from render logic, makes the abort/streaming state isolated, and is immediately testable in isolation. Your `completeChat` and swarm calls are good candidates.

2. **Settings/auth state → a custom hook (`useSettings`, `useAuth`).** Settings open/close, API key storage, and defaults are self-contained. Extracting them gives you a hook you can unit-test without mounting anything.

3. **UI sub-components → `SettingsPanel`, `ChatMessage`, `Sidebar`.** These are lower urgency than the logic extraction, but they eliminate re-render bleed between unrelated UI trees.

The goal is not to hit a line-count target. It's that `App.tsx` becomes an orchestrator — composing hooks and components — rather than an implementation. Target ~150–200 lines for the root component after extraction.

The concrete forcing function: next time you try to test a form validation rule or an API retry and you can't without spinning up the whole auth tree, you'll feel exactly why this split is necessary.

## Dissent worth keeping

The Devil's Advocate: "The instinct to split is itself the problem. Every time you split prematurely you create prop drilling, context spaghetti, or over-engineered abstractions you don't need. If you don't have tests now, splitting won't give you tests — it'll give you six files with no tests. Stay in the monolith until the pain is specific and concrete."

## Confidence

Medium-high — four of the five perspectives agreed splitting is necessary; the disagreement is only about timing, not the end state.
