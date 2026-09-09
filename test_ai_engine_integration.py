import json
import os
import tempfile
import unittest
from unittest.mock import MagicMock

import database
from ai_engine import AIEngine


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.original_db_path = database.DB_PATH
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = self.original_db_path
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Describe screen"
        expected_json = {"action": "none", "text": "This is cached response"}

        # Pre-populate database cache using DB_PATH
        database.save_answer(user_intent, json.dumps(expected_json))

        # Call process_screen_and_intent without screenshot (pure text query)
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        # Verify cached result returned directly without calling Gemini API
        self.assertEqual(result, expected_json)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
