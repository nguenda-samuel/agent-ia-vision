## 2026-10-12 - Parameterized Queries for SQLite Database Cache

**Vulnerability:** Raw or unparameterized database access in user intent response caching can allow SQL injection attacks if input strings are directly formatted into SQL statements.
**Learning:** `ai_engine.py` depended on a missing `database` module that required implementation for answer caching. Additionally, strict `.gitignore` patterns can accidentally omit crucial source files unless un-ignored.
**Prevention:** Always use parameterized SQL placeholders (`?`) for SQLite queries when accepting user inputs or prompt strings, and verify `.gitignore` explicit rules when adding new required modules.
