# Bolt's Journal - Critical Performance Learnings

## 2026-08-30 - SQLite routine lookup index
**Learning:** `ActionMemory.get_routine` queries `routines` filtered on `(screen_hash, user_intent)` and ordered by `id DESC LIMIT 1`. Without an index, SQLite performs a full table scan `SCAN routines` across all historical routines. Creating a composite index `(screen_hash, user_intent, id DESC)` allows SQLite to use a b-tree search and satisfies the reverse ID ordering directly, eliminating sorting and scanning overhead.
**Action:** Always create matching composite indexes covering equality filter columns and ordering columns for cache/routine databases in SQLite.
