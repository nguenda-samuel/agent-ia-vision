import os
import sqlite3
import tempfile
import pytest
from database import get_cached_answer, save_answer


@pytest.fixture
def temp_db():
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    yield path
    if os.path.exists(path):
        os.remove(path)


def test_save_and_get_cached_answer(temp_db):
    user_intent = "Open browser"
    cached_response = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

    assert get_cached_answer(user_intent, db_path=temp_db) is None

    save_answer(user_intent, cached_response, db_path=temp_db)

    retrieved = get_cached_answer(user_intent, db_path=temp_db)
    assert retrieved == cached_response


def test_update_cached_answer(temp_db):
    user_intent = "Open browser"
    first_response = '{"action": "none", "text": "Wait"}'
    second_response = '{"action": "click", "text": "Done"}'

    save_answer(user_intent, first_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == first_response

    save_answer(user_intent, second_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == second_response


def test_sql_injection_prevention(temp_db):
    # Payload designed to attempt SQL injection / table drop if unparameterized
    sql_injection_payload = "test' UNION SELECT sqlite_version() --"
    save_answer(sql_injection_payload, "safe_response", db_path=temp_db)

    result = get_cached_answer(sql_injection_payload, db_path=temp_db)
    assert result == "safe_response"

    # Verify database structure remains intact
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='answer_cache'")
        assert cursor.fetchone() is not None
