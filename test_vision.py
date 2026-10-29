import os
import sys
from unittest import TestCase, mock

# Set headless environment variables
os.environ["SDL_AUDIODRIVER"] = "dummy"
if "GEMINI_API_KEY" not in os.environ:
    os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

# Mock database module if missing
if "database" not in sys.modules:
    mock_db = mock.MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer.return_value = None
    sys.modules["database"] = mock_db

from main_vision import VisionAssistantApp


class TestVisionErrorHandling(TestCase):

    @mock.patch("main_vision.keyboard.GlobalHotKeys")
    @mock.patch("main_vision.mouse.Listener")
    @mock.patch("main_vision.AvatarWindow.animate_ring_and_levitate")
    def test_autonomous_agent_step_sanitizes_generic_exceptions(
        self, mock_animate, mock_mouse_listener, mock_hotkeys
    ):
        app = VisionAssistantApp()
        self.addCleanup(app.destroy)

        # Mock ai_engine.process_screen_and_intent to raise a sensitive exception containing sensitive paths or keys
        sensitive_error = "Error connecting to server at https://internal.secret.net/api?key=SECRET_TOKEN_123 path /etc/passwd"
        app.ai_engine.process_screen_and_intent = mock.Mock(
            side_effect=RuntimeError(sensitive_error)
        )
        app.ai_engine.stream.wait_until_stable = mock.Mock(
            return_value=mock.MagicMock()
        )
        app.get_active_monitor = mock.Mock(
            return_value={"left": 0, "top": 0, "width": 800, "height": 600}
        )

        app.workflow_active = True
        app.current_workflow_goal = "Test Goal"

        # Execute autonomous_agent_step directly
        app.autonomous_agent_step(use_vision=True)

        # Retrieve chat history messages
        # Find the CTkLabel texts in children of chat_history
        chat_messages = []
        for child in app.chat_history.winfo_children():
            for subchild in child.winfo_children():
                if hasattr(subchild, "cget"):
                    chat_messages.append(subchild.cget("text"))

        # Verify that the sensitive exception text was NOT leaked into the chat UI
        for msg in chat_messages:
            self.assertNotIn("SECRET_TOKEN_123", msg)
            self.assertNotIn("/etc/passwd", msg)
            self.assertNotIn("internal.secret.net", msg)

        # Verify that generic error message is present
        generic_error_found = any(
            "Une erreur est survenue lors de l'analyse" in msg for msg in chat_messages
        )
        self.assertTrue(generic_error_found, "Generic error message should be added to chat.")
