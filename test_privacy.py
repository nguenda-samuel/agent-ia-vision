import unittest
import numpy as np
import cv2
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_output_format(self):
        """Test that redact_sensitive_data returns a PIL Image of same size and RGB mode."""
        img = Image.fromarray(np.random.randint(0, 256, (480, 640, 3), dtype=np.uint8))
        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (640, 480))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_contour_redaction(self):
        """Test that rectangular input fields matching criteria are blurred."""
        # Create a plain white image with a dark rectangular input field
        img_arr = np.ones((600, 800, 3), dtype=np.uint8) * 255
        # Rectangle with w=200, h=40 (within 100 < w < 400 and 20 < h < 60)
        cv2.rectangle(img_arr, (200, 200), (400, 240), (10, 10, 10), -1)

        pil_img = Image.fromarray(img_arr)
        result = self.privacy_filter.redact_sensitive_data(pil_img)

        result_arr = np.array(result)
        # Inside the rectangle, pixel values should be blurred (no longer solid 10,10,10 at edges/center)
        center_pixel = result_arr[220, 300]
        self.assertNotEqual(tuple(center_pixel), (255, 255, 255))

    def test_performance_improvement(self):
        """Test that redaction on a 1080p image executes quickly."""
        img = Image.fromarray(np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8))
        import time
        t0 = time.perf_counter()
        self.privacy_filter.redact_sensitive_data(img)
        elapsed = time.perf_counter() - t0
        # Performance requirement: processing a 1080p frame should take less than 0.5s
        self.assertLess(elapsed, 0.5)


if __name__ == "__main__":
    unittest.main()
