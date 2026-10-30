import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory, MAX_SCREEN_HASH_LENGTH, MAX_USER_INTENT_LENGTH


class TestActionMemorySecurity(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine_success(self):
        screen_hash = "abc123hash"
        user_intent = "click on button"
        action_data = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_invalid_input_types_raise_error_on_save(self):
        with self.assertRaises(TypeError):
            self.memory.save_routine(12345, "intent", {"action": "none"})

        with self.assertRaises(TypeError):
            self.memory.save_routine("hash", None, {"action": "none"})

        with self.assertRaises(TypeError):
            self.memory.save_routine("hash", "intent", "invalid_action_data")

    def test_exceeding_max_lengths_raise_error_on_save(self):
        oversized_hash = "a" * (MAX_SCREEN_HASH_LENGTH + 1)
        oversized_intent = "b" * (MAX_USER_INTENT_LENGTH + 1)

        with self.assertRaises(ValueError):
            self.memory.save_routine(oversized_hash, "intent", {"action": "none"})

        with self.assertRaises(ValueError):
            self.memory.save_routine("hash", oversized_intent, {"action": "none"})

    def test_get_routine_invalid_inputs_returns_none(self):
        self.assertIsNone(self.memory.get_routine(12345, "intent"))
        self.assertIsNone(self.memory.get_routine("hash", None))
        oversized_hash = "a" * (MAX_SCREEN_HASH_LENGTH + 1)
        self.assertIsNone(self.memory.get_routine(oversized_hash, "intent"))

    def test_corrupted_json_in_db_returns_none_gracefully(self):
        screen_hash = "corrupt_hash"
        user_intent = "corrupt_intent"

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO routines (screen_hash, user_intent, action_data)
                VALUES (?, ?, ?)
            """,
                (screen_hash, user_intent, "{invalid json payload: 123"),
            )
            conn.commit()

        # get_routine should handle json.JSONDecodeError safely and return None
        result = self.memory.get_routine(screen_hash, user_intent)
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
