# Bolt's Journal - Critical Learnings

## 2026-08-30 - Composite SQLite index for routine lookups
**Learning:** `ActionMemory.get_routine` queries `routines` filtered on `(screen_hash, user_intent)` and ordered by `id DESC LIMIT 1`. Without an index, SQLite performs a full table scan `SCAN routines` across all historical routines. Creating a composite index `(screen_hash, user_intent, id DESC)` allows SQLite to use a B-tree search and satisfies the reverse ID ordering directly, eliminating sorting and scanning overhead.
**Action:** Always create matching composite indexes covering equality filter columns and ordering columns for cache/routine databases in SQLite.
