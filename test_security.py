import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Set dummy env vars for headless test environment
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock database module if missing
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer.return_value = None
    sys.modules["database"] = mock_db

from main_vision import VisionAssistantApp


class TestSecurityErrorSanitization(unittest.TestCase):

    @patch("main_vision.AvatarWindow")
    @patch("main_vision.SubtitleWindow")
    @patch("main_vision.QuickInputWindow")
    @patch("main_vision.AnimatedPointerWindow")
    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    def test_error_handling_sanitizes_exception_messages(
        self,
        mock_mouse_listener,
        mock_hotkeys,
        mock_pointer,
        mock_quick_input,
        mock_subtitle,
        mock_avatar,
    ):
        app = VisionAssistantApp()
        chat_messages = []

        def fake_append_to_chat(text, is_user=False):
            chat_messages.append((text, is_user))

        app.append_to_chat = fake_append_to_chat
        app.workflow_active = True

        # Mock ai_engine.process_screen_and_intent to raise an exception containing secret info
        secret_error_msg = (
            "API_KEY_EXPOSED_secret12345: Internal error at /var/secret/path"
        )
        app.ai_engine.process_screen_and_intent = MagicMock(
            side_effect=Exception(secret_error_msg)
        )
        app.ai_engine.stream.wait_until_stable = MagicMock(
            return_value=MagicMock()
        )
        app.get_active_monitor = MagicMock(
            return_value={"left": 0, "top": 0, "width": 100, "height": 100}
        )

        app.autonomous_agent_step(use_vision=True)

        # Ensure raw secret_error_msg is NOT present in any appended chat message
        for msg, is_user in chat_messages:
            self.assertNotIn(
                "secret12345",
                msg,
                "Raw exception message with sensitive info was leaked to chat UI!",
            )
            self.assertNotIn(
                "/var/secret/path",
                msg,
                "Internal file path details were leaked to chat UI!",
            )

        # Check that generic error message was logged
        has_generic_error = any(
            "Une erreur s'est produite lors du traitement" in msg
            for msg, _ in chat_messages
        )
        self.assertTrue(
            has_generic_error,
            "Generic error message was not appended to chat UI.",
        )

        app.destroy()


if __name__ == "__main__":
    unittest.main()
