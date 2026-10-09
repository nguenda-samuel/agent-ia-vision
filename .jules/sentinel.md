## 2026-10-09 - Parameterized SQL Queries for Local Cache
**Vulnerability:** Missing database caching module required by `ai_engine.py` posed a risk of introducing unsafe string formatting or concatenation when persisting user prompts and AI responses.
**Learning:** Raw user input (`user_intent`) stored in SQLite database tables can lead to SQL injection vulnerabilities if dynamically constructed SQL strings are used instead of parameterized queries.
**Prevention:** Always use parameterized SQLite queries (`?` placeholders) when executing SQL statements with user input. Maintain strict `.gitignore` whitelist entries to ensure security modules and tests are tracked.
