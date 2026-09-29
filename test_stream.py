import unittest
import numpy as np
from PIL import Image
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed_first_call(self):
        img_arr = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img_arr[100:500, 100:500] = 255
        img = Image.fromarray(img_arr)
        self.assertTrue(self.stream.has_screen_changed(img))

    def test_has_screen_changed_identical_image(self):
        img_arr = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img_arr[100:500, 100:500] = 255
        img1 = Image.fromarray(img_arr)
        img2 = Image.fromarray(img_arr.copy())

        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertFalse(self.stream.has_screen_changed(img2))

    def test_has_screen_changed_modified_image(self):
        img_arr1 = np.zeros((1080, 1920, 3), dtype=np.uint8)
        img_arr1[100:500, 100:500] = 255

        img_arr2 = img_arr1.copy()
        img_arr2[600:900, 600:900] = 255

        img1 = Image.fromarray(img_arr1)
        img2 = Image.fromarray(img_arr2)

        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertTrue(self.stream.has_screen_changed(img2))


if __name__ == "__main__":
    unittest.main()
