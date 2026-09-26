import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_image(self):
        img_array = np.zeros((100, 100, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        result = self.filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (100, 100))

    def test_redact_sensitive_data_preserves_dimensions(self):
        img_array = np.full((200, 300, 3), 128, dtype=np.uint8)
        img = Image.fromarray(img_array)
        result = self.filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (300, 200))


if __name__ == "__main__":
    unittest.main()
