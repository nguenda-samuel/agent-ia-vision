import sqlite3

DB_PATH = "cache.db"


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Get SQLite database connection and ensure schema table exists."""
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            user_intent TEXT PRIMARY KEY,
            answer TEXT
        )
        """
    )
    return conn


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve cached answer using parameterized query to prevent SQL injection."""
    conn = _get_connection(db_path)
    try:
        cursor = conn.cursor()
        # Security: Parameterized query protects against SQL injection
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        conn.close()


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Save user_intent and answer using parameterized query to prevent SQL injection."""
    conn = _get_connection(db_path)
    try:
        with conn:
            conn.execute(
                "INSERT OR REPLACE INTO cache (user_intent, answer) VALUES (?, ?)",
                (user_intent, answer),
            )
    finally:
        conn.close()
