import sqlite3

DB_PATH = "agent_cache.db"


def init_db(db_path: str = DB_PATH) -> None:
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée par requête paramétrée."""
    if not isinstance(user_intent, str) or not user_intent.strip():
        return None

    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Requête paramétrée anti-injection SQL
            cursor.execute(
                "SELECT cached_answer FROM answer_cache WHERE user_intent = ?",
                (user_intent.strip(),),
            )
            result = cursor.fetchone()
            return result[0] if result else None
    except Exception:
        return None


def save_answer(
    user_intent: str, answer: str, db_path: str = DB_PATH
) -> None:
    """Sauvegarde ou met à jour une réponse en cache avec requête paramétrée."""
    if not isinstance(user_intent, str) or not user_intent.strip():
        return
    if not isinstance(answer, str):
        return

    try:
        init_db(db_path)
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Requête paramétrée UPSERT anti-injection SQL
            cursor.execute(
                """
                INSERT INTO answer_cache (user_intent, cached_answer)
                VALUES (?, ?)
                ON CONFLICT(user_intent) DO UPDATE SET
                    cached_answer = excluded.cached_answer,
                    created_at = CURRENT_TIMESTAMP
                """,
                (user_intent.strip(), answer),
            )
            conn.commit()
    except Exception:
        pass
