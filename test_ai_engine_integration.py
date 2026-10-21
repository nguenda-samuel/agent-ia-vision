import json
import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock external modules if not installed
for mod in ['google', 'google.genai', 'google.genai.types', 'privacy', 'stream', 'memory', 'cv2', 'PIL', 'imagehash']:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import database
from database import save_answer


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.db_path = "test_cache.db"
        database.DB_PATH = self.db_path
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_cache_integration(self):
        from ai_engine import AIEngine

        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        intent = "test intent for caching"
        cached_dict = {"action": "none", "text": "cached response"}
        save_answer(intent, json.dumps(cached_dict), db_path=self.db_path)

        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)

        self.assertEqual(result, cached_dict)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
