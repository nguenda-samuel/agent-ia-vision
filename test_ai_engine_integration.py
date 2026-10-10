import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch
import database
from ai_engine import AIEngine


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_uses_cached_answer_without_screenshot(self):
        intent = "What is 2+2?"
        cached_result = '{"action": "none", "text": "2+2 is 4"}'
        database.save_answer(intent, cached_result, db_path=self.db_path)

        mock_gemini = MagicMock()
        engine = AIEngine(gemini_client=mock_gemini)

        def mock_get_cached(user_intent):
            return database.get_cached_answer(user_intent, db_path=self.db_path)

        with patch("ai_engine.get_cached_answer", side_effect=mock_get_cached):
            res = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)
            self.assertEqual(res, {"action": "none", "text": "2+2 is 4"})
            mock_gemini.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
