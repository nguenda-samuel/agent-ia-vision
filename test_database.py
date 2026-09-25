import unittest
from unittest.mock import MagicMock
import database
import ai_engine


class TestDatabaseCache(unittest.TestCase):

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur web"
        response = '{"action": "none", "text": "Ouverture du navigateur"}'

        database.save_answer(user_intent, response)
        cached = database.get_cached_answer(user_intent)

        self.assertEqual(cached, response)

    def test_sql_injection_resilience(self):
        # Input standard de tentative d'injection SQL
        malicious_intent = "'; DROP TABLE cached_answers; --"
        response = '{"action": "none", "text": "Secured"}'

        database.save_answer(malicious_intent, response)
        cached = database.get_cached_answer(malicious_intent)

        self.assertEqual(cached, response)

        # Vérifier que la table existe toujours et fonctionne
        normal_cached = database.get_cached_answer("non_existent_intent")
        self.assertIsNone(normal_cached)

    def test_ai_engine_uses_database_cache(self):
        user_intent = "Intention de test cache"
        expected_dict = {"action": "none", "text": "Réponse depuis la base"}
        database.save_answer(user_intent, '{"action": "none", "text": "Réponse depuis la base"}')

        mock_client = MagicMock()
        engine = ai_engine.AIEngine(gemini_client=mock_client)

        # Lorsque raw_screenshot est None, AIEngine doit lire depuis database.get_cached_answer
        res = engine.process_screen_and_intent(None, user_intent)
        self.assertEqual(res, expected_dict)


if __name__ == "__main__":
    unittest.main()
