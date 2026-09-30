import sqlite3

DB_PATH = "agent_memory.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table de cache pour les réponses textuelles."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Recherche une réponse en cache en utilisant des requêtes paramétrées contre l'injection SQL."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection vulnerabilities from user_intent
        cursor.execute(
            "SELECT response FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour la réponse en cache de manière sécurisée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection vulnerabilities
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response
            """,
            (user_intent, response),
        )
        conn.commit()
