# Bolt's Journal - Critical Learnings

## 2026-10-24 - SQLite Composite Indexing in ActionMemory
**Learning:** In SQLite, querying `routines` with `WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1` performs a full table scan and temporary sort when unindexed. Adding a composite index on `(screen_hash, user_intent, id DESC)` optimizes both the filter condition and the descending ordering directly from index B-tree traversal (~15x speedup).
**Action:** When creating tables for routine or cached data with composite lookup keys and ordering, always create covering composite indexes including the sort key.
