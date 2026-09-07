import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.db_file.name
        self.db_file.close()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Verify that composite index idx_routines_hash_intent exists on routines table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result)
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routine from ActionMemory."""
        screen_hash = "hash_abc123"
        user_intent = "click login"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clique sur Connexion"}

        # Initially no routine
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Save routine
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Retrieve routine
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
