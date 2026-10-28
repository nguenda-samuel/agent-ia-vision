import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_runs_on_normal_image(self):
        # Create a basic RGB image
        img_array = np.zeros((200, 200, 3), dtype=np.uint8)
        img = Image.fromarray(img_array)
        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 200))

    def test_redact_sensitive_data_handles_small_or_empty_roi(self):
        # Verify PrivacyFilter gracefully processes images without error
        img_array = np.ones((50, 50, 3), dtype=np.uint8) * 255
        img = Image.fromarray(img_array)
        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)


if __name__ == "__main__":
    unittest.main()
