import os
import json
import pytest
from unittest.mock import MagicMock
import database
from ai_engine import AIEngine

TEST_DB = "test_ai_cache.db"


@pytest.fixture(autouse=True)
def patch_db_path(monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", TEST_DB)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_ai_engine_uses_cached_answer_for_text_only():
    user_intent = "Bonjour agent"
    cached_payload = json.dumps({"action": "none", "text": "Bonjour! Comment puis-je vous aider?"})
    database.save_answer(user_intent, cached_payload, db_path=TEST_DB)

    mock_client = MagicMock()
    engine = AIEngine(gemini_client=mock_client)

    result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=user_intent)

    assert result == json.loads(cached_payload)
    mock_client.models.generate_content.assert_not_called()
