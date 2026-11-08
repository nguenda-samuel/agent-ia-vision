import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock database if missing before importing main_vision / ai_engine
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer.return_value = None
    sys.modules["database"] = mock_db

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"

import customtkinter as ctk
from main_vision import CTkTooltip, VisionAssistantApp


class TestUXTooltip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def setUp(self):
        self.root = ctk.CTk()
        self.root.geometry("200x200+0+0")
        self.root.update()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_creation_and_lifecycle(self):
        btn = ctk.CTkButton(self.root, text="Test")
        btn.pack()
        self.root.update()

        tooltip = CTkTooltip(btn, "Explanatory tooltip text", delay_ms=50)
        self.assertIsNone(tooltip.tip_window)

        # Trigger show
        tooltip.show()
        self.root.update()
        self.assertIsNotNone(tooltip.tip_window)
        self.assertTrue(tooltip.tip_window.winfo_exists())

        # Trigger hide
        tooltip.hide()
        self.root.update()
        self.assertIsNone(tooltip.tip_window)

    def test_tooltip_event_schedule_and_cancel(self):
        btn = ctk.CTkButton(self.root, text="Icon")
        btn.pack()
        self.root.update()

        tooltip = CTkTooltip(btn, "Hint", delay_ms=100)
        tooltip._on_enter()
        self.assertIsNotNone(tooltip._schedule_id)

        # Leaving cancels the timer before it shows
        tooltip._on_leave()
        self.assertIsNone(tooltip._schedule_id)
        self.assertIsNone(tooltip.tip_window)

    def test_app_buttons_have_tooltips_bound(self):
        app = VisionAssistantApp()
        app.update()

        # Check main window buttons exist
        self.assertTrue(hasattr(app, "btn_vision"))
        self.assertTrue(hasattr(app, "btn_send"))
        self.assertIn("<Enter>", app.btn_vision._canvas.bind())
        self.assertIn("<Enter>", app.btn_send._canvas.bind())

        # Check QuickInput window button
        self.assertTrue(hasattr(app.quick_input, "btn_send"))
        self.assertIn("<Enter>", app.quick_input.btn_send._canvas.bind())

        app.on_closing()


if __name__ == "__main__":
    unittest.main()
