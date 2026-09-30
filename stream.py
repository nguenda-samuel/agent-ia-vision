from PIL import Image
import imagehash


class ScreenStream:

    def __init__(self, threshold: int = 5):
        self.last_hash = None
        # Plus le seuil est bas, plus la détection de changement est sensible
        self.threshold = threshold

    def _get_fast_phash(self, current_image: Image.Image) -> imagehash.ImageHash:
        """Optimisation performance : redimensionne l'image si elle est grande
        avant de calculer le pHash.

        `imagehash.phash` redimensionne l'image interne en 32x32 avec du
        LANCZOS/BICUBIC de haute précision. En effectuant un pré-redimensionnement
        rapide (BOX) aux dimensions max de 512x512, on réduit significativement
        le coût de conversion pour les captures 1080p/4K (~2.5x à 3x plus rapide).
        """
        max_dim = 512
        width, height = current_image.size
        if width > max_dim or height > max_dim:
            ratio = max_dim / float(max(width, height))
            new_size = (int(width * ratio), int(height * ratio))
            # Resampling.BOX est ultra-rapide pour la réduction de résolution
            current_image = current_image.resize(new_size, Image.Resampling.BOX)
        return imagehash.phash(current_image)

    def has_screen_changed(self, current_image: Image.Image) -> bool:
        """Calcule l'empreinte pHash de l'écran et vérifie s'il a bougé.

        Renvoie True si l'écran a changé, False s'il est identique à la capture
        précédente.
        """
        current_hash = self._get_fast_phash(current_image)

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
