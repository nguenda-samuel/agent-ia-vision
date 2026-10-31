# Bolt's Journal
## 2026-10-31 - ActionMemory SQLite composite index
**Learning:** SQLite tables storing user interaction sequences/routines experience sequential scans `SCAN routines` when querying `(screen_hash, user_intent)` without an index. Adding a composite index on `(screen_hash, user_intent, id DESC)` allows the optimizer to perform an index search and retrieve the latest matching routine in O(log N) time without filesort.
**Action:** Always verify query plans with `EXPLAIN QUERY PLAN` on SQLite tables querying multiple criteria with `ORDER BY ... DESC LIMIT 1`.
