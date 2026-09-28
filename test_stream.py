import unittest
from PIL import Image
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed_first_run(self):
        img1 = Image.new("RGB", (100, 100), color=(255, 0, 0))
        self.assertTrue(self.stream.has_screen_changed(img1))

    def test_has_screen_changed_same_image(self):
        img1 = Image.new("RGB", (100, 100), color=(255, 0, 0))
        self.stream.has_screen_changed(img1)
        self.assertFalse(self.stream.has_screen_changed(img1))

    def test_wait_until_stable(self):
        img_red = Image.new("RGB", (100, 100), color=(255, 0, 0))
        frames = [img_red, img_red]
        idx = 0

        def capture():
            nonlocal idx
            img = frames[min(idx, len(frames) - 1)]
            idx += 1
            return img

        res = self.stream.wait_until_stable(capture, max_wait_sec=1.0, poll_interval=0.01)
        self.assertIsNotNone(res)


if __name__ == "__main__":
    unittest.main()
