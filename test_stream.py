import unittest
from PIL import Image, ImageDraw
from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed_initial(self):
        img = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        self.assertTrue(self.stream.has_screen_changed(img))

    def test_has_screen_changed_identical(self):
        img = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 300, 300], fill=(255, 0, 0))

        self.assertTrue(self.stream.has_screen_changed(img))
        self.assertFalse(self.stream.has_screen_changed(img.copy()))

    def test_has_screen_changed_different(self):
        img1 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        draw1 = ImageDraw.Draw(img1)
        draw1.rectangle([100, 100, 300, 300], fill=(255, 0, 0))

        img2 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        draw2 = ImageDraw.Draw(img2)
        draw2.rectangle([500, 500, 800, 800], fill=(0, 255, 0))

        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertTrue(self.stream.has_screen_changed(img2))

    def test_wait_until_stable(self):
        img1 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        draw1 = ImageDraw.Draw(img1)
        draw1.rectangle([100, 100, 300, 300], fill=(255, 0, 0))

        img2 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        draw2 = ImageDraw.Draw(img2)
        draw2.rectangle([500, 500, 800, 800], fill=(0, 255, 0))

        frames = [img1, img2, img2, img2]
        frame_idx = [0]

        def capture_fn():
            idx = min(frame_idx[0], len(frames) - 1)
            frame_idx[0] += 1
            return frames[idx]

        stable_img = self.stream.wait_until_stable(
            capture_fn, max_wait=1.0, poll_interval=0.01
        )
        self.assertIsNotNone(stable_img)


if __name__ == "__main__":
    unittest.main()
