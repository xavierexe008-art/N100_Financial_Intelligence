from pathlib import Path
import pandas as pd
from normaliser import normalize_year, normalize_ticker

# Get project root folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]

RAW_FOLDER = PROJECT_ROOT / "data" / "raw"
PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"

PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

print("Raw Folder:", RAW_FOLDER)
print("Processed Folder:", PROCESSED_FOLDER)

# Create processed folder if it doesn't exist
PROCESSED_FOLDER.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("N100 DATA CLEANING")
print("=" * 70)

for file in RAW_FOLDER.glob("*.xlsx"):
    print(f"\nProcessing {file.name}")

    try:
        df = pd.read_excel(file)

        # Normalize year columns
        for col in df.columns:
            if "year" in col.lower():
                df[col] = df[col].apply(normalize_year)

        # Normalize company/ticker columns
        for col in df.columns:
            col_name = col.lower()

            if (
                "ticker" in col_name
                or "symbol" in col_name
                or "company" in col_name
                or "stock" in col_name
            ):
                df[col] = df[col].apply(normalize_ticker)

        # Save cleaned file
        output_file = PROCESSED_FOLDER / file.name
        df.to_excel(output_file, index=False)

        print(f"✓ Saved -> {output_file.name}")

    except Exception as e:
        print(f"✗ Error in {file.name}")
        print(e)

print("\n" + "=" * 70)
print("ALL FILES CLEANED SUCCESSFULLY")
print("=" * 70)