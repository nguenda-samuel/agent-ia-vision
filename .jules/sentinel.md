## 2026-09-04 - Parameterized Queries for AI Cache Database
**Vulnerability:** The AI Engine relied on a `database` module (`get_cached_answer` and `save_answer`) for caching responses based on `user_intent`, which was missing and exposed SQL injection risks if implemented via string concatenation.
**Learning:** Raw user inputs (such as user prompt intents in AI assistants) passed directly into SQL statements can allow attacker-controlled SQL execution or cache tampering.
**Prevention:** Always use parameterized SQL queries (`?` placeholders with argument tuples in `sqlite3`) when querying or persisting user-supplied inputs in the database.
