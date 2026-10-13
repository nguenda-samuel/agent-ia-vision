import sqlite3

DB_PATH = "cached_answers.db"


def _init_db(db_path: str = DB_PATH):
    """Initializes the SQLite database table for cached answers if it does not exist."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cached_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Retrieves a cached AI response for a given user intent using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection
        cursor.execute(
            "SELECT answer_json FROM cached_answers WHERE user_intent = ? LIMIT 1",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer_json: str, db_path: str = DB_PATH):
    """Saves or updates an AI response for a user intent using parameterized query."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection
        cursor.execute(
            """
            INSERT INTO cached_answers (user_intent, answer_json)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer_json = excluded.answer_json
        """,
            (user_intent, answer_json),
        )
        conn.commit()
