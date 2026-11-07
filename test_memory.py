import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_composite_index_exists(self):
        """Verify that the composite index idx_routines_screen_hash_user_intent was created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_hash_user_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_screen_hash_user_intent")

    def test_query_plan_uses_index(self):
        """Verify SQLite query planner uses the composite index for routine lookup."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                EXPLAIN QUERY PLAN
                SELECT action_data FROM routines
                WHERE screen_hash = ? AND user_intent = ?
                ORDER BY id DESC LIMIT 1
                """,
                ("hash123", "intent123"),
            )
            plan = " ".join(str(row) for row in cursor.fetchall())
            self.assertIn("USING INDEX idx_routines_screen_hash_user_intent", plan)

    def test_save_and_get_routine(self):
        """Verify routine saving and retrieval returns expected payload."""
        screen_hash = "screen_hash_abc"
        user_intent = "cliquer sur le bouton connexion"
        action = {"action": "click", "x": 150, "y": 300, "text": "Connexion"}

        self.memory.save_routine(screen_hash, user_intent, action)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action)

    def test_get_routine_returns_latest(self):
        """Verify routine retrieval returns the latest action when multiple exist."""
        screen_hash = "screen_hash_abc"
        user_intent = "cliquer sur le bouton connexion"
        action_old = {"action": "click", "x": 100, "y": 200, "text": "Old"}
        action_new = {"action": "click", "x": 150, "y": 300, "text": "New"}

        self.memory.save_routine(screen_hash, user_intent, action_old)
        self.memory.save_routine(screen_hash, user_intent, action_new)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_new)

    def test_get_nonexistent_routine(self):
        """Verify routine retrieval returns None when no match exists."""
        self.assertIsNone(self.memory.get_routine("unknown_hash", "unknown_intent"))


if __name__ == "__main__":
    unittest.main()
