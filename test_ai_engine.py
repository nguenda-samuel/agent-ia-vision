import os
import tempfile
import unittest
from unittest.mock import MagicMock, patch


class TestAIEngine(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    @patch("ai_engine.get_cached_answer")
    @patch("ai_engine.PrivacyFilter")
    @patch("ai_engine.ScreenStream")
    @patch("ai_engine.ActionMemory")
    def test_cache_hit_returns_cached_response(
        self, mock_memory, mock_stream, mock_privacy, mock_get_cached
    ):
        from ai_engine import AIEngine

        mock_get_cached.return_value = '{"action": "none", "text": "Bonjour !"}'
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "dire bonjour"

        # Call process_screen_and_intent without screenshot -> should hit database cache
        result = engine.process_screen_and_intent(None, user_intent)

        self.assertEqual(result, {"action": "none", "text": "Bonjour !"})
        mock_get_cached.assert_called_once_with(user_intent)
        # Verify gemini client was NOT called due to cache hit
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
