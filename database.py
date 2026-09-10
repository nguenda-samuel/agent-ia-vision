import sqlite3

DB_PATH = "cache.db"
_initialized_dbs = set()


def init_db(db_path: str = DB_PATH):
    """Initialize SQLite cache database table (executes once per db path)."""
    if db_path in _initialized_dbs:
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
    _initialized_dbs.add(db_path)


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve cached answer using parameterized queries to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Save answer to cache using parameterized queries to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
