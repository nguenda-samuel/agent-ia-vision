import os
import unittest
import tkinter as tk
import customtkinter as ctk

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy_key"

from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.root = ctk.CTk()
        cls.root.withdraw()

    @classmethod
    def tearDownClass(cls):
        cls.root.destroy()

    def test_tooltip_show_and_hide(self):
        btn = ctk.CTkButton(self.root, text="🚀")
        btn.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(btn, "Envoyer la demande (🚀)")

        self.assertIsNone(tooltip.tooltip_window)

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)
        self.assertTrue(tooltip.tooltip_window.winfo_exists())

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_keyboard_focus_events(self):
        btn = ctk.CTkButton(self.root, text="📸")
        btn.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(btn, "Analyser l'écran (📸)")

        # FocusIn event
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        # FocusOut event
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)

    def test_empty_tooltip(self):
        btn = ctk.CTkButton(self.root, text="Test")
        btn.pack()
        self.root.update_idletasks()

        tooltip = CTkToolTip(btn, "")
        tooltip.show_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
