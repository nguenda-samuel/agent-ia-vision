import os
import unittest
from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_agent_memory.db"
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine(self):
        screen_hash = "hash_12345"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Clicking login"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        retrieved = self.memory.get_routine("non_existent", "do something")
        self.assertIsNone(retrieved)

    def test_special_characters_in_query(self):
        # Ensure parameterized query handles special characters securely without SQL injection
        screen_hash = "hash' OR '1'='1"
        user_intent = "intent' --"
        action_data = {"action": "click", "x": 50, "y": 50}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)
        # Check that another search does not match due to injection
        self.assertIsNone(self.memory.get_routine("hash", user_intent))


if __name__ == "__main__":
    unittest.main()
