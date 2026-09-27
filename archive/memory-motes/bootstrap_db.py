"""Bootstrap the SacredSpace SQLite database"""
import sqlite3, pathlib

DB = pathlib.Path("D:/SacredSpace_OS/archive/memory-motes/sacred.db")
SQL = pathlib.Path("D:/SacredSpace_OS/archive/memory-motes/schema.sql")
DB.parent.mkdir(parents=True, exist_ok=True)
conn = sqlite3.connect(DB)
conn.executescript(SQL.read_text())
conn.commit(); conn.close()
print("∆∆∆ sacred.db bootstrapped ∆∆∆")
