## 2025-05-18 - Composite Index for SQLite Routines Lookups
**Learning:** SQLite query lookups in `routines` filtered on `(screen_hash, user_intent)` perform sequential scans without indexes, taking ~26ms for 10k rows. Adding a composite index reduces query execution time to ~3.6ms (~7x speedup).
**Action:** Always check SQLite query execution plans when matching multiple conditions like hash + user input intent.
