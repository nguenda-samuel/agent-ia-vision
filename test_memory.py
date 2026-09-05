import os
import sqlite3
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_agent_memory.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db_creates_table_and_index(self):
        memory = ActionMemory(db_path=self.db_path)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Verify routines table exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='routines';"
            )
            table = cursor.fetchone()
            self.assertIsNotNone(table)

            # Verify index exists
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index)

    def test_save_and_get_routine(self):
        memory = ActionMemory(db_path=self.db_path)
        screen_hash = "abc123hash"
        user_intent = "click_button"
        action_data = {"action": "click", "x": 100, "y": 200}

        # Check non-existent routine
        result = memory.get_routine(screen_hash, user_intent)
        self.assertIsNone(result)

        # Save routine
        memory.save_routine(screen_hash, user_intent, action_data)

        # Retrieve saved routine
        retrieved = memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
