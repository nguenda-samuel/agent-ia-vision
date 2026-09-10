import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure SDL uses dummy audio for headless test execution
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock database module if not present
sys.modules["database"] = MagicMock()

from main_vision import VisionAssistantApp


class TestUXEnhancements(unittest.TestCase):

    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    @patch("main_vision.genai.Client")
    def test_avatar_canvas_hand_cursor(
        self, mock_genai, mock_mouse, mock_keyboard
    ):
        """Test that AvatarWindow canvas is configured with hand2 cursor for visual affordance."""
        app = VisionAssistantApp()
        cursor = app.avatar.canvas.cget("cursor")
        self.assertEqual(cursor, "hand2")
        app.destroy()

    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    @patch("main_vision.genai.Client")
    def test_escape_key_binding(self, mock_genai, mock_mouse, mock_keyboard):
        """Test that <Escape> key is bound on VisionAssistantApp to toggle main window."""
        app = VisionAssistantApp()
        bindings = app.bind()
        # Tkinter normalizes '<Escape>' to '<Key-Escape>'
        self.assertTrue(
            "<Escape>" in bindings or "<Key-Escape>" in bindings,
            f"Expected Escape key binding in {bindings}",
        )
        app.destroy()

    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    @patch("main_vision.genai.Client")
    @patch("threading.Thread")
    def test_button_disabled_state_during_processing(
        self, mock_thread, mock_genai, mock_mouse, mock_keyboard
    ):
        """Test that btn_send and btn_vision are disabled when request processing starts, and re-enabled on stop."""
        app = VisionAssistantApp()
        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")

        # Trigger process_request
        app.process_request(use_vision=True)

        self.assertEqual(app.btn_send.cget("state"), "disabled")
        self.assertEqual(app.btn_vision.cget("state"), "disabled")

        # Stop workflow and ensure buttons return to normal
        app.stop_agent_workflow()

        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        app.destroy()


if __name__ == "__main__":
    unittest.main()
