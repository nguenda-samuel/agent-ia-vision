import sqlite3

_initialized_dbs = set()


def init_db(db_path: str = "cache.db"):
    """Initialise la table SQLite pour le cache de réponses AI."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                response_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()
    _initialized_dbs.add(db_path)


def save_answer(
    user_intent: str, response_text: str, db_path: str = "cache.db"
):
    """Sauvegarde une réponse en cache avec des requêtes paramétrées anti-SQLi."""
    if db_path not in _initialized_dbs:
        init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Utilisation de requête paramétrée (?) pour prévenir toute injection SQL
        cursor.execute(
            """
            INSERT OR REPLACE INTO cache (user_intent, response_text)
            VALUES (?, ?)
            """,
            (user_intent, response_text),
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str = "cache.db"
) -> str | None:
    """Récupère la réponse en cache pour l'intention utilisateur via une requête sécurisée."""
    if db_path not in _initialized_dbs:
        init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Utilisation de requête paramétrée (?) pour prévenir toute injection SQL
        cursor.execute(
            """
            SELECT response_text FROM cache WHERE user_intent = ?
            """,
            (user_intent,),
        )
        row = cursor.fetchone()
        return row[0] if row else None
