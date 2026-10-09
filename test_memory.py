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

    def test_composite_index_exists(self):
        """Verify that the composite index idx_routines_hash_intent was created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines from memory."""
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking login"}

        # Initially non-existent
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Save routine
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Retrieve routine
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved, action_data)

    def test_get_routine_returns_latest(self):
        """Verify that get_routine returns the latest action when multiple exist."""
        screen_hash = "hash_multi"
        user_intent = "multi_intent"

        action_1 = {"action": "wait", "text": "Waiting"}
        action_2 = {"action": "click", "x": 50, "y": 50, "text": "Clicking"}

        self.memory.save_routine(screen_hash, user_intent, action_1)
        self.memory.save_routine(screen_hash, user_intent, action_2)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_2)


if __name__ == "__main__":
    unittest.main()
