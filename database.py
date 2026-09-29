import sqlite3

# Security: Parameterized queries are used throughout to prevent SQL injection vulnerabilities.

DEFAULT_DB_PATH = "cache.db"


def init_db(db_path: str = DEFAULT_DB_PATH):
    """Initializes the SQLite cache database table safely."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                prompt TEXT PRIMARY KEY,
                answer TEXT NOT NULL
            )
            """
        )
        conn.commit()


def get_cached_answer(prompt: str, db_path: str = DEFAULT_DB_PATH) -> str | None:
    """Retrieves a cached answer using a parameterized SQL query to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM cache WHERE prompt = ?", (prompt,))
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(prompt: str, answer: str, db_path: str = DEFAULT_DB_PATH):
    """Saves or updates a cached answer using a parameterized SQL query to prevent SQL injection."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO cache (prompt, answer) VALUES (?, ?)",
            (prompt, answer),
        )
        conn.commit()
