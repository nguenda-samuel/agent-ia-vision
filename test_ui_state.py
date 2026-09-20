import unittest
from unittest.mock import MagicMock, patch
import os
import sys

os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock database module which is imported in ai_engine but absent in codebase
sys.modules["database"] = MagicMock()

import customtkinter as ctk

class TestUIState(unittest.TestCase):

    @patch("main_vision.AvatarWindow")
    @patch("main_vision.SubtitleWindow")
    @patch("main_vision.QuickInputWindow")
    @patch("main_vision.AnimatedPointerWindow")
    @patch("main_vision.genai.Client")
    @patch("main_vision.AIEngine")
    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    def test_input_disabled_during_processing(
        self, mock_mouse, mock_hotkeys, mock_ai_engine, mock_genai_client,
        mock_pointer, mock_quick, mock_sub, mock_avatar
    ):
        from main_vision import VisionAssistantApp

        app = VisionAssistantApp()

        # Verify initial states are normal
        self.assertEqual(app.entry.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")

        # Disable inputs
        app._set_inputs_disabled(True)
        self.assertEqual(app.entry.cget("state"), "disabled")
        self.assertEqual(app.btn_vision.cget("state"), "disabled")
        self.assertEqual(app.btn_send.cget("state"), "disabled")

        # Enable inputs
        app._set_inputs_disabled(False)
        self.assertEqual(app.entry.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")

        # Stop workflow restores state
        app._set_inputs_disabled(True)
        app.stop_agent_workflow()
        self.assertEqual(app.entry.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")

        app.destroy()


if __name__ == "__main__":
    unittest.main()
