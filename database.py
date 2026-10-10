import sqlite3

DB_PATH = "cache.db"

def _init_db(conn):
    conn.execute("CREATE TABLE IF NOT EXISTS answer_cache (user_intent TEXT UNIQUE, cached_response TEXT)")

def get_cached_answer(user_intent: str, db_path: str = DB_PATH) -> str | None:
    try:
        with sqlite3.connect(db_path) as conn:
            _init_db(conn)
            cursor = conn.execute("SELECT cached_response FROM answer_cache WHERE user_intent = ?", (user_intent,))
            row = cursor.fetchone()
            return row[0] if row else None
    except sqlite3.Error:
        return None

def save_answer(user_intent: str, cached_response: str, db_path: str = DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            _init_db(conn)
            conn.execute("INSERT OR REPLACE INTO answer_cache (user_intent, cached_response) VALUES (?, ?)", (user_intent, cached_response))
            conn.commit()
    except sqlite3.Error:
        pass
