import unittest
from PIL import Image
import numpy as np
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create dummy RGB image of 800x600
        img = Image.new("RGB", (800, 600), color="white")
        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (800, 600))

    def test_redact_sensitive_data_non_empty(self):
        # Create synthetic image with random pixel values
        img_array = np.random.randint(0, 256, (300, 400, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertEqual(redacted.size, (400, 300))


if __name__ == "__main__":
    unittest.main()
