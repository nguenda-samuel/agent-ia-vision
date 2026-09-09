import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Initialize answer_cache table if it doesn't exist."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Safely retrieves cached answer using parameterized SQLite query to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # SECURITY: Parameterized query prevents SQL injection from user_intent input
        cursor.execute(
            "SELECT answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Safely saves or updates cached answer using parameterized SQLite query."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # SECURITY: Parameterized query prevents SQL injection
        cursor.execute(
            """
            INSERT OR REPLACE INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
