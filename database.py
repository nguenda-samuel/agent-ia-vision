import sqlite3

DB_PATH = "cache.db"


def init_db(db_path: str = DB_PATH):
    """Initialise la table de cache pour les réponses."""
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
    """Récupère une réponse en cache de façon sécurisée (requête paramétrée anti-SQLi)."""
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
        # En utilisant des requêtes paramétrées '?', nous prévenons les injections SQL.
        cursor.execute(
            "SELECT cached_answer FROM answer_cache WHERE user_intent = ?",
            (user_intent,),
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour une réponse en cache de façon sécurisée (requête paramétrée anti-SQLi)."""
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
        # Requête paramétrée pour éviter les vulnérabilités d'injection SQL
        cursor.execute(
            """
            INSERT INTO answer_cache (user_intent, cached_answer)
            VALUES (?, ?)
            ON CONFLICT(user_intent) DO UPDATE SET cached_answer = excluded.cached_answer
        """,
            (user_intent, answer),
        )
        conn.commit()
