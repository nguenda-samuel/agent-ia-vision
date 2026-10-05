import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialize SQLite database for caching AI responses safely."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS answers (intent TEXT PRIMARY KEY, response TEXT)"
        )


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve cached AI answer using parameterized SQL query to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            "SELECT response FROM answers WHERE intent = ?", (user_intent,)
        ).fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Save AI answer using parameterized SQL query to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT OR REPLACE INTO answers (intent, response) VALUES (?, ?)",
            (user_intent, response),
        )
