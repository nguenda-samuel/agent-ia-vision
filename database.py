import sqlite3

DB_PATH = "answers_cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache de réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answers_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str = DB_PATH
) -> str | None:
    """Recherche une réponse sauvegardée pour l'intention utilisateur donnée."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute(
            "SELECT cached_response FROM answers_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse dans la base de données SQLite."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL injection
        cursor.execute(
            """
            INSERT OR REPLACE INTO answers_cache (user_intent, cached_response)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
