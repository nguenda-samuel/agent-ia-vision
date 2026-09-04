import os
import sqlite3
import pytest
import database

TEST_DB = "test_cache.db"


@pytest.fixture(autouse=True)
def clean_db():
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    yield
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


def test_save_and_get_cached_answer():
    intent = "clique sur le bouton start"
    answer = '{"action": "click", "x": 100, "y": 200, "text": "Je clique"}'

    database.save_answer(intent, answer, db_path=TEST_DB)
    cached = database.get_cached_answer(intent, db_path=TEST_DB)

    assert cached == answer


def test_sql_injection_prevention():
    # Attempt SQL injection in intent and answer fields
    sqli_intent = "test' OR '1'='1"
    sqli_answer = "malicious_payload'); DROP TABLE cache; --"

    database.save_answer(sqli_intent, sqli_answer, db_path=TEST_DB)

    # Verify query treats input strictly as literal string
    result = database.get_cached_answer(sqli_intent, db_path=TEST_DB)
    assert result == sqli_answer

    # Verify standard query for non-matching string returns None
    assert database.get_cached_answer("normal_intent", db_path=TEST_DB) is None

    # Verify table structure was not altered
    with sqlite3.connect(TEST_DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='cache'")
        assert cursor.fetchone() is not None
