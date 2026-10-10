import sqlite3

DEFAULT_DB_PATH = "cache.db"


def _init_db(db_path: str = DEFAULT_DB_PATH):
    """Initialize the SQLite table for response caching."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DEFAULT_DB_PATH) -> str | None:
    """Safely fetch a cached response for the given user intent using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Use parameterized query '?' to prevent SQL injection vulnerabilities
        cursor.execute(
            "SELECT response_text FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response_text: str, db_path: str = DEFAULT_DB_PATH):
    """Safely insert or update a cached response using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Use parameterized query '?' to prevent SQL injection vulnerabilities
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, response_text)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response_text = excluded.response_text
            """,
            (user_intent, response_text),
        )
        conn.commit()
