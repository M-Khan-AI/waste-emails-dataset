
import csv

CSV_FILE = "emails_labeled.csv"

REQUIRED_COLUMNS = {"email_id", "email_text", "category"}

ALLOWED_CATEGORIES = {
    "Missed Pickup",
    "Schedule Change",
    "Complaint",
    "Other",
}


def validate_csv():
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            columns = set(reader.fieldnames or [])
            missing_columns = REQUIRED_COLUMNS - columns

            if missing_columns:
                print("Missing columns:", sorted(missing_columns))
                return False

            rows = list(reader)

        if len(rows) < 200:
            print(f"Error: Only {len(rows)} rows found. Need at least 200.")
            return False

        categories = {row["category"].strip() for row in rows}

        invalid_categories = categories - ALLOWED_CATEGORIES

        if invalid_categories:
            print("Invalid categories:", sorted(invalid_categories))
            return False

        if categories != ALLOWED_CATEGORIES:
            print("Error: Dataset must contain all four categories.")
            return False

        for number, row in enumerate(rows, start=2):
            if not row["email_text"].strip():
                print(f"Error: Empty email text on CSV line {number}.")
                return False

        print("CSV validation passed!")
        print(f"Total emails: {len(rows)}")
        print("All four required categories are present.")
        return True

    except FileNotFoundError:
        print(f"Error: {CSV_FILE} was not found.")
        return False


if __name__ == "__main__":
    assert validate_csv(), "CSV validation failed."