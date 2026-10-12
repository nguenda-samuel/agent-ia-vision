import json
import os
import tempfile
import unittest

from ai_engine import AIEngine
from database import get_cached_answer, save_answer


class DummyGeminiClient:
    pass


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_uses_database_cache(self):
        engine = AIEngine(gemini_client=DummyGeminiClient())
        intent = "Test Intent Integration"
        expected = {"action": "none", "text": "Cached response test"}

        # Save to database cache
        save_answer(intent, json.dumps(expected), db_path=self.db_path)

        # Retrieve using database function
        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(json.loads(cached), expected)

        # Call process_screen_and_intent without screenshot
        # Override DB_PATH in database module during test
        import database
        original_db = database.DB_PATH
        database.DB_PATH = self.db_path
        try:
            result = engine.process_screen_and_intent(
                raw_screenshot=None, user_intent=intent
            )
            self.assertEqual(result, expected)
        finally:
            database.DB_PATH = original_db


if __name__ == "__main__":
    unittest.main()
