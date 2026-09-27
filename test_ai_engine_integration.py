import json
from unittest.mock import MagicMock
import pytest

import ai_engine
import database
from database import get_cached_answer, save_answer


def test_ai_engine_uses_database_cache(tmp_path, monkeypatch):
    db_file = str(tmp_path / "test_cache.db")

    def mock_get_cached_answer(user_intent):
        return get_cached_answer(user_intent, db_path=db_file)

    def mock_save_answer(user_intent, cached_response):
        save_answer(user_intent, cached_response, db_path=db_file)

    monkeypatch.setattr(ai_engine, "get_cached_answer", mock_get_cached_answer)
    monkeypatch.setattr(ai_engine, "save_answer", mock_save_answer)

    user_intent = "open browser"
    cached_payload = json.dumps({"action": "none", "text": "Opening browser"})

    save_answer(user_intent, cached_payload, db_path=db_file)

    mock_client = MagicMock()
    engine = ai_engine.AIEngine(gemini_client=mock_client)

    result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

    assert result == {"action": "none", "text": "Opening browser"}
    # Verify gemini generate_content was not called because cache hit occurred
    mock_client.models.generate_content.assert_not_called()
