import pandas as pd
from database import get_connection

conn = get_connection()

query = """
SELECT
    company_id,
    year,
    sales,
    net_profit
FROM profitandloss
"""

df = pd.read_sql(query, conn)
conn.close()

# Convert to numbers
df["sales"] = pd.to_numeric(df["sales"], errors="coerce")
df["net_profit"] = pd.to_numeric(df["net_profit"], errors="coerce")

# Sort by company and year
df = df.sort_values(["company_id", "year"])

# Sales Growth %
df["sales_growth"] = (
    df.groupby("company_id")["sales"]
      .pct_change() * 100
)

# Profit Growth %
df["profit_growth"] = (
    df.groupby("company_id")["net_profit"]
      .pct_change() * 100
)

df = df.round(2)

print("=" * 70)
print("GROWTH ANALYSIS")
print("=" * 70)
print(df.head(20))

df.to_csv("growth_analysis.csv", index=False)

print("\nSaved: growth_analysis.csv")