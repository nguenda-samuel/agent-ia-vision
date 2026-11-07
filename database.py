import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS answer_cache (
                user_intent TEXT PRIMARY KEY,
                cached_response TEXT
            )
        """)
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée (requête paramétrée)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éviter toute injection SQL
        cursor.execute(
            "SELECT cached_response FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Enregistre ou met à jour une réponse en cache avec une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éviter toute injection SQL
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, cached_response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET cached_response = excluded.cached_response
        """,
            (user_intent, answer),
        )
        conn.commit()
