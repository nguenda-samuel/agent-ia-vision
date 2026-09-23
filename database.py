import sqlite3

DB_PATH = "agent_cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the SQLite database cache table."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def save_answer(
    user_intent: str, response_text: str, db_path: str = DB_PATH
) -> None:
    """Saves or updates a cached response safely using parameterized queries."""
    if not isinstance(user_intent, str) or not isinstance(response_text, str):
        return

    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cache (user_intent, response_text)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET
                response_text = excluded.response_text,
                created_at = CURRENT_TIMESTAMP
        """,
            (user_intent, response_text),
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str = DB_PATH
) -> str | None:
    """Retrieves a cached response safely using parameterized queries."""
    if not isinstance(user_intent, str):
        return None

    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT response_text FROM cache
            WHERE user_intent = ?
        """,
            (user_intent,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        return None
