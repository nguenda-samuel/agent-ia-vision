import unittest
from PIL import Image
import numpy as np
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed(self):
        img1 = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))
        # Image with distinct pattern
        arr2 = np.zeros((100, 100, 3), dtype=np.uint8)
        arr2[:50, :50] = 255
        img2 = Image.fromarray(arr2)

        # First frame always returns True
        self.assertTrue(self.stream.has_screen_changed(img1))
        # Identical frame returns False
        self.assertFalse(self.stream.has_screen_changed(img1))
        # Significantly changed frame returns True
        self.assertTrue(self.stream.has_screen_changed(img2))


if __name__ == "__main__":
    unittest.main()
