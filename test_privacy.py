import unittest
from PIL import Image
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_format_and_dimensions(self):
        # Create a test RGB image
        width, height = 640, 480
        img_array = np.random.randint(0, 256, (height, width, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (width, height))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Test with small image edge case
        width, height = 100, 100
        img_array = np.zeros((height, width, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (width, height))


if __name__ == "__main__":
    unittest.main()
