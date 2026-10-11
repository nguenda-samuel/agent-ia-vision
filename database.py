import sqlite3

DB_PATH = "cache.db"
_initialized_dbs = set()


def _ensure_db_initialized(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses une seule fois par chemin de BD."""
    if db_path in _initialized_dbs:
        return
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answers_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()
    _initialized_dbs.add(db_path)


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache de manière sécurisée.

    Utilise des requêtes paramétrées (?) pour se protéger contre les injections SQL.
    """
    _ensure_db_initialized(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection vulnerabilities
        cursor.execute(
            "SELECT response FROM answers_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        if result:
            return result[0]
        return None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour une réponse en cache.

    Utilise des requêtes paramétrées (?) pour se protéger contre les injections SQL.
    """
    _ensure_db_initialized(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Security: Parameterized query prevents SQL injection vulnerabilities
        cursor.execute(
            """
            INSERT INTO answers_cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response
        """,
            (user_intent, response),
        )
        conn.commit()
