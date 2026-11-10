import os
import sqlite3
import tempfile
import unittest

from memory import ActionMemory


class TestActionMemory(unittest.TestCase):

    def setUp(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_db:
            self.db_path = temp_db.name
        self.memory = ActionMemory(db_path=self.db_path)

    def tearDown(self):
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_init_creates_table_and_index(self):
        """Verify that routines table and composite index are created."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='routines'"
            )
            self.assertIsNotNone(cursor.fetchone())

            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='index' AND name='idx_routines_screen_intent'"
            )
            self.assertIsNotNone(cursor.fetchone())

    def test_query_plan_uses_composite_index(self):
        """Verify EXPLAIN QUERY PLAN uses the composite index rather than a table scan."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                EXPLAIN QUERY PLAN
                SELECT action_data FROM routines
                WHERE screen_hash = ? AND user_intent = ?
                ORDER BY id DESC LIMIT 1
                """,
                ("hash123", "click_button"),
            )
            plan = cursor.fetchall()
            plan_str = " ".join([str(step) for step in plan])
            self.assertIn("USING INDEX idx_routines_screen_intent", plan_str)
            self.assertNotIn("SCAN routines", plan_str)

    def test_save_and_get_routine(self):
        """Verify routine saving and retrieval."""
        action_data = {
            "action": "click",
            "x": 100,
            "y": 200,
            "text": "Clicking button",
        }
        self.memory.save_routine("screen_abc", "click submit", action_data)

        retrieved = self.memory.get_routine("screen_abc", "click submit")
        self.assertEqual(retrieved, action_data)

    def test_get_routine_returns_latest(self):
        """Verify retrieving the most recent routine matching screen_hash and user_intent."""
        old_action = {"action": "wait", "text": "waiting"}
        new_action = {"action": "click", "x": 50, "y": 50, "text": "click"}

        self.memory.save_routine("screen_xyz", "submit", old_action)
        self.memory.save_routine("screen_xyz", "submit", new_action)

        retrieved = self.memory.get_routine("screen_xyz", "submit")
        self.assertEqual(retrieved, new_action)

    def test_get_routine_not_found(self):
        """Verify get_routine returns None when no match exists."""
        result = self.memory.get_routine("non_existent_hash", "some intent")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
