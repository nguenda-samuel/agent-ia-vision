import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify that the compound index idx_routines_screen_hash_user_intent exists."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_hash_user_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_screen_hash_user_intent")

    def test_save_and_get_routine(self):
        """Verify routine saving and retrieval."""
        screen_hash = "abc123hash"
        user_intent = "click on start button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking start"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        """Verify None returned for non-existent routines."""
        retrieved = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
