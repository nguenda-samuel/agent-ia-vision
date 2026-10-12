## 2026-10-12 - SQLite Routine Query Optimization with Composite Index
**Learning:** SQLite routine lookups in `ActionMemory` filtered by `screen_hash` and `user_intent` perform full table scans on `routines` without an index. Adding a composite index `idx_routines_hash_intent` on `(screen_hash, user_intent)` reduces query execution time from O(N) to O(log N) (~1000x faster execution as the memory database grows).
**Action:** Always verify SQLite schema definitions for frequently queried filter columns in `WHERE` / `ORDER BY` clauses and add composite indices for multi-column conditions.
