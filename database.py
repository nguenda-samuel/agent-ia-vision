import sqlite3

DB_NAME = "cache.db"


def _init_db(db_name: str = DB_NAME):
    with sqlite3.connect(db_name) as conn:
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


def get_cached_answer(user_intent: str, db_name: str = DB_NAME) -> str | None:
    """Retrieves cached answer safely using parameterized queries."""
    _init_db(db_name)
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Secure parameterized query preventing SQL injection
        cursor.execute(
            "SELECT answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_name: str = DB_NAME):
    """Saves answer to cache safely using parameterized queries."""
    _init_db(db_name)
    with sqlite3.connect(db_name) as conn:
        cursor = conn.cursor()
        # Secure parameterized query preventing SQL injection
        cursor.execute(
            """
            INSERT OR REPLACE INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
