## 2026-09-24 - SQLite Composite Index for Routine Lookups
**Learning:** Routine lookups in `ActionMemory` filter on both `screen_hash` and `user_intent` without a database index, resulting in O(N) full table scans in `agent_memory.db`.
**Action:** Always ensure composite indexes are added to SQLite tables for multi-column query filters (`screen_hash`, `user_intent`) during initialization.
