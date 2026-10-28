import os
import sys
import unittest
from unittest import mock

os.environ["GEMINI_API_KEY"] = "dummy_key"
sys.modules["database"] = mock.MagicMock()

import main_vision


class TestUIFeedback(unittest.TestCase):

    def setUp(self):
        self.app = main_vision.VisionAssistantApp()

    def tearDown(self):
        self.app.destroy()

    def test_set_inputs_enabled(self):
        # Initial states should be normal
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")

        # Disable inputs
        self.app._set_inputs_enabled(False)
        self.assertEqual(self.app.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.btn_vision.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "disabled")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "disabled")

        # Enable inputs
        self.app._set_inputs_enabled(True)
        self.assertEqual(self.app.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.btn_vision.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_send.cget("state"), "normal")
        self.assertEqual(self.app.quick_input.btn_vision.cget("state"), "normal")


if __name__ == "__main__":
    unittest.main()
