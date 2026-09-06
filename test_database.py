import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Navigateur ouvert"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        sql_injection_intent = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(sql_injection_intent, response, db_path=self.db_path)
        cached = get_cached_answer(sql_injection_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Ensure normal query doesn't retrieve it when looking for something else
        cached_other = get_cached_answer("test", db_path=self.db_path)
        self.assertIsNone(cached_other)


if __name__ == "__main__":
    unittest.main()
