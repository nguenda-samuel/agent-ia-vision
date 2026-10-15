import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock

import database
from ai_engine import AIEngine


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = "cache.db"
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_uses_database_cache_for_text_request(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Bonjour"
        cached_val = json.dumps({"action": "none", "text": "Bonjour ! Comment puis-je vous aider ?"})
        database.save_answer(user_intent, cached_val, db_path=self.db_path)

        # Lorsque raw_screenshot est None, ai_engine doit retourner la réponse en cache sans appeler Gemini
        res = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        self.assertEqual(res["text"], "Bonjour ! Comment puis-je vous aider ?")
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
