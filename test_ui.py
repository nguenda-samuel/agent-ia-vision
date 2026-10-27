import os
import sys
import unittest
from unittest.mock import MagicMock

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

# Mock database module before importing main_vision
mock_db = MagicMock()
mock_db.get_cached_answer.return_value = None
sys.modules["database"] = mock_db

import customtkinter as ctk  # noqa: E402
import main_vision  # noqa: E402


class TestCTkToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.root.withdraw()
        self.button = ctk.CTkButton(self.root, text="🚀")
        self.tooltip = main_vision.CTkToolTip(
            self.button, "Envoyer la commande à l'agent"
        )

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_initialization(self):
        self.assertEqual(self.tooltip.text, "Envoyer la commande à l'agent")
        self.assertIsNone(self.tooltip.tooltip_window)

    def test_tooltip_show_and_hide(self):
        # Simulate hover event
        self.tooltip.show_tooltip()
        self.assertIsNotNone(self.tooltip.tooltip_window)

        # Simulate leave event
        self.tooltip.hide_tooltip()
        self.assertIsNone(self.tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
