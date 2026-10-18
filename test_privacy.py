import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        arr = np.ones((200, 200, 3), dtype=np.uint8) * 128
        pil_img = Image.fromarray(arr)
        result = self.privacy_filter.redact_sensitive_data(pil_img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 200))

    def test_redact_sensitive_data_dimensions_and_mode(self):
        arr = np.zeros((300, 400, 3), dtype=np.uint8)
        pil_img = Image.fromarray(arr)
        result = self.privacy_filter.redact_sensitive_data(pil_img)
        self.assertEqual(result.size, (400, 300))
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
