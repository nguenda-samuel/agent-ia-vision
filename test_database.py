import os
import sqlite3
import pytest

import database


@pytest.fixture(autouse=True)
def cleanup_db():
    if os.path.exists(database.DB_PATH):
        os.remove(database.DB_PATH)
    yield
    if os.path.exists(database.DB_PATH):
        os.remove(database.DB_PATH)


def test_save_and_get_cached_answer():
    intent = "open settings"
    response = '{"action": "click", "x": 100, "y": 200, "text": "Opening settings"}'

    database.save_answer(intent, response)
    cached = database.get_cached_answer(intent)

    assert cached == response


def test_update_cached_answer():
    intent = "open settings"
    initial_response = "initial"
    updated_response = "updated"

    database.save_answer(intent, initial_response)
    database.save_answer(intent, updated_response)

    cached = database.get_cached_answer(intent)
    assert cached == updated_response


def test_sql_injection_protection():
    # Attempt SQL injection payloads as user_intent
    sqli_intent = "' OR '1'='1"
    response = "safe_response"

    database.save_answer(sqli_intent, response)

    # Verify query for a different intent returns None, not all rows
    assert database.get_cached_answer("normal_intent") is None
    # Verify exact match retrieves the response safely
    assert database.get_cached_answer(sqli_intent) == response

    # Drop table attempt payload
    drop_intent = "test'; DROP TABLE cache; --"
    database.save_answer(drop_intent, "drop_test")
    assert database.get_cached_answer(drop_intent) == "drop_test"

    # Verify cache table still exists
    with sqlite3.connect(database.DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cache'")
        assert cursor.fetchone() is not None
