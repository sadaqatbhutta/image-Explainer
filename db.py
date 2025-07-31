import sqlite3
import json
import os
from datetime import datetime

DB_NAME = "image_data.db"
JSON_FILE = "results.json"

# Create DB table if not exists
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS image_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT NOT NULL,
            description TEXT,
            timestamp TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Save record in both SQLite and JSON
def save_analysis(filename, description):
    timestamp = datetime.now().isoformat()

    # Save to SQLite
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO image_analysis (filename, description, timestamp)
        VALUES (?, ?, ?)
    ''', (filename, description, timestamp))
    conn.commit()
    conn.close()

    # Save to JSON
    record = {"filename": filename, "description": description, "timestamp": timestamp}
    data = []

    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = []

    data.append(record)
    with open(JSON_FILE, "w") as f:
        json.dump(data, f, indent=4)

# Get all analyses
def get_all_analyses():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT id, filename, description, timestamp FROM image_analysis ORDER BY timestamp DESC')
    rows = cursor.fetchall()
    conn.close()
    return rows

# Search by filename (partial match)
def search_by_filename(query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, filename, description, timestamp
        FROM image_analysis
        WHERE filename LIKE ?
        ORDER BY timestamp DESC
    ''', (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()
    return rows
