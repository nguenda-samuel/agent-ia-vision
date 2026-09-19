import cv2
import numpy as np
from PIL import Image
import pytest

from privacy import PrivacyFilter


def test_privacy_filter_returns_pil_image():
    pf = PrivacyFilter()
    img = Image.new("RGB", (640, 480), color="white")
    redacted = pf.redact_sensitive_data(img)
    assert isinstance(redacted, Image.Image)
    assert redacted.size == (640, 480)


def test_privacy_filter_redacts_input_box():
    pf = PrivacyFilter()
    arr = np.full((500, 500, 3), 255, dtype=np.uint8)
    # Draw a rectangular input box with content inside
    cv2.rectangle(arr, (50, 50), (250, 90), (0, 0, 0), 2)
    cv2.putText(arr, "secret123", (60, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    img = Image.fromarray(arr)

    redacted = pf.redact_sensitive_data(img)
    redacted_arr = np.array(redacted)

    # The region inside the box should have been blurred
    assert not np.array_equal(arr[50:90, 50:250], redacted_arr[50:90, 50:250])


def test_privacy_filter_rgb_direct_equivalence():
    """Verify that removing BGR conversions yields pixel-identical outputs."""
    pf = PrivacyFilter()
    arr = np.full((400, 400, 3), 240, dtype=np.uint8)
    cv2.rectangle(arr, (100, 100), (250, 140), (20, 20, 20), -1)
    img = Image.fromarray(arr)

    # Reference computation using BGR conversions
    cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if 100 < w < 400 and 20 < h < 60:
            roi = cv_img[y : y + h, x : x + w]
            cv_img[y : y + h, x : x + w] = cv2.GaussianBlur(roi, (51, 51), 0)
    expected_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB))

    # Optimized PrivacyFilter call
    actual_img = pf.redact_sensitive_data(img)

    assert np.array_equal(np.array(expected_img), np.array(actual_img))
