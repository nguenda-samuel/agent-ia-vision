import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify that the composite index on (screen_hash, user_intent) is created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_screen_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines from ActionMemory."""
        screen_hash = "hash_abc123"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 450, "y": 300}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        """Verify that searching for a non-existent routine returns None."""
        retrieved = self.memory.get_routine("unknown_hash", "unknown_intent")
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
