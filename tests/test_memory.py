import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_table_and_index_created(self):
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute("PRAGMA index_list(routines)")
            indices = [row[1] for row in cursor.fetchall()]
            self.assertIn("idx_routines_screen_intent_id", indices)

    def test_query_plan_uses_composite_index(self):
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                EXPLAIN QUERY PLAN
                SELECT action_data FROM routines
                WHERE screen_hash = ? AND user_intent = ?
                ORDER BY id DESC LIMIT 1
            """,
                ("test_hash", "test_intent"),
            )
            plan = cursor.fetchall()
            plan_str = " ".join(row[-1] for row in plan)
            self.assertIn("USING INDEX idx_routines_screen_intent_id", plan_str)
            self.assertNotIn("SCAN routines", plan_str)

    def test_save_and_get_routine(self):
        # Empty retrieval
        self.assertIsNone(self.memory.get_routine("hash1", "intent1"))

        # Save first routine
        action1 = {"action": "click", "x": 100, "y": 200, "text": "Clicking button"}
        self.memory.save_routine("hash1", "intent1", action1)
        self.assertEqual(self.memory.get_routine("hash1", "intent1"), action1)

        # Save second routine with same key - get_routine should return the latest one (ORDER BY id DESC LIMIT 1)
        action2 = {"action": "wait", "text": "Waiting for page"}
        self.memory.save_routine("hash1", "intent1", action2)
        self.assertEqual(self.memory.get_routine("hash1", "intent1"), action2)

        # Query different screen hash or intent returns None
        self.assertIsNone(self.memory.get_routine("hash2", "intent1"))
        self.assertIsNone(self.memory.get_routine("hash1", "intent2"))


if __name__ == "__main__":
    unittest.main()
