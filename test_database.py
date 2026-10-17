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
        intent = "quelle est la météo"
        answer = '{"action": "none", "text": "Il fait beau."}'

        save_answer(intent, answer, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_upsert_cached_answer(self):
        intent = "quelle est la météo"
        answer1 = '{"action": "none", "text": "Il fait beau."}'
        answer2 = '{"action": "none", "text": "Il pleut."}'

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer2)

    def test_non_existent_intent(self):
        cached = get_cached_answer("inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_safety(self):
        sqli_intent = "test' OR '1'='1"
        answer = '{"action": "none", "text": "safe"}'

        save_answer(sqli_intent, answer, db_path=self.db_path)
        cached = get_cached_answer(sqli_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)
        self.assertIsNone(get_cached_answer("other_intent", db_path=self.db_path))

    def test_invalid_input_handling(self):
        self.assertIsNone(get_cached_answer("", db_path=self.db_path))
        self.assertIsNone(get_cached_answer(None, db_path=self.db_path))  # type: ignore


if __name__ == "__main__":
    unittest.main()
