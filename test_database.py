import os
import tempfile
import unittest
import database


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Je clique"}'

        database.save_answer(user_intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(user_intent, db_path=self.db_path)

        self.assertEqual(cached, answer)

    def test_get_nonexistent_answer(self):
        cached = database.get_cached_answer("Inexistant", db_path=self.db_path)
        self.assertIsNone(cached)

    def test_update_cached_answer(self):
        user_intent = "Ouvrir le navigateur"
        answer1 = "Reponse 1"
        answer2 = "Reponse 2"

        database.save_answer(user_intent, answer1, db_path=self.db_path)
        database.save_answer(user_intent, answer2, db_path=self.db_path)

        cached = database.get_cached_answer(user_intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)

    def test_invalid_input_handling(self):
        self.assertIsNone(database.get_cached_answer("", db_path=self.db_path))
        self.assertIsNone(
            database.get_cached_answer(None, db_path=self.db_path)
        )

        database.save_answer("", "answer", db_path=self.db_path)
        database.save_answer(None, "answer", db_path=self.db_path)
        database.save_answer("intent", "", db_path=self.db_path)

        self.assertIsNone(database.get_cached_answer("intent", db_path=self.db_path))

    def test_sql_injection_prevention(self):
        sqli_payload = "' OR '1'='1' --"
        answer = "Secret Answer"

        database.save_answer(sqli_payload, answer, db_path=self.db_path)

        # Ensure searching for another intent does not return the secret answer via SQLi
        self.assertIsNone(
            database.get_cached_answer(
                "' OR '1'='1", db_path=self.db_path
            )
        )
        # Ensure searching exact string returns the stored answer
        self.assertEqual(
            database.get_cached_answer(sqli_payload, db_path=self.db_path),
            answer,
        )

        # Drop table attempt payload
        drop_payload = "test'; DROP TABLE cache; --"
        database.save_answer(drop_payload, answer, db_path=self.db_path)
        self.assertEqual(
            database.get_cached_answer(drop_payload, db_path=self.db_path),
            answer,
        )


if __name__ == "__main__":
    unittest.main()
