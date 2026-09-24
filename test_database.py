import os
import unittest
from database import get_cached_answer, save_answer

TEST_DB_PATH = "test_cache.db"


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Clicking settings"}'

        self.assertIsNone(get_cached_answer(intent, db_path=TEST_DB_PATH))

        save_answer(intent, response, db_path=TEST_DB_PATH)

        cached = get_cached_answer(intent, db_path=TEST_DB_PATH)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "Open settings"
        response1 = '{"action": "none"}'
        response2 = '{"action": "click", "x": 10, "y": 20}'

        save_answer(intent, response1, db_path=TEST_DB_PATH)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB_PATH), response1)

        save_answer(intent, response2, db_path=TEST_DB_PATH)
        self.assertEqual(get_cached_answer(intent, db_path=TEST_DB_PATH), response2)

    def test_sql_injection_resistance(self):
        sqli_payload = "'; DROP TABLE answer_cache; --"
        response = '{"action": "none", "text": "Safe"}'

        save_answer(sqli_payload, response, db_path=TEST_DB_PATH)
        cached = get_cached_answer(sqli_payload, db_path=TEST_DB_PATH)

        self.assertEqual(cached, response)

        # Ensure the table wasn't dropped
        normal_intent = "Normal request"
        self.assertIsNone(get_cached_answer(normal_intent, db_path=TEST_DB_PATH))


if __name__ == "__main__":
    unittest.main()
