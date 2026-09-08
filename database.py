import sqlite3

DB_PATH = "cache.db"


def _init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str) -> str | None:
    """Retrieve cached response for user_intent using parameterized query."""
    _init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT response FROM cache WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, response: str) -> None:
    """Save or update response for user_intent using parameterized query."""
    _init_db()
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response
        """,
            (user_intent, response),
        )
        conn.commit()
