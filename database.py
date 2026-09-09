import sqlite3

DEFAULT_DB_PATH = "agent_cache.db"
_initialized_dbs = set()


def _init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initializes SQLite database table for caching AI answers using parameterized schema."""
    if db_path in _initialized_dbs:
        return
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
    _initialized_dbs.add(db_path)


def get_cached_answer(
    user_intent: str, db_path: str = DEFAULT_DB_PATH
) -> str | None:
    """Retrieves cached response for user intent using parameterized query to prevent SQL Injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized SQL query protects against SQL injection
        cursor.execute(
            "SELECT cached_answer FROM answer_cache WHERE user_intent = ? ORDER BY id DESC LIMIT 1",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(
    user_intent: str, answer: str, db_path: str = DEFAULT_DB_PATH
) -> None:
    """Saves answer to SQLite cache using parameterized query to prevent SQL Injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized SQL query protects against SQL injection
        cursor.execute(
            "INSERT OR REPLACE INTO answer_cache (user_intent, cached_answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
