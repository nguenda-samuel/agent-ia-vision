import sqlite3


def get_cached_answer(user_intent: str, db_path: str = "agent_memory.db") -> str | None:
    """Retrieve cached answer for a given user intent if it exists.

    SECURITY: Uses parameterized queries to prevent SQL injection.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT action_data FROM routines
                WHERE user_intent = ?
                ORDER BY id DESC LIMIT 1
            """,
                (user_intent,),
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    except Exception:
        return None


def save_answer(user_intent: str, action_data_str: str, db_path: str = "agent_memory.db"):
    """Save an answer for a user intent in the database cache.

    SECURITY: Uses parameterized queries to prevent SQL injection.
    """
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Ensure table exists if database module is used standalone
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS routines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    screen_hash TEXT,
                    user_intent TEXT,
                    action_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            cursor.execute(
                """
                INSERT INTO routines (screen_hash, user_intent, action_data)
                VALUES (?, ?, ?)
            """,
                ("text_cache", user_intent, action_data_str),
            )
            conn.commit()
    except Exception:
        pass
