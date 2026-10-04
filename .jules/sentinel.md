## 2026-10-04 - Parameterized SQLite Query Protection for AI Response Cache
**Vulnerability:** Missing database caching module referenced by `ai_engine.py` risking SQL injection if implemented with unparameterized raw string formatting or concatenation.
**Learning:** SQLite queries constructed with string concatenation or format strings allow malicious user intent strings to break out of query context and execute arbitrary SQL commands or manipulate database state.
**Prevention:** Always use parameterized queries with placeholder bindings (`?` parameters) in SQLite and database drivers to guarantee untrusted inputs are bound strictly as data parameters rather than executable SQL statements.
