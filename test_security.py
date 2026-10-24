import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Set dummy environment variables for headless test execution
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock 'database' module before importing ai_engine or main_vision if database module is missing
if "database" not in sys.modules:
    db_mock = MagicMock()
    db_mock.get_cached_answer.return_value = None
    db_mock.save_answer.return_value = None
    sys.modules["database"] = db_mock

from ai_engine import AIEngine
from PIL import Image


class TestSecurityFixes(unittest.TestCase):

    def test_user_intent_length_limit_and_sanitization(self):
        """Verify that user_intent is truncated to 500 characters and handles non-string/empty input securely."""
        mock_client = MagicMock()
        ai_engine = AIEngine(gemini_client=mock_client)

        # Test overly long intent input (DoS / prompt exhaustion vector)
        long_intent = "A" * 1200
        img = Image.new("RGB", (100, 100), color="white")

        with patch.object(ai_engine.client.models, "generate_content") as mock_generate:
            mock_resp = MagicMock()
            mock_resp.text = '{"action": "none", "text": "OK"}'
            mock_generate.return_value = mock_resp

            ai_engine.process_screen_and_intent(img, long_intent)

            self.assertTrue(mock_generate.called)
            args, kwargs = mock_generate.call_args
            contents = kwargs.get("contents") or args[0]
            prompt = contents[1]
            # Verify the prompt does not contain the original 1200 'A's, but is capped at 500
            self.assertNotIn("A" * 501, prompt)
            self.assertIn("A" * 500, prompt)

    def test_user_intent_empty_or_invalid_fallback(self):
        """Verify that empty or non-string user_intent falls back to default safe string."""
        mock_client = MagicMock()
        ai_engine = AIEngine(gemini_client=mock_client)
        img = Image.new("RGB", (100, 100), color="white")

        with patch.object(ai_engine.client.models, "generate_content") as mock_generate:
            mock_resp = MagicMock()
            mock_resp.text = '{"action": "none", "text": "OK"}'
            mock_generate.return_value = mock_resp

            ai_engine.process_screen_and_intent(img, None)

            args, kwargs = mock_generate.call_args
            contents = kwargs.get("contents") or args[0]
            prompt = contents[1]
            self.assertIn("Assistance et guidage sur l'écran", prompt)

    def test_error_handling_no_raw_exception_leak_in_ui(self):
        """Verify that raw exception details (sensitive tracebacks / internal details) are not added to chat UI."""
        from main_vision import VisionAssistantApp

        with patch("main_vision.keyboard.GlobalHotKeys"), \
             patch("main_vision.mouse.Listener"):
            app = VisionAssistantApp()
            try:
                sensitive_exception_msg = "SECRET_PATH_/etc/shadow_OR_API_KEY_EXPOSED_12345"

                with patch.object(app.ai_engine, "process_screen_and_intent") as mock_process, \
                     patch.object(app, "get_active_monitor", return_value={"left": 0, "top": 0, "width": 800, "height": 600}), \
                     patch("mss.MSS"):
                    mock_process.side_effect = Exception(sensitive_exception_msg)
                    app.workflow_active = True
                    app.autonomous_agent_step(use_vision=True)

                # Collect all chat bubble texts
                chat_texts = []
                for child in app.chat_history.winfo_children():
                    for subchild in child.winfo_children():
                        if hasattr(subchild, "cget"):
                            chat_texts.append(subchild.cget("text"))

                all_chat_content = " ".join(chat_texts)

                # Ensure sensitive exception details were NOT appended to UI chat history
                self.assertNotIn(sensitive_exception_msg, all_chat_content)
                self.assertIn("Une erreur est survenue lors de l'analyse.", all_chat_content)
            finally:
                app.destroy()


if __name__ == "__main__":
    unittest.main()
