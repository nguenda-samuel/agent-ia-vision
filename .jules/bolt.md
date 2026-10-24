## 2026-10-24 - SQLite Composite Indexing for Routine Lookups
**Learning:** In `memory.py`, querying `routines` by `screen_hash` and `user_intent` without a composite database index forced SQLite to perform an O(N) full table scan on every lookup. Adding a composite index `(screen_hash, user_intent)` makes query lookups O(log N) and improves lookup speeds by over 200x (0.67ms -> 0.0027ms for 10k rows).
**Action:** Always check SQLite schema definitions for missing composite indexes on frequently queried combinations of columns.
