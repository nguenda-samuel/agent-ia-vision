## 2025-08-31 - Secure SQLite Cache Implementation for AI Engine
**Vulnerability:** `ai_engine.py` imported a missing `database` module for caching query answers. If implemented naively without query parameterization, user input intents could lead to SQL injection vulnerabilities.
**Learning:** Cache implementations handling untrusted user input strings must use SQL parameterization (`?` placeholders) rather than string interpolation.
**Prevention:** Always use parameterized SQL queries with sqlite3 or ORMs when dealing with dynamic input.
