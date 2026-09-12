import sqlite3

DEFAULT_DB_PATH = "agent_cache.db"


def _init_db(db_path: str | None = None) -> None:
    """Initialise la table de cache SQLite de façon sécurisée."""
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )
        conn.commit()


def get_cached_answer(
    user_intent: str, db_path: str | None = None
) -> str | None:
    """Recherche une réponse en cache pour une intention utilisateur.

    SECURITY NOTE: Utilise des requêtes paramétrées (?) pour prévenir toute
    injection SQL.
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée sécurisée (?)
        cursor.execute(
            "SELECT answer FROM cache WHERE user_intent = ?", (user_intent,)
        )
        row = cursor.fetchone()
        return row[0] if row else None


def save_answer(
    user_intent: str, answer: str, db_path: str | None = None
) -> None:
    """Sauvegarde une réponse dans le cache pour l'intention donnée.

    SECURITY NOTE: Utilise des requêtes paramétrées (?) pour prévenir toute
    injection SQL.
    """
    if db_path is None:
        db_path = DEFAULT_DB_PATH
    _init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée sécurisée (?) pour insertion/remplacement
        cursor.execute(
            "INSERT OR REPLACE INTO cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
