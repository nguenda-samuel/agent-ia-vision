import unittest
import numpy as np
from PIL import Image

from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def test_has_screen_changed_initial(self):
        stream = ScreenStream(threshold=5)
        img = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 128)
        self.assertTrue(stream.has_screen_changed(img))

    def test_has_screen_changed_identical(self):
        stream = ScreenStream(threshold=5)
        img1 = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 128)
        img2 = Image.fromarray(np.ones((100, 100, 3), dtype=np.uint8) * 128)

        self.assertTrue(stream.has_screen_changed(img1))
        self.assertFalse(stream.has_screen_changed(img2))

    def test_has_screen_changed_different(self):
        stream = ScreenStream(threshold=5)
        img1 = Image.fromarray(np.zeros((100, 100, 3), dtype=np.uint8))

        # Create a contrasting image
        arr2 = np.zeros((100, 100, 3), dtype=np.uint8)
        arr2[:50, :50] = 255
        img2 = Image.fromarray(arr2)

        self.assertTrue(stream.has_screen_changed(img1))
        self.assertTrue(stream.has_screen_changed(img2))


if __name__ == "__main__":
    unittest.main()
