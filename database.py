import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str | None = None):
    """Initialise la table SQLite pour le cache de réponses."""
    path = db_path or DB_PATH
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str | None = None) -> str | None:
    """Récupère la réponse mise en cache pour une intention utilisateur (requête sécurisée)."""
    path = db_path or DB_PATH
    init_db(path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée contre les injections SQL
        cursor.execute(
            "SELECT response FROM cache WHERE user_intent = ?", (user_intent,)
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str | None = None):
    """Sauvegarde la réponse Gemini dans le cache DB (requête sécurisée)."""
    path = db_path or DB_PATH
    init_db(path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée contre les injections SQL
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (user_intent, response)
            VALUES (?, ?)
        """,
            (user_intent, response),
        )
        conn.commit()
