import os
import sys
import unittest
from unittest.mock import MagicMock

# Set required environment variables before imports
os.environ["GEMINI_API_KEY"] = "dummy_key_for_testing"
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Mock database module if missing
if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()

import customtkinter as ctk
import main_vision
from main_vision import ToolTip, VisionAssistantApp


class TestUIUXEnhancements(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Prevent mainloop from blocking and ensure GUI headless compatibility
        ctk.set_appearance_mode("Dark")

    def test_tooltip_creation(self):
        root = ctk.CTk()
        btn = ctk.CTkButton(root, text="📸")
        tooltip = ToolTip(btn, "Analyser l'écran")
        self.assertEqual(tooltip.text, "Analyser l'écran")
        self.assertIsNone(tooltip.tip_window)
        root.destroy()

    def test_set_processing_ui_toggles_button_states(self):
        app = VisionAssistantApp()

        # Verify initial state is normal
        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(app.quick_input.btn_vision.cget("state"), "normal")

        # Disable UI during processing
        app.set_processing_ui(True)
        self.assertEqual(app.btn_send.cget("state"), "disabled")
        self.assertEqual(app.btn_vision.cget("state"), "disabled")
        self.assertEqual(app.quick_input.btn_send.cget("state"), "disabled")
        self.assertEqual(app.quick_input.btn_vision.cget("state"), "disabled")

        # Enable UI after processing finishes
        app.set_processing_ui(False)
        self.assertEqual(app.btn_send.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(app.quick_input.btn_vision.cget("state"), "normal")

        app.on_closing()


if __name__ == "__main__":
    unittest.main()
