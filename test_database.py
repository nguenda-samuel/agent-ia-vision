import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'
        database.save_answer(intent, response, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = database.get_cached_answer("Nonexistent intent", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        intent = "Open settings"
        response1 = '{"action": "wait"}'
        response2 = '{"action": "none"}'

        database.save_answer(intent, response1, db_path=self.db_path)
        database.save_answer(intent, response2, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_sql_injection_resilience(self):
        # Malicious intent trying SQL injection
        sql_injection_intent = "' OR '1'='1"
        payload_response = "Malicious Payload"

        database.save_answer(sql_injection_intent, payload_response, db_path=self.db_path)

        # Ensure searching for normal intent does not match the injected record
        self.assertIsNone(database.get_cached_answer("Normal Intent", db_path=self.db_path))

        # Ensure searching specifically for the literal injected string returns the exact record
        self.assertEqual(
            database.get_cached_answer(sql_injection_intent, db_path=self.db_path),
            payload_response
        )


if __name__ == "__main__":
    unittest.main()
