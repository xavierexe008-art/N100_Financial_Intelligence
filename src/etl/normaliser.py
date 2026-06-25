import pandas as pd


def normalize_year(value):
    """
    Convert year values into integer format.
    """

    if pd.isna(value):
        return None

    try:
        return int(float(value))
    except:
        return None


def normalize_ticker(value):
    """
    Clean ticker/company names.
    """

    if pd.isna(value):
        return None

    return str(value).strip().upper()