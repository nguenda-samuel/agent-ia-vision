import os
import unittest
import database


class TestDatabaseSecurityAndCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "Open settings"
        response = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

        # Verify initial cache is empty
        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertIsNone(cached)

        # Save answer and verify retrieval
        database.save_answer(intent, response, db_path=self.test_db)
        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response)

    def test_update_cached_answer(self):
        intent = "Open settings"
        response1 = '{"action": "click", "x": 100, "y": 200, "text": "Old"}'
        response2 = '{"action": "click", "x": 100, "y": 200, "text": "Updated"}'

        database.save_answer(intent, response1, db_path=self.test_db)
        database.save_answer(intent, response2, db_path=self.test_db)

        cached = database.get_cached_answer(intent, db_path=self.test_db)
        self.assertEqual(cached, response2)

    def test_sql_injection_prevention(self):
        sqli_payload = "' OR '1'='1"
        response = '{"action": "none", "text": "Malicious payload test"}'

        database.save_answer(sqli_payload, response, db_path=self.test_db)

        # Should retrieve the exact payload safely without returning all records or failing
        cached = database.get_cached_answer(sqli_payload, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Normal query should still return None
        normal_query = "Normal query"
        self.assertIsNone(database.get_cached_answer(normal_query, db_path=self.test_db))

    def test_drop_table_injection_prevention(self):
        drop_payload = "'; DROP TABLE answer_cache; --"
        response = '{"action": "none", "text": "Drop table test"}'

        database.save_answer(drop_payload, response, db_path=self.test_db)
        cached = database.get_cached_answer(drop_payload, db_path=self.test_db)
        self.assertEqual(cached, response)

        # Ensure table still exists and functions properly
        database.save_answer("safe_intent", "safe_response", db_path=self.test_db)
        self.assertEqual(
            database.get_cached_answer("safe_intent", db_path=self.test_db),
            "safe_response",
        )


if __name__ == "__main__":
    unittest.main()
