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
