import time
import unittest
import numpy as np
from PIL import Image

from stream import ScreenStream


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed_initial_capture(self):
        img = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        self.assertTrue(self.stream.has_screen_changed(img))

    def test_has_screen_changed_identical_capture(self):
        img1 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        img2 = Image.new("RGB", (1920, 1080), color=(100, 100, 100))
        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertFalse(self.stream.has_screen_changed(img2))

    def test_has_screen_changed_modified_capture(self):
        arr1 = np.full((1080, 1920, 3), 50, dtype=np.uint8)
        arr2 = np.full((1080, 1920, 3), 50, dtype=np.uint8)
        arr2[200:500, 200:500] = 240  # Add large bright rectangle

        img1 = Image.fromarray(arr1)
        img2 = Image.fromarray(arr2)

        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertTrue(self.stream.has_screen_changed(img2))

    def test_wait_until_stable(self):
        arr1 = np.full((1080, 1920, 3), 100, dtype=np.uint8)
        img = Image.fromarray(arr1)

        def mock_capture():
            return img

        stable_img = self.stream.wait_until_stable(mock_capture, max_wait=0.5, check_interval=0.05)
        self.assertIsNotNone(stable_img)

    def test_phash_performance_speedup(self):
        # Measure time taken for 5 calls on a high-res screenshot
        arr = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(arr)

        start = time.perf_counter()
        for _ in range(5):
            self.stream.has_screen_changed(img)
        elapsed = time.perf_counter() - start

        # 5 calls should complete in under 0.25 seconds (typically ~0.03s with downscaling)
        self.assertLess(elapsed, 0.25)


if __name__ == "__main__":
    unittest.main()
