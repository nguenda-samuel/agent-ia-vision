import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS response_cache (
                user_intent TEXT PRIMARY KEY,
                response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )""")


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse en cache avec une requête paramétrée sécurisée."""
    if not isinstance(user_intent, str) or not user_intent.strip():
        return None
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        # Parameterized query to prevent SQL injection vulnerabilities
        cursor = conn.execute(
            "SELECT response FROM response_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str = DB_PATH):
    """Enregistre ou met à jour une réponse en cache avec une requête paramétrée."""
    if not isinstance(user_intent, str) or not user_intent.strip():
        return
    if not isinstance(response, str):
        return
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        # Parameterized query to prevent SQL injection vulnerabilities
        conn.execute(
            """INSERT INTO response_cache (user_intent, response)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response""",
            (user_intent, response),
        )
