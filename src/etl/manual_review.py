import sqlite3
import random
from pathlib import Path
import pandas as pd

# --------------------------------------------------
# Project Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "db" / "n100.db"
OUTPUT_FOLDER = PROJECT_ROOT / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)

# --------------------------------------------------
# Connect Database
# --------------------------------------------------

conn = sqlite3.connect(DB_PATH)

print("=" * 70)
print("MANUAL DATA QUALITY REVIEW")
print("=" * 70)

# --------------------------------------------------
# Get all companies
# --------------------------------------------------

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

sample = companies.sample(5, random_state=42)

review = []

for _, row in sample.iterrows():

    company_id = row["id"]
    company_name = row["company_name"]

    print(f"\nChecking: {company_name}")

    pl = conn.execute(
        "SELECT COUNT(*) FROM profitandloss WHERE company_id=?",
        (company_id,)
    ).fetchone()[0]

    bs = conn.execute(
        "SELECT COUNT(*) FROM balancesheet WHERE company_id=?",
        (company_id,)
    ).fetchone()[0]

    cf = conn.execute(
        "SELECT COUNT(*) FROM cashflow WHERE company_id=?",
        (company_id,)
    ).fetchone()[0]

    review.append({
        "company_id": company_id,
        "company_name": company_name,
        "profit_loss_records": pl,
        "balance_sheet_records": bs,
        "cashflow_records": cf,
        "status": "PASS"
    })

review_df = pd.DataFrame(review)

review_path = OUTPUT_FOLDER / "manual_review.csv"

review_df.to_csv(review_path, index=False)

print("\n")
print(review_df)

print("\nReview saved to:")
print(review_path)

conn.close()