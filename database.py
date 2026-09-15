import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the SQLite database table for caching AI answers."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS response_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


# Ensure database table exists on module load
_init_db()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves a cached answer safely using parameterized queries to prevent SQL injection."""
    if not user_intent:
        return None
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Use parameterized query (?) to prevent SQL injection
        cursor.execute(
            "SELECT response_text FROM response_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response_text: str, db_path: str = DB_PATH):
    """Saves or updates a cached answer safely using parameterized queries."""
    if not user_intent or not response_text:
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Use parameterized query (?, ?) to prevent SQL injection
        cursor.execute(
            """
            INSERT INTO response_cache (user_intent, response_text)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response_text=excluded.response_text
            """,
            (user_intent, response_text),
        )
        conn.commit()
