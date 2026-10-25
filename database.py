import sqlite3

DB_PATH = "cache.db"


def _init_db():
    """Initializes SQLite cache database with parameterized table schema."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                query TEXT PRIMARY KEY,
                response TEXT
            )
            """
        )
        conn.commit()


_init_db()


def get_cached_answer(query: str) -> str | None:
    """Retrieves cached response securely using parameterized query to prevent SQL injection."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Secure parameterized query against SQL injection
        cursor.execute("SELECT response FROM cache WHERE query = ?", (query,))
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(query: str, response: str) -> None:
    """Saves response into cache securely using parameterized query to prevent SQL injection."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Secure parameterized query against SQL injection
        cursor.execute(
            "INSERT OR REPLACE INTO cache (query, response) VALUES (?, ?)",
            (query, response),
        )
        conn.commit()
