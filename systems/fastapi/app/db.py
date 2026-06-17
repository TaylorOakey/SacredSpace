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

def init_sigil_tables():
    """Create sigil_history and sigil_profile tables if they don't exist."""
    conn = get_sqlite()
    conn.execute("""CREATE TABLE IF NOT EXISTS sigil_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        dimension TEXT,
        result_count INTEGER DEFAULT 0,
        source TEXT DEFAULT 'api',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""CREATE TABLE IF NOT EXISTS sigil_profile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT UNIQUE NOT NULL,
        value INTEGER DEFAULT 0,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.execute("""INSERT OR IGNORE INTO sigil_profile (key, value) VALUES
        ('resonance', 50), ('xp', 0), ('insight', 0), ('level', 1),
        ('queries_cast', 0), ('spells_cast', 0)
    """)
    conn.execute("""CREATE TABLE IF NOT EXISTS sigil_macros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        composition TEXT NOT NULL,
        description TEXT DEFAULT '',
        agent TEXT DEFAULT 'CUSTOM',
        active INTEGER DEFAULT 1,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()
    conn.close()
    return True


def get_chroma_client():
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        return client
    except Exception as e:
        return None
