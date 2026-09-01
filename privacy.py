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
            open_cv_image[y : y + h, x : x + w] = cv2.GaussianBlur(
                roi, (99, 99), 30
            )

        # Masquage opaque (solide) des champs de saisie rectangulaires (ex: mots de passe)
        # Sécurité : le floutage est réversible via déconvolution ; un rectangle noir élimine tout risque de fuite.
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if 100 < w < 400 and 20 < h < 60:
                cv2.rectangle(open_cv_image, (x, y), (x + w, y + h), (0, 0, 0), -1)

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
