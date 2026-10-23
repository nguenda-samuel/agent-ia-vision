import cv2
import numpy as np
from PIL import Image


class PrivacyFilter:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def _safe_blur(self, roi: np.ndarray, max_ksize: int = 51) -> np.ndarray:
        """Applique un flou gaussien de manière sécurisée sans dépasser la taille de la région."""
        h, w = roi.shape[:2]
        if h == 0 or w == 0:
            return roi
        kh = min(h if h % 2 == 1 else h - 1, max_ksize)
        kw = min(w if w % 2 == 1 else w - 1, max_ksize)
        if kh < 1 or kw < 1:
            return roi
        return cv2.GaussianBlur(roi, (kw, kh), 0)

    def redact_sensitive_data(self, pil_image: Image.Image) -> Image.Image:
        pil_image = pil_image.convert("RGB")
        open_cv_image = np.array(pil_image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Floutage automatique des visages à l'écran
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        for x, y, w, h in faces:
            roi = open_cv_image[y : y + h, x : x + w]
            open_cv_image[y : y + h, x : x + w] = self._safe_blur(
                roi, max_ksize=99
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
                open_cv_image[y : y + h, x : x + w] = self._safe_blur(
                    roi, max_ksize=51
                )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
