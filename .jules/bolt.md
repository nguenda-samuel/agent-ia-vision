# Bolt's Journal - Critical Learnings

## 2026-10-09 - SQLite Composite Index for Routine Lookups
**Learning:** Frequent query filtering on multiple unindexed text columns (`screen_hash`, `user_intent`) causes full table scans in SQLite as memory db grows. Adding a composite index on `(screen_hash, user_intent)` reduces lookup time from ~0.70s to ~0.01s for 1000 queries over 10k rows (~50x speedup).
**Action:** Always ensure composite indexes exist for multi-column WHERE filter patterns in SQLite tables.
