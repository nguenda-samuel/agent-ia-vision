import unittest
import cv2
import numpy as np
from PIL import Image

from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        img = Image.new("RGB", (200, 200), color=(100, 150, 200))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 200))

    def test_redact_sensitive_data_applies_blur(self):
        # Create an image with a dark box containing text/content matching sensitive input dimensions
        img_array = np.full((300, 500, 3), 200, dtype=np.uint8)
        img_array[100:130, 100:300] = (10, 10, 10)
        # Add white text/content inside the box so GaussianBlur produces changes
        img_array[110:120, 120:280] = (255, 255, 255)
        input_img = Image.fromarray(img_array.copy())

        redacted_img = self.privacy_filter.redact_sensitive_data(input_img)
        redacted_array = np.array(redacted_img)

        # The region around (100:130, 100:300) should be blurred
        self.assertFalse(
            np.array_equal(
                redacted_array[100:130, 100:300], img_array[100:130, 100:300]
            )
        )


if __name__ == "__main__":
    unittest.main()
