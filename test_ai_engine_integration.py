import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock

from ai_engine import AIEngine
import database


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        database.init_db(self.db_path)

        # Patch default DB_PATH for testing
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_cached_text_response(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Explain what is on the screen"
        cached_data = {"action": "none", "text": "This is a cached explanation."}
        database.save_answer(user_intent, json.dumps(cached_data), db_path=self.db_path)

        # Calling process_screen_and_intent without screenshot should hit cache
        result = engine.process_screen_and_intent(None, user_intent)

        self.assertEqual(result, cached_data)
        # Verify gemini client was NOT called when serving from cache
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
