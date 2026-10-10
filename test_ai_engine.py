import unittest
from unittest.mock import MagicMock
from PIL import Image
from ai_engine import AIEngine


class TestAIEngine(unittest.TestCase):

    def test_process_screen_and_intent_handles_exception_securely(self):
        mock_client = MagicMock()
        mock_client.models.generate_content.side_effect = Exception("Sensitive DB credentials leak")
        engine = AIEngine(gemini_client=mock_client)
        dummy_img = Image.new("RGB", (10, 10), color="white")

        result = engine.process_screen_and_intent(dummy_img, "test")
        self.assertEqual(result["action"], "none")
        self.assertEqual(result["text"], "Désolé, je n'ai pas pu analyser l'écran.")
        self.assertNotIn("Sensitive DB credentials leak", str(result))


if __name__ == "__main__":
    unittest.main()
