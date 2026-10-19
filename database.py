import sqlite3

DEFAULT_DB_PATH = "cache.db"


def _init_db(db_path: str = DEFAULT_DB_PATH):
    """Initialize SQLite database for caching AI responses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DEFAULT_DB_PATH) -> str | None:
    """Retrieve cached answer for a user intent using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Secure parameterized query preventing SQL injection
        cursor.execute(
            "SELECT response FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, response: str, db_path: str = DEFAULT_DB_PATH):
    """Save user intent and response to cache using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Secure parameterized query preventing SQL injection
        cursor.execute(
            """
            INSERT INTO cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET
                response = excluded.response,
                created_at = CURRENT_TIMESTAMP
            """,
            (user_intent, response),
        )
        conn.commit()
