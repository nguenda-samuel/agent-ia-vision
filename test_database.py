import os
import sqlite3
import tempfile
import json
import pytest
import database
from database import get_cached_answer, save_answer
from ai_engine import AIEngine


@pytest.fixture
def temp_db(monkeypatch):
    """Creates a temporary database file for isolated testing."""
    db_fd, db_path = tempfile.mkstemp(suffix=".db")
    os.close(db_fd)
    monkeypatch.setattr(database, "DEFAULT_DB_PATH", db_path)
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)


def test_cache_miss(temp_db):
    assert get_cached_answer("non_existent_intent", db_path=temp_db) is None


def test_cache_save_and_hit(temp_db):
    intent = "Ouvrir le navigateur"
    answer = '{"action": "click", "x": 100, "y": 200, "text": "Ouverture"}'

    save_answer(intent, answer, db_path=temp_db)
    cached = get_cached_answer(intent, db_path=temp_db)

    assert cached == answer


def test_sql_injection_resilience(temp_db):
    # Intent trying SQL injection attack
    sql_injection_payload = "'; DROP TABLE cache; --"
    answer = '{"action": "none", "text": "Safe"}'

    save_answer(sql_injection_payload, answer, db_path=temp_db)

    # Verify table was not dropped and payload is retrieved safely as literal string
    cached = get_cached_answer(sql_injection_payload, db_path=temp_db)
    assert cached == answer

    # Verify cache table still exists in SQLite
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cache'")
        assert cursor.fetchone() is not None


def test_ai_engine_cache_integration(temp_db):
    # Test that AIEngine directly uses database module for caching
    intent = "Demande textuelle"
    expected_response = {"action": "none", "text": "Reponse en cache"}
    save_answer(intent, json.dumps(expected_response), db_path=temp_db)

    class DummyClient:
        pass

    engine = AIEngine(gemini_client=DummyClient())
    result = engine.process_screen_and_intent(raw_screenshot=None, user_intent=intent)

    assert result == expected_response
