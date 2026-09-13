import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache de réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache pour l'intention utilisateur donnée.

    Utilise des requêtes paramétrées pour prévenir les injections SQL.
    """
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT response_text FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, response_text: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache pour l'intention utilisateur.

    Utilise des requêtes paramétrées pour prévenir les injections SQL.
    """
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, response_text)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET
                response_text = excluded.response_text,
                created_at = CURRENT_TIMESTAMP
        """,
            (user_intent, response_text),
        )
        conn.commit()
