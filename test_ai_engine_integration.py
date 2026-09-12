import json
import os
import unittest
from unittest.mock import MagicMock, patch
from ai_engine import AIEngine
from database import save_answer, DB_PATH

TEST_DB_PATH = "test_ai_engine_cache.db"


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def tearDown(self):
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_process_screen_and_intent_uses_database_cache(self):
        user_intent = "What is the capital of France?"
        cached_data = {"action": "none", "text": "Paris"}
        save_answer(user_intent, json.dumps(cached_data), db_path=TEST_DB_PATH)

        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        # Patch get_cached_answer in ai_engine to use our TEST_DB_PATH
        with patch("ai_engine.get_cached_answer", lambda intent: save_answer(user_intent, json.dumps(cached_data), db_path=TEST_DB_PATH) or get_cached_answer(intent, db_path=TEST_DB_PATH)):
            from database import get_cached_answer
            result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

            self.assertEqual(result, cached_data)
            mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
