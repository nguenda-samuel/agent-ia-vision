import os
import sqlite3
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_memory_temp.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify that composite index idx_routines_hash_intent exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routine data."""
        hash_val = "hash123"
        intent_val = "click_button"
        action = {"action": "click", "x": 100, "y": 200}

        # Initially None
        self.assertIsNone(self.memory.get_routine(hash_val, intent_val))

        # Save routine
        self.memory.save_routine(hash_val, intent_val, action)

        # Retrieve routine
        retrieved = self.memory.get_routine(hash_val, intent_val)
        self.assertEqual(retrieved, action)


if __name__ == "__main__":
    unittest.main()
