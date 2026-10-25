import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_image_same_dimensions(self):
        # Test image 200x200
        img = Image.fromarray(np.random.randint(0, 256, (200, 200, 3), dtype=np.uint8))
        redacted = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (200, 200))

    def test_redact_sensitive_data_handles_empty_or_small_images(self):
        img = Image.fromarray(np.zeros((10, 10, 3), dtype=np.uint8))
        redacted = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(redacted.size, (10, 10))


if __name__ == "__main__":
    unittest.main()
