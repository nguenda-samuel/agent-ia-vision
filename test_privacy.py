import time
import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions_and_type(self):
        # Create a sample RGB image (1920x1080)
        arr = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, img.size)
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_performance(self):
        arr = np.random.randint(0, 256, (1080, 1920, 3), dtype=np.uint8)
        img = Image.fromarray(arr, mode="RGB")

        # Warm-up pass
        self.privacy_filter.redact_sensitive_data(img)

        t0 = time.perf_counter()
        _ = self.privacy_filter.redact_sensitive_data(img)
        elapsed = time.perf_counter() - t0

        # Expect 1080p redaction pass to complete well under 0.7 seconds with optimization
        self.assertLess(
            elapsed, 0.7, f"Redaction took too long: {elapsed:.3f}s"
        )


if __name__ == "__main__":
    unittest.main()
