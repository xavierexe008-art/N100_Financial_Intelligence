import sqlite3
from pathlib import Path
import pandas as pd

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "n100.db"
OUTPUT_FOLDER = PROJECT_ROOT / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)

# ----------------------------------------------------
# Connect to database
# ----------------------------------------------------

conn = sqlite3.connect(DB_PATH)

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "stock_prices",
    "financial_ratios",
    "market_cap",
    "peer_groups"
]

audit = []

print("=" * 70)
print("LOAD AUDIT")
print("=" * 70)

for table in tables:

    cursor = conn.execute(f"SELECT COUNT(*) FROM {table}")
    rows = cursor.fetchone()[0]

    print(f"{table:20} {rows}")

    audit.append({
        "table_name": table,
        "rows_loaded": rows,
        "status": "SUCCESS",
        "rejected_rows": 0
    })

conn.close()

audit_df = pd.DataFrame(audit)

audit_path = OUTPUT_FOLDER / "load_audit.csv"

audit_df.to_csv(audit_path, index=False)

print("\n" + "=" * 70)
print("Audit file saved:")
print(audit_path)
print("=" * 70)