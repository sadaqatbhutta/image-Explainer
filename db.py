import sqlite3
from datetime import datetime

DB_NAME = "image_data.db"

def create_analysis_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            description TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_names_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS names (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            source_filename TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def create_search_logs_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            search_term TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    create_analysis_table()
    create_names_table()
    create_search_logs_table()

def save_analysis(filename, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO analysis (filename, description, timestamp)
        VALUES (?, ?, ?)
    ''', (filename, description, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def search_analysis(filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT description FROM analysis WHERE filename=?', (filename,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

def save_names(names, source_filename):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().isoformat()
    for name in names:
        clean = name.strip()
        if clean:
            cursor.execute('''
                INSERT INTO names (name, source_filename, timestamp)
                VALUES (?, ?, ?)
            ''', (clean, source_filename, timestamp))
    conn.commit()
    conn.close()

def search_name(name_query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT name, source_filename, timestamp
        FROM names
        WHERE LOWER(name) LIKE LOWER(?)
    ''', (f"%{name_query}%",))
    results = cursor.fetchall()
    conn.close()
    return results

def log_search(session_id, search_term):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO search_logs (session_id, search_term, timestamp)
        VALUES (?, ?, ?)
    ''', (session_id, search_term, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_search_counts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT search_term, COUNT(*) as total
        FROM search_logs
        GROUP BY search_term
        ORDER BY total DESC
    ''')
    results = cursor.fetchall()
    conn.close()
    return results