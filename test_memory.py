import os
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            self.db_path = f.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine_success(self):
        screen_hash = "abc123hash"
        user_intent = "Clique sur le bouton Valider"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Validation"}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved, action_data)

    def test_get_routine_not_found(self):
        result = self.memory.get_routine("nonexistent_hash", "some intent")
        self.assertIsNone(result)

    def test_invalid_screen_hash_type(self):
        with self.assertRaises(ValueError):
            self.memory.save_routine(12345, "intent", {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine(12345, "intent")

    def test_empty_screen_hash(self):
        with self.assertRaises(ValueError):
            self.memory.save_routine("   ", "intent", {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine("", "intent")

    def test_screen_hash_too_long(self):
        oversized_hash = "h" * (ActionMemory.MAX_SCREEN_HASH_LEN + 1)
        with self.assertRaises(ValueError):
            self.memory.save_routine(oversized_hash, "intent", {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine(oversized_hash, "intent")

    def test_invalid_user_intent_type(self):
        with self.assertRaises(ValueError):
            self.memory.save_routine("hash123", None, {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine("hash123", None)

    def test_empty_user_intent(self):
        with self.assertRaises(ValueError):
            self.memory.save_routine("hash123", "", {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine("hash123", "   ")

    def test_user_intent_too_long(self):
        oversized_intent = "i" * (ActionMemory.MAX_USER_INTENT_LEN + 1)
        with self.assertRaises(ValueError):
            self.memory.save_routine("hash123", oversized_intent, {"action": "click"})

        with self.assertRaises(ValueError):
            self.memory.get_routine("hash123", oversized_intent)

    def test_invalid_action_data_type(self):
        with self.assertRaises(TypeError):
            self.memory.save_routine("hash123", "intent", "not_a_dict")

    def test_oversized_action_data_payload(self):
        bloated_data = {"key": "x" * (ActionMemory.MAX_ACTION_DATA_BYTES + 10)}
        with self.assertRaises(ValueError):
            self.memory.save_routine("hash123", "intent", bloated_data)


if __name__ == "__main__":
    unittest.main()
