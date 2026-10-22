import cv2
import numpy as np
from PIL import Image


class PrivacyFilter:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def _fast_blur(
        self, roi: np.ndarray, ksize: tuple[int, int], sigma: float
    ) -> np.ndarray:
        """Fast ROI blur: downscale ROI, apply Gaussian blur, and upscale back.

        Downscaling the ROI significantly reduces computation time while
        maintaining strong privacy blur effect.
        """
        h, w = roi.shape[:2]
        if h < 16 or w < 16:
            return cv2.GaussianBlur(roi, ksize, sigma)
        small = cv2.resize(
            roi, (max(1, w // 2), max(1, h // 2)), interpolation=cv2.INTER_LINEAR
        )
        kw = max(3, (ksize[0] // 2) | 1)
        kh = max(3, (ksize[1] // 2) | 1)
        blurred = cv2.GaussianBlur(small, (kw, kh), sigma)
        return cv2.resize(blurred, (w, h), interpolation=cv2.INTER_LINEAR)

    def redact_sensitive_data(self, pil_image: Image.Image) -> Image.Image:
        open_cv_image = np.array(pil_image)
        open_cv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)

        # Performance Optimization: Downscale grayscale image by 0.5x for
        # faster face detection and contour finding on large screenshots.
        scale = 0.5
        small_gray = cv2.resize(
            gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR
        )
        inv_scale = 1.0 / scale

        # Floutage automatique des visages à l'écran
        min_face_size = (int(30 * scale), int(30 * scale))
        faces = self.face_cascade.detectMultiScale(
            small_gray, scaleFactor=1.1, minNeighbors=5, minSize=min_face_size
        )
        for x, y, w, h in faces:
            fx, fy, fw, fh = (
                int(x * inv_scale),
                int(y * inv_scale),
                int(w * inv_scale),
                int(h * inv_scale),
            )
            roi = open_cv_image[fy : fy + fh, fx : fx + fw]
            if roi.size > 0:
                open_cv_image[fy : fy + fh, fx : fx + fw] = self._fast_blur(
                    roi, (99, 99), 30
                )

        # Floutage des champs de saisie rectangulaires (ex: mots de passe)
        _, thresh = cv2.threshold(small_gray, 30, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        min_w, max_w = 100 * scale, 400 * scale
        min_h, max_h = 20 * scale, 60 * scale

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            if min_w < w < max_w and min_h < h < max_h:
                fx, fy, fw, fh = (
                    int(x * inv_scale),
                    int(y * inv_scale),
                    int(w * inv_scale),
                    int(h * inv_scale),
                )
                roi = open_cv_image[fy : fy + fh, fx : fx + fw]
                if roi.size > 0:
                    open_cv_image[fy : fy + fh, fx : fx + fw] = self._fast_blur(
                        roi, (51, 51), 0
                    )

        return Image.fromarray(cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2RGB))
