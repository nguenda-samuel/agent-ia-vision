import sqlite3


def _init_db(db_path: str = "cache.db"):
    """Initialize the SQLite cache table if it does not exist."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = "cache.db") -> str | None:
    """Retrieve cached answer using parameterized query to prevent SQL injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection attacks
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = "cache.db"):
    """Save answer to cache using parameterized query to prevent SQL injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection attacks
        cursor.execute(
            "INSERT OR REPLACE INTO cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
