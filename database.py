import sqlite3

DB_PATH = "answers_cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initialize SQLite database for caching answers."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cached_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve a cached answer using parameterized query (prevents SQL injection)."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query protects against SQL injection from user_intent
        cursor.execute(
            "SELECT answer FROM cached_answers WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Save or update a cached answer using parameterized query (prevents SQL injection)."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query protects against SQL injection from user_intent and answer
        cursor.execute(
            """
            INSERT OR REPLACE INTO cached_answers (user_intent, answer)
            VALUES (?, ?)
            """,
            (user_intent, answer),
        )
        conn.commit()
