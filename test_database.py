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
    cached_response = '{"action": "click", "x": 100, "y": 200}'

    # First fetch should return None
    assert get_cached_answer(user_intent, db_path=temp_db) is None

    # Save answer
    save_answer(user_intent, cached_response, db_path=temp_db)

    # Retrieve answer
    retrieved = get_cached_answer(user_intent, db_path=temp_db)
    assert retrieved == cached_response


def test_update_existing_cached_answer(temp_db):
    user_intent = "Open settings menu"
    first_response = '{"action": "wait"}'
    updated_response = '{"action": "click", "x": 50, "y": 50}'

    save_answer(user_intent, first_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == first_response

    # Update on conflict
    save_answer(user_intent, updated_response, db_path=temp_db)
    assert get_cached_answer(user_intent, db_path=temp_db) == updated_response


def test_sql_injection_prevention(temp_db):
    # Craft malicious SQL injection payloads
    sql_injection_intent = "test' OR '1'='1"
    malicious_payload = "'; DROP TABLE answer_cache; --"
    fake_response = '{"action": "none"}'

    # Save with payload as key and content
    save_answer(sql_injection_intent, fake_response, db_path=temp_db)
    save_answer("normal_intent", malicious_payload, db_path=temp_db)

    # Verify table answer_cache still exists and contains expected data
    assert get_cached_answer(sql_injection_intent, db_path=temp_db) == fake_response
    assert get_cached_answer("normal_intent", db_path=temp_db) == malicious_payload

    # Ensure another key returns None and table was not wiped or bypassed
    assert get_cached_answer("non_existent_key", db_path=temp_db) is None

    # Verify DB table integrity
    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM answer_cache")
        count = cursor.fetchone()[0]
        assert count == 2


def test_error_redaction_pattern():
    import re
    raw_error = "API Error: https://generativelanguage.googleapis.com/v1beta/models?key=AIzaSyA1b2C3d4E5f6G7h8I9j0K1L2M3N4O5P6"
    safe_err = re.sub(r'key=[A-Za-z0-9_\-]+', 'key=[REDACTED]', raw_error)
    safe_err = re.sub(r'AIza[0-9A-Za-z-_]{35}', '[REDACTED_API_KEY]', safe_err)

    assert "AIzaSyA1b2C3d4E5f6G7h8I9j0K1L2M3N4O5P6" not in safe_err
    assert "key=[REDACTED]" in safe_err
