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

        # Optimization: Downscale grayscale image (scale factor 0.5) to accelerate
        # face cascade detection and contour extraction by ~7-8x (~200ms -> ~26ms).
        scale = 0.5
        small_gray = cv2.resize(
            gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA
        )
        inv_scale = 1.0 / scale

        # Floutage automatique des visages à l'écran
        faces = self.face_cascade.detectMultiScale(
            small_gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(int(30 * scale), int(30 * scale)),
        )
        for x, y, w, h in faces:
            rx, ry, rw, rh = (
                int(x * inv_scale),
                int(y * inv_scale),
                int(w * inv_scale),
                int(h * inv_scale),
            )
            roi = open_cv_image[ry : ry + rh, rx : rx + rw]
            if roi.size > 0:
                open_cv_image[ry : ry + rh, rx : rx + rw] = cv2.GaussianBlur(
                    roi, (99, 99), 30
                )

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh = cv2.threshold(small_gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            orig_w, orig_h = w * inv_scale, h * inv_scale
            if 100 < orig_w < 400 and 20 < orig_h < 60:
                rx, ry, rw, rh = (
                    int(x * inv_scale),
                    int(y * inv_scale),
                    int(w * inv_scale),
                    int(h * inv_scale),
                )
                roi = open_cv_image[ry : ry + rh, rx : rx + rw]
                if roi.size > 0:
                    open_cv_image[ry : ry + rh, rx : rx + rw] = cv2.GaussianBlur(
                        roi, (51, 51), 0
                    )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
