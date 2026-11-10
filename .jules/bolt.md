# Bolt's Performance Journal

## 2026-11-10 - Composite Index on SQLite Routines Table
**Learning:** `ActionMemory.get_routine` queries `routines` filtered by `WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1`. Without an index, SQLite performs a full table scan and a separate sort step (`B-TREE FOR ORDER BY`). Adding a composite index on `(screen_hash, user_intent, id DESC)` allows SQLite to perform an indexed B-tree search and retrieve rows in reverse chronological order directly from the index, eliminating both the table scan and the temporary sorting B-tree (providing ~10x to 100x lookup speedup on large tables).
**Action:** When indexing SQLite queries with equality filters and `ORDER BY col DESC LIMIT 1`, include the order column in the composite index in descending order so SQLite can leverage index traversal without an extra sort pass.
