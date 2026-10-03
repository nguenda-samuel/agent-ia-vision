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

    def test_get_cached_answer_missing(self):
        result = get_cached_answer("non_existent_intent", db_path=self.db_path)
        self.assertIsNone(result)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Navigateur ouvert"}'
        save_answer(intent, response, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "rechercher"
        response1 = '{"action": "none", "text": "Recherche 1"}'
        response2 = '{"action": "none", "text": "Recherche 2"}'

        save_answer(intent, response1, db_path=self.db_path)
        save_answer(intent, response2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        sqli_intent = "' OR '1'='1"
        sqli_response = "'; DROP TABLE answer_cache; --"

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, sqli_response)

        # Confirm another intent still returns None and table was not dropped
        self.assertIsNone(get_cached_answer("other_intent", db_path=self.db_path))


if __name__ == "__main__":
    unittest.main()
