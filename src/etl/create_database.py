import sqlite3
from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Database paths
DB_FOLDER = PROJECT_ROOT / "db"
DB_PATH = DB_FOLDER / "n100.db"
SCHEMA_PATH = DB_FOLDER / "schema.sql"

print("=" * 60)
print("CREATING N100 DATABASE")
print("=" * 60)

# Connect to SQLite
connection = sqlite3.connect(DB_PATH)

# Read schema.sql
with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = f.read()

# Execute schema
connection.executescript(schema)

connection.commit()
connection.close()

print("\nDatabase created successfully!")
print(f"Location: {DB_PATH}")