## 2026-09-04 - Parameterized SQL Queries for AI Response Caching
**Vulnerability:** Unsafe SQL string interpolation when querying or saving cached user intents and AI responses in SQLite database.
**Learning:** Missing database abstraction module in ai_engine.py led to direct database calls that could introduce SQL injection if user intents containing malicious SQL characters were improperly concatenated into SQL statements.
**Prevention:** Always use parameterized SQL query placeholders (`?` in sqlite3) rather than string formatting or concatenation when inserting or retrieving user input from SQLite.
