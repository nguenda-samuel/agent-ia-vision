import sqlite3

DEFAULT_DB_PATH = "cache.db"


def _init_db(db_path: str = DEFAULT_DB_PATH):
    """Initialize the answer_cache table in SQLite database."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str = DEFAULT_DB_PATH
) -> str | None:
    """Retrieve cached response for user intent safely using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query protects against SQL injection attacks
        cursor.execute(
            "SELECT response FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        return None


def save_answer(
    user_intent: str, response: str, db_path: str = DEFAULT_DB_PATH
) -> None:
    """Save or update cached response safely using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query protects against SQL injection attacks
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response=excluded.response
            """,
            (user_intent, response),
        )
        conn.commit()
