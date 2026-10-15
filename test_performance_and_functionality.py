import os
import sqlite3
import tempfile
import unittest
import numpy as np
from PIL import Image, ImageDraw

from memory import ActionMemory
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_format_and_dimensions(self):
        # Create a test PIL image (500x300 RGB) with a dark rectangle simulating an input box
        img_np = np.ones((300, 500, 3), dtype=np.uint8) * 240
        pil_img = Image.fromarray(img_np)
        draw = ImageDraw.Draw(pil_img)
        # Draw dark input field rectangle (w: 200, h: 30)
        draw.rectangle([100, 100, 300, 130], fill=(10, 10, 10))

        redacted = self.privacy.redact_sensitive_data(pil_img)

        # Ensure return type and image dimensions are preserved
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (500, 300))

        # Convert to numpy array and check that pixel values changed in redacted region (blurred)
        redacted_np = np.array(redacted)
        self.assertFalse(np.array_equal(img_np, redacted_np))


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.memory = ActionMemory(self.temp_db.name)

    def tearDown(self):
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_index_created(self):
        with sqlite3.connect(self.temp_db.name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            index = cursor.fetchone()
            self.assertIsNotNone(index)
            self.assertEqual(index[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        hash_val = "abc123hash"
        intent = "click on submit"
        action_data = {"action": "click", "x": 100, "y": 200}

        # Non-existent routine should return None
        self.assertIsNone(self.memory.get_routine(hash_val, intent))

        # Save and retrieve
        self.memory.save_routine(hash_val, intent, action_data)
        retrieved = self.memory.get_routine(hash_val, intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
