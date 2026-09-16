# Q03 Arm A raw output
# salvaged_from_context: true
# salvage_note: Skill-suppression preamble used. No contamination.
# model: sonnet-4.6

Start with EXPLAIN ANALYZE. Run it on your slowest queries and look at the actual row estimates vs. actual rows — when the planner thinks a step will return 10 rows but gets 50,000, that's usually where things go wrong. The key numbers to focus on are actual time on each node, and whether you're seeing Seq Scan on large tables (almost always bad) vs. Index Scan.

From there, the diagnosis usually branches into a few distinct causes:

Bad estimates and stale statistics are more common than people expect. If EXPLAIN ANALYZE shows the planner making wildly wrong row count guesses, run ANALYZE on the relevant tables, and check your autovacuum settings — if it's not running frequently enough, statistics get stale and the planner makes poor choices. You can also run pg_stat_user_tables to see when tables were last analyzed.

Missing indexes are easy to spot: look for Seq Scan nodes on large tables combined with a Filter line showing many rows being removed. The fix is usually straightforward — create an index on the filtered or joined column. But pay attention to join order in the EXPLAIN output too; if you're joining a big table to a small one in the wrong direction, an index on the wrong side won't help much.

Query structure issues show up as nested loop joins with huge loop counts, or hash joins that spill to disk (you'll see "Batches: N" where N > 1 in the hash join node). Too many joins isn't inherently the problem — it's usually that the joins are happening in suboptimal order, or that intermediate result sets are exploding in size before the filtering happens. Moving WHERE clauses earlier, using CTEs carefully (in Postgres 12+ they're inlined by default, but in older versions they act as optimization fences), and avoiding SELECT * so you're not hauling unnecessary columns through joins all help here.

For systematic diagnosis, enable pg_stat_statements if it's not already on. It aggregates query stats over time and lets you rank queries by total time, mean time, and call count — which tells you whether you have one catastrophically slow query or many moderately slow ones adding up. That distinction matters because the fix is different.

The practical workflow: pg_stat_statements to find your worst offenders by total_time, EXPLAIN (ANALYZE, BUFFERS) on each one to see the actual execution plan and buffer hits/misses, then check whether you're hitting shared buffers or going to disk (Buffers: shared hit vs. read). If you're seeing a lot of disk reads on a query that should be hot, your shared_buffers or work_mem might be undersized for the workload, which is a configuration problem rather than a query problem.

Don't tune indexes in isolation — each index adds write overhead, so identify the highest-impact ones first rather than indexing everything that appears in a WHERE clause.
