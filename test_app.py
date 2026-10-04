import os
import sys
from unittest.mock import MagicMock
import unittest

# Stub missing database module for ai_engine
if "database" not in sys.modules:
    db_mock = MagicMock()
    db_mock.get_cached_answer.return_value = None
    sys.modules["database"] = db_mock

os.environ["SDL_AUDIODRIVER"] = "dummy"
os.environ["GEMINI_API_KEY"] = "dummy"

import main_vision


class TestToolTipUX(unittest.TestCase):

    def test_tooltip_creation_and_removal(self):
        root = main_vision.ctk.CTk()
        btn = main_vision.ctk.CTkButton(root, text="📸")
        tooltip = main_vision.ToolTip(btn, "Test Tooltip")

        tooltip.show_tooltip()
        self.assertIsNotNone(tooltip.tooltip_window)

        tooltip.hide_tooltip()
        self.assertIsNone(tooltip.tooltip_window)
        root.destroy()


if __name__ == "__main__":
    unittest.main()
