# Bolt's Journal - Critical Performance Learnings

## 2026-08-30 - SQLite routine lookup composite index
**Learning:** `ActionMemory.get_routine` queries `routines` filtered on `(screen_hash, user_intent)` and ordered by `id DESC LIMIT 1`. Without an index, SQLite performs a full table scan across all historical entries (`SCAN routines`). Creating a composite index on `(screen_hash, user_intent, id DESC)` allows SQLite to use a direct B-tree search and satisfies the reverse ID ordering directly, eliminating sorting and scanning overhead.
**Action:** When designing lookup caches in SQLite with equality filters and order-by clauses, create composite indexes matching both the filter columns and the ordering column.
