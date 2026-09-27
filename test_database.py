import os
import sqlite3
import tempfile
import pytest

from database import get_cached_answer, save_answer, _ensure_db_init


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_save_and_get_cached_answer(temp_db):
    user_intent = "Open settings menu"
    response = '{"action": "click", "x": 100, "y": 200, "text": "Click settings"}'

    save_answer(user_intent, response, db_path=temp_db)
    cached = get_cached_answer(user_intent, db_path=temp_db)

    assert cached == response


def test_update_cached_answer_on_conflict(temp_db):
    user_intent = "Open settings menu"
    initial_response = '{"action": "none", "text": "Wait"}'
    updated_response = '{"action": "click", "x": 50, "y": 50, "text": "Click"}'

    save_answer(user_intent, initial_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == initial_response

    save_answer(user_intent, updated_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == updated_response


def test_sql_injection_prevention(temp_db):
    # Intent containing SQL injection payload intended to drop the table or bypass queries
    sqli_intent = "test'; DROP TABLE answer_cache; --"
    payload_response = '{"action": "none", "text": "Safe"}'

    save_answer(sqli_intent, payload_response, db_path=temp_db)
    cached = get_cached_answer(sqli_intent, db_path=temp_db)

    assert cached == payload_response

    # Verify that the table was not dropped
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache'")
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == "answer_cache"


def test_sql_injection_boolean_payload(temp_db):
    save_answer("intent_1", "response_1", db_path=temp_db)
    save_answer("intent_2", "response_2", db_path=temp_db)

    # Attempting SQL injection OR 1=1 boolean bypass
    sqli_intent = "' OR 1=1 --"
    cached = get_cached_answer(sqli_intent, db_path=temp_db)

    # Should return None because "' OR 1=1 --" is matched as a literal string, not evaluated as SQL
    assert cached is None
