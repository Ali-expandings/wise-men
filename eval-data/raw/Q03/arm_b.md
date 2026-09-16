# Q03 Arm B raw output
# salvaged_from_context: true
# salvage_note: First call leaked STEP 1 perspectives visibly (4 persona paragraphs + "Agent tool not available" preamble). Retried with stricter prompt; second call cleanly emitted ## Answer / ## Dissent / ## Confidence with internal reasoning inside <thinking> tags. <thinking> stripped during blinding.
# model: sonnet-4.6
# leakage_check: PASSED after 1 retry

[<thinking> block stripped during blinding contained: difficulty assessment + 5 persona internal answers (Pragmatist, Skeptic, Architect, Performance Hawk, Devil's Advocate) + Stage 2 simulated scores]

[VISIBLE OUTPUT — judge sees:]
## Answer

Start with `EXPLAIN (ANALYZE, BUFFERS) <your query>` — not just EXPLAIN, add both flags. This tells you two things no other tool gives you in one shot: the actual row counts vs planner estimates (divergence here = stale statistics, fix with `ANALYZE <table>`), and the buffer hit/read ratio (shared read >> shared hit = I/O bound, not CPU bound). Look specifically for:

- **Seq Scan on a table with >10k rows** — almost always a missing index. The fix is obvious.
- **Nested Loop with `loops=N` where N is large** — a join is iterating an inner table many times. Fix: check if the inner table has an index on the join column.
- **`rows=10 (actual rows=50000)`** — planner estimate is wildly off. Run `ANALYZE` on that table, then re-run EXPLAIN. The planner will pick a better plan without touching the query.

Second step, run this against `pg_stat_statements`:
```sql
SELECT query, calls, mean_exec_time, total_exec_time
FROM pg_stat_statements
ORDER BY total_exec_time DESC LIMIT 10;
```
This shows you where total wall-clock time actually goes across all executions — not just the one query you're staring at. Optimize the top of this list, not the query that happened to be slow when someone was watching.

Third, check if the slow query is slow *in psql directly* or only through your app/ORM. If it's fast in psql, the problem is connection pooling overhead or ORM generating a different query than you think — not Postgres internals. Add `pg_stat_activity` to check for lock waits:
```sql
SELECT pid, wait_event_type, wait_event, query
FROM pg_stat_activity WHERE wait_event IS NOT NULL;
```

The likely culprits in rough order of frequency: (1) missing index causing Seq Scan, (2) stale statistics causing wrong join order, (3) function applied to indexed column (`WHERE lower(email) = $1` can't use a plain index — needs a functional index), (4) covering index missing (index finds rows but heap fetch is still slow — add the selected columns to the index). "Too many joins" is rarely the root cause — Postgres handles joins fine when cardinality estimates are accurate.

## Dissent worth keeping

The Devil's Advocate position deserves weight before you touch a single index: if you have no connection pooler (PgBouncer or equivalent) in front of Postgres, your 3-4 seconds may be connection establishment overhead that indexing will not touch. Check that first — it takes 10 minutes and can eliminate the problem entirely. More broadly: if the joins are the problem at the data model level (8-table joins to generate a dashboard), query optimization is bounded and the real fix is a materialized view or application-side cache. Every index you add also makes writes slower. Don't assume the bottleneck is inside Postgres until you've confirmed it.

## Confidence

High — EXPLAIN (ANALYZE, BUFFERS) + pg_stat_statements is the deterministic triage path that will isolate the bottleneck class in under 30 minutes for any query in this latency range; the only uncertainty is whether the root cause sits outside Postgres (connection pooling, lock contention), which the dissent covers.
