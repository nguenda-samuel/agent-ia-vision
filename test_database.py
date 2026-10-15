import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'

        database.save_answer(user_intent, response, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        # Attempt SQL injection payload in user_intent
        sqli_payload = "test' OR '1'='1"
        response = "Safe response"

        database.save_answer(sqli_payload, response, db_path=self.db_path)

        # Retrieving exact intent should return response
        cached = database.get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Querying for non-existent intent should return None, not trigger SQLi bypass
        other_cached = database.get_cached_answer(
            "non_existent", db_path=self.db_path
        )
        self.assertIsNone(other_cached)


if __name__ == "__main__":
    unittest.main()
