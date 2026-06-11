"""SacredSpace OS — Database layer (SQLite + ChromaDB)"""

import sqlite3, os
from app.config import SQLITE_PATH, CHROMA_PATH

def get_sqlite():
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    conn = sqlite3.connect(SQLITE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("""CREATE TABLE IF NOT EXISTS memory_motes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        entity TEXT NOT NULL,
        pillar TEXT,
        content TEXT,
        tags TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'raw'
    )""")
    conn.commit()
    return conn

def get_chroma_client():
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        return client
    except Exception as e:
        return None
