## 2026-09-04 - Parameterized Queries for SQLite Database Cache

**Vulnerability:**
The `ai_engine` depended on a database cache module for storing and retrieving cached responses using `user_intent`. Unbound string formatting or concatenation when querying SQLite databases with user-controlled input introduces SQL Injection risks.

**Learning:**
`user_intent` originates directly from user input (voice or text). If database caching functions concatenate `user_intent` into raw SQL query strings, attackers could inject arbitrary SQL syntax to manipulate or bypass cache queries. Furthermore, repo files excluded by wildcard `.gitignore` patterns can cause missing module errors if safe database modules are not explicitly whitelisted.

**Prevention:**
Always use parameterized queries (`?` placeholders) with SQLite for all dynamic variables. Never concatenate user input directly into SQL statements. When using wildcard exclusion patterns in `.gitignore`, explicitly whitelist new security-relevant modules (`!database.py`, `!test_database.py`).
