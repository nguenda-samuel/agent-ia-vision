import json
import os
import unittest
from unittest.mock import MagicMock

os.environ["GEMINI_API_KEY"] = "dummy_key"

from ai_engine import AIEngine
import database


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.test_db = "test_ai_cache.db"
        database.DB_PATH = self.test_db
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        database.DB_PATH = "cache.db"

    def test_ai_engine_uses_database_cache(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Quelle heure est-il ?"
        cached_payload = json.dumps(
            {"action": "none", "text": "Il est 12h00"}
        )

        # Save cached answer in database
        database.save_answer(user_intent, cached_payload, db_path=self.test_db)

        # process_screen_and_intent should return cached answer when raw_screenshot is None
        res = engine.process_screen_and_intent(None, user_intent)
        self.assertEqual(res, {"action": "none", "text": "Il est 12h00"})
        # gemini client should not be called when cached
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
