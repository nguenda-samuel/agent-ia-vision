## 2025-05-18 - Input Validation & Defensive JSON Deserialization in SQLite Memory
**Vulnerability:** Unvalidated parameter types passed to SQLite query methods and uncaught `json.JSONDecodeError` during data retrieval could lead to database corruption or unhandled runtime crashes.
**Learning:** SQLite parameterized queries prevent SQL injection, but unvalidated inputs or corrupted records retrieved from storage can still cause downstream failures if deserialization isn't defensively wrapped.
**Prevention:** Always validate incoming parameter types before query execution and wrap `json.loads` calls in try-except blocks to fail securely when loading untrusted or stored JSON data.
