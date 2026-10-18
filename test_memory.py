import os
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemorySecurity(unittest.TestCase):

    def setUp(self):
        self.temp_db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.temp_db_fd)
        self.memory = ActionMemory(db_path=self.temp_db_path)

    def tearDown(self):
        if os.path.exists(self.temp_db_path):
            os.remove(self.temp_db_path)

    def test_save_and_get_routine_normal(self):
        screen_hash = "hash_12345"
        user_intent = "open browser"
        action_data = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        result = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(result, action_data)

    def test_sql_injection_payloads(self):
        """Verify that SQL injection payloads in parameters do not compromise database queries."""
        sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE routines; --",
            "1' UNION SELECT action_data FROM routines WHERE '1'='1",
            "\" OR \"1\"=\"1",
            "'; DELETE FROM routines; --",
        ]

        for payload in sql_injection_payloads:
            # Saving with SQL injection payload in user_intent and screen_hash
            action_data = {"action": "click", "payload": payload}
            self.memory.save_routine(payload, payload, action_data)

            # Retrieving with exact payload string
            retrieved = self.memory.get_routine(payload, payload)
            self.assertEqual(retrieved, action_data)

            # Retrieving with non-matching intent should return None, not leak or bypass
            non_matching = self.memory.get_routine(payload, "different_intent")
            self.assertIsNone(non_matching)


if __name__ == "__main__":
    unittest.main()
