import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table de cache si elle n'existe pas."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée en utilisant une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT response_text FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, response_text: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse dans le cache de manière sécurisée en utilisant une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO cache (user_intent, response_text)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response_text = excluded.response_text
        """,
            (user_intent, response_text),
        )
        conn.commit()
