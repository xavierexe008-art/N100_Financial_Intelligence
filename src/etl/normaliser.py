import re


def normalize_year(year):
    """
    Convert year values to integer format.
    Example: '2023', '2023.0' -> 2023
    """

    try:
        return int(float(year))
    except:
        return None


def normalize_ticker(ticker):
    """
    Standardize ticker symbols.
    """

    if ticker is None:
        return None

    return str(ticker).strip().upper()


def normalize_company_name(name):
    """
    Standardize company names.
    """

    if name is None:
        return None

    name = str(name).strip()

    # remove extra spaces
    name = re.sub(r"\s+", " ", name)

    return name.title()


if __name__ == "__main__":

    print(normalize_year("2023"))
    print(normalize_year("2023.0"))

    print(normalize_ticker(" tcs "))
    print(normalize_ticker("reliance"))

    print(normalize_company_name("   tata   consultancy services "))