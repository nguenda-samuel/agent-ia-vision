import os
import unittest
from unittest.mock import MagicMock
import ai_engine

class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def test_ai_engine_imports_database(self):
        # Verify AIEngine imports get_cached_answer and save_answer from database
        self.assertTrue(hasattr(ai_engine, "get_cached_answer"))
        self.assertTrue(hasattr(ai_engine, "save_answer"))

if __name__ == "__main__":
    unittest.main()
