import os
import unittest
from unittest.mock import MagicMock, patch
from ai_engine import AIEngine
from database import get_cached_answer, save_answer

TEST_DB = "test_ai_cache.db"


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def tearDown(self):
        if os.path.exists(TEST_DB):
            os.remove(TEST_DB)

    def test_ai_engine_uses_cached_answer(self):
        intent = "quelle est l'heure"
        expected_json = '{"action": "none", "text": "Il est 12:00"}'
        save_answer(intent, expected_json, db_path=TEST_DB)

        with patch(
            "ai_engine.get_cached_answer",
            side_effect=lambda i: get_cached_answer(i, db_path=TEST_DB),
        ):
            mock_client = MagicMock()
            ai = AIEngine(mock_client)
            res = ai.process_screen_and_intent(
                raw_screenshot=None, user_intent=intent
            )
            self.assertEqual(res["text"], "Il est 12:00")


if __name__ == "__main__":
    unittest.main()
