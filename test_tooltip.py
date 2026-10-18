import os
import sys
import unittest
from unittest.mock import MagicMock

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

# Mock database module if not present
if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()

import customtkinter as ctk
import main_vision


class TestCTkToolTipAndUX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def test_tooltip_creation_and_events(self):
        root = ctk.CTk()
        btn = ctk.CTkButton(root, text="🚀")
        tooltip = main_vision.CTkToolTip(btn, "Test Tooltip")

        self.assertIsNone(tooltip.tooltip_window)
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertEqual(tooltip.text, "Test Tooltip")

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)
        root.destroy()

    def test_app_escape_keybinding(self):
        app = main_vision.VisionAssistantApp()
        # Verify Escape binding exists on app (Tkinter returns <Key-Escape>)
        bindings = app.bind()
        self.assertTrue(
            any("Escape" in binding for binding in bindings),
            f"Escape binding not found in {bindings}",
        )
        app.on_closing()


if __name__ == "__main__":
    unittest.main()
