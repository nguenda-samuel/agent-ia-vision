import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_sensitive_data_returns_pil_image(self):
        # Create a test image
        arr = np.zeros((200, 200, 3), dtype=np.uint8)
        img = Image.fromarray(arr)

        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (200, 200))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_rectangles(self):
        # Create an image with a dark rectangular box matching contour threshold
        arr = np.ones((200, 500, 3), dtype=np.uint8) * 255
        # Draw a dark box 200 wide x 30 high
        arr[50:80, 50:250] = 0
        img = Image.fromarray(arr)

        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (500, 200))


if __name__ == "__main__":
    unittest.main()
