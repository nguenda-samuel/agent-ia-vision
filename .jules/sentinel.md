## 2026-09-14 - Missing Database Cache Module with SQL Injection Risk
**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was missing from the repository. Re-implementing dynamic SQL query string construction would expose user input (`user_intent`) to SQL injection vulnerabilities.
**Learning:** When adding caching or persistence layers for user queries/intents, always use parameterized queries (`?` placeholders) in SQLite to ensure user inputs are sanitized and safely stored/queried.
**Prevention:** Use parameterized queries in all SQLite operations (`cursor.execute("... WHERE col = ?", (param,))`) and include automated tests verifying resilience against SQL injection payloads.
