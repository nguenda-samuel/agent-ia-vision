import sys
from unittest.mock import MagicMock, patch

# Mock missing database module before main_vision imports ai_engine
sys.modules["database"] = MagicMock()

import tkinter as tk
import unittest

import customtkinter as ctk

import main_vision
from main_vision import CTkToolTip, VisionAssistantApp


class TestUIAndAccessibility(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        try:
            cls.root = tk.Tk()
            cls.root.withdraw()
        except Exception:
            cls.root = None

    @classmethod
    def tearDownClass(cls):
        if cls.root:
            cls.root.destroy()

    def test_tooltip_creation(self):
        if not self.root:
            self.skipTest("No GUI display available")
        btn = ctk.CTkButton(self.root, text="🚀")
        tooltip = CTkToolTip(btn, "Test Tooltip")
        self.assertEqual(tooltip.text, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

    @patch("main_vision.AIEngine")
    @patch("main_vision.keyboard.GlobalHotKeys")
    @patch("main_vision.mouse.Listener")
    @patch("main_vision.pygame.mixer.init")
    @patch("main_vision.genai.Client")
    def test_toggle_main_window_focus(
        self, mock_genai, mock_pygame, mock_mouse, mock_hotkeys, mock_ai_engine
    ):
        if not self.root:
            self.skipTest("No GUI display available")
        app = VisionAssistantApp()
        self.assertFalse(app.main_window_visible)

        # Toggle to show
        app.toggle_main_window()
        self.assertTrue(app.main_window_visible)

        # Focused widget should be the entry or a child widget
        focused = app.focus_get()
        self.assertIsNotNone(focused)

        # Toggle back to hide
        app.toggle_main_window()
        self.assertFalse(app.main_window_visible)

        app.destroy()


if __name__ == "__main__":
    unittest.main()
