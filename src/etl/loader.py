import pandas as pd
from pathlib import Path

RAW_DATA_PATH = Path(r"C:\Users\ghosh\PycharmProjects\N100_Financial_Intelligence\data\raw")

print("=" * 70)
print("N100 DATASET AUDIT")
print("=" * 70)

summary = []

for file in sorted(RAW_DATA_PATH.glob("*.xlsx")):
    try:
        df = pd.read_excel(file)

        rows = len(df)
        cols = len(df.columns)

        summary.append([file.name, rows, cols])

        print(f"\n{file.name}")
        print(f"Rows: {rows}")
        print(f"Columns: {cols}")

    except Exception as e:
        print(f"\nERROR: {file.name}")
        print(e)

print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)

for item in summary:
    print(f"{item[0]:25} Rows={item[1]:6}  Columns={item[2]}")

print("\nDataset Scan Complete")