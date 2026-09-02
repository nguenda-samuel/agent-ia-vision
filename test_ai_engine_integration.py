from unittest.mock import MagicMock
import pytest
from database import get_cached_answer, save_answer, DB_PATH
from ai_engine import AIEngine


def test_ai_engine_uses_database_cache(monkeypatch):
    # Ensure save_answer writes to default DB_PATH so get_cached_answer inside ai_engine finds it
    save_answer("pure_text_intent", '{"action": "none", "text": "Cached response"}')

    try:
        mock_client = MagicMock()
        engine = AIEngine(gemini_client=mock_client)

        # When raw_screenshot is None, it should fetch from database cache without calling Gemini API
        result = engine.process_screen_and_intent(raw_screenshot=None, user_intent="pure_text_intent")

        assert result == {"action": "none", "text": "Cached response"}
        mock_client.models.generate_content.assert_not_called()
    finally:
        # Cleanup cached response from DB
        import sqlite3
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM answer_cache WHERE user_intent = ?", ("pure_text_intent",))
            conn.commit()
