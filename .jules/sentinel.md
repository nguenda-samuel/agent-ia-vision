## 2026-09-04 - SQLite Parameterized Queries in Answer Cache
**Vulnerability:** Raw string formatting/concatenation in SQLite database queries could lead to SQL injection vulnerabilities when processing untrusted user intents.
**Learning:** SQLite database caching module was missing in `ai_engine.py` imports (`database.py`). Re-implementing cache query operations using standard parameter substitution (`?`) prevents SQL injection attacks and handles special characters safely.
**Prevention:** Always use parameterized placeholders (`?`) in SQLite queries instead of formatted strings or string concatenation.
