import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialize the cache database table safely."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                user_intent TEXT PRIMARY KEY,
                cached_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve a cached answer for a user intent safely using parameterized queries."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Secure parameterized query prevents SQL injection
        cursor.execute(
            "SELECT cached_answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Save or update a cached answer using parameterized queries to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Secure parameterized query prevents SQL injection
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, cached_answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET
                cached_answer = excluded.cached_answer,
                created_at = CURRENT_TIMESTAMP
        """,
            (user_intent, answer),
        )
        conn.commit()
