import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the database schema using parameterized execution."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves cached answer for a given user intent safely using parameterized SQL query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection vulnerabilities
        cursor.execute(
            "SELECT cached_answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        if row:
            return row[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Saves or updates cached answer for a given user intent safely using parameterized SQL query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection vulnerabilities
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, cached_answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET cached_answer = EXCLUDED.cached_answer
            """,
            (user_intent, answer),
        )
        conn.commit()
