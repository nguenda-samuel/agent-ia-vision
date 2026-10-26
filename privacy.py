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

        # Floutage automatique des visages à l'écran
        faces = self.face_cascade.detectMultiScale(
            gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
        )
        for x, y, w, h in faces:
            roi = open_cv_image[y : y + h, x : x + w]
            blurred_roi = self._apply_blur(roi, max_kernel_size=99)
            if blurred_roi is not None:
                open_cv_image[y : y + h, x : x + w] = blurred_roi

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 100 < w < 400 and 20 < h < 60:
                roi = open_cv_image[y : y + h, x : x + w]
                blurred_roi = self._apply_blur(roi, max_kernel_size=51)
                if blurred_roi is not None:
                    open_cv_image[y : y + h, x : x + w] = blurred_roi

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))

    def _apply_blur(
        self, roi: np.ndarray, max_kernel_size: int = 51
    ) -> np.ndarray | None:
        """Applique un flou gaussien de manière sécurisée en adaptant le noyau à la taille de la ROI."""
        h, w = roi.shape[:2]
        if h <= 0 or w <= 0:
            return None

        # Le noyau de flou doit avoir une dimension impaire et <= aux dimensions de la ROI
        kw = min(max_kernel_size, w if w % 2 == 1 else w - 1)
        kh = min(max_kernel_size, h if h % 2 == 1 else h - 1)

        kw = max(1, kw)
        kh = max(1, kh)

        # Si le noyau est 1x1, aucun flou ne peut être appliqué
        if kw <= 1 and kh <= 1:
            return roi

        return cv2.GaussianBlur(roi, (kw, kh), 0)
