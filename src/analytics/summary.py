import sqlite3
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_PATH = PROJECT_ROOT / "db" / "n100.db"

conn = sqlite3.connect(DB_PATH)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print("=" * 60)
print("DATABASE SUMMARY")
print("=" * 60)

print("\nTables Found:")
print(tables)

for table in tables["name"]:
    count = pd.read_sql(
        f"SELECT COUNT(*) AS rows FROM {table}",
        conn
    )

    print(f"{table:20} {count.iloc[0,0]} rows")

conn.close()