## 2026-08-31 - [Missing database module with parameterized SQLite cache]
**Vulnerability:** Missing database module caused ModuleNotFoundError in ai_engine.py when accessing cache, creating risk of unparameterized inline query implementation.
**Learning:** The application ai_engine.py relies on database.py for caching user intent responses.
**Prevention:** Implement database.py using parameterized SQLite queries (`?`) to ensure cached user intents are safely handled without SQL injection risks.
