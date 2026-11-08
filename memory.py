import json
import sqlite3


class ActionMemory:

    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialise la table SQLite pour enregistrer les routines."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS routines (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    screen_hash TEXT,
                    user_intent TEXT,
                    action_data TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    MAX_SCREEN_HASH_LEN = 128
    MAX_USER_INTENT_LEN = 1000
    MAX_ACTION_DATA_BYTES = 65536  # 64 KB limit to prevent DoS via bloated routines

    def _validate_inputs(self, screen_hash: str, user_intent: str):
        # Security: Enforce strict input types and limits to avoid memory/storage exhaustion
        if not isinstance(screen_hash, str) or not screen_hash.strip():
            raise ValueError("screen_hash must be a non-empty string")
        if len(screen_hash) > self.MAX_SCREEN_HASH_LEN:
            raise ValueError(
                f"screen_hash exceeds max length of {self.MAX_SCREEN_HASH_LEN}"
            )

        if not isinstance(user_intent, str) or not user_intent.strip():
            raise ValueError("user_intent must be a non-empty string")
        if len(user_intent) > self.MAX_USER_INTENT_LEN:
            raise ValueError(
                f"user_intent exceeds max length of {self.MAX_USER_INTENT_LEN}"
            )

    def save_routine(self, screen_hash: str, user_intent: str, action_data: dict):
        """Enregistre une action réussie associée à l'empreinte d'écran."""
        self._validate_inputs(screen_hash, user_intent)

        if not isinstance(action_data, dict):
            raise TypeError("action_data must be a dictionary")

        serialized_action = json.dumps(action_data)
        if len(serialized_action.encode("utf-8")) > self.MAX_ACTION_DATA_BYTES:
            raise ValueError(
                f"action_data exceeds max payload size of {self.MAX_ACTION_DATA_BYTES} bytes"
            )

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO routines (screen_hash, user_intent, action_data)
                VALUES (?, ?, ?)
            """,
                (screen_hash, user_intent, serialized_action),
            )
            conn.commit()

    def get_routine(self, screen_hash: str, user_intent: str) -> dict | None:
        """Recherche si une action existe déjà pour cet écran et cette demande."""
        self._validate_inputs(screen_hash, user_intent)

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
            if result:
                return json.loads(result[0])
            return None
