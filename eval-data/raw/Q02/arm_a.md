# Q02 Arm A raw output
# salvaged_from_context: false
# model: sonnet-4.6
# skill-suppressed: clean direct prose, no headers, no contamination.
# generated: 2026-05-31 (clean rerun — pilot Q02 was context-only, never persisted)

Your tech lead is right, but probably for the wrong reasons people usually give.

The real argument isn't "design systems are good practice" — it's that 50 engineers writing raw Tailwind utility classes directly in components will produce inconsistent UI within weeks, and the inconsistency compounds. One engineer writes `text-gray-600`, another writes `text-gray-500`, another writes `text-slate-600`. Now your "disabled" state looks three different ways across the app. With raw Tailwind this is nearly impossible to audit or fix systematically.

That said, you don't need a full design system. You need something much smaller: a component library. Concretely, that means:

A `tailwind.config` with a locked-down color palette (remove the full Tailwind color scale, keep only your named semantic tokens like `primary`, `surface`, `muted`, `danger`). This alone eliminates most drift.

A small set of shared primitive components — `Button`, `Input`, `Badge`, `Card`, maybe a layout wrapper. Not 80 components. Eight to twelve. These wrap the Tailwind classes so engineers stop copy-pasting `className="px-4 py-2 rounded text-sm font-medium bg-blue-600 hover:bg-blue-700 text-white"` in fifty places.

That's it. No Storybook required. No design tokens JSON pipeline. No theming engine. Just a `components/ui/` folder with a handful of files and a constrained config.

The cost of doing this up front is maybe two days. The cost of not doing it is that in six months you have a codebase where every "fix the button styles" change requires grep-and-pray across 200 files, and the UI looks like it was built by a committee that never talked to each other — which it was.

So the framing "design system vs. raw Tailwind" is a false choice. The real answer is: constrained Tailwind with shared primitives for the hot-path components. You get 90% of the benefit for 5% of the effort of a proper design system.
