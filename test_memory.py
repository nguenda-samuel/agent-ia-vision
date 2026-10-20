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

    def test_init_db_creates_index(self):
        """Verify that _init_db creates the composite index on routines."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_screen_hash_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routine action data."""
        hash_val = "abc123hash"
        intent_val = "Click submit button"
        action_val = {"action": "click", "x": 100, "y": 200, "text": "Click submit"}

        # Non-existent routine should return None
        self.assertIsNone(self.memory.get_routine(hash_val, intent_val))

        # Save routine
        self.memory.save_routine(hash_val, intent_val, action_val)

        # Retrieve saved routine
        retrieved = self.memory.get_routine(hash_val, intent_val)
        self.assertEqual(retrieved, action_val)


if __name__ == "__main__":
    unittest.main()
