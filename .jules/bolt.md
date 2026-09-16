## 2026-09-16 - SQLite Composite Index on Action Memory
**Learning:** Querying SQLite tables by multiple non-indexed columns (`screen_hash` and `user_intent`) causes O(N) full table scans that degrade linearly as routine history grows.
**Action:** Always add composite indexes on multi-column lookup predicates (`(screen_hash, user_intent)`) during schema initialization in SQLite-backed memory systems.
