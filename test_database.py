import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "quelle est la météo ?"
        response = '{"action": "none", "text": "Il fait beau."}'

        # Initially cached answer should be None
        self.assertIsNone(get_cached_answer(intent, db_path=self.db_path))

        # Save answer and verify retrieval
        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_sql_injection_prevention(self):
        # Malicious intent trying SQL injection
        sqli_intent = "' OR '1'='1"
        sqli_response = '{"action": "none", "text": "Injected"}'

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Querying a different intent should NOT return the injected response
        result = get_cached_answer("normal intent", db_path=self.db_path)
        self.assertIsNone(result)

        # Querying exact sqli intent should safely return the saved value
        result = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(result, sqli_response)

    def test_upsert_cached_answer(self):
        intent = "ouvir le navigateur"
        response1 = '{"action": "click", "x": 100, "y": 200}'
        response2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, response1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response1)

        # Updating response for same intent
        save_answer(intent, response2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response2)


if __name__ == "__main__":
    unittest.main()
