import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clique sur Se connecter"}

        # Initially routine should be None
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Save routine and verify lookup
        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)

    def test_get_routine_returns_latest(self):
        screen_hash = "hash_v1"
        user_intent = "open menu"
        action_1 = {"action": "click", "x": 10, "y": 10}
        action_2 = {"action": "click", "x": 50, "y": 50}

        self.memory.save_routine(screen_hash, user_intent, action_1)
        self.memory.save_routine(screen_hash, user_intent, action_2)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_2)

    def test_index_is_used_for_query(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            query_plan = cursor.execute(
                "EXPLAIN QUERY PLAN SELECT action_data FROM routines WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1",
                ("dummy_hash", "dummy_intent")
            ).fetchall()

        # Query plan should mention SEARCH using INDEX idx_routines_hash_intent
        plan_detail = " ".join(row[-1] for row in query_plan)
        self.assertIn("USING INDEX idx_routines_hash_intent", plan_detail)


if __name__ == "__main__":
    unittest.main()
