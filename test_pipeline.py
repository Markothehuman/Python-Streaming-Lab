"""Check the complete pipeline using only Python's standard library."""

import csv
import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from queue import Queue
from unittest.mock import patch

from consumer import Consumer
from pipeline import main


class PipelineTests(unittest.TestCase):
    @patch("time.sleep", return_value=None)
    def test_all_transactions_are_processed_in_order(self, mock_sleep):
        csv_path = Path(__file__).with_name("transactions.csv")
        with open(csv_path, newline="", encoding="utf-8") as csv_file:
            expected = list(csv.DictReader(csv_file))

        output = io.StringIO()
        original_directory = Path.cwd()
        # The CSV should also be found when launched from another directory.
        with tempfile.TemporaryDirectory() as other_directory:
            try:
                os.chdir(other_directory)
                with redirect_stdout(output):
                    main()
            finally:
                os.chdir(original_directory)

        lines = output.getvalue().splitlines()
        produced = [line for line in lines if line.startswith("Producing: ")]
        consumed = [line for line in lines if line.startswith("Consumed: ")]
        amounts = [line for line in lines if line.startswith("Processed amount: ")]

        self.assertEqual(produced, [f"Producing: {row}" for row in expected])
        self.assertEqual(consumed, [f"Consumed: {row}" for row in expected])
        self.assertEqual(amounts, [
            f"Processed amount: {float(row['amount']):.2f}" for row in expected
        ])
        self.assertEqual(lines[-1], "Pipeline complete: all transactions processed.")

    def test_stop_signal_ends_consumer_without_processing_a_row(self):
        q = Queue()
        q.put(None)
        output = io.StringIO()
        with redirect_stdout(output):
            Consumer(q).start()
        self.assertTrue(q.empty())
        self.assertEqual(output.getvalue(), "")

    @patch("time.sleep", return_value=None)
    def test_consumer_finishes_queued_rows_before_stopping(self, mock_sleep):
        q = Queue()
        q.put({"amount": "12.5"})
        q.put({"amount": "7"})
        q.put(None)
        output = io.StringIO()
        with redirect_stdout(output):
            Consumer(q).start()
        self.assertEqual(output.getvalue().splitlines(), [
            "Consumed: {'amount': '12.5'}",
            "Processed amount: 12.50",
            "Consumed: {'amount': '7'}",
            "Processed amount: 7.00",
        ])
        self.assertTrue(q.empty())


if __name__ == "__main__":
    unittest.main()
