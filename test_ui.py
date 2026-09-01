import sys
from unittest.mock import MagicMock

# Mock database module before importing main_vision since database.py is not in main branch
sys.modules["database"] = MagicMock()

import unittest
from unittest.mock import patch
import customtkinter as ctk

import main_vision


class TestUIKeyboardAndFocus(unittest.TestCase):

    @patch("main_vision.AIEngine")
    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    @patch("main_vision.pygame.mixer.init")
    @patch("main_vision.genai.Client")
    def test_toggle_main_window_focus_and_escape(
        self, mock_genai, mock_pygame, mock_mouse, mock_hotkeys, mock_ai_engine
    ):
        app = main_vision.VisionAssistantApp()
        self.assertFalse(app.main_window_visible)

        # Show main window
        app.toggle_main_window()
        self.assertTrue(app.main_window_visible)

        # Check focus is set on input widget or child entry
        focused_widget = app.focus_get()
        self.assertIsNotNone(focused_widget)

        # Verify btn_vision text
        self.assertEqual(app.btn_vision.cget("text"), "📸 Écran")

        # Toggle back off
        app.toggle_main_window()
        self.assertFalse(app.main_window_visible)

        app.destroy()


if __name__ == "__main__":
    unittest.main()
