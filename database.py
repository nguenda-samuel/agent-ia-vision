import sqlite3

DB_PATH = "cache.db"


def _ensure_db_init(db_path: str = DB_PATH):
    """Initializes SQLite database table for response caching."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves a cached response for a given user intent.

    Uses parameterized queries (?) to prevent SQL injection vulnerabilities.
    """
    _ensure_db_init(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT cached_response FROM answer_cache WHERE user_intent = ?",
                (user_intent,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    except sqlite3.Error:
        return None


def save_answer(user_intent: str, cached_response: str, db_path: str = DB_PATH):
    """Saves or updates a response in the cache for a given user intent.

    Uses parameterized queries (?) to prevent SQL injection vulnerabilities.
    """
    _ensure_db_init(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO answer_cache (user_intent, cached_response)
                VALUES (?, ?)
                ON CONFLICT(user_intent) DO UPDATE SET cached_response=excluded.cached_response
                """,
                (user_intent, cached_response),
            )
            conn.commit()
    except sqlite3.Error:
        pass
