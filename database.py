import sqlite3

DB_PATH = "agent_cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the SQLite cache table safely."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves a cached answer using parameterized queries to prevent SQL injection."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT answer FROM answer_cache
            WHERE user_intent = ?
            ORDER BY id DESC LIMIT 1
            """,
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Saves or updates an answer cache entry securely using parameterized queries."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer = excluded.answer, created_at = CURRENT_TIMESTAMP
            """,
            (user_intent, answer),
        )
        conn.commit()
