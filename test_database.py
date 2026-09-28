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
            os.unlink(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(user_intent, response, db_path=self.db_path)
        cached = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("Intent inexistant", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        response = '{"action": "none", "text": "test"}'

        save_answer(sqli_intent, response, db_path=self.db_path)

        # Attempting SQL injection when retrieving
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Ensure that searching for a different intent doesn't match due to SQL injection
        other_cached = get_cached_answer("Another intent", db_path=self.db_path)
        self.assertIsNone(other_cached)


if __name__ == "__main__":
    unittest.main()
