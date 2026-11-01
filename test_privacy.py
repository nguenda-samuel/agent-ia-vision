import unittest
import numpy as np
from PIL import Image

from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_preserves_dimensions_and_mode(self):
        """Ensure image dimensions and RGB mode are preserved after redaction."""
        img = Image.new("RGB", (640, 480), color=(120, 140, 160))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (640, 480))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_blurs_sensitive_input_box(self):
        """Ensure sensitive dark rectangular input fields are detected and blurred."""
        # Create a background image
        img_array = np.full((300, 500, 3), 200, dtype=np.uint8)
        # Create dark input field within 100 < w < 400 and 20 < h < 60
        # Box from y: 100 to 140 (h=40), x: 100 to 300 (w=200)
        img_array[100:140, 100:300] = (15, 15, 15)
        # Put high-contrast text content inside
        img_array[115:125, 120:280] = (255, 255, 255)
        input_img = Image.fromarray(img_array.copy())

        redacted_img = self.privacy_filter.redact_sensitive_data(input_img)
        redacted_array = np.array(redacted_img)

        # Region inside the box should have been blurred
        self.assertFalse(
            np.array_equal(
                redacted_array[100:140, 100:300], img_array[100:140, 100:300]
            )
        )


if __name__ == "__main__":
    unittest.main()
