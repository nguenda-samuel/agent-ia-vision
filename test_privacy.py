import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format_and_size(self):
        # Create a blank RGB image (300x200)
        img = Image.fromarray(np.zeros((200, 300, 3), dtype=np.uint8))
        redacted_img = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (300, 200))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_with_random_noise(self):
        # Create random noise RGB image (1080x1920) simulating screen capture
        np.random.seed(42)
        random_array = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(random_array)

        redacted_img = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (1920, 1080))


if __name__ == "__main__":
    unittest.main()
