# Q01 Arm A raw output
# salvaged_from_context: true
# salvage_note: First call invoked wise-men skill (harness bug). Retry with skill-suppression preamble used.
# model: sonnet-4.6
# spec_hash: 5a42ae140f8c44a42c0a60076d0aec9a026a04ef37f74e976d4417daa78571b8

Split it up. A 1200-line component doing auth, form state, and API calls is three or four distinct concerns crammed into one place, and that's the actual problem — the line count is just the symptom.

The practical cost you're already paying: when something breaks, you have to hold the entire file in your head to reason about it. When you want to reuse the auth logic or the API calls somewhere else, you can't. When you write a test, you have to set up everything at once — which is probably why your tests are minimal.

The split that makes sense here is roughly: extract the auth logic into a custom hook (useAuth or similar), extract the API calls into either a custom hook or a service layer, and let the form state live in its own hook too. The component itself then becomes mostly JSX that wires those hooks together. Each piece becomes independently testable and the component drops to maybe 150-200 lines.

The "should I split" question is really about whether the pieces have different reasons to change. Auth logic changes when your auth provider changes. API calls change when your backend changes. Form state changes when your UX changes. Those are genuinely independent, so they belong in different places.

The one caveat: if you're planning to delete this component soon, or it truly is a one-off throwaway, the cost of splitting might not be worth it. But if you keep adding to it — which you said you do — the compounding cost of not splitting grows every week. The longer you wait, the harder the extraction becomes because everything gets more tangled.

Do it now while you can still see the seams. Start with the API calls since those are usually the easiest to pull out cleanly.
