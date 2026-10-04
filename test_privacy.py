import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        # Create a test PIL image (1080p RGB)
        img_array = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        pil_image = Image.fromarray(img_array, mode="RGB")

        redacted_image = self.privacy_filter.redact_sensitive_data(pil_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, pil_image.size)
        self.assertEqual(redacted_image.mode, "RGB")

    def test_redact_sensitive_data_small_image(self):
        # Create a smaller test image (200x200 RGB)
        img_array = np.zeros((200, 200, 3), dtype=np.uint8)
        pil_image = Image.fromarray(img_array, mode="RGB")

        redacted_image = self.privacy_filter.redact_sensitive_data(pil_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (200, 200))


if __name__ == "__main__":
    unittest.main()
