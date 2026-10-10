import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        img = Image.new("RGB", (400, 300), color=(100, 150, 200))
        result = self.filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (400, 300))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_returns_new_instance(self):
        img = Image.new("RGB", (200, 200), color=(255, 255, 255))
        result = self.filter.redact_sensitive_data(img)

        self.assertIsNot(result, img)


if __name__ == "__main__":
    unittest.main()
