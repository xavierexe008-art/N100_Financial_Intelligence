import sqlite3
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Correct database path
DB_PATH = PROJECT_ROOT / "db" / "n100.db"

print("Database Path:", DB_PATH)

def get_connection():
    return sqlite3.connect(DB_PATH)