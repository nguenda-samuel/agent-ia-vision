import sqlite3

DB_PATH = "cache.db"


def _ensure_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache via requête paramétrée anti-injection."""
    _ensure_db(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.execute(
                "SELECT cached_response FROM answer_cache WHERE user_intent = ?",
                (user_intent,),
            )
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        return None


def save_answer(user_intent: str, cached_response: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour une réponse via requête paramétrée anti-injection."""
    _ensure_db(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                INSERT INTO answer_cache (user_intent, cached_response)
                VALUES (?, ?)
                ON CONFLICT(user_intent) DO UPDATE SET cached_response=excluded.cached_response
                """,
                (user_intent, cached_response),
            )
    except sqlite3.Error:
        pass
