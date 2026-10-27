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
        self, capture_fn, max_wait: float = 2.0, poll_interval: float = 0.1
    ) -> Image.Image:
        """Attend localement que l'écran se stabilise avant d'envoyer l'image à l'API."""
        start_time = time.time()
        img = capture_fn()
        self.has_screen_changed(img)
        while time.time() - start_time < max_wait:
            time.sleep(poll_interval)
            next_img = capture_fn()
            if not self.has_screen_changed(next_img):
                return next_img
            img = next_img
        return img
