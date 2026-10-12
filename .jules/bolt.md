## 2026-10-12 - Composite SQLite index on ActionMemory routines

**Learning:** Lookups in SQLite `routines` table filtering on `(screen_hash, user_intent)` were executing O(N) full table scans. Adding a composite index `idx_routines_hash_intent ON routines(screen_hash, user_intent)` speeds up routine query lookups by ~7.0x (from ~1.40ms/query down to ~0.20ms/query for 10k rows).

**Action:** Always verify that multi-column query filters in SQLite (like `WHERE screen_hash = ? AND user_intent = ?`) have corresponding composite database indexes defined in `_init_db()` schema setup.
