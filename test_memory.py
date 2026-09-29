import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_created(self):
        """Vérifie que l'index composite idx_routines_hash_intent est bien créé."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent';"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(result, "L'index idx_routines_hash_intent doit exister dans la base de données.")
            self.assertEqual(result[0], "idx_routines_hash_intent")

    def test_save_and_get_routine(self):
        """Vérifie la sauvegarde et la récupération d'une routine."""
        screen_hash = "hash_12345"
        user_intent = "Clique sur le bouton Valider"
        action_data = {"action": "click", "x": 100, "y": 200, "text": "Validation"}

        # Récupération avant sauvegarde (doit être None)
        self.assertIsNone(self.memory.get_routine(screen_hash, user_intent))

        # Sauvegarde
        self.memory.save_routine(screen_hash, user_intent, action_data)

        # Récupération après sauvegarde
        retrieved = self.memory.get_routine(screen_hash, user_intent)
        self.assertEqual(retrieved, action_data)


if __name__ == "__main__":
    unittest.main()
