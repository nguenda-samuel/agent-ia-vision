import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_composite_index_exists(self):
        """Verify that the composite index idx_routines_screen_hash_user_intent_id exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_hash_user_intent_id'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(
                result,
                "Expected idx_routines_screen_hash_user_intent_id index to be present",
            )
            self.assertEqual(result[0], "idx_routines_screen_hash_user_intent_id")

    def test_query_plan_uses_index(self):
        """Verify that get_routine query plan uses the composite index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "EXPLAIN QUERY PLAN SELECT action_data FROM routines WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1",
                ("dummy_hash", "dummy_intent"),
            )
            plan = cursor.fetchall()
            plan_str = " ".join(str(step) for step in plan)
            self.assertIn(
                "USING INDEX idx_routines_screen_hash_user_intent_id", plan_str
            )
            self.assertNotIn("SCAN routines", plan_str)

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines."""
        screen_hash = "screen_hash_abc"
        user_intent = "click start button"
        action_data = {
            "action": "click",
            "x": 100,
            "y": 200,
            "text": "Clicking start",
        }

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_routine_returns_latest_id(self):
        """Verify that get_routine returns the most recently inserted routine."""
        screen_hash = "screen_hash_xyz"
        user_intent = "open settings"
        action_v1 = {
            "action": "click",
            "x": 10,
            "y": 20,
            "text": "Old",
        }
        action_v2 = {
            "action": "click",
            "x": 50,
            "y": 60,
            "text": "New",
        }

        self.memory.save_routine(screen_hash, user_intent, action_v1)
        self.memory.save_routine(screen_hash, user_intent, action_v2)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_v2)

    def test_get_nonexistent_routine(self):
        """Verify that get_routine returns None when no match exists."""
        retrieved = self.memory.get_routine("unknown_hash", "unknown_intent")
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
