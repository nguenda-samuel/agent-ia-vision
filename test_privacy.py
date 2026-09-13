import unittest
from PIL import Image
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format_and_size(self):
        # Create a sample RGB image (800x600)
        img_array = np.full((600, 800, 3), 200, dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (800, 600))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_with_dark_rectangle(self):
        # Create an image with a dark input box (w=200, h=40)
        img_array = np.full((600, 800, 3), 240, dtype=np.uint8)
        img_array[100:140, 100:300] = 10  # dark rectangular input box
        pil_img = Image.fromarray(img_array)

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (800, 600))


if __name__ == "__main__":
    unittest.main()
