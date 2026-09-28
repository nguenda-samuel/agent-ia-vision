import time
from PIL import Image
import imagehash


class ScreenStream:

    def __init__(self, threshold: int = 5):
        self.last_hash = None
        # Plus le seuil est bas, plus la détection de changement est sensible
        self.threshold = threshold

    def has_screen_changed(self, current_image: Image.Image) -> bool:
        """Calcule l'empreinte pHash de l'écran et vérifie s'il a bougé.

        Renvoie True si l'écran a changé, False s'il est identique à la capture
        précédente.
        """
        current_hash = imagehash.phash(current_image)

        # Premier lancement : on enregistre l'empreinte initiale
        if self.last_hash is None:
            self.last_hash = current_hash
            return True

        # Calcul de la différence entre la nouvelle et l'ancienne capture
        difference = current_hash - self.last_hash

        # Si la différence dépasse le seuil, l'écran a été modifié
        if difference > self.threshold:
            self.last_hash = current_hash
            return True

        return False

    def wait_until_stable(
        self, capture_func, max_wait_sec: float = 3.0, poll_interval: float = 0.2
    ) -> Image.Image:
        """Capture des images jusqu'à ce que l'écran se stabilise ou que le délai soit dépassé."""
        start_time = time.time()
        img = capture_func()
        self.last_hash = None
        self.has_screen_changed(img)

        while time.time() - start_time < max_wait_sec:
            time.sleep(poll_interval)
            next_img = capture_func()
            if not self.has_screen_changed(next_img):
                return next_img
            img = next_img
        return img
