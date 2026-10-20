import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses."""
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
    """Récupère une réponse en cache de manière sécurisée (requête paramétrée anti-injection SQL)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # SECURITY: Use parameterized query to prevent SQL injection vulnerabilities
        cursor.execute(
            "SELECT answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde une réponse en cache de manière sécurisée (requête paramétrée anti-injection SQL)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # SECURITY: Use parameterized query to prevent SQL injection vulnerabilities
        cursor.execute(
            """
            INSERT OR REPLACE INTO answer_cache (user_intent, answer)
            VALUES (?, ?)
        """,
            (user_intent, answer),
        )
        conn.commit()
