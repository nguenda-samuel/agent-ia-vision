import sqlite3
from typing import Optional

DEFAULT_DB_PATH = "agent_memory.db"


def _init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialise la table cache des réponses dans la base de données SQLite."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cached_answers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT UNIQUE,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(
    intent: str, db_path: str = DEFAULT_DB_PATH
) -> Optional[str]:
    """Récupère la réponse mise en cache pour une intention donnée de manière sécurisée (requête paramétrée)."""
    if not intent:
        return None
    try:
        _init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Utilisation de requêtes paramétrées (?) pour prévenir toute injection SQL
            cursor.execute(
                "SELECT answer FROM cached_answers WHERE intent = ? ORDER BY id DESC LIMIT 1",
                (intent,),
            )
            row = cursor.fetchone()
            return row[0] if row else None
    except Exception:
        # Évite d'exposer des détails internes ou stack traces en cas d'erreur DB
        return None


def save_answer(
    intent: str, answer: str, db_path: str = DEFAULT_DB_PATH
) -> None:
    """Sauvegarde ou met à jour la réponse dans le cache SQLite de manière sécurisée (requête paramétrée)."""
    if not intent or not answer:
        return
    try:
        _init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Utilisation de requêtes paramétrées (?) pour prévenir toute injection SQL
            cursor.execute(
                """
                INSERT INTO cached_answers (intent, answer)
                VALUES (?, ?)
                ON CONFLICT(intent) DO UPDATE SET answer = excluded.answer, created_at = CURRENT_TIMESTAMP
            """,
                (intent, answer),
            )
            conn.commit()
    except Exception:
        # Évite d'exposer des détails internes en cas d'erreur DB
        pass
