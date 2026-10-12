import os
import sqlite3
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = self.temp_db.name
        self.temp_db.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "Ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Clic sur le navigateur"}'

        save_answer(intent, answer, db_path=self.db_path)
        cached = get_cached_answer(intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_uncached_answer_returns_none(self):
        cached = get_cached_answer("Intent non existant", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_overwrite_cached_answer(self):
        intent = "Ouvrir le terminal"
        answer1 = "Reponse 1"
        answer2 = "Reponse 2"

        save_answer(intent, answer1, db_path=self.db_path)
        save_answer(intent, answer2, db_path=self.db_path)

        cached = get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_sql_injection_defense(self):
        # Payloads SQL d'injection
        sqli_intent_1 = "' OR '1'='1"
        sqli_intent_2 = "'; DROP TABLE cache; --"
        sqli_answer = "Injecter reponse"

        save_answer(sqli_intent_1, sqli_answer, db_path=self.db_path)

        # Vérifier que le résultat est récupéré sans altérer les autres lignes ou la table
        cached = get_cached_answer(sqli_intent_1, db_path=self.db_path)
        self.assertEqual(cached, sqli_answer)

        # Vérifier que la table cache existe toujours et fonctionne normalement
        save_answer(sqli_intent_2, "Autre reponse", db_path=self.db_path)
        cached_2 = get_cached_answer(sqli_intent_2, db_path=self.db_path)
        self.assertEqual(cached_2, "Autre reponse")


if __name__ == "__main__":
    unittest.main()
