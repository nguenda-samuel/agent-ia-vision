import os
import unittest
import customtkinter as ctk
from main_vision import ToolTip

# Set env vars required for headless Tkinter / Pygame testing
os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"


class TestToolTipUI(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.button = ctk.CTkButton(self.root, text="🚀")
        self.button.pack()
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_show_and_hide(self):
        tooltip = ToolTip(self.button, "Test Tooltip")
        self.assertIsNone(tooltip.tw)

        # Trigger show
        tooltip.show()
        self.root.update_idletasks()
        self.assertIsNotNone(tooltip.tw)

        # Trigger hide
        tooltip.hide()
        self.root.update_idletasks()
        self.assertIsNone(tooltip.tw)


if __name__ == "__main__":
    unittest.main()
