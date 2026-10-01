import sqlite3
from typing import Optional

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH) -> None:
    """Initialise la table SQLite de cache de manière sécurisée."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str = DB_PATH
) -> Optional[str]:
    """Récupère une réponse en cache en utilisant des requêtes paramétrées (protégé contre l'injection SQL)."""
    if not user_intent or not isinstance(user_intent, str):
        return None

    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec placeholder '?' pour éviter l'injection SQL
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?",
            (user_intent.strip(),),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH) -> None:
    """Sauvegarde ou met à jour une réponse en cache en utilisant des requêtes paramétrées (protégé contre l'injection SQL)."""
    if not user_intent or not isinstance(user_intent, str) or not answer:
        return

    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec placeholders '?' pour éviter l'injection SQL
        cursor.execute(
            """
            INSERT INTO cache (user_intent, answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET answer = excluded.answer
        """,
            (user_intent.strip(), str(answer)),
        )
        conn.commit()
