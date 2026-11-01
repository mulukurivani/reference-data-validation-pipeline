
import unittest
from main import validate_record


class TestPipeline(unittest.TestCase):

    def setUp(self):
        self.reference_data = [
            {
                "code": "IND",
                "status": "active",
                "valid_from": "2025-01-01",
                "valid_to": "2027-12-31",
                "version": "v1"
            },
            {
                "code": "UK",
                "status": "deprecated",
                "valid_from": "2025-01-01",
                "valid_to": "2027-12-31",
                "version": "v1"
            }
        ]

    def test_valid_code(self):
        row = {
            "record_id": "1",
            "code": "IND",
            "effective_date": "2026-01-10",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertEqual(result, [])

    def test_unknown_code(self):
        row = {
            "record_id": "2",
            "code": "XYZ",
            "effective_date": "2026-01-10",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Unknown code", result)

    def test_deprecated_code(self):
        row = {
            "record_id": "3",
            "code": "UK",
            "effective_date": "2026-01-10",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Deprecated code", result)

    def test_duplicate_record(self):
        row = {
            "record_id": "4",
            "code": "IND",
            "effective_date": "2026-01-10",
            "reference_version": "v1"
        }

        seen_ids = {"4"}

        result = validate_record(row, self.reference_data, seen_ids)
        self.assertIn("Duplicate record ID", result)

    def test_missing_field(self):
        row = {
            "record_id": "5",
            "code": "",
            "effective_date": "2026-01-10",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Missing required field", result)

    def test_invalid_date(self):
        row = {
            "record_id": "6",
            "code": "IND",
            "effective_date": "wrong-date",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Invalid date format", result)

    def test_wrong_version(self):
        row = {
            "record_id": "7",
            "code": "IND",
            "effective_date": "2026-01-10",
            "reference_version": "v2"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Reference version not found", result)
    def test_missing_reference_version(self):
        row = {
            "record_id": "9",
            "code": "IND",
            "effective_date": "2026-01-10",
            "reference_version": ""
      }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Missing required field", result)
    def test_outside_effective_date(self):
        row = {
            "record_id": "8",
            "code": "IND",
            "effective_date": "2028-01-10",
            "reference_version": "v1"
        }

        result = validate_record(row, self.reference_data, set())
        self.assertIn("Code outside effective date range", result)
    
if __name__ == "__main__":
    unittest.main()
