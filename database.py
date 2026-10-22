import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialize the SQLite database table for answer caching."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(prompt: str, db_path: str = DB_PATH) -> str | None:
    """Retrieve a cached answer for a given prompt using parameterized queries to prevent SQL injection."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT answer FROM cache WHERE prompt = ?", (prompt,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    except sqlite3.OperationalError:
        # Table might not exist yet; initialize once and retry
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT answer FROM cache WHERE prompt = ?", (prompt,))
            result = cursor.fetchone()
            if result:
                return result[0]
            return None


def save_answer(prompt: str, answer: str, db_path: str = DB_PATH):
    """Save an answer in the cache using parameterized queries to prevent SQL injection."""
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO cache (prompt, answer)
                VALUES (?, ?)
                """,
                (prompt, answer),
            )
            conn.commit()
    except sqlite3.OperationalError:
        # Table might not exist yet; initialize once and retry
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT OR REPLACE INTO cache (prompt, answer)
                VALUES (?, ?)
                """,
                (prompt, answer),
            )
            conn.commit()
