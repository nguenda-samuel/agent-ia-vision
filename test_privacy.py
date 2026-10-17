import unittest
import time
import numpy as np
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        """Verify that redact_sensitive_data returns a PIL Image with identical dimensions."""
        width, height = 768, 768
        img = Image.new("RGB", (width, height), color=(200, 200, 200))
        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (width, height))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_input_blurring(self):
        """Verify that rectangular input regions are processed without error and modified if matching criteria."""
        width, height = 768, 768
        img = Image.new("RGB", (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Draw a dark border input box matching the filter criteria (100 < w < 400 and 20 < h < 60)
        draw.rectangle([50, 50, 250, 90], fill=(255, 255, 255), outline=(0, 0, 0))

        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (width, height))

    def test_performance_benchmark(self):
        """Benchmark redact_sensitive_data execution time across multiple iterations."""
        width, height = 768, 768
        img = Image.new("RGB", (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        draw.rectangle([100, 100, 300, 140], fill=(255, 255, 255), outline=(50, 50, 50))

        # Warmup
        self.privacy_filter.redact_sensitive_data(img)

        iterations = 50
        start_time = time.perf_counter()
        for _ in range(iterations):
            self.privacy_filter.redact_sensitive_data(img)
        elapsed_ms = ((time.perf_counter() - start_time) / iterations) * 1000

        print(f"\n[Benchmark] PrivacyFilter.redact_sensitive_data average latency: {elapsed_ms:.2f} ms / frame")
        self.assertLess(elapsed_ms, 50.0)


if __name__ == "__main__":
    unittest.main()
