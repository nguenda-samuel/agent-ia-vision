import sqlite3


def init_db(db_path: str = "cache.db"):
    """Initialise la table de cache SQLite pour les réponses IA."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS qa_cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT
            )
            """
        )
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = "cache.db") -> str | None:
    """Récupère une réponse en cache de manière sécurisée (requête paramétrée)."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éviter toute injection SQL
        cursor.execute(
            "SELECT answer FROM qa_cache WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = "cache.db") -> None:
    """Enregistre ou met à jour une réponse en cache avec une requête paramétrée."""
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éviter toute injection SQL
        cursor.execute(
            "INSERT OR REPLACE INTO qa_cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
