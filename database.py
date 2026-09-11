import sqlite3

DB_PATH = "agent_memory.db"


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
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
    return conn


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve cached answer using parameterized query to prevent SQL injection."""
    if not user_intent:
        return None
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Save answer to cache using parameterized query to prevent SQL injection."""
    if not user_intent or not answer:
        return
    with _get_connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer = excluded.answer
        """,
            (user_intent, answer),
        )
        conn.commit()
