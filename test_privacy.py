import unittest
import numpy as np
from PIL import Image
from privacy import PrivacyFilter

class TestPrivacyFilter(unittest.TestCase):
    def test_redact_sensitive_data_runs_and_returns_image(self):
        filter_obj = PrivacyFilter()
        # Create a test image with RGB array
        arr = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        img = Image.fromarray(arr)
        redacted = filter_obj.redact_sensitive_data(img)
        self.assertIsInstance(redacted, Image.Image)
        self.assertEqual(redacted.size, (200, 200))

if __name__ == '__main__':
    unittest.main()
