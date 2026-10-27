import unittest
from PIL import Image
import numpy as np
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def test_has_screen_changed_initial(self):
        stream = ScreenStream(threshold=5)
        arr = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img1 = Image.fromarray(arr)

        # First call should register initial hash and return True
        self.assertTrue(stream.has_screen_changed(img1))

    def test_has_screen_changed_identical(self):
        stream = ScreenStream(threshold=5)
        arr = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img1 = Image.fromarray(arr)
        img2 = Image.fromarray(arr.copy())

        self.assertTrue(stream.has_screen_changed(img1))
        # Identical image should return False
        self.assertFalse(stream.has_screen_changed(img2))

    def test_has_screen_changed_different(self):
        stream = ScreenStream(threshold=5)
        arr1 = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img1 = Image.fromarray(arr1)

        arr2 = np.zeros((1080, 1920, 3), dtype=np.uint8)
        arr2[200:800, 200:800] = 255
        img2 = Image.fromarray(arr2)

        self.assertTrue(stream.has_screen_changed(img1))
        # Significantly different image should return True
        self.assertTrue(stream.has_screen_changed(img2))


if __name__ == "__main__":
    unittest.main()
