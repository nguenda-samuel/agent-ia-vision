## 2026-09-09 - Parameterized Queries for AI Response SQLite Cache
**Vulnerability:** Unsanitized user intent strings passed into SQLite database queries create a risk of SQL injection attacks if string formatting/concatenation is used.
**Learning:** Cache lookups based on raw user inputs (like user intent prompts) must always bind parameters dynamically using DB driver parameterization (`?`) rather than building raw SQL queries.
**Prevention:** Always use parameterized SQLite queries (`cursor.execute("... WHERE col = ?", (param,))`) when querying or saving data derived from user inputs.
