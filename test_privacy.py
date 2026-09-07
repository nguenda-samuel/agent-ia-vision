import numpy as np
from PIL import Image
from privacy import PrivacyFilter


def test_privacy_filter_redact_sensitive_data():
    filter_inst = PrivacyFilter()

    # Create a 400x400 RGB test image
    img_array = np.full((400, 400, 3), 128, dtype=np.uint8)
    pil_img = Image.fromarray(img_array)

    redacted_img = filter_inst.redact_sensitive_data(pil_img)

    assert isinstance(redacted_img, Image.Image)
    assert redacted_img.size == (400, 400)
    assert redacted_img.mode == "RGB"


def test_privacy_filter_empty_or_small():
    filter_inst = PrivacyFilter()

    img_array = np.zeros((100, 100, 3), dtype=np.uint8)
    pil_img = Image.fromarray(img_array)

    redacted_img = filter_inst.redact_sensitive_data(pil_img)

    assert isinstance(redacted_img, Image.Image)
    assert redacted_img.size == (100, 100)
