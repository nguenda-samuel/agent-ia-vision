import json
import time
try:
    from database import get_cached_answer, save_answer
except ImportError:
    def get_cached_answer(intent):
        return None

    def save_answer(intent, answer):
        pass
from google import genai
from google.genai import types
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
        """Nettoie l'image et analyse l'écran avec Gemini (avec cache DB intelligent)."""

        # -------------------------------------------------------------
        # 1. CORRECTION : VÉRIFICATION DANS LA BASE DE DONNÉES EN PREMIER
        # -------------------------------------------------------------
        # Nous ne vérifions le cache QUE si c'est une requête PUREMENT textuelle.
        # Si nous avons une capture d'écran, nous DEVONS analyser l'image actuelle.
        cached_response = get_cached_answer(user_intent)

        # On n'utilise le cache que si raw_screenshot est absent/None.
        if cached_response and not raw_screenshot:
            print(
                f"⚡ [DB Cache] Réponse textuelle trouvée pour '{user_intent}' (Instantané) !"
            )
            try:
                # On reconvertit le texte sauvegardé en dictionnaire JSON
                return json.loads(cached_response)
            except Exception:
                return {"action": "none", "text": cached_response}

        # -------------------------------------------------------------
        # 2. Si pas en cache, ou si vision requise : on traite
        # -------------------------------------------------------------
        if not raw_screenshot:
             # Gestion erreur si pas d'image
             return {
                "action": "none",
                "text": "Désolé, je ne peux pas analyser l'écran sans image.",
            }

        # Nettoyage image
        clean_image = self.privacy.redact_sensitive_data(raw_screenshot)

        # =============================================================
        # C'EST ICI QUE TU AJOUTES LE CODE DU PROMPT
        # =============================================================
        print("[Gemini] Analyse de l'image via l'API...")
        
        # Le code que tu dois copier-coller :
        prompt = f"""
        Tu es un assistant virtuel qui regarde l'écran d'un utilisateur pour l'aider à accomplir : "{user_intent}".
        Réponds STRICTEMENT avec un objet JSON au format suivant :
        {{
            "action": "click" ou "wait" ou "none",
            "x": coordonnée_X_entière_ou_null,
            "y": coordonnée_Y_entière_ou_null,
            "text": "Une phrase fluide en français expliquant ton action à l'utilisateur (Ex: Je clique sur le bouton de lecture de musique)."
        }}

        Comment choisir "action" :
        - "click" : tu vois clairement un élément cliquable pertinent pour la tâche. Donne ses coordonnées précises.
        - "wait" : à utiliser UNIQUEMENT si tu vois une preuve visuelle CONCRÈTE de chargement (roue qui tourne, barre de progression, mot "Chargement", zones grises/vides à la place d'un contenu attendu). Si la page affiche déjà du texte, des boutons et des images de façon stable et lisible, ce n'est PAS un cas de "wait" — clique ou réponds "none" selon ce que tu vois vraiment.
        - "none" : la tâche est terminée, ou il n'y a vraiment aucune action pertinente à faire.

        IMPORTANT : ne réponds "wait" que si tu identifies un indice visuel concret de chargement encore présent à l'écran. Ne l'utilise jamais par prudence ou par défaut quand tu n'es pas sûr.
        ATTENTION : La valeur de "text" ne doit JAMAIS être juste "click", "wait" ou "coordonnées". Décris clairement et précisément ce que tu vois et ce que tu fais. C'est crucial pour l'accessibilité vocale.
        """
        # =============================================================

        # 3. Ensuite, ton code fait l'appel à l'API avec ce prompt :
        max_retries = 3
        
        # -------------------------------------------------------------
        # CORRECTION 2 : DÉFINIR retry_delay AVANT LA BOUCLE
        # -------------------------------------------------------------
        retry_delay = 2  # Délai initial de 2 secondes
        
        for attempt in range(max_retries):
            try:
                # Appel Gemini (on utilise le 'prompt' mis à jour)
                response = self.client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=[clean_image, prompt],
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    ),
                )

                action_result = json.loads(response.text)

                # -------------------------------------------------------------
                # 3. SAUVEGARDE DE LA RÉPONSE DANS LA DB POUR LA PROCHAINE FOIS
                # -------------------------------------------------------------
                # Nous sauvegardons la réponse UNIQUEMENT si nous avons dû appeler Gemini.
                # Et nous ne sauvegardons QUE les réponses textuelles d'intérêt (pas les actions de clic)
                # Note: ici, on sauvegarde la réponse JSON complète pour le moment.
                save_answer(
                    user_intent, json.dumps(action_result, ensure_ascii=False)
                )

                return action_result

            except Exception as e:
                err_str = str(e)
                # Détection des erreurs de surcharge ou de quota temporaire (503, 429)
                if (
                    "503" in err_str
                    or "UNAVAILABLE" in err_str
                    or "429" in err_str
                ) and attempt < max_retries - 1:
                    # Ici, retry_delay est bien défini grâce à la correction
                    print(
                        f"[Gemini API Surchargée] Nouvelle tentative dans {retry_delay}s... (Essai {attempt + 1}/{max_retries})"
                    )
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Augmente le temps d'attente à chaque échec
                else:
                    print(f"[Erreur Gemini API] : {e}")
                    return {
                        "action": "none",
                        "text": "Désolé, je n'ai pas pu analyser l'écran.",
                    }

