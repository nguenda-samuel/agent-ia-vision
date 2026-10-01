import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str | None = None):
    """Initialise la table SQLite pour les réponses en cache."""
    if db_path is None:
        db_path = DB_PATH
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


def get_cached_answer(user_intent: str, db_path: str | None = None) -> str | None:
    """Récupère la réponse en cache pour une intention donnée de manière sécurisée.

    Utilise des requêtes paramétrées (?) pour éviter les injections SQL.
    """
    if db_path is None:
        db_path = DB_PATH
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT answer FROM cached_answers WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, answer: str, db_path: str | None = None):
    """Sauvegarde la réponse dans la base de données de manière sécurisée.

    Utilise des requêtes paramétrées (?) pour éviter les injections SQL.
    """
    if db_path is None:
        db_path = DB_PATH
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT OR REPLACE INTO cached_answers (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
