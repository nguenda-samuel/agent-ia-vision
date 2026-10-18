import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_update_existing_cached_answer(self):
        intent = "cliquer sur rechercher"
        resp1 = '{"action": "wait"}'
        resp2 = '{"action": "click", "x": 50, "y": 50}'

        save_answer(intent, resp1, db_path=self.db_path)
        save_answer(intent, resp2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, resp2)

    def test_get_nonexistent_intent(self):
        cached = get_cached_answer("intent_inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        sqli_intent = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(sqli_intent, response, db_path=self.db_path)
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)
        self.assertEqual(cached, response)

        # Confirm non-matching intent does not return the SQL injection record
        other = get_cached_answer("test", db_path=self.db_path)
        self.assertIsNone(other)


if __name__ == "__main__":
    unittest.main()
