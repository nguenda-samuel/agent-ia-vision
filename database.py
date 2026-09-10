import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée (requête paramétrée contre les injections SQL)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Sécurité: Utilisation de requête paramétrée ? pour prévenir les injections SQL
        cursor.execute(
            "SELECT answer FROM answers WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour une réponse dans le cache de manière sécurisée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Sécurité: Utilisation de requête paramétrée ? pour prévenir les injections SQL
        cursor.execute(
            """
            INSERT INTO answers (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer = excluded.answer
            """,
            (user_intent, answer),
        )
        conn.commit()
