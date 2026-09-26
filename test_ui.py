import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock database module if not present in environment
if "database" not in sys.modules:
    db_mock = MagicMock()
    db_mock.get_cached_answer.return_value = None
    db_mock.save_answer = MagicMock()
    sys.modules["database"] = db_mock

os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
os.environ["SDL_AUDIODRIVER"] = "dummy"

import customtkinter as ctk
from main_vision import ToolTip, VisionAssistantApp, QuickInputWindow


class TestUIEnhancements(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_creation_and_events(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack()
        self.root.update()

        tooltip = ToolTip(btn, "Test Tooltip Text", delay_ms=10)
        self.assertEqual(tooltip.text, "Test Tooltip Text")
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger tooltip show
        tooltip.show_tooltip()
        self.root.update()
        self.assertIsNotNone(tooltip.tooltip_window)

        # Trigger tooltip hide
        tooltip.hide_tooltip()
        self.root.update()
        self.assertIsNone(tooltip.tooltip_window)

    def test_vision_assistant_app_tooltips(self):
        app = VisionAssistantApp()
        self.assertIsNotNone(app.btn_vision)
        self.assertIsNotNone(app.btn_send)
        app.on_closing()


if __name__ == "__main__":
    unittest.main()
