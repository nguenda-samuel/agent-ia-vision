import os
import sqlite3
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_memory_db.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify composite index idx_routines_hash_intent is created in the database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(
                result, "Composite index idx_routines_hash_intent should exist"
            )

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines works accurately."""
        screen_hash = "hash_12345"
        user_intent = "click play button"
        action_data = {"action": "click", "x": 100, "y": 200}

        # Initially routine should not exist
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertIsNone(retrieved)

        # Save routine
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Retrieve routine
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
