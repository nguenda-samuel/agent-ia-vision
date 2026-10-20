import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_mode(self):
        # Create test image (100x100 RGB)
        arr = np.random.randint(0, 256, (100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_high_res(self):
        # Create test high-res image (1080x1920 RGB)
        arr = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (1920, 1080))
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
