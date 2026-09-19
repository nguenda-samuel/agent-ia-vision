## 2026-09-19 - Fix Missing Database Module and SQL Injection Vulnerability in AI Engine Cache

**Vulnerability:** `ai_engine.py` imported `get_cached_answer` and `save_answer` from a missing `database` module, which caused a runtime `ModuleNotFoundError`. Building database caching logic without parameterized queries could lead to SQL injection vulnerabilities when processing user intents.
**Learning:** Core engine files had hard dependencies on missing helper modules (`database.py`), causing runtime crashes and leaving room for unsanitized database interactions.
**Prevention:** Always implement database interactions using parameterized queries (`?` placeholders in SQLite) and ensure all imported modules exist and are covered by automated unit tests.
