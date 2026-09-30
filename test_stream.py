import unittest
from PIL import Image, ImageDraw
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def test_has_screen_changed(self):
        stream = ScreenStream(threshold=5)

        # Initial screen capture
        img1 = Image.new("RGB", (1920, 1080), color=(255, 255, 255))
        d1 = ImageDraw.Draw(img1)
        d1.rectangle([10, 10, 100, 100], fill=(0, 0, 0))

        # First capture should always register as change (initialization)
        self.assertTrue(stream.has_screen_changed(img1))

        # Identical image should return False
        img2 = img1.copy()
        self.assertFalse(stream.has_screen_changed(img2))

        # Significantly modified image should return True
        img3 = Image.new("RGB", (1920, 1080), color=(255, 255, 255))
        d3 = ImageDraw.Draw(img3)
        d3.rectangle([500, 500, 1000, 1000], fill=(0, 0, 0))
        self.assertTrue(stream.has_screen_changed(img3))


if __name__ == "__main__":
    unittest.main()
