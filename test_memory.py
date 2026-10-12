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

    def test_index_exists(self):
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index, "Composite index idx_routines_hash_intent should exist.")

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        user_intent = "click start"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Click start button"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        retrieved = self.memory.get_routine("nonexistent_hash", "nonexistent_intent")
        self.assertIsNone(retrieved)

    def test_get_latest_routine(self):
        screen_hash = "abc123hash"
        user_intent = "click start"
        first_action = {"action": "click", "x": 100, "y": 200}
        second_action = {"action": "click", "x": 150, "y": 250}

        self.memory.save_routine(screen_hash, user_intent, first_action)
        self.memory.save_routine(screen_hash, user_intent, second_action)

        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, second_action)


if __name__ == "__main__":
    unittest.main()
