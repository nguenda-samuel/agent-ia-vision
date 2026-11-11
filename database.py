import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS response_cache (
                user_intent TEXT PRIMARY KEY,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """)


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de façon sécurisée (requête paramétrée)."""
    if not isinstance(user_intent, str):
        return None
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute(
            "SELECT response FROM response_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Enregistre ou met à jour une réponse en cache de façon sécurisée."""
    if not isinstance(user_intent, str) or not isinstance(response, str):
        raise TypeError("user_intent and response must be strings")
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            INSERT INTO response_cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response
            """,
            (user_intent, response),
        )
