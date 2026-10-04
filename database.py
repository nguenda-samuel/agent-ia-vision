import sqlite3


def init_db(db_path: str = "cache.db"):
    """Initialise la table SQLite pour la mise en cache des réponses."""
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


def save_answer(user_intent: str, answer: str, db_path: str = "cache.db"):
    """Sauvegarde une réponse dans le cache SQLite en utilisant des requêtes paramétrées."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = "cache.db") -> str | None:
    """Récupère la réponse mise en cache de manière sécurisée sans risque d'injection SQL."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT answer FROM answer_cache WHERE user_intent = ?
        """,
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None
