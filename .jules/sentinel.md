## 2026-09-18 - Parameterized Queries for Database Cache

**Vulnerability:** Unsanitized user inputs in raw SQL queries create severe SQL injection vulnerabilities when persisting or querying cached response data.
**Learning:** `ai_engine.py` relied on an external database module for caching user intent answers. Storing dynamic user prompts directly in SQL queries without parameterization allows attackers to manipulate SQL commands.
**Prevention:** Always use SQLite parameterized queries (`?` placeholders) when binding dynamic values into SQL statements.
