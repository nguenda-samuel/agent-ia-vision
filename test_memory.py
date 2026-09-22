import os
import tempfile
import unittest
import sqlite3
from memory import ActionMemory


class TestActionMemorySecurityAndFunctionality(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_routine_success(self):
        hash_val = "abc123hash"
        intent = "click login button"
        action = {"action": "click", "x": 100, "y": 200, "text": "clicking login"}

        self.memory.save_routine(hash_val, intent, action)
        retrieved = self.memory.get_routine(hash_val, intent)

        self.assertEqual(retrieved, action)

    def test_get_routine_not_found(self):
        retrieved = self.memory.get_routine("nonexistent", "unknown")
        self.assertIsNone(retrieved)

    def test_save_routine_type_validation(self):
        with self.assertRaises(TypeError):
            self.memory.save_routine(123, "intent", {"a": 1})

        with self.assertRaises(TypeError):
            self.memory.save_routine("hash", None, {"a": 1})

        with self.assertRaises(TypeError):
            self.memory.save_routine("hash", "intent", "invalid_action_dict")

    def test_get_routine_type_validation(self):
        with self.assertRaises(TypeError):
            self.memory.get_routine(123, "intent")

        with self.assertRaises(TypeError):
            self.memory.get_routine("hash", ["intent"])

    def test_sql_injection_resilience(self):
        sql_payload_hash = "hash' OR '1'='1"
        sql_payload_intent = "intent'; DROP TABLE routines; --"
        action = {"action": "none", "text": "test injection"}

        self.memory.save_routine(sql_payload_hash, sql_payload_intent, action)
        retrieved = self.memory.get_routine(sql_payload_hash, sql_payload_intent)

        self.assertEqual(retrieved, action)

        # Verify table routines still exists and was not dropped
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT count(*) FROM routines")
            count = cursor.fetchone()[0]
            self.assertEqual(count, 1)

    def test_corrupted_json_handling(self):
        hash_val = "corrupt_hash"
        intent = "corrupt_intent"

        # Directly insert corrupted JSON in DB
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO routines (screen_hash, user_intent, action_data) VALUES (?, ?, ?)",
                (hash_val, intent, "{invalid_json: true,"),
            )
            conn.commit()

        # get_routine should handle json parse failure gracefully and return None
        retrieved = self.memory.get_routine(hash_val, intent)
        self.assertIsNone(retrieved)


if __name__ == "__main__":
    unittest.main()
