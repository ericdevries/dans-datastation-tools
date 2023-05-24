# Tests the csv_report module

import csv

from datastation.common.csv import CsvReport


class TestCsvReport:

    def test_csv_report(self, tmp_path):
        # Given
        filename = tmp_path / "test.csv"
        headers = ["header1", "header2"]
        # When
        with CsvReport(filename, headers) as csv_report:
            csv_report.write({"header1": "value1", "header2": "value2"})
        # Then
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            row = next(reader)
            assert row["header1"] == "value1"
            assert row["header2"] == "value2"

    def test_csv_report_stdout(self, capsys):
        # Given
        headers = ["header1", "header2"]
        # When
        with CsvReport("-", headers) as csv_report:
            csv_report.write({"header1": "value1", "header2": "value2"})
        # Then
        captured = capsys.readouterr()
        assert captured.out == "header1,header2\nvalue1,value2\n"

    def test_empty_csv_report(self, tmp_path):
        # Given
        filename = tmp_path / "test.csv"
        headers = ["header1", "header2"]
        # When
        with CsvReport(filename, headers) as _:
            pass
        # Then
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            assert len(list(reader)) == 0

    def test_report_with_zero_columns(self, tmp_path):
        # Given
        filename = tmp_path / "test.csv"
        headers = []
        # When
        with CsvReport(filename, headers) as _:
            pass
        # Then
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            assert len(list(reader)) == 0