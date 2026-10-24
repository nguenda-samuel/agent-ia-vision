import os
import sqlite3
import tempfile
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_index_created(self):
        """Verify that the composite index idx_routines_hash_intent is created in the database."""
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result, "Index idx_routines_hash_intent should exist in the database.")
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving a routine from ActionMemory."""
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 150, "y": 250, "text": "Clicking login"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        """Verify that searching for a non-existent routine returns None."""
        retrieved = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(retrieved)

    def test_get_latest_routine(self):
        """Verify that get_routine returns the most recently saved routine."""
        screen_hash = "hash_repeat"
        user_intent = "intent_repeat"
        action_old = {"action": "wait", "text": "Old action"}
        action_new = {"action": "click", "x": 500, "y": 600, "text": "New action"}

        self.memory.save_routine(screen_hash, user_intent, action_old)
        self.memory.save_routine(screen_hash, user_intent, action_new)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_new)


if __name__ == "__main__":
    unittest.main()
