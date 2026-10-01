import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock

# Mock third-party dependencies if not installed in headless test environment
for mod in ["google", "google.genai", "google.genai.types", "cv2", "imagehash", "mss", "numpy", "PIL"]:
    if mod not in sys.modules:
        try:
            __import__(mod)
        except ImportError:
            sys.modules[mod] = MagicMock()

import database
from ai_engine import AIEngine


class TestAIEngineCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        os.close(self.db_fd)
        self.orig_db_path = database.DB_PATH
        database.DB_PATH = self.db_path

    def tearDown(self):
        database.DB_PATH = self.orig_db_path
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(mock_client)

        user_intent = "Affiche l'aide"
        cached_result = {"action": "none", "text": "Voici l'aide."}
        database.save_answer(
            user_intent,
            json.dumps(cached_result),
        )

        result = engine.process_screen_and_intent(
            raw_screenshot=None, user_intent=user_intent
        )

        self.assertEqual(result, cached_result)
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
