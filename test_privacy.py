import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a test image (768x768 RGB)
        img_np = np.random.randint(0, 256, (768, 768, 3), dtype=np.uint8)
        input_image = Image.fromarray(img_np, mode="RGB")

        redacted_image = self.privacy_filter.redact_sensitive_data(input_image)

        self.assertIsInstance(redacted_image, Image.Image)
        self.assertEqual(redacted_image.size, (768, 768))
        self.assertEqual(redacted_image.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
