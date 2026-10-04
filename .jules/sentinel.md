## 2026-09-04 - SQLite Parameterized Queries in Caching Layer
**Vulnerability:** The AI engine module (`ai_engine.py`) imported `get_cached_answer` and `save_answer` from `database`, but `database.py` was missing from the repository, risking unsafe string concatenation if re-implemented without query parameterization.
**Learning:** SQLite caching layers taking user inputs (`user_intent`) can be vulnerable to SQL injection if string formatting or concatenation is used instead of parameterized queries (`?` placeholders).
**Prevention:** Always use parameterized SQL queries (`?`) for database operations involving user input, and ensure core database modules referenced by imports are tracked in version control.
