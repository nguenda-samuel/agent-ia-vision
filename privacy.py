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

        # Performance optimization:
        # Downscale gray image by 0.5x for faster face detection and contour search.
        # This reduces image area by 4x, making Haar Cascade detection ~3x faster per frame.
        small_gray = cv2.resize(
            gray, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR
        )

        # Floutage automatique des visages à l'écran
        # Detect on downscaled image (minSize 15x15 corresponds to 30x30 on full resolution)
        faces = self.face_cascade.detectMultiScale(
            small_gray, scaleFactor=1.1, minNeighbors=5, minSize=(15, 15)
        )
        for x, y, w, h in faces:
            # Scale coordinates back to original full resolution (2x)
            X, Y, W, H = x * 2, y * 2, w * 2, h * 2
            roi = open_cv_image[Y : Y + H, X : X + W]
            open_cv_image[Y : Y + H, X : X + W] = cv2.GaussianBlur(
                roi, (99, 99), 30
            )

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh_small = cv2.threshold(
            small_gray, 30, 255, cv2.THRESH_BINARY_INV
        )
        contours, _ = cv2.findContours(
            thresh_small, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # Scaled check: 100 < full_w < 400 -> 50 < w < 200, 20 < full_h < 60 -> 10 < h < 30
            if 50 < w < 200 and 10 < h < 30:
                X, Y, W, H = x * 2, y * 2, w * 2, h * 2
                roi = open_cv_image[Y : Y + H, X : X + W]
                open_cv_image[Y : Y + H, X : X + W] = cv2.GaussianBlur(
                    roi, (51, 51), 0
                )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
