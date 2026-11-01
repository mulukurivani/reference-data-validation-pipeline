# Versioned Reference Data Validation Pipeline

## Project Overview
This project is a Python-based data validation pipeline that validates incoming records against versioned reference data.

It checks whether codes are valid, active, and within their effective date ranges.

## Features
- Reads input and reference CSV files.
- Validates required fields.
- Detects duplicate record IDs.
- Identifies unknown and deprecated codes.
- Checks reference versions.
- Validates effective date ranges.
- Generates valid and rejected CSV files.
- Creates a summary report.
- Maintains pipeline execution logs.
- Handles missing and empty input files.

## Project Structure
```text
reference_data_pipeline/
│
├── data/
│   ├── input.csv
│   └── reference.csv
│
├── output/
├── tests/
│   └── test_pipeline.py
│
├── main.py
├── README.md
└── requirements.txt
```

## Technologies Used
- Python
- CSV
- Logging
- Unittest

## How to Run

1. Clone or download the repository.
2. Open the project folder in VS Code.
3. Run:

```bash
python main.py
```

## Run Automated Tests

```bash
python -m unittest discover -s tests -v
```

## Output Files
- `valid_records.csv` – Valid records.
- `rejected_records.csv` – Rejected records with reasons.
- `summary.txt` – Validation summary.
- `pipeline.log` – Execution logs.

## Test Results
All 9 automated tests passed successfully.

## Author
Mulukuri Vani