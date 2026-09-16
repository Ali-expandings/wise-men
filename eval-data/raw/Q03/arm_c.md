# Q03 Arm C Chairman synthesis
# salvaged_from_context: true
# Council: 5 sonnet-4.6 members (Pragmatist, Skeptic, Architect, Maintainer, Devil's Advocate)
# Reviewers: 5 haiku-4.5
# Chairman: main thread sonnet-4.6

## Answer

Don't guess — measure. Start with `EXPLAIN (ANALYZE, BUFFERS) <your slowest query>` (both flags matter: ANALYZE gives actual rows vs estimates, BUFFERS shows disk vs cache). In parallel, enable `pg_stat_statements` if not already on and query it sorted by `total_exec_time` to find the worst offenders across all executions, not just the one you're staring at. That's your triage in under 30 minutes.

What the EXPLAIN output tells you, in order of how often it's the answer:

1. **Seq Scan on a table with >10k rows** → missing index. Most common. Add the index on the filter or join column.
2. **`rows=10 (actual rows=50000)`** → stale statistics. Run `ANALYZE <table>` to refresh `pg_statistic`; the planner will pick a better plan with no schema change.
3. **High `Buffers: shared read` vs `shared hit`** → I/O bound, working set doesn't fit in `shared_buffers` cache. Either grow shared_buffers or reduce the working set.
4. **Nested Loop with `loops=N` on large N** → join is iterating an inner table many times; check for missing index on the join column or a function applied to an indexed column (e.g., `WHERE lower(email)=$1` won't use a plain index on `email`).

"Too many joins" is rarely the root cause — Postgres handles joins fine when cardinality estimates are accurate. If you see correct plans with correct estimates and still 3-4 seconds, you're in the harder cases: dead-tuple bloat from neglected vacuum (`SELECT relname, n_dead_tup FROM pg_stat_user_tables`), N+1 patterns from your ORM (visible as many short queries in `pg_stat_activity`, not one long one), or lock contention (`SELECT pid, wait_event_type FROM pg_stat_activity WHERE wait_event IS NOT NULL`).

Before adding any index: verify the slow query is slow *in psql directly*. If it's fast in psql and slow through the app, the problem is ORM query generation, connection pool exhaustion, or network — none of which indexing fixes.

## Dissent worth keeping

Devil's Advocate position, preserved: the most common diagnostic trap is jumping to EXPLAIN ANALYZE and adding an index that drops latency to 800ms today, while the real underlying problem — dead-tuple bloat, autovacuum starvation, connection pool saturation — silently compounds, and three weeks later queries are back to 6 seconds. The 5-minute-cheap check before any query tuning: `pg_stat_user_tables.n_dead_tup` vs `n_live_tup` ratios, `pg_stat_activity` lock-waits, and whether a connection pooler exists at all. If you don't have a connection pooler and your app opens a connection per request, that overhead alone can be 2-3 seconds before Postgres even sees the query — and no index will fix that.

## Confidence

High on the diagnostic path (EXPLAIN+pg_stat_statements is universally applicable); medium on the specific fix because without seeing the schema and query text, any concrete recommendation is conditional on what the EXPLAIN reveals.
