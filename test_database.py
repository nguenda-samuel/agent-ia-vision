import os
import tempfile
import unittest
from unittest.mock import MagicMock

from database import _initialized_dbs, get_cached_answer, init_db, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        _initialized_dbs.discard(self.db_path)
        init_db(self.db_path)

    def tearDown(self):
        _initialized_dbs.discard(self.db_path)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture du navigateur"}'
        save_answer(intent, answer, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_get_cached_answer_not_found(self):
        cached = get_cached_answer("inconnu", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_save_answer_overwrite(self):
        intent = "cliquer ici"
        answer1 = "reponse1"
        answer2 = "reponse2"

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_prevention(self):
        sql_injection_payloads = [
            "' OR '1'='1",
            "'; DROP TABLE cache; --",
            "test' UNION SELECT 'hacked' --",
            "admin'--",
            "1' OR 1=1 --",
        ]

        for payload in sql_injection_payloads:
            save_answer(payload, "safe_answer", db_path=self.db_path)
            retrieved = get_cached_answer(payload, db_path=self.db_path)
            self.assertEqual(
                retrieved,
                "safe_answer",
                f"Failed for SQL injection payload: {payload}",
            )

            normal_query = get_cached_answer("normal", db_path=self.db_path)
            self.assertIsNone(normal_query)

    def test_ai_engine_integration(self):
        from ai_engine import AIEngine

        intent = "test_ai_engine_intent"
        cached_json = '{"action": "none", "text": "Reponse en cache"}'

        save_answer(intent, cached_json, db_path="cache.db")
        try:
            mock_client = MagicMock()
            ai_engine = AIEngine(gemini_client=mock_client)

            res = ai_engine.process_screen_and_intent(None, intent)
            self.assertEqual(res, {"action": "none", "text": "Reponse en cache"})
        finally:
            if os.path.exists("cache.db"):
                os.remove("cache.db")


if __name__ == "__main__":
    unittest.main()
