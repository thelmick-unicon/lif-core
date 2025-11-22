def convert_csv_to_set(csv: str) -> set[str]:
    """
    Utility function to convert a comma-separated string into a set of strings.
    Trims whitespace around each item, removes duplicates, and ignores empty items.
    """
    return {item.strip() for item in csv.split(",") if item.strip()}
