import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_file.name
        self.temp_file.close()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify that idx_routines_screen_intent index is properly created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_intent'"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index)
            self.assertEqual(index[0], "idx_routines_screen_intent")

    def test_query_plan_uses_index(self):
        """Verify that SQLite uses the composite index for get_routine queries."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "EXPLAIN QUERY PLAN SELECT action_data FROM routines WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1",
                ("test_hash", "test_intent"),
            )
            plan = cursor.fetchall()
            plan_str = " ".join([str(p) for p in plan])
            self.assertIn("idx_routines_screen_intent", plan_str)

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines behaves correctly."""
        action = {"action": "click", "x": 100, "y": 200, "text": "Click here"}
        self.memory.save_routine("hash123", "open settings", action)

        retrieved = self.memory.get_routine("hash123", "open settings")
        self.assertEqual(retrieved, action)

        # Non-matching intent or hash returns None
        self.assertIsNone(self.memory.get_routine("hash123", "other intent"))
        self.assertIsNone(self.memory.get_routine("other_hash", "open settings"))

    def test_get_routine_returns_latest(self):
        """Verify get_routine returns the most recent routine matching hash and intent."""
        action1 = {"action": "click", "x": 10}
        action2 = {"action": "click", "x": 20}
        self.memory.save_routine("hash123", "click button", action1)
        self.memory.save_routine("hash123", "click button", action2)

        retrieved = self.memory.get_routine("hash123", "click button")
        self.assertEqual(retrieved, action2)


if __name__ == "__main__":
    unittest.main()
