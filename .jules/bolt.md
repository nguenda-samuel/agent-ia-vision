# Bolt's Journal - Critical Learnings

## 2026-09-07 - SQLite indexing on ActionMemory routines
**Learning:** `ActionMemory.get_routine` filters by `screen_hash` and `user_intent` without a composite index on `(screen_hash, user_intent)`. Adding `CREATE INDEX IF NOT EXISTS idx_routines_hash_intent ON routines(screen_hash, user_intent)` converts linear table scans $O(N)$ into $O(\log N)$ index lookups.
**Action:** Always create compound indexes on foreign/query columns when filtering by multiple keys in SQLite tables.
