import os
import tempfile
import pytest
import sqlite3
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

    save_answer(user_intent, cached_response, db_path=temp_db)
    result = get_cached_answer(user_intent, db_path=temp_db)

    assert result == cached_response


def test_get_nonexistent_answer(temp_db):
    result = get_cached_answer("Nonexistent intent", db_path=temp_db)
    assert result is None


def test_update_existing_cached_answer(temp_db):
    user_intent = "Open browser"
    first_response = '{"action": "wait", "text": "Please wait"}'
    second_response = '{"action": "click", "text": "Clicked"}'

    save_answer(user_intent, first_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == first_response

    save_answer(user_intent, second_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == second_response


def test_sql_injection_prevention(temp_db):
    injection_intent = "test' OR '1'='1"
    injection_response = "injected_response"

    save_answer(injection_intent, injection_response, db_path=temp_db)

    # Check that normal query returns None for a different string
    assert get_cached_answer("test", db_path=temp_db) is None
    # Check that exact injection string query returns only its assigned response
    assert get_cached_answer(injection_intent, db_path=temp_db) == injection_response

    # Verify only 1 row was inserted in database
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM answer_cache")
        count = cursor.fetchone()[0]
        assert count == 1
