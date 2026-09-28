import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        img = Image.new("RGB", (200, 200), color=(255, 255, 255))
        redacted = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (200, 200))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_input_field(self):
        # Create an image with a dark input field rectangle (width 150, height 30) with text/content inside
        img_array = np.full((200, 300, 3), 255, dtype=np.uint8)
        img_array[50:80, 50:200] = 10
        img_array[60:70, 60:190] = 200  # inner content (password text)
        img = Image.fromarray(img_array)

        redacted = self.privacy.redact_sensitive_data(img)
        redacted_array = np.array(redacted)

        # Pixels inside the rectangle should have been modified/blurred
        self.assertFalse(np.array_equal(img_array[50:80, 50:200], redacted_array[50:80, 50:200]))


if __name__ == "__main__":
    unittest.main()
