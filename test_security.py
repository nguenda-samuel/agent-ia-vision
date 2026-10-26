import os
import sys
import unittest
from unittest.mock import MagicMock

# Set environment variable defaults for headless tests
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy-api-key"

# Mock database module if missing
mock_db = MagicMock()
mock_db.get_cached_answer.return_value = None
mock_db.save_answer.return_value = None
sys.modules["database"] = mock_db

from ai_engine import AIEngine  # noqa: E402


class TestSecurityEnhancements(unittest.TestCase):

    def test_user_intent_validation_and_truncation(self):
        client = MagicMock()
        engine = AIEngine(gemini_client=client)

        # Test long user_intent string > 500 chars
        long_intent = "A" * 1000

        # Call process_screen_and_intent with None screenshot
        engine.process_screen_and_intent(raw_screenshot=None, user_intent=long_intent)

        # Verify get_cached_answer was called with truncated intent (500 chars)
        mock_db.get_cached_answer.assert_called_with("A" * 500)

    def test_user_intent_null_or_invalid(self):
        client = MagicMock()
        engine = AIEngine(gemini_client=client)

        engine.process_screen_and_intent(raw_screenshot=None, user_intent=None)
        mock_db.get_cached_answer.assert_called_with("")

    def test_sanitized_error_handling_in_app(self):
        # Verify main_vision exception handling does not leak sensitive details
        from main_vision import VisionAssistantApp

        # Instantiate VisionAssistantApp mock
        with unittest.mock.patch.object(
            VisionAssistantApp, "__init__", return_value=None
        ):
            app = VisionAssistantApp()
            app.workflow_active = True
            app.is_processing = True
            app.current_workflow_goal = "test"
            app.ai_engine = MagicMock()
            app.ai_engine.stream.wait_until_stable.side_effect = Exception(
                "SECRET_API_KEY_LEAK_12345 internal stack trace details"
            )
            app.append_to_chat = MagicMock()
            app.after = MagicMock()
            app.stop_agent_workflow = MagicMock()
            app.avatar = MagicMock()
            app.get_active_monitor = MagicMock(
                return_value={"left": 0, "top": 0, "width": 1000, "height": 1000}
            )

            # Run autonomous_agent_step
            app.autonomous_agent_step(use_vision=True)

            # Verify append_to_chat was NOT called with secret key/trace details
            for call_args in app.append_to_chat.call_args_list:
                chat_msg = call_args[0][0]
                self.assertNotIn("SECRET_API_KEY_LEAK_12345", chat_msg)
                self.assertNotIn("internal stack trace", chat_msg)

            # Verify safe message was appended
            app.append_to_chat.assert_called_with(
                "❌ Une erreur est survenue lors du traitement. Veuillez réessayer.",
                is_user=False,
            )


if __name__ == "__main__":
    unittest.main()
