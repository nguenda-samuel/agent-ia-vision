import sqlite3

DB_PATH = "cache.db"
_db_initialized = False


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    global _db_initialized
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
    _db_initialized = True


def _ensure_db(db_path: str):
    if not _db_initialized or db_path != DB_PATH:
        init_db(db_path)


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée (requête paramétrée)."""
    _ensure_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM cache WHERE intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache de manière sécurisée (requête paramétrée)."""
    _ensure_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
