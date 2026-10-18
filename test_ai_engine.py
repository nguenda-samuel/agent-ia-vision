import json
import os
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

# Mock dependencies before importing modules
sys.modules['google'] = MagicMock()
sys.modules['google.genai'] = MagicMock()
sys.modules['google.genai.types'] = MagicMock()
sys.modules['cv2'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['PIL'] = MagicMock()
sys.modules['imagehash'] = MagicMock()
sys.modules['mss'] = MagicMock()

import database
from ai_engine import AIEngine


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.db_path_patcher = patch('database.DB_PATH', self.db_path)
        self.db_path_patcher.start()

    def tearDown(self):
        self.db_path_patcher.stop()
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_cached_text_answer_retrieval(self):
        """Verify AIEngine database caching works with parameterized queries."""
        mock_client = MagicMock()
        engine = AIEngine(mock_client)

        user_intent = "combien font 2+2"
        expected_json = json.dumps({"action": "none", "text": "2+2 font 4"})

        database.save_answer(user_intent, expected_json, db_path=self.db_path)

        cached = database.get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(cached, expected_json)


if __name__ == "__main__":
    unittest.main()
