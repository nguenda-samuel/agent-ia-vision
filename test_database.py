import os
import tempfile
import pytest

from database import get_cached_answer, save_answer, init_db


@pytest.fixture
def temp_db():
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    init_db(db_path)
    yield db_path
    if os.path.exists(db_path):
        os.remove(db_path)


def test_database_cache_miss_returns_none(temp_db):
    assert get_cached_answer("nonexistent intent", db_path=temp_db) is None


def test_database_save_and_get_cached_answer(temp_db):
    intent = "open browser"
    answer = '{"action": "click", "x": 100, "y": 200, "text": "Opening browser"}'

    save_answer(intent, answer, db_path=temp_db)
    cached = get_cached_answer(intent, db_path=temp_db)

    assert cached == answer


def test_database_upsert_answer(temp_db):
    intent = "open browser"
    answer1 = "answer 1"
    answer2 = "answer 2"

    save_answer(intent, answer1, db_path=temp_db)
    save_answer(intent, answer2, db_path=temp_db)

    assert get_cached_answer(intent, db_path=temp_db) == answer2
