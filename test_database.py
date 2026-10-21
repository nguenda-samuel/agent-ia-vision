import os
import tempfile
import unittest

import database


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_db_and_caching(self):
        database.init_db(self.db_path)
        intent = "clique sur le bouton"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "OK"}'

        self.assertIsNone(database.get_cached_answer(intent, db_path=self.db_path))

        database.save_answer(intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_save_answer_replace(self):
        database.init_db(self.db_path)
        intent = "test intent"
        answer1 = "answer 1"
        answer2 = "answer 2"

        database.save_answer(intent, answer1, db_path=self.db_path)
        database.save_answer(intent, answer2, db_path=self.db_path)

        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)


if __name__ == "__main__":
    unittest.main()
