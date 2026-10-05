import os
import tempfile
import unittest

from database import get_cached_answer, save_answer


class TestDatabase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_cache_and_sqli_prevention(self):
        sqli_intent = "'; DROP TABLE answers; --"
        save_answer(sqli_intent, "safe_response", db_path=self.db_path)
        self.assertEqual(
            get_cached_answer(sqli_intent, db_path=self.db_path),
            "safe_response",
        )


if __name__ == "__main__":
    unittest.main()
