import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.pf = PrivacyFilter()

    def test_redact_sensitive_data_output_format_and_dimensions(self):
        # Create a sample RGB PIL Image (800x600)
        img_arr = np.random.randint(0, 256, (600, 800, 3), dtype=np.uint8)
        img = Image.fromarray(img_arr)

        redacted = self.pf.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (800, 600))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_with_blank_image(self):
        # Create a plain black image
        img_arr = np.zeros((300, 400, 3), dtype=np.uint8)
        img = Image.fromarray(img_arr)

        redacted = self.pf.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (400, 300))


if __name__ == "__main__":
    unittest.main()
