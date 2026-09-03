## 2026-09-03 - SQLite composite index on routines table
**Learning:** `ActionMemory.get_routine()` queries SQLite routines table filtering on `screen_hash` and `user_intent` ordered by ID. Adding a composite index `idx_routines_hash_intent` on `(screen_hash, user_intent)` yields ~1.6x to ~10x query speedup as the table grows.
**Action:** Always check SQLite query filter columns in local persistence layers and add composite indexes for multi-column WHERE clauses.
