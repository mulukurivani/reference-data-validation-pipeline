
import csv
import logging
from pathlib import Path
from datetime import datetime
from uuid import uuid4

# Project folder paths
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input.csv"
REFERENCE_FILE = BASE_DIR / "data" / "reference.csv"
OUTPUT_DIR = BASE_DIR / "output"

VALID_FILE = OUTPUT_DIR / "valid_records.csv"
REJECT_FILE = OUTPUT_DIR / "rejected_records.csv"
REPORT_FILE = OUTPUT_DIR / "summary.txt"

# Create output folder
OUTPUT_DIR.mkdir(exist_ok=True)

# Logging setup
logging.basicConfig(
    filename=OUTPUT_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def read_csv(file_path):
    with open(file_path, "r", newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def validate_record(row, reference_data, seen_ids):

    reasons = []

    record_id = row.get("record_id", "").strip()
    code = row.get("code", "").strip()
    date_text = row.get("effective_date", "").strip()
    version = row.get("reference_version", "").strip()

    # Check required fields
    if not all([record_id, code, date_text, version]):
        reasons.append("Missing required field")
        return reasons

    # Check duplicate records
    if record_id in seen_ids:
        reasons.append("Duplicate record ID")
    else:
        seen_ids.add(record_id)

    # Check date format
    try:
        effective_date = datetime.strptime(
            date_text, "%Y-%m-%d"
        ).date()
    except ValueError:
        reasons.append("Invalid date format")
        return reasons

    # Find matching code
    code_matches = [
        ref for ref in reference_data
        if ref["code"].strip() == code
    ]

    if not code_matches:
        reasons.append("Unknown code")
        return reasons

    # Check reference version
    version_matches = [
        ref for ref in code_matches
        if ref["version"].strip() == version
    ]

    if not version_matches:
        reasons.append("Reference version not found")
        return reasons

    # Check effective dates
    valid_reference = None

    for ref in version_matches:
        start = datetime.strptime(
            ref["valid_from"], "%Y-%m-%d"
        ).date()

        end = datetime.strptime(
            ref["valid_to"], "%Y-%m-%d"
        ).date()

        if start <= effective_date <= end:
            valid_reference = ref
            break

    if valid_reference is None:
        reasons.append("Code outside effective date range")
        return reasons

    # Check deprecated codes
    if valid_reference["status"].strip().lower() != "active":
        reasons.append("Deprecated code")

    return reasons


def main():

    run_id = str(uuid4())

    logging.info("Pipeline started: %s", run_id)
    if not INPUT_FILE.exists():
        print("Error: input.csv file not found.")
        logging.error("Input file not found")
        return

    if not REFERENCE_FILE.exists():
        print("Error: reference.csv file not found.")
        logging.error("Reference file not found")
        return
    input_data = read_csv(INPUT_FILE)
    if not input_data:
        print("Input file is empty. No records to process.")
        logging.warning("Input file is empty")
        return
    reference_data = read_csv(REFERENCE_FILE)

    valid_records = []
    rejected_records = []
    seen_ids = set()

    for row in input_data:

        reasons = validate_record(
            row, reference_data, seen_ids
        )

        result = row.copy()

        if reasons:
            result["rejection_reason"] = "; ".join(reasons)
            rejected_records.append(result)
        else:
            result["rejection_reason"] = ""
            valid_records.append(result)

    # Save valid records
    fields = list(input_data[0].keys()) + ["rejection_reason"]

    def save_csv(file_path, records):
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(records)

    save_csv(VALID_FILE, valid_records)
    save_csv(REJECT_FILE, rejected_records)

    # Generate summary report
    total = len(input_data)
    valid = len(valid_records)
    rejected = len(rejected_records)

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        file.write("REFERENCE DATA VALIDATION REPORT\n")
        file.write("--------------------------------\n")
        file.write(f"Run ID: {run_id}\n")
        file.write(f"Total records: {total}\n")
        file.write(f"Valid records: {valid}\n")
        file.write(f"Rejected records: {rejected}\n")

    logging.info(
        "Pipeline completed. Total=%d Valid=%d Rejected=%d",
        total, valid, rejected
    )

    print("Pipeline completed successfully!")
    print("Total records:", total)
    print("Valid records:", valid)
    print("Rejected records:", rejected)
    print("Check the output folder for results.")


if __name__ == "__main__":
    main()
