import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB = "test_agent_memory.db"


class TestDatabaseSecurity(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_save_and_get_cached_answer(self):
        intent = "Open music player"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening music player"}'

        save_answer(intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(intent, db_path=TEST_DB)

        self.assertEqual(cached, answer)

    def test_sql_injection_safety(self):
        # Malicious intent trying SQL injection attack
        sql_inj_intent = "Open music'; DROP TABLE cached_answers; --"
        answer = '{"action": "none", "text": "Safe response"}'

        save_answer(sql_inj_intent, answer, db_path=TEST_DB)
        cached = get_cached_answer(sql_inj_intent, db_path=TEST_DB)

        self.assertEqual(cached, answer)

        # Confirm table was not dropped and normal functionality works
        normal_intent = "Normal intent"
        save_answer(normal_intent, answer, db_path=TEST_DB)
        self.assertEqual(get_cached_answer(normal_intent, db_path=TEST_DB), answer)

    def test_empty_or_none_inputs(self):
        self.assertIsNone(get_cached_answer("", db_path=TEST_DB))
        save_answer("", "some answer", db_path=TEST_DB)
        self.assertIsNone(get_cached_answer("", db_path=TEST_DB))

    def test_nonexistent_intent(self):
        self.assertIsNone(get_cached_answer("Nonexistent intent", db_path=TEST_DB))


if __name__ == "__main__":
    unittest.main()
