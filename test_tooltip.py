import os
import sys
import unittest
from unittest.mock import MagicMock

# Environment mocks for headless testing
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

# Mock database module if not available
if "database" not in sys.modules:
    mock_db = MagicMock()
    mock_db.get_cached_answer.return_value = None
    sys.modules["database"] = mock_db

import customtkinter as ctk
from main_vision import ToolTip


class TestToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = ctk.CTk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_tooltip_show_and_hide(self):
        btn = ctk.CTkButton(self.root, text="Test")
        btn.pack()
        self.root.update_idletasks()

        tooltip = ToolTip(btn, "Test Hover Tooltip")

        # Initially no tooltip window
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger hover event
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        # Trigger leave event
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
