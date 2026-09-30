import unittest
from unittest.mock import patch, MagicMock
import numpy as np
from PIL import Image
from privacy import PrivacyFilter


class TestPrivacyFilter(unittest.TestCase):

    @patch("cv2.CascadeClassifier.detectMultiScale")
    def test_redact_sensitive_data_masks_detected_faces(self, mock_detect):
        # Mock face detection returning a face bounding box (x=50, y=50, w=40, h=40)
        mock_detect.return_value = np.array([[50, 50, 40, 40]])

        # Create image with white region where face is
        img_arr = np.ones((150, 150, 3), dtype=np.uint8) * 255
        pil_img = Image.fromarray(img_arr)

        filter = PrivacyFilter()
        redacted_img = filter.redact_sensitive_data(pil_img)
        redacted_arr = np.array(redacted_img)

        # Check that the face region (50:90, 50:90) has been solid blacked out (0)
        face_box = redacted_arr[50:90, 50:90]
        self.assertEqual(np.max(face_box), 0)


if __name__ == "__main__":
    unittest.main()
