import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create a synthetic image (1080x1920, RGB)
        arr = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(img)

        self.assertEqual(redacted_img.size, (1920, 1080))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Create a small synthetic image (100x100, RGB)
        arr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        redacted_img = self.privacy_filter.redact_sensitive_data(img)

        self.assertEqual(redacted_img.size, (100, 100))
        self.assertEqual(redacted_img.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
