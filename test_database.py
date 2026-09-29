import os
import unittest
from unittest.mock import MagicMock, patch
from PIL import Image
import database
from ai_engine import AIEngine


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_cache.db"
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_save_and_get_cached_answer(self):
        intent = "What is the weather today?"
        response = '{"action": "none", "text": "It is sunny."}'

        database.save_answer(intent, response, db_path=self.test_db)
        cached = database.get_cached_answer(intent, db_path=self.test_db)

        self.assertEqual(cached, response)

    def test_sql_injection_protection(self):
        sqli_intent = "test' OR '1'='1"
        response = '{"action": "none", "text": "Safe response"}'

        database.save_answer(sqli_intent, response, db_path=self.test_db)

        # Non-matching intent should return None, proving SQL injection didn't bypass lookup
        other_intent = "test"
        self.assertIsNone(database.get_cached_answer(other_intent, db_path=self.test_db))

        # Exact match returns correct response
        self.assertEqual(database.get_cached_answer(sqli_intent, db_path=self.test_db), response)

    def test_ai_engine_input_sanitization(self):
        os.environ["GEMINI_API_KEY"] = "dummy_key"
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        long_intent = "A" * 1500

        with patch("ai_engine.get_cached_answer") as mock_get_cached:
            mock_get_cached.side_effect = lambda intent: '{"action": "none", "text": "Cached truncated"}' if len(intent) == 1000 else None
            result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=long_intent)
            self.assertEqual(result, {"action": "none", "text": "Cached truncated"})
            mock_get_cached.assert_called_once_with("A" * 1000)


if __name__ == "__main__":
    unittest.main()
