import os
import sqlite3
import tempfile
import unittest
from PIL import Image, ImageDraw

from memory import ActionMemory
from privacy import PrivacyFilter
from stream import ScreenStream


class TestActionMemoryPerformance(unittest.TestCase):

    def setUp(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
        self.temp_db.close()
        self.db_path = self.temp_db.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_database_index_exists(self):
        """Verify that composite index idx_routines_hash_intent exists on routines table."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_hash_intent'"
            )
            result = cursor.fetchone()
            self.assertIsNotNone(
                result, "Database index idx_routines_hash_intent should exist"
            )

    def test_save_and_get_routine(self):
        """Verify saving and retrieving routines from ActionMemory."""
        screen_hash = "abc123hash"
        user_intent = "click login button"
        action_data = {"action": "click", "x": 100, "y": 200}

        self.memory.save_routine(screen_hash, user_intent, action_data)
        retrieved = self.memory.get_routine(screen_hash, user_intent)

        self.assertEqual(retrieved, action_data)

    def test_get_nonexistent_routine(self):
        """Verify None is returned when routine does not exist."""
        retrieved = self.memory.get_routine("nonexistent", "do something")
        self.assertIsNone(retrieved)


class TestScreenStream(unittest.TestCase):

    def setUp(self):
        self.stream = ScreenStream(threshold=5)

    def test_has_screen_changed(self):
        img1 = Image.new("RGB", (100, 100), color="white")
        img2 = Image.new("RGB", (100, 100), color="white")
        img3 = Image.new("RGB", (100, 100), color="white")
        draw = ImageDraw.Draw(img3)
        draw.rectangle([10, 10, 80, 80], fill="black")

        self.assertTrue(self.stream.has_screen_changed(img1))
        self.assertFalse(self.stream.has_screen_changed(img2))
        self.assertTrue(self.stream.has_screen_changed(img3))

    def test_wait_until_stable(self):
        img_white = Image.new("RGB", (100, 100), color="white")
        captures = [img_white, img_white]
        call_count = [0]

        def capture_fn():
            idx = min(call_count[0], len(captures) - 1)
            call_count[0] += 1
            return captures[idx]

        stable_img = self.stream.wait_until_stable(
            capture_fn, max_wait=0.5, poll_interval=0.01
        )
        self.assertIsNotNone(stable_img)
        self.assertGreaterEqual(call_count[0], 2)


class TestPrivacyFilter(unittest.TestCase):

    def setUp(self):
        self.privacy = PrivacyFilter()

    def test_unmodified_image_returns_same_object(self):
        """Unmodified images should return the exact same PIL image object without re-allocation."""
        img = Image.new("RGB", (200, 200), color=(240, 240, 240))
        result = self.privacy.redact_sensitive_data(img)
        self.assertIs(
            result,
            img,
            "PrivacyFilter should return same image object when unmodified",
        )

    def test_redact_sensitive_data_structure(self):
        """Verify PrivacyFilter handles images correctly and returns a PIL Image."""
        img = Image.new("RGB", (500, 500), color=(240, 240, 240))
        result = self.privacy.redact_sensitive_data(img)
        self.assertIsInstance(result, Image.Image)


if __name__ == "__main__":
    unittest.main()
