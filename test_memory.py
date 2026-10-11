import os
import sqlite3
import tempfile
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        user_intent = "open settings"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        retrieved = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(retrieved)

    def test_composite_index_created(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_hash_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_screen_hash_intent")

    def test_query_plan_uses_index(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "EXPLAIN QUERY PLAN SELECT action_data FROM routines WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1",
                ("hash1", "intent1"),
            )
            plan = cursor.fetchall()
            plan_detail = " ".join([row[-1] for row in plan])
            self.assertIn("USING INDEX idx_routines_screen_hash_intent", plan_detail)


if __name__ == "__main__":
    unittest.main()
