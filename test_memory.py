import os
import sqlite3
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_agent_memory.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index)
            self.assertEqual(index[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        user_intent = "click play button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking play"}

        # Initially no routine
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Save routine
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Get routine
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
