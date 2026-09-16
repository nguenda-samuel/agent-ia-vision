import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db_creates_index(self):
        """Verify that _init_db creates routines table and composite index."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent'"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index, "Composite index idx_routines_hash_intent should exist.")

    def test_save_and_get_routine(self):
        """Test saving and retrieving routines from ActionMemory."""
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking login"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_routine_returns_latest(self):
        """Test that get_routine returns the most recent entry when multiple match."""
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_1 = {"action": "click", "x": 100, "y": 200}
        action_2 = {"action": "click", "x": 150, "y": 250}

        self.memory.save_routine(screen_hash, user_intent, action_1)
        self.memory.save_routine(screen_hash, user_intent, action_2)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_2)

    def test_get_routine_non_existent(self):
        """Test retrieving non-existent routine returns None."""
        retrieved = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
