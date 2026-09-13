import json
import os
import sqlite3
import pytest
from memory import ActionMemory, MAX_HASH_LENGTH, MAX_INTENT_LENGTH


@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_agent_memory.db"
    return str(db_file)


def test_init_db(temp_db):
    memory = ActionMemory(db_path=temp_db)
    assert os.path.exists(temp_db)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='routines';")
        table = cursor.fetchone()
        assert table is not None
        assert table[0] == "routines"


def test_save_routine_parameterized(temp_db):
    memory = ActionMemory(db_path=temp_db)

    screen_hash = "hash_123"
    # SQL injection payload in user intent
    user_intent = "test_intent'; DROP TABLE routines; --"
    action_data = {"action": "click", "x": 100, "y": 200}

    memory.save_routine(screen_hash, user_intent, action_data)

    with sqlite3.connect(temp_db) as conn:
        cursor = conn.cursor()
        # Verify routines table still exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='routines';")
        assert cursor.fetchone() is not None

        # Verify entry saved correctly without SQL injection execution
        cursor.execute("SELECT screen_hash, user_intent, action_data FROM routines WHERE screen_hash = ?", (screen_hash,))
        row = cursor.fetchone()
        assert row is not None
        assert row[0] == screen_hash
        assert row[1] == user_intent
        assert json.loads(row[2]) == action_data


def test_input_validation_type_errors(temp_db):
    memory = ActionMemory(db_path=temp_db)

    with pytest.raises(TypeError):
        memory.save_routine(123, "intent", {"action": "none"})

    with pytest.raises(TypeError):
        memory.save_routine("hash", None, {"action": "none"})

    with pytest.raises(TypeError):
        memory.save_routine("hash", "intent", ["not", "a", "dict"])

    with pytest.raises(TypeError):
        memory.get_routine(123, "intent")


def test_input_validation_length_limits(temp_db):
    memory = ActionMemory(db_path=temp_db)

    long_hash = "a" * (MAX_HASH_LENGTH + 1)
    long_intent = "b" * (MAX_INTENT_LENGTH + 1)

    with pytest.raises(ValueError):
        memory.save_routine(long_hash, "intent", {"action": "none"})

    with pytest.raises(ValueError):
        memory.save_routine("hash", long_intent, {"action": "none"})

    assert memory.get_routine(long_hash, "intent") is None
    assert memory.get_routine("hash", long_intent) is None
