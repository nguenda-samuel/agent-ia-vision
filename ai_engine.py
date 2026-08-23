from memory import ActionMemory
from privacy import PrivacyFilter
from stream import ScreenStream


class AIEngine:

    def __init__(self, gemini_client):
        self.client = gemini_client
        self.privacy = PrivacyFilter()
        self.stream = ScreenStream()
        self.memory = ActionMemory()

    def process_screen_and_intent(
        self, raw_screenshot, user_intent: str
    ) -> dict:
        """Traite l'image, vérifie la mémoire et appelle l'IA si nécessaire."""
        # 1. Nettoyage des données sensibles
        clean_image = self.privacy.redact_sensitive_data(raw_screenshot)

        # 2. Vérification de l'immobilité de l'écran
        screen_changed = self.stream.has_screen_changed(clean_image)
        screen_hash = str(self.stream.last_hash)

        # 3. Recherche dans la mémoire locale (RAG)
        cached_action = self.memory.get_routine(screen_hash, user_intent)
        if cached_action:
            print("[RAG] Action trouvée en mémoire locale (0 API consommée) !")
            return cached_action

        # 4. Appel à l'API Gemini si l'action est nouvelle
        if screen_changed:
            print("[Gemini] Analyse de l'image via l'API...")
            # L'appel à Gemini standard s'exécute ici
            # response = self.client.models.generate_content(...)
            action_result = {
                "action": "click",
                "x": 500,
                "y": 300,
            }  # Résultat d'exemple

            # Enregistrement dans la mémoire SQLite pour la prochaine fois
            self.memory.save_routine(screen_hash, user_intent, action_result)
            return action_result

        return {"action": "wait", "reason": "L'écran n'a pas changé"}
