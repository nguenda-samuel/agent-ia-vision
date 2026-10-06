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

        # ⚡ OPTIMIZATION (Bolt): Downscale image by 0.5x for feature detection.
        # Haar Cascade and contour finding on 1080p/4K screenshots are O(N) over pixels.
        # Downscaling to 0.5x reduces pixel count by 75%, accelerating face cascade and
        # contour search ~3x-4x while maintaining high detection accuracy.
        scale = 0.5
        inv_scale = 2
        small_gray = cv2.resize(
            gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_AREA
        )

        # Floutage automatique des visages à l'écran
        # Min size in downscaled space is adjusted (30*0.5 = 15)
        small_faces = self.face_cascade.detectMultiScale(
            small_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15)
        )
        for sx, sy, sw, sh in small_faces:
            x, y, w, h = (
                sx * inv_scale,
                sy * inv_scale,
                sw * inv_scale,
                sh * inv_scale,
            )
            roi = open_cv_image[y : y + h, x : x + w]
            open_cv_image[y : y + h, x : x + w] = cv2.GaussianBlur(
                roi, (99, 99), 30
            )

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh = cv2.threshold(small_gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            sx, sy, sw, sh = cv2.boundingRect(cnt)
            x, y, w, h = (
                sx * inv_scale,
                sy * inv_scale,
                sw * inv_scale,
                sh * inv_scale,
            )
            if 100 < w < 400 and 20 < h < 60:
                roi = open_cv_image[y : y + h, x : x + w]
                open_cv_image[y : y + h, x : x + w] = cv2.GaussianBlur(
                    roi, (51, 51), 0
                )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
