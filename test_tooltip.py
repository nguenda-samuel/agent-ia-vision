import sys
import unittest
from unittest.mock import MagicMock

if "database" not in sys.modules:
    sys.modules["database"] = MagicMock()

import customtkinter as ctk
from main_vision import CToolTip


class TestCToolTip(unittest.TestCase):

    def setUp(self):
        self.root = ctk.CTk()
        self.btn = ctk.CTkButton(self.root, text="🚀")
        self.btn.pack()
        self.root.update()

    def tearDown(self):
        self.root.destroy()

    def test_tooltip_creation_and_destruction(self):
        tooltip = CToolTip(self.btn, "Envoyer la demande (Entrée)")
        self.assertIsNone(tooltip.tooltip_window)

        # Trigger hover (<Enter>)
        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        # Trigger leave (<Leave>)
        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)


if __name__ == "__main__":
    unittest.main()
