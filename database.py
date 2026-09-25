import sqlite3

DB_PATH = "agent_memory.db"


def _get_connection():
    """Initialise et retourne une connexion SQLite avec la table de cache."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cached_answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_intent TEXT UNIQUE,
            response TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()
    return conn


def get_cached_answer(user_intent: str) -> str | None:
    """Récupère une réponse en cache à partir de l'intention utilisateur via une requête paramétrée."""
    try:
        with _get_connection() as conn:
            cursor = conn.cursor()
            # Utilisation de requêtes paramétrées pour prévenir les injections SQL
            cursor.execute(
                "SELECT response FROM cached_answers WHERE user_intent = ? ORDER BY id DESC LIMIT 1",
                (user_intent,),
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            return None
    except Exception as e:
        print(f"[Database Error] Erreur de lecture du cache : {e}")
        return None


def save_answer(user_intent: str, response: str) -> None:
    """Sauvegarde une réponse dans la base de données SQLite via une requête paramétrée."""
    try:
        with _get_connection() as conn:
            cursor = conn.cursor()
            # Utilisation de requêtes paramétrées pour prévenir les injections SQL
            cursor.execute(
                """
                INSERT INTO cached_answers (user_intent, response)
                VALUES (?, ?)
                ON CONFLICT(user_intent) DO UPDATE SET response = excluded.response
                """,
                (user_intent, response),
            )
            conn.commit()
    except Exception as e:
        print(f"[Database Error] Erreur de sauvegarde du cache : {e}")
