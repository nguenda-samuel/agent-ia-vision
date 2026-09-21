import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock missing database module if absent
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    mock_db.save_answer.return_value = None
    sys.modules["database"] = mock_db

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

import customtkinter as ctk
from main_vision import ToolTip, VisionAssistantApp


class TestGUIToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def test_tooltip_creation_and_hover(self):
        root = ctk.CTk()
        btn = ctk.CTkButton(root, text="🚀")
        tooltip = ToolTip(btn, "Envoyer l'instruction")

        self.assertIsNone(tooltip.tip_window)

        # Simulate hover show
        tooltip.show_tip()
        self.assertIsNotNone(tooltip.tip_window)

        # Simulate hover hide
        tooltip.hide_tip()
        self.assertIsNone(tooltip.tip_window)

        root.destroy()

    def test_app_and_quick_input_initialization(self):
        app = VisionAssistantApp()
        self.assertIsNotNone(app)
        self.assertIsNotNone(app.btn_vision)
        self.assertIsNotNone(app.btn_send)
        self.assertIsNotNone(app.quick_input.btn_send)
        app.destroy()


if __name__ == "__main__":
    unittest.main()
