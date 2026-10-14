import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initialise la table de cache si elle n'existe pas."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cached_answers (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée via requête paramétrée."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée '?' pour prévenir les injections SQL
        cursor.execute(
            "SELECT answer FROM cached_answers WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache de manière sécurisée via requête paramétrée."""
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée '?' pour prévenir les injections SQL
        cursor.execute(
            """
            INSERT OR REPLACE INTO cached_answers (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
