import numpy as np
from PIL import Image
from privacy import PrivacyFilter


def test_privacy_filter_redact_sensitive_data():
    filter_obj = PrivacyFilter()
    test_img = Image.new("RGB", (300, 300), color=(200, 200, 200))
    result_img = filter_obj.redact_sensitive_data(test_img)

    assert isinstance(result_img, Image.Image)
    assert result_img.size == (300, 300)
    assert result_img.mode == "RGB"


def test_privacy_filter_output_array_shape():
    filter_obj = PrivacyFilter()
    test_img = Image.new("RGB", (250, 150), color=(100, 100, 100))
    result_img = filter_obj.redact_sensitive_data(test_img)

    arr = np.array(result_img)
    assert arr.shape == (150, 250, 3)
