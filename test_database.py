import os
import tempfile
import unittest
import numpy as np
from PIL import Image

import database
from privacy import PrivacyFilter


class TestDatabaseCache(unittest.TestCase):

    def setUp(self):
        self.temp_db_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.db_path = self.temp_db_file.name
        self.temp_db_file.close()

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_get_cached_answer(self):
        intent = "ouvrir le navigateur"
        answer = '{"action": "click", "x": 100, "y": 200, "text": "Je clique sur le navigateur."}'

        # Verify initially None
        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertIsNone(cached)

        # Save answer and retrieve
        database.save_answer(intent, answer, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer)

    def test_replace_existing_cache_entry(self):
        intent = "ouvrir le navigateur"
        answer1 = '{"action": "click", "x": 100, "y": 200}'
        answer2 = '{"action": "click", "x": 150, "y": 250}'

        database.save_answer(intent, answer1, db_path=self.db_path)
        database.save_answer(intent, answer2, db_path=self.db_path)
        cached = database.get_cached_answer(intent, db_path=self.db_path)
        self.assertEqual(cached, answer2)


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy_filter = PrivacyFilter()

    def test_redact_sensitive_data_returns_image_of_same_size_and_mode(self):
        # Create dummy image
        img = Image.new("RGB", (300, 200), color=(100, 150, 200))
        result = self.privacy_filter.redact_sensitive_data(img)

        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (300, 200))
        self.assertEqual(result.mode, "RGB")


if __name__ == "__main__":
    unittest.main()
