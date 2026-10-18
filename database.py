import sqlite3

DB_PATH = "cache.db"


def _init_db(db_path: str = DB_PATH):
    """Initialise la table SQLite pour le cache des réponses si elle n'existe pas."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS answer_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_intent TEXT UNIQUE,
                cached_response TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    """Récupère une réponse mise en cache pour un intent utilisateur donné.

    Utilise des requêtes paramétrées (?) pour se prémunir des injections SQL.
    """
    _init_db(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Sécurité: Utilisation de paramètres (?) pour prévenir l'injection SQL
            cursor.execute(
                "SELECT cached_response FROM answer_cache WHERE user_intent = ?",
                (user_intent,),
            )
            row = cursor.fetchone()
            if row:
                return row[0]
            return None
    except Exception as e:
        print(f"[Database Error] Erreur lors de la lecture du cache: {e}")
        return None


def save_answer(user_intent: str, cached_response: str, db_path: str = DB_PATH):
    """Sauvegarde ou met à jour une réponse dans le cache pour un intent utilisateur.

    Utilise des requêtes paramétrées (?) pour se prémunir des injections SQL.
    """
    _init_db(db_path)
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            # Sécurité: Utilisation de paramètres (?) pour prévenir l'injection SQL
            cursor.execute(
                """
                INSERT INTO answer_cache (user_intent, cached_response)
                VALUES (?, ?)
                ON CONFLICT(user_intent) DO UPDATE SET cached_response=excluded.cached_response
                """,
                (user_intent, cached_response),
            )
            conn.commit()
    except Exception as e:
        print(f"[Database Error] Erreur lors de la sauvegarde dans le cache: {e}")
