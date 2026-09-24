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
        screen_hash = "phash_12345678"
        user_intent = "Clique sur le bouton Valider"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Validation"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved["action"], "click")
        self.assertEqual(retrieved["x"], 100)
        self.assertEqual(retrieved["y"], 200)

    def test_get_routine_not_found(self):
        result = self.memory.get_routine("non_existent_hash", "non_existent_intent")
        self.assertIsNone(result)

    def test_composite_index_exists_and_used(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent'"
            )
            row = cursor.fetchone()
            self.assertIsNotNone(row, "Composite index idx_routines_hash_intent should exist")

            # Check EXPLAIN QUERY PLAN
            cursor.execute(
                "EXPLAIN QUERY PLAN SELECT action_data FROM routines WHERE screen_hash = ? AND user_intent = ? ORDER BY id DESC LIMIT 1",
                ("hash1", "intent1")
            )
            plan = cursor.fetchall()
            plan_str = " ".join([str(p) for p in plan])
            self.assertIn("idx_routines_hash_intent", plan_str, "Query plan should utilize idx_routines_hash_intent index")


if __name__ == "__main__":
    unittest.main()
