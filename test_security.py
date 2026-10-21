import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from PIL import Image

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

# Mock database module if missing
if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()


class TestSecurityErrorHandling(unittest.TestCase):

    @patch("main_vision.AvatarWindow")
    @patch("main_vision.SubtitleWindow")
    @patch("main_vision.QuickInputWindow")
    @patch("main_vision.AnimatedPointerWindow")
    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    def test_error_message_does_not_leak_exception_details(
        self,
        mock_mouse_listener,
        mock_hotkeys,
        mock_pointer,
        mock_quick_input,
        mock_subtitle,
        mock_avatar,
    ):
        from main_vision import VisionAssistantApp

        app = VisionAssistantApp()
        app.withdraw()

        mock_image = Image.new("RGB", (100, 100))
        app.ai_engine.stream.wait_until_stable = MagicMock(return_value=mock_image)

        chat_messages = []

        def capture_chat(text, is_user=False):
            chat_messages.append((text, is_user))

        app.append_to_chat = capture_chat
        app.workflow_active = True

        sensitive_error_text = (
            "InternalServerError: API_KEY=sk_secret_12345 at https://internal.api/v1/endpoint"
        )

        with patch.object(
            app.ai_engine,
            "process_screen_and_intent",
            side_effect=Exception(sensitive_error_text),
        ), patch.object(
            app,
            "get_active_monitor",
            return_value={"left": 0, "top": 0, "width": 800, "height": 600},
        ):
            app.autonomous_agent_step(use_vision=True)

        for msg, is_user in chat_messages:
            self.assertNotIn(
                "sk_secret_12345",
                msg,
                "Sensitive API key detail leaked into chat message!",
            )
            self.assertNotIn(
                "InternalServerError",
                msg,
                "Internal exception details leaked into chat message!",
            )

        safe_messages = [
            msg
            for msg, is_user in chat_messages
            if "Une erreur est survenue" in msg
        ]
        self.assertTrue(
            len(safe_messages) > 0,
            "Expected generic safe error message was not sent to chat.",
        )

        app.destroy()


if __name__ == "__main__":
    unittest.main()
