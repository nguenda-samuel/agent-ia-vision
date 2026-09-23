import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        # Create a sample RGB PIL image (768x768)
        img_array = np.random.randint(0, 256, (768, 768, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (768, 768))
        self.assertEqual(redacted_img.mode, "RGB")

    def test_redact_sensitive_data_different_size(self):
        img_array = np.zeros((300, 400, 3), dtype=np.uint8)
        pil_img = Image.fromarray(img_array)

        redacted_img = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted_img, Image.Image)
        self.assertEqual(redacted_img.size, (400, 300))


if __name__ == "__main__":
    unittest.main()
