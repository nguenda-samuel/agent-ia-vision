import unittest
import numpy as np
from PIL import Image
import cv2
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed(self):
        # Create image 1 (blank canvas)
        arr1 = np.full((100, 100, 3), 255, dtype=np.uint8)
        img1 = Image.fromarray(arr1)

        # Create image 2 (identical to canvas 1)
        arr2 = np.full((100, 100, 3), 255, dtype=np.uint8)
        img2 = Image.fromarray(arr2)

        # Create image 3 (with shapes/patterns)
        arr3 = np.full((100, 100, 3), 255, dtype=np.uint8)
        cv2.rectangle(arr3, (10, 10), (90, 90), (0, 0, 0), -1)
        img3 = Image.fromarray(arr3)

        # First call always returns True
        self.assertTrue(self.stream.has_screen_changed(img1))

        # Identical image returns False
        self.assertFalse(self.stream.has_screen_changed(img2))

        # Significantly different image returns True
        self.assertTrue(self.stream.has_screen_changed(img3))

    def test_wait_until_stable(self):
        img_white = Image.new("RGB", (100, 100), color="white")

        captures = [img_white, img_white]

        def capture_func():
            if captures:
                return captures.pop(0)
            return img_white

        result = self.stream.wait_until_stable(capture_func, max_wait_sec=1.0, poll_interval=0.01)
        self.assertIsInstance(result, Image.Image)


if __name__ == "__main__":
    unittest.main()
