import unittest
from PIL import Image, ImageDraw
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_dimensions(self):
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (800, 600))
        self.assertEqual(result.mode, "RGB")

    def test_redact_sensitive_data_input_box(self):
        img = Image.new("RGB", (800, 600), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        # Draw password field candidate: width 200, height 30
        draw.rectangle([200, 200, 400, 230], fill=(10, 10, 10))

        result = self.privacy_filter.redact_sensitive_data(img)
        self.assertEqual(result.size, (800, 600))


if __name__ == "__main__":
    unittest.main()
