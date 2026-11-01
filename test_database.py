import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        response = '{"action": "none", "text": "Ouverture du navigateur"}'

        save_answer(intent, response, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, response)

    def test_get_nonexistent_answer(self):
        cached = get_cached_answer("inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_sql_injection_prevention(self):
        malicious_intent = "test' UNION SELECT 'hacked' --"
        save_answer(malicious_intent, '{"action": "none"}', db_path=self.db_path)

        normal_query = "test"
        cached = get_cached_answer(normal_query, db_path=self.db_path)
        self.assertIsNone(cached)

        cached_malicious = get_cached_answer(malicious_intent, db_path=self.db_path)
        self.assertEqual(cached_malicious, '{"action": "none"}')

    def test_update_existing_cache_entry(self):
        intent = "cliquer sur le bouton"
        response_v1 = '{"action": "click", "x": 100, "y": 200}'
        response_v2 = '{"action": "click", "x": 150, "y": 250}'

        save_answer(intent, response_v1, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response_v1)

        save_answer(intent, response_v2, db_path=self.db_path)
        self.assertEqual(get_cached_answer(intent, db_path=self.db_path), response_v2)

    def test_invalid_input_handling(self):
        self.assertIsNone(get_cached_answer("", db_path=self.db_path))
        self.assertIsNone(get_cached_answer(None, db_path=self.db_path))
        # Should fail safely without raising exception
        save_answer(None, "response", db_path=self.db_path)
        save_answer("intent", None, db_path=self.db_path)


if __name__ == "__main__":
    unittest.main()
