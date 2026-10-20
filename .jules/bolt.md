## 2026-10-20 - SQLite Composite Indexing for Routine Lookups

**Learning:** `ActionMemory.get_routine` queries `routines` filtered by `screen_hash` and `user_intent`. Without a composite index on `(screen_hash, user_intent)`, SQLite performs a full table scan O(N) on every screen match attempt. Adding a composite index reduces query latency from ~2.09ms down to ~0.19ms on 10k records (>11x speedup).
**Action:** When creating SQLite schema tables for cached or frequent lookups, always create composite indexes on the filtered columns during `_init_db`.
