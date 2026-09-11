import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format_and_dimensions(self):
        # Create a mock 1080p image (1920x1080)
        np.random.seed(42)
        array = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        input_image = Image.fromarray(array, mode="RGB")

        redacted_image = self.privacy_filter.redact_sensitive_data(input_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (1920, 1080))
        self.assertEqual(redacted_image.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Create a small image (100x100)
        array = np.zeros((100, 100, 3), dtype=np.uint8)
        input_image = Image.fromarray(array, mode="RGB")

        redacted_image = self.privacy_filter.redact_sensitive_data(input_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (100, 100))


if __name__ == "__main__":
    unittest.main()
