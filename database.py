import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the SQLite database cache table."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves cached answer using parameterized query to prevent SQL injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query protects against SQL injection
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Saves answer to cache using parameterized query to prevent SQL injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query protects against SQL injection
        cursor.execute(
            "INSERT OR REPLACE INTO cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
