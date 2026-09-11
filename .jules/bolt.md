# Bolt's Journal - Critical Learnings

## 2025-09-11 - SQLite Routine Lookup Indexing
**Learning:** Querying `routines` table by `screen_hash` and `user_intent` without an index causes full table scans in SQLite as routine history grows.
**Action:** Always ensure composite index on `(screen_hash, user_intent)` is created when initializing `routines` table.
