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

    def test_get_cached_answer_empty(self):
        result = get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "Open Settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_save_answer_conflict_update(self):
        intent = "Open Settings"
        response1 = '{"action": "click", "x": 100, "y": 200}'
        response2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        response = '{"action": "none", "text": "safe response"}'

        save_answer(sqli_intent, response, db_path=self.db_path)

        # Ensure normal lookup for a different intent returns None and not the injected intent response
        result = get_cached_answer("normal_intent", db_path=self.db_path)
        self.assertIsNone(result)

        # Ensure looking up the exact string works correctly
        result_exact = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(result_exact, response)


if __name__ == "__main__":
    unittest.main()
