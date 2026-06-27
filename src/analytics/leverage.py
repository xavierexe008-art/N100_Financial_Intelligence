import pandas as pd
from database import get_connection

conn = get_connection()

query = """
SELECT
    company_id,
    year,
    borrowings,
    reserves,
    equity_capital
FROM balancesheet
"""

df = pd.read_sql(query, conn)
conn.close()

for col in ["borrowings", "reserves", "equity_capital"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Debt to Equity
df["debt_to_equity"] = (
    df["borrowings"] /
    (df["equity_capital"] + df["reserves"])
)

df = df.round(2)

print("=" * 70)
print("LEVERAGE ANALYSIS")
print("=" * 70)
print(df.head(20))

df.to_csv("leverage_analysis.csv", index=False)

print("\nSaved: leverage_analysis.csv")