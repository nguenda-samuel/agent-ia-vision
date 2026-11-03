import sqlite3


def init_db(db_path: str = "cache.db") -> None:
    """Initialise la table de cache SQLite pour les réponses IA."""
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS qa_cache (
                user_intent TEXT PRIMARY KEY,
                answer TEXT
            )
            """)
        conn.commit()


def get_cached_answer(user_intent: str, db_path: str = "cache.db") -> str | None:
    """Récupère une réponse en cache avec une requête paramétrée sécurisée."""
    if not isinstance(user_intent, str) or not user_intent:
        return None
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éliminer le risque d'injection SQL
        cursor.execute(
            "SELECT answer FROM qa_cache WHERE user_intent = ?", (user_intent,)
        )
        result = cursor.fetchone()
        return result[0] if result else None


def save_answer(user_intent: str, answer: str, db_path: str = "cache.db") -> None:
    """Enregistre ou remplace une réponse en cache via une requête paramétrée."""
    if not isinstance(user_intent, str) or not isinstance(answer, str):
        return
    init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        # Requête paramétrée avec '?' pour éliminer le risque d'injection SQL
        cursor.execute(
            "INSERT OR REPLACE INTO qa_cache (user_intent, answer) VALUES (?, ?)",
            (user_intent, answer),
        )
        conn.commit()
