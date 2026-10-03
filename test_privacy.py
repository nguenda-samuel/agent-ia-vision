import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        # Create a dummy RGB image
        img_array = np.zeros((300, 300, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)

        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (300, 300))

    def test_redact_sensitive_data_with_rectangular_shapes(self):
        # Create an image with a dark box matching input field size criteria
        img_array = np.full((300, 300, 3), 255, dtype=np.uint8)
        # Draw a dark box (w=200, h=40 in original scale => w=100, h=20 in 0.5x scale)
        img_array[100:140, 50:250] = 0
        img = Image.fromarray(img_array)

        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (300, 300))


if __name__ == "__main__":
    unittest.main()
