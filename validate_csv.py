
import csv
from pathlib import Path

# CSV file is in the same folder as this script
CSV_FILE = Path(__file__).with_name("emails_labeled.csv")

# Required column headings
REQUIRED_COLUMNS = [
    "email_id",
    "subject",
    "body",
    "category"
]

# Exactly four allowed category labels
EXPECTED_CATEGORIES = {
    "Missed Pickup",
    "Schedule Change",
    "Complaint",
    "Other"
}


def validate_csv():

    # Check that the CSV file exists
    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"CSV file not found: {CSV_FILE}"
        )

    # Read the CSV file
    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        # Check required columns
        columns = reader.fieldnames or []

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in columns
        ]

        if missing_columns:
            raise AssertionError(
                f"Missing required fields: {missing_columns}"
            )

        # Read all rows
        rows = list(reader)

    # Check minimum number of rows
    if len(rows) < 200:
        raise AssertionError(
            f"Dataset contains only {len(rows)} rows. "
            "At least 200 rows are required."
        )

    # Get all category labels
    categories = {
        row["category"].strip()
        for row in rows
        if row["category"]
    }

    # Check exactly four category labels
    if categories != EXPECTED_CATEGORIES:
        raise AssertionError(
            "Category labels are incorrect.\n"
            f"Expected: {sorted(EXPECTED_CATEGORIES)}\n"
            f"Found: {sorted(categories)}"
        )

    # Check for empty required fields
    empty_fields = []

    for row_number, row in enumerate(rows, start=2):
        for column in REQUIRED_COLUMNS:
            if not row[column].strip():
                empty_fields.append(
                    f"Row {row_number}: {column}"
                )

    if empty_fields:
        raise AssertionError(
            "Empty required fields found:\n"
            + "\n".join(empty_fields)
        )

    # Everything passed
    print("CSV validation passed!")
    print(f"Rows: {len(rows)}")
    print(f"Columns: {columns}")
    print(f"Categories: {sorted(categories)}")


if __name__ == "__main__":
    validate_csv()

