import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "What is on screen?"
        cached_response = '{"action": "none", "text": "Testing screen response"}'

        self.assertIsNone(get_cached_answer(user_intent, db_path=self.db_path))

        save_answer(user_intent, cached_response, db_path=self.db_path)

        retrieved = get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(retrieved, cached_response)

    def test_update_cached_answer(self):
        user_intent = "Open browser"
        first_response = '{"action": "click", "x": 10, "y": 20}'
        second_response = '{"action": "click", "x": 100, "y": 200}'

        save_answer(user_intent, first_response, db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(user_intent, db_path=self.db_path), first_response
        )

        save_answer(user_intent, second_response, db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(user_intent, db_path=self.db_path),
            second_response,
        )

    def test_sql_injection_prevention(self):
        sqli_payload = "test' OR '1'='1"
        response_text = '{"action": "none", "text": "safe"}'

        save_answer(sqli_payload, response_text, db_path=self.db_path)

        retrieved = get_cached_answer(sqli_payload, db_path=self.db_path)
        self.assertEqual(retrieved, response_text)

        normal_query = "unrelated query"
        self.assertIsNone(get_cached_answer(normal_query, db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
