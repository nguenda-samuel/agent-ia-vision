import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        # Create a sample 1080p image
        img = Image.fromarray(np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8))
        result = self.filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (1920, 1080))
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
