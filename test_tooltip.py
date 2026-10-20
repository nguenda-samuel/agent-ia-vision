import os
import sys
import unittest
from unittest.mock import MagicMock

# Mock database module if not present
sys.modules["database"] = MagicMock()

import tkinter as tk
import customtkinter as ctk

# Set dummy SDL_AUDIODRIVER and GEMINI_API_KEY for headless test execution
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import ToolTip


class TestToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="🚀")
        self.button.pack()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation_and_events(self):
        tooltip = ToolTip(self.button, "Test Tooltip")
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger show
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        # Trigger hide
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
