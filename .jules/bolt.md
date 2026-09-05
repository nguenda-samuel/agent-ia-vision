## 2026-03-05 - SQLite Indexing on Routine Memory Lookups
**Learning:** Frequent queries filtering on `screen_hash` and `user_intent` in SQLite memory routines perform full table scans without an index. Creating a compound index `idx_routines_hash_intent(screen_hash, user_intent)` reduces query execution time dramatically (from O(N) to O(log N)).
**Action:** Always check SQLite schema initialization in local memory or cache layers and add compound indexes for multi-column lookup patterns.
