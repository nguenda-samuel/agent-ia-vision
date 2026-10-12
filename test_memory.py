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
        """Verify that the compound index idx_routines_hash_intent exists in SQLite schema."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Test saving and retrieving routines from ActionMemory."""
        screen_hash = "abc123hash"
        user_intent = "click on button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicked"}

        # Initially non-existent routine
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Save routine
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Retrieve routine
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
