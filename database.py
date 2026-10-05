import sqlite3

DB_PATH = "cache.db"


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves a cached answer for a user intent safely using parameterized query."""
    if not user_intent:
        return None
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS qa_cache (user_intent TEXT PRIMARY KEY, answer TEXT)"
        )
        # SECURITY: Parameterized query prevents SQL injection
        cursor.execute(
            "SELECT answer FROM qa_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Saves or updates a cached answer for a user intent safely using parameterized query."""
    if not user_intent or answer is None:
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS qa_cache (user_intent TEXT PRIMARY KEY, answer TEXT)"
        )
        # SECURITY: Parameterized query prevents SQL injection
        cursor.execute(
            "INSERT OR REPLACE INTO qa_cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
