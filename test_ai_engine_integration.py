import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock

import database
from database import get_cached_answer, save_answer


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        if os.path.exists(self.db_path):
            os.unlink(self.db_path)

    def test_ai_engine_uses_database_cache(self):
        from ai_engine import AIEngine

        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Explain this concept"
        cached_data = '{"action": "none", "text": "This is cached explanation"}'
        save_answer(user_intent, cached_data)

        res = engine.process_screen_and_intent(None, user_intent)
        self.assertEqual(res, json.loads(cached_data))
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
