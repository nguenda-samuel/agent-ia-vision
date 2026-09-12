import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        """Ensure redact_sensitive_data returns an image with the same dimensions."""
        img_array = np.full((1080, 1920, 3), 128, dtype=np.uint8)
        input_image = Image.fromarray(img_array)

        result_image = self.privacy_filter.redact_sensitive_data(input_image)

        self.assertIsInstance(result_image, Image.Image)
        self.assertEqual(result_image.size, (1920, 1080))

    def test_redact_sensitive_data_performance(self):
        """Verify performance optimization: processing a 1080p frame should complete under 400ms."""
        import time

        # Create realistic screen-like image with UI elements
        img_array = np.full((1080, 1920, 3), 40, dtype=np.uint8)
        img_array[200:240, 500:800] = 10
        img_array[300:340, 500:800] = 10
        input_image = Image.fromarray(img_array)

        # Warmup
        self.privacy_filter.redact_sensitive_data(input_image)

        t0 = time.perf_counter()
        self.privacy_filter.redact_sensitive_data(input_image)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        # Pre-optimization runtime was ~650ms+; optimized downscaled runtime is ~80-150ms.
        self.assertLess(
            elapsed_ms,
            400,
            f"Privacy redaction took too long: {elapsed_ms:.2f}ms (expected < 400ms)",
        )


if __name__ == "__main__":
    unittest.main()
