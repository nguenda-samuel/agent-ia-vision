import sqlite3

DEFAULT_DB_PATH = "cache.db"


def init_db(db_path: str = DEFAULT_DB_PATH):
    """Initialize the SQLite cache table if it does not exist."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DEFAULT_DB_PATH) -> str | None:
    """Retrieve a cached answer safely using parameterized queries."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL Injection
        cursor.execute(
            "SELECT response_text FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, response_text: str, db_path: str = DEFAULT_DB_PATH):
    """Save an answer response to the cache safely using parameterized queries."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL Injection
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (user_intent, response_text)
            VALUES (?, ?)
            """,
            (user_intent, response_text),
        )
        conn.commit()
