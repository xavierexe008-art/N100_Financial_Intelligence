import sqlite3
import traceback
from pathlib import Path

import pandas as pd

# --------------------------------------------------
# Project Paths
# --------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_FOLDER = PROJECT_ROOT / "data" / "processed"
DB_PATH = PROJECT_ROOT / "db" / "n100.db"

# --------------------------------------------------
# Files that have headers on the second row
# --------------------------------------------------
CORE_FILES = {
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx"
}

FILES = [
    "companies.xlsx",
    "profitandloss.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx"
]

print("=" * 70)
print("LOADING DATA INTO SQLITE DATABASE")
print("=" * 70)

# --------------------------------------------------
# Connect to SQLite
# --------------------------------------------------
conn = sqlite3.connect(DB_PATH)

for filename in FILES:

    file_path = DATA_FOLDER / filename

    if not file_path.exists():
        print(f"\n❌ File not found: {filename}")
        continue

    print("\n" + "=" * 70)
    print(f"Loading {filename}")
    print("=" * 70)

    try:

        # Read Excel
        if filename in CORE_FILES:
            df = pd.read_excel(file_path, header=1)
        else:
            df = pd.read_excel(file_path, header=0)

        # Clean column names
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.replace(" ", "_", regex=False)
            .str.replace("-", "_", regex=False)
            .str.replace("%", "pct", regex=False)
            .str.replace("/", "_", regex=False)
            .str.replace("(", "", regex=False)
            .str.replace(")", "", regex=False)
        )

        table_name = file_path.stem

        print(f"Table   : {table_name}")
        print(f"Rows    : {len(df)}")
        print(f"Columns : {len(df.columns)}")
        print("Column Names:")
        print(df.columns.tolist())

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

        print("✅ Loaded Successfully")

    except Exception as e:

        print("\n" + "=" * 70)
        print("❌ ERROR OCCURRED")
        print("=" * 70)

        print(f"File : {filename}")
        print(f"Table: {table_name}")

        print("\nException Type:")
        print(type(e).__name__)

        print("\nException Message:")
        print(e)

        print("\nFull Traceback:")
        traceback.print_exc()

        conn.close()
        raise

conn.commit()
conn.close()

print("\n" + "=" * 70)
print("🎉 ALL DATA LOADED SUCCESSFULLY")
print("=" * 70)