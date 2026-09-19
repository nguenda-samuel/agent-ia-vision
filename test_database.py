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
        user_intent = "clique sur le bouton bleu"
        cached_response = '{"action": "click", "x": 100, "y": 200}'

        save_answer(user_intent, cached_response, db_path=self.db_path)
        retrieved = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(retrieved, cached_response)

    def test_update_cached_answer_on_conflict(self):
        user_intent = "clique sur le bouton bleu"
        initial_response = '{"action": "click", "x": 100, "y": 200}'
        updated_response = '{"action": "click", "x": 150, "y": 250}'

        save_answer(user_intent, initial_response, db_path=self.db_path)
        save_answer(user_intent, updated_response, db_path=self.db_path)
        retrieved = get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(retrieved, updated_response)

    def test_sql_injection_safety(self):
        sqli_intent = "' OR '1'='1"
        sqli_response = '{"action": "none", "text": "injected"}'

        save_answer(sqli_intent, sqli_response, db_path=self.db_path)

        # Ensure searching for another string does not return the injected row
        self.assertIsNone(
            get_cached_answer("normal intent", db_path=self.db_path)
        )
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=self.db_path),
            sqli_response,
        )


if __name__ == "__main__":
    unittest.main()
