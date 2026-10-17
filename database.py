import sqlite3

DB_PATH = "answers_cache.db"
_db_initialized = False


def _init_db():
    """Initializes the SQLite cache database lazily with an indexed user_intent column."""
    global _db_initialized
    if _db_initialized:
        return
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    _db_initialized = True


def get_cached_answer(user_intent: str) -> str | None:
    """Fast indexed lookup for cached prompt response."""
    try:
        _init_db()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT answer FROM answer_cache WHERE user_intent = ?",
                (user_intent,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
    except sqlite3.Error:
        pass
    return None


def save_answer(user_intent: str, answer: str):
    """Saves prompt response into SQLite cache using INSERT OR REPLACE."""
    try:
        _init_db()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO answer_cache (user_intent, answer)
                VALUES (?, ?)
                """,
                (user_intent, answer),
            )
            conn.commit()
    except sqlite3.Error:
        pass
