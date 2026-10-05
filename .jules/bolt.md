## 2026-10-05 - SQLite Indexing for Routine Lookups
**Learning:** In action/routine memory stores (`ActionMemory`), `routines` queries filter by `screen_hash` and `user_intent`. Without a composite index on `(screen_hash, user_intent)`, SQLite executes full table scans (`SCAN routines`), causing linear degrading lookup latency as history grows.
**Action:** Always verify composite indexes exist for multi-column WHERE clauses on frequently queried SQLite tables in agent memory/cache modules.
