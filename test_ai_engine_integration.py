import os
import tempfile
import unittest
from unittest.mock import MagicMock

os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

from ai_engine import AIEngine
import database


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_database_cache_integration(self):
        mock_client = MagicMock()
        engine = AIEngine(mock_client)

        intent = "quelle est la meteo"
        cached_json = '{"action": "none", "text": "Il fait beau"}'

        # Save cached answer into database using parameterized query
        database.save_answer(intent, cached_json, db_path=self.db_path)

        # Temporarily redirect DB_PATH in database module
        original_db = database.DB_PATH
        database.DB_PATH = self.db_path
        try:
            # When calling process_screen_and_intent without screenshot, it should return cached response from DB
            result = engine.process_screen_and_intent(None, intent)
            self.assertEqual(result["action"], "none")
            self.assertEqual(result["text"], "Il fait beau")
            # Gemini client should not have been called
            mock_client.models.generate_content.assert_not_called()
        finally:
            database.DB_PATH = original_db


if __name__ == "__main__":
    unittest.main()
