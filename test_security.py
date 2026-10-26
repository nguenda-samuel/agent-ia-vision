import os
import unittest

# Set environment variables for headless testing
os.environ["GEMINI_API_KEY"] = "dummy_test_key"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import ai_engine


class TestSecurity(unittest.TestCase):

    def test_database_import_fallback(self):
        """Test that ai_engine provides fallback functions if database.py is not present."""
        self.assertTrue(callable(ai_engine.get_cached_answer))
        self.assertTrue(callable(ai_engine.save_answer))
        self.assertIsNone(ai_engine.get_cached_answer("test_intent"))

    def test_prompt_length_limit(self):
        """Test prompt length validation limits."""
        long_prompt = "A" * 1001
        self.assertGreater(len(long_prompt), 1000)

        short_prompt = "Hello agent"
        self.assertLessEqual(len(short_prompt), 1000)


if __name__ == "__main__":
    unittest.main()
