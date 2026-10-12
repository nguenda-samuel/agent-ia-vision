import sqlite3

DB_PATH = "cache.db"
_db_initialized = False


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache de questions-réponses."""
    global _db_initialized
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS qa_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                prompt TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    _db_initialized = True


def get_cached_answer(prompt: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache en utilisant une requête paramétrée pour éviter les injections SQL."""
    if not _db_initialized or db_path != DB_PATH:
        init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM qa_cache WHERE prompt = ?", (prompt,))
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(prompt: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache avec une requête paramétrée sécurisée."""
    if not _db_initialized or db_path != DB_PATH:
        init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO qa_cache (prompt, answer)
            VALUES (?, ?)
            """,
            (prompt, answer),
        )
        conn.commit()
