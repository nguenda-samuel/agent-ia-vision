import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Set required environment variables before importing GUI components
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "test_key_dummy"

# Mock database module if missing
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer.return_value = None
    sys.modules["database"] = mock_db

from main_vision import VisionAssistantApp


class TestSecurityErrorHandling(unittest.TestCase):

    @patch("main_vision.AvatarWindow.animate_ring_and_levitate")
    @patch("main_vision.AIEngine")
    @patch("main_vision.genai.Client")
    def test_autonomous_agent_step_error_sanitization(
        self, mock_genai_client, mock_ai_engine, mock_animate
    ):
        """Test that internal exceptions in autonomous_agent_step do not leak detailed error strings to the chat UI."""
        app = VisionAssistantApp()
        app.append_to_chat = MagicMock()

        # Simulate workflow active and force an unexpected internal exception with sensitive info
        app.workflow_active = True
        sensitive_error_msg = "Database connection string postgresql://user:secret_password@db.internal:5432 failed"

        with patch.object(
            app.ai_engine,
            "process_screen_and_intent",
            side_effect=RuntimeError(sensitive_error_msg),
        ):
            with patch("main_vision.mss.MSS"):
                with patch("main_vision.Image.frombytes"):
                    app.autonomous_agent_step(use_vision=True)

        # Ensure append_to_chat was called with a safe, generic message
        app.append_to_chat.assert_called()
        calls = [call[0][0] for call in app.append_to_chat.call_args_list]

        # Check that none of the chat messages contain sensitive details
        for message in calls:
            self.assertNotIn(
                sensitive_error_msg,
                message,
                "Sensitive internal exception details were leaked in chat UI!",
            )
            self.assertNotIn(
                "secret_password",
                message,
                "Password details were leaked in chat UI!",
            )

        # Check that the safe error message was appended
        self.assertTrue(
            any(
                "❌ Une erreur est survenue lors de l'analyse." in msg
                for msg in calls
            ),
            "Expected safe error message not found in append_to_chat calls.",
        )

        app.destroy()


if __name__ == "__main__":
    unittest.main()
