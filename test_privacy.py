import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_dimensions(self):
        """Verify that redact_sensitive_data preserves image dimensions and type."""
        img_array = np.full((600, 800, 3), 200, dtype=np.uint8)
        pil_img = Image.fromarray(img_array)
        redacted = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, pil_img.size)

    def test_redact_sensitive_data_with_simulated_input_box(self):
        """Verify processing on an image with a dark input field rectangle."""
        img_array = np.full((600, 800, 3), 200, dtype=np.uint8)
        # Draw a rectangle matching 100 < w < 400 and 20 < h < 60
        img_array[100:140, 100:300] = 10
        pil_img = Image.fromarray(img_array)
        redacted = self.privacy_filter.redact_sensitive_data(pil_img)

        self.assertEqual(redacted.size, pil_img.size)


if __name__ == "__main__":
    unittest.main()
