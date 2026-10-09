## 2026-09-04 - Parameterized Queries for SQLite Cache Module
**Vulnerability:** Raw string formatting/concatenation or unparameterized queries when storing user intent strings in SQLite database caches can allow SQL injection attacks.
**Learning:** `ai_engine.py` depended on `database.py` (`get_cached_answer` and `save_answer`), which was missing from tracking/repository state. Implementing parameterization using `?` placeholders prevents SQL injection vulnerabilities when handling arbitrary user input.
**Prevention:** Always use parameterized SQL queries (`cursor.execute(sql, (param1, param2))`) instead of string formatting or concatenation when inserting or selecting user-provided strings.
