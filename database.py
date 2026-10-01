import sqlite3

DB_PATH = "answers_cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
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


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée via une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM cache WHERE intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(
    user_intent: str, answer_json: str, db_path: str = DB_PATH
) -> None:
    """Sauvegarde une réponse dans le cache de manière sécurisée via une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer_json),
        )
        conn.commit()
