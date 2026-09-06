import json
import os
import unittest
from unittest.mock import MagicMock

from ai_engine import AIEngine
from database import DB_PATH, get_cached_answer, save_answer


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def tearDown(self):
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)

    def test_process_screen_and_intent_uses_database_cache(self):
        mock_client = MagicMock()
        ai = AIEngine(gemini_client=mock_client)

        user_intent = "Ouvrir Firefox"
        cached_payload = json.dumps({"action": "none", "text": "Firefox est ouvert."})
        save_answer(user_intent, cached_payload)

        # Calling without raw_screenshot should return cached response from DB
        res = ai.process_screen_and_intent(None, user_intent)
        self.assertEqual(res, json.loads(cached_payload))
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
