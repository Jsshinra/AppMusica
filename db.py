import sqlite3
import datetime
import os

DB_FILE = "history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            original_text TEXT,
            parsed_query TEXT,
            url_played TEXT,
            success BOOLEAN
        )
    ''')
    conn.commit()
    conn.close()

def log_history(original_text, parsed_query, url_played, success):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''
            INSERT INTO history (timestamp, original_text, parsed_query, url_played, success)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.datetime.now().isoformat(), original_text, parsed_query, url_played, success))
        conn.commit()
        conn.close()
    except Exception as e:
        import logging
        logging.error(f"Error logging to DB: {e}")

def get_recent_history(limit=10):
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # Group by query to avoid duplicates in the UI
        c.execute('''
            SELECT parsed_query, url_played, timestamp 
            FROM history 
            WHERE url_played != "" AND url_played IS NOT NULL
            GROUP BY parsed_query
            ORDER BY id DESC LIMIT ?
        ''', (limit,))
        rows = c.fetchall()
        conn.close()
        return rows
    except Exception as e:
        return []
