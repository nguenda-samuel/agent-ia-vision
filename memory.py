import json
import sqlite3


class ActionMemory:

    def __init__(self, db_path: str = "agent_memory.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialise la table SQLite et les index pour enregistrer les routines."""
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
            # Performance optimization: compound index on (screen_hash, user_intent)
            # Speeds up get_routine lookups from O(N) full table scan to O(log N) index lookup
            cursor.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_routines_screen_hash_user_intent
                ON routines (screen_hash, user_intent)
            """
            )
            conn.commit()

    def save_routine(
        self, screen_hash: str, user_intent: str, action_data: dict
    ):
        """Enregistre une action réussie associée à l'empreinte d'écran."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO routines (screen_hash, user_intent, action_data)
                VALUES (?, ?, ?)
            """,
                (screen_hash, user_intent, json.dumps(action_data)),
            )
            conn.commit()

    def get_routine(self, screen_hash: str, user_intent: str) -> dict | None:
        """Recherche si une action existe déjà pour cet écran et cette demande."""
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
