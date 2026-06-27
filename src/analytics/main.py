import pandas as pd

from database import get_connection

conn = get_connection()

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table';",
    conn
)

print("=" * 60)
print("TABLES IN DATABASE")
print("=" * 60)

print(tables)

conn.close()