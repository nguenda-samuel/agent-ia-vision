import sqlite3

DEFAULT_DB_PATH = "cache.db"


def _init_db(db_path: str = DEFAULT_DB_PATH):
    """Initialize the SQLite database table for answer caching."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DEFAULT_DB_PATH) -> str | None:
    """Retrieve cached AI answer safely using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DEFAULT_DB_PATH):
    """Save or update AI answer in database safely using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cache (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer=excluded.answer
            """,
            (user_intent, answer),
        )
        conn.commit()
