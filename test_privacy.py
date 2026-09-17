import numpy as np
from PIL import Image
from privacy import PrivacyFilter


def test_redact_sensitive_data_dimensions_and_mode():
    filter_inst = PrivacyFilter()
    # Create dummy image (1080p RGB)
    img_array = np.zeros((1080, 1920, 3), dtype=np.uint8)
    pil_img = Image.fromarray(img_array)

    redacted = filter_inst.redact_sensitive_data(pil_img)

    assert redacted.size == (1920, 1080)
    assert redacted.mode == "RGB"


def test_redact_sensitive_data_runs_without_error():
    filter_inst = PrivacyFilter()
    # Create random noise image simulating screen contents
    img_array = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    pil_img = Image.fromarray(img_array)

    redacted = filter_inst.redact_sensitive_data(pil_img)

    assert isinstance(redacted, Image.Image)
    assert redacted.size == (640, 480)
