import json
import sqlite3

# Maximum allowed lengths for stored inputs to prevent DoS/memory exhaustion
MAX_SCREEN_HASH_LENGTH = 1024
MAX_USER_INTENT_LENGTH = 4096


class ActionMemory:

    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialise la table SQLite pour enregistrer les routines."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS routines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    screen_hash TEXT,
                    user_intent TEXT,
                    action_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            conn.commit()

    def save_routine(
        self, screen_hash: str, user_intent: str, action_data: dict
    ):
        """Enregistre une action réussie associée à l'empreinte d'écran."""
        if not isinstance(screen_hash, str) or not isinstance(user_intent, str):
            raise TypeError("screen_hash and user_intent must be strings")

        if len(screen_hash) > MAX_SCREEN_HASH_LENGTH:
            raise ValueError("screen_hash exceeds maximum allowed length")

        if len(user_intent) > MAX_USER_INTENT_LENGTH:
            raise ValueError("user_intent exceeds maximum allowed length")

        if not isinstance(action_data, dict):
            raise TypeError("action_data must be a dictionary")

        json_str = json.dumps(action_data)

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO routines (screen_hash, user_intent, action_data)
                VALUES (?, ?, ?)
            """,
                (screen_hash, user_intent, json_str),
            )
            conn.commit()

    def get_routine(self, screen_hash: str, user_intent: str) -> dict | None:
        """Recherche si une action existe déjà pour cet écran et cette demande."""
        if not isinstance(screen_hash, str) or not isinstance(user_intent, str):
            return None

        if len(screen_hash) > MAX_SCREEN_HASH_LENGTH or len(user_intent) > MAX_USER_INTENT_LENGTH:
            return None

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT action_data FROM routines
                WHERE screen_hash = ? AND user_intent = ?
                ORDER BY id DESC LIMIT 1
            """,
                (screen_hash, user_intent),
            )
            result = cursor.fetchone()
            if result and result[0]:
                try:
                    return json.loads(result[0])
                except (json.JSONDecodeError, TypeError):
                    return None
            return None
