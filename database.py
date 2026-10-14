import sqlite3

DB_PATH = "answers_cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                user_intent TEXT PRIMARY KEY,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache en utilisant une requête paramétrée contre l'injection SQL."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # En utilisant '?' pour les paramètres, SQLite prévient toute injection SQL
        cursor.execute(
            "SELECT response FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache avec une requête paramétrée contre l'injection SQL."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée sécurisée
        cursor.execute(
            "INSERT OR REPLACE INTO answer_cache (user_intent, response) VALUES (?, ?)",
            (user_intent, response),
        )
        conn.commit()
