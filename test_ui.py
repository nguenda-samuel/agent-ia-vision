import os
import sys
import types
import unittest

# Ensure headless audio driver for pygame
os.environ["SDL_AUDIODRIVER"] = "dummy"

# Stub missing database module if needed
if "database" not in sys.modules:
    dummy_db = types.ModuleType("database")
    dummy_db.get_cached_answer = lambda intent: None
    dummy_db.save_answer = lambda intent, ans: None
    sys.modules["database"] = dummy_db

import customtkinter as ctk
from main_vision import CTkToolTip


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="🚀")
        self.button.pack()
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_initialization(self):
        tooltip = CTkToolTip(self.button, "Envoyer la demande (Entrée)")
        self.assertEqual(tooltip.text, "Envoyer la demande (Entrée)")
        self.assertIsNone(tooltip.tooltip_window)

    def test_tooltip_show_and_hide(self):
        tooltip = CTkToolTip(self.button, "Analyser l'écran (F9)")
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
