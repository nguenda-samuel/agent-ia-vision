import sqlite3
from typing import Optional

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH) -> None:
    """Initialize the cache table if it does not exist."""
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


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> Optional[str]:
    """Retrieve cached answer for a given user_intent securely using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Save or update cached answer for a given user_intent securely using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute(
            """
            INSERT INTO cache (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer = excluded.answer
            """,
            (user_intent, answer),
        )
        conn.commit()
