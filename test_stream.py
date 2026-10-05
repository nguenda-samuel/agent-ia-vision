import unittest
from PIL import Image, ImageDraw
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed(self):
        img1 = Image.new("RGB", (100, 100), color="white")
        img2 = Image.new("RGB", (100, 100), color="white")

        img3 = Image.new("RGB", (100, 100), color="white")
        draw = ImageDraw.Draw(img3)
        draw.rectangle([10, 10, 90, 90], fill="blue")
        draw.ellipse([20, 20, 80, 80], fill="red")

        # First image returns True (initial hash set)
        self.assertTrue(self.stream.has_screen_changed(img1))

        # Same image returns False
        self.assertFalse(self.stream.has_screen_changed(img2))

        # Significantly different image returns True
        self.assertTrue(self.stream.has_screen_changed(img3))

    def test_wait_until_stable(self):
        stable_img = Image.new("RGB", (50, 50), color="blue")

        def mock_capture():
            return stable_img

        result = self.stream.wait_until_stable(
            mock_capture, max_wait_sec=1.0, check_interval=0.1
        )
        self.assertEqual(result, stable_img)


if __name__ == "__main__":
    unittest.main()
