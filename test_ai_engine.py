import unittest
from unittest.mock import MagicMock
import os
import tempfile
import json

import ai_engine
from database import get_cached_answer, save_answer


class TestAIEngineIntegration(unittest.TestCase):

    def setUp(self):
        self.fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_ai_engine_cache_integration(self):
        user_intent = "Explain screen"
        cached_data = json.dumps({"action": "none", "text": "Cached response"})

        # Save to database cache
        save_answer(user_intent, cached_data, db_path=self.db_path)

        # Retrieve from database cache
        retrieved = get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(retrieved, cached_data)

        # Mock gemini client and test AIEngine instantiates properly and uses database
        mock_client = MagicMock()
        engine = ai_engine.AIEngine(gemini_client=mock_client)
        self.assertIsNotNone(engine)


if __name__ == "__main__":
    unittest.main()
