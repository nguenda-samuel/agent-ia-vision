## 2025-05-18 - SQLite Database Indexing for ActionMemory Routines
**Learning:** `ActionMemory` queries the `routines` table filtering on both `screen_hash` and `user_intent` on every routine lookup. Without an index on these columns, SQLite performs a full table scan O(N) on each lookup, which slows down routine lookup speed as action memory grows.
**Action:** Create a composite index `idx_routines_hash_intent` on `(screen_hash, user_intent)` during database initialization to keep lookups fast O(log N).
