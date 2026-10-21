import time
import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_format_and_size(self):
        # Create a test synthetic RGB image
        img = Image.fromarray(
            np.random.randint(0, 255, (200, 300, 3), dtype=np.uint8)
        )
        redacted = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (300, 200))
        self.assertEqual(redacted.mode, "RGB")

    def test_redact_sensitive_data_performance(self):
        # Benchmark image (768x768 frame)
        img = Image.fromarray(
            np.random.randint(0, 255, (768, 768, 3), dtype=np.uint8)
        )

        # Warmup
        self.privacy_filter.redact_sensitive_data(img)

        start = time.perf_counter()
        iterations = 5
        for _ in range(iterations):
            self.privacy_filter.redact_sensitive_data(img)
        elapsed = time.perf_counter() - start

        avg_ms = (elapsed / iterations) * 1000
        # Redaction should complete in under 200ms per frame
        self.assertLess(avg_ms, 200)


if __name__ == "__main__":
    unittest.main()
