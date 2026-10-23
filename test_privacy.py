import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_redact_rgba_image(self):
        # Create an RGBA image
        img_rgba = Image.new("RGBA", (200, 100), (255, 255, 255, 255))
        result = self.privacy.redact_sensitive_data(img_rgba)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.mode, "RGB")

    def test_redact_small_input_boxes(self):
        # Create an image with black rectangular shapes that match contour conditions (100 < w < 400 and 20 < h < 60)
        # e.g., w=150, h=25 (where 25 is smaller than default ksize 51)
        arr = np.ones((100, 300, 3), dtype=np.uint8) * 255
        # Draw a dark box (simulating input field)
        arr[30:55, 50:200] = 0
        img = Image.fromarray(arr, mode="RGB")

        # Before fix, this would throw cv2.error due to ksize 51 > height 25
        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)

    def test_safe_blur_directly(self):
        # Test _safe_blur helper with tiny ROIs
        tiny_roi = np.zeros((10, 10, 3), dtype=np.uint8)
        blurred = self.privacy._safe_blur(tiny_roi, max_ksize=51)
        self.assertEqual(blurred.shape, tiny_roi.shape)


if __name__ == "__main__":
    unittest.main()
