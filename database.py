import sqlite3

DB_PATH = "agent_memory.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache de réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache à l'aide d'une requête paramétrée sécurisée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL Injection
        cursor.execute(
            "SELECT answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Sauvegarde ou met à jour une réponse en cache avec une requête paramétrée sécurisée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Parameterized query to prevent SQL Injection
        cursor.execute(
            """
            INSERT OR REPLACE INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
            """,
            (user_intent, answer),
        )
        conn.commit()
