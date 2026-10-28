import os
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine(self):
        screen_hash = "abc123hash"
        user_intent = "click start button"
        action_data = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        retrieved = self.memory.get_routine("nonexistent_hash", "some_intent")
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
