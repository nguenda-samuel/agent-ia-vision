import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Mock database module if not present
if "database" not in sys.modules:
    mock_db = MagicMock()
    sys.modules["database"] = mock_db

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import VisionAssistantApp


class TestSecurityErrorHandling(unittest.TestCase):

    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.AvatarWindow")
    @patch("main_vision.SubtitleWindow")
    @patch("main_vision.QuickInputWindow")
    @patch("main_vision.AnimatedPointerWindow")
    @patch("main_vision.AIEngine")
    @patch("main_vision.genai.Client")
    def test_autonomous_agent_step_does_not_leak_error_details(
        self,
        mock_genai_client,
        mock_ai_engine,
        mock_pointer,
        mock_quick_input,
        mock_subtitle,
        mock_avatar,
        mock_hotkeys,
    ):
        app = VisionAssistantApp()
        chat_messages = []

        def mock_append_to_chat(text, is_user=False):
            chat_messages.append(text)

        app.append_to_chat = mock_append_to_chat
        app.workflow_active = True

        # Simulate exception during screen/intent processing containing sensitive details
        app.ai_engine.process_screen_and_intent.side_effect = Exception(
            "DATABASE_PASSWORD=secret_db_pass_123 SQL connection string fail"
        )
        app.ai_engine.stream = MagicMock()
        app.ai_engine.stream.wait_until_stable.return_value = MagicMock()

        # Call autonomous_agent_step
        app.autonomous_agent_step(use_vision=True)

        # Verify chat messages do not leak internal/sensitive error details
        for msg in chat_messages:
            self.assertNotIn("secret_db_pass_123", msg)
            self.assertNotIn("DATABASE_PASSWORD", msg)

        app.destroy()


if __name__ == "__main__":
    unittest.main()
