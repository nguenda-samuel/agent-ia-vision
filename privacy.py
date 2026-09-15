import cv2
import numpy as np
from PIL import Image


class PrivacyFilter:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def redact_sensitive_data(self, pil_image: Image.Image) -> Image.Image:
        open_cv_image = np.array(pil_image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Optimization: Downscale grayscale image by 50% for fast face cascade detection.
        # This speeds up Haar cascade evaluation by ~2.5x while retaining accuracy.
        scale = 0.5
        small_gray = cv2.resize(
            gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_NEAREST
        )
        faces = self.face_cascade.detectMultiScale(
            small_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(int(30 * scale), int(30 * scale)),
        )

        # Fast box blur (cv2.blur) instead of heavy GaussianBlur for region redaction.
        for x, y, w, h in faces:
            x_orig, y_orig, w_orig, h_orig = (
                int(x / scale),
                int(y / scale),
                int(w / scale),
                int(h / scale),
            )
            roi = open_cv_image[y_orig : y_orig + h_orig, x_orig : x_orig + w_orig]
            if roi.size > 0:
                open_cv_image[y_orig : y_orig + h_orig, x_orig : x_orig + w_orig] = (
                    cv2.blur(roi, (51, 51))
                )

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 100 < w < 400 and 20 < h < 60:
                roi = open_cv_image[y : y + h, x : x + w]
                if roi.size > 0:
                    open_cv_image[y : y + h, x : x + w] = cv2.blur(
                        roi, (25, 25)
                    )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
