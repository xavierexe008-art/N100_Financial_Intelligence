from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parents[2]

PROCESSED_FOLDER = PROJECT_ROOT / "data" / "processed"
OUTPUT_FOLDER = PROJECT_ROOT / "output"

OUTPUT_FOLDER.mkdir(exist_ok=True)

validation_results = []

print("=" * 70)
print("N100 DATA VALIDATION")
print("=" * 70)

for file in PROCESSED_FOLDER.glob("*.xlsx"):

    print(f"\nChecking {file.name}")

    df = pd.read_excel(file)

    # -----------------------------
    # DQ-01 Duplicate Primary Key
    # -----------------------------
    if "id" in df.columns:

        duplicate_ids = df["id"].duplicated().sum()

        if duplicate_ids > 0:
            validation_results.append([
                file.name,
                "DQ-01 Duplicate Primary Key",
                "CRITICAL",
                duplicate_ids
            ])

    # -----------------------------
    # DQ-02 Duplicate Company-Year
    # -----------------------------
    if "company_id" in df.columns and "year" in df.columns:

        duplicate_company_year = df.duplicated(
            subset=["company_id", "year"]
        ).sum()

        if duplicate_company_year > 0:
            validation_results.append([
                file.name,
                "DQ-02 Duplicate Company-Year",
                "CRITICAL",
                duplicate_company_year
            ])

    # -----------------------------
    # DQ-03 Missing Company IDs
    # -----------------------------
    if "company_id" in df.columns:

        missing_company = df["company_id"].isna().sum()

        if missing_company > 0:
            validation_results.append([
                file.name,
                "DQ-03 Missing Company ID",
                "CRITICAL",
                missing_company
            ])

    # -----------------------------
    # DQ-04 Invalid Years
    # -----------------------------
    if "year" in df.columns:

        invalid_year = (
            (df["year"] < 2000) |
            (df["year"] > 2035)
        ).sum()

        if invalid_year > 0:
            validation_results.append([
                file.name,
                "DQ-04 Invalid Year",
                "WARNING",
                invalid_year
            ])

    # -----------------------------
    # DQ-05 Negative Sales
    # -----------------------------
    for col in df.columns:

        if "sales" in col.lower():

            negative_sales = (df[col] < 0).sum()

            if negative_sales > 0:
                validation_results.append([
                    file.name,
                    "DQ-05 Negative Sales",
                    "WARNING",
                    negative_sales
                ])

print("\nValidation Finished")

validation_df = pd.DataFrame(
    validation_results,
    columns=[
        "Dataset",
        "Rule",
        "Severity",
        "Details"
    ]
)

validation_df.to_csv(
    OUTPUT_FOLDER / "validation_failures.csv",
    index=False
)

print("\nSaved:")
print(OUTPUT_FOLDER / "validation_failures.csv")