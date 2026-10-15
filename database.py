import sqlite3

DB_PATH = "cache.db"


def _init_table(conn: sqlite3.Connection):
    """Initialise la table cache sur une connexion active."""
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cache (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_intent TEXT UNIQUE,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )


def init_db(db_path: str | None = None):
    """Initialise la base de données SQLite pour le cache."""
    if db_path is None:
        db_path = DB_PATH
    with sqlite3.connect(db_path) as conn:
        _init_table(conn)
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str | None = None) -> str | None:
    """Récupère la réponse mise en cache pour une intention utilisateur (requête paramétrée)."""
    if db_path is None:
        db_path = DB_PATH
    with sqlite3.connect(db_path) as conn:
        _init_table(conn)
        cursor = conn.cursor()
        # Requête paramétrée avec ? pour prévenir les injections SQL
        cursor.execute(
            "SELECT response FROM cache WHERE user_intent = ?",
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(user_intent: str, response: str, db_path: str | None = None):
    """Sauvegarde ou met à jour la réponse dans le cache (requête paramétrée)."""
    if db_path is None:
        db_path = DB_PATH
    with sqlite3.connect(db_path) as conn:
        _init_table(conn)
        cursor = conn.cursor()
        # Requête paramétrée avec ? pour prévenir les injections SQL
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (user_intent, response)
            VALUES (?, ?)
            """,
            (user_intent, response),
        )
        conn.commit()
