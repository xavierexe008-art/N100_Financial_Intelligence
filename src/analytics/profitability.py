import pandas as pd
from database import get_connection

# -----------------------------------------
# Connect to Database
# -----------------------------------------

conn = get_connection()

query = """
SELECT
    company_id,
    year,
    sales,
    operating_profit,
    net_profit,
    opm_percentage,
    eps
FROM profitandloss
"""

df = pd.read_sql(query, conn)

conn.close()

# -----------------------------------------
# Convert numeric columns
# -----------------------------------------

numeric_cols = [
    "sales",
    "operating_profit",
    "net_profit",
    "opm_percentage",
    "eps"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# -----------------------------------------
# Calculate KPIs
# -----------------------------------------

# Net Profit Margin
df["net_profit_margin"] = (
    df["net_profit"] / df["sales"]
) * 100

# Operating Profit Margin
df["operating_margin"] = (
    df["operating_profit"] / df["sales"]
) * 100

# EPS Growth %
df["eps_growth"] = (
    df.groupby("company_id")["eps"]
      .pct_change() * 100
)

# Net Profit Growth %
df["profit_growth"] = (
    df.groupby("company_id")["net_profit"]
      .pct_change() * 100
)

# -----------------------------------------
# Round values
# -----------------------------------------

df = df.round(2)

# -----------------------------------------
# Display Result
# -----------------------------------------

print("=" * 80)
print("PROFITABILITY KPI ENGINE")
print("=" * 80)

print(df.head(20))

# -----------------------------------------
# Save Output
# -----------------------------------------

df.to_csv("profitability_kpis.csv", index=False)

print("\nSaved: profitability_kpis.csv")