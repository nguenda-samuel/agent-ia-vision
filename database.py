import sqlite3

DB_PATH = "answers_cache.db"


def _init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answers_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str) -> str | None:
    # Input validation: enforce string type and non-empty input
    if not isinstance(user_intent, str) or not user_intent.strip():
        return None

    # Input length limit: sanitize input to prevent DoS via massive queries
    clean_intent = user_intent.strip()[:1000]
    try:
        _init_db()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # SECURITY: Use parameterized queries (?) to prevent SQL Injection
            cursor.execute(
                "SELECT answer FROM answers_cache WHERE user_intent = ?",
                (clean_intent,),
            )
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        # Fail securely without leaking internal database error details
        return None


def save_answer(user_intent: str, answer: str) -> None:
    # Input validation
    if not isinstance(user_intent, str) or not user_intent.strip():
        return
    if not isinstance(answer, str) or not answer.strip():
        return

    clean_intent = user_intent.strip()[:1000]
    try:
        _init_db()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            # SECURITY: Parameterized query prevents SQL Injection on cache inserts
            cursor.execute(
                """
                INSERT OR REPLACE INTO answers_cache (user_intent, answer)
                VALUES (?, ?)
                """,
                (clean_intent, answer),
            )
            conn.commit()
    except sqlite3.Error:
        # Fail securely
        pass
