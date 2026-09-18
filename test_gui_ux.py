import os
import sys
from unittest.mock import MagicMock

# Mock missing database module before importing main_vision
try:
    import database
except ImportError:
    db_mock = MagicMock()
    db_mock.get_cached_answer = MagicMock(return_value=None)
    db_mock.save_answer = MagicMock()
    sys.modules["database"] = db_mock

import unittest
import customtkinter as ctk
import tkinter as tk

from main_vision import ToolTip, VisionAssistantApp, QuickInputWindow


class TestGUIUX(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        ctk.set_appearance_mode("Dark")

    def setUp(self):
        os.environ["GEMINI_API_KEY"] = "fake_test_key"
        self.root = ctk.CTk()
        self.root.withdraw()

    def tearDown(self):
        try:
            self.root.destroy()
        except Exception:
            pass

    def test_tooltip_creation_and_events(self):
        btn = ctk.CTkButton(self.root, text="📸")
        btn.pack()
        tooltip = ToolTip(btn, "Analyser l'écran (F9)")

        self.assertIsNone(tooltip.tip_window)
        tooltip.show_tip()
        self.assertIsNotNone(tooltip.tip_window)

        tooltip.hide_tip()
        self.assertIsNone(tooltip.tip_window)

    def test_set_input_state_toggles(self):
        app = VisionAssistantApp.__new__(VisionAssistantApp)
        app.entry = ctk.CTkEntry(self.root)
        app.btn_vision = ctk.CTkButton(self.root, text="📸")
        app.btn_send = ctk.CTkButton(self.root, text="🚀")

        app.set_input_state("disabled")
        self.assertEqual(app.entry.cget("state"), "disabled")
        self.assertEqual(app.btn_vision.cget("state"), "disabled")
        self.assertEqual(app.btn_send.cget("state"), "disabled")

        app.set_input_state("normal")
        self.assertEqual(app.entry.cget("state"), "normal")
        self.assertEqual(app.btn_vision.cget("state"), "normal")
        self.assertEqual(app.btn_send.cget("state"), "normal")

    def test_quick_input_window_empty_prompt(self):
        class DummyApp:
            def __init__(self):
                self.chat_messages = []
                self.processed_prompts = []

            def append_to_chat(self, text, is_user=True):
                self.chat_messages.append((text, is_user))

            def process_custom_prompt(self, text, use_vision=True):
                self.processed_prompts.append((text, use_vision))

        dummy_app = DummyApp()
        qw = QuickInputWindow.__new__(QuickInputWindow)
        qw.app = dummy_app
        qw.entry = ctk.CTkEntry(self.root)
        qw.entry.insert(0, "  ")
        qw.withdraw = lambda: None

        qw.send_prompt(use_vision=True)
        self.assertEqual(len(dummy_app.chat_messages), 0)
        self.assertEqual(len(dummy_app.processed_prompts), 1)
        self.assertEqual(dummy_app.processed_prompts[0], ("", True))


if __name__ == "__main__":
    unittest.main()
