import json
import unittest
from unittest.mock import MagicMock
from ai_engine import AIEngine
from database import get_cached_answer, save_answer


class TestAIEngineDatabaseIntegration(unittest.TestCase):

    def test_cached_answer_text_query(self):
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        user_intent = "Aide-moi avec une question textuelle"
        cached_json = json.dumps({"action": "none", "text": "Réponse en cache"})

        # Save to database cache
        save_answer(user_intent, cached_json)

        # Process screen and intent with raw_screenshot=None
        res = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

        self.assertEqual(res, {"action": "none", "text": "Réponse en cache"})
        # Gemini client should not have been called because result was cached
        mock_client.models.generate_content.assert_not_called()


if __name__ == "__main__":
    unittest.main()
