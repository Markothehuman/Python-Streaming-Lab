"""
producer.py
----------------
This file contains the logic for a Producer that simulates a real-time data
stream by reading events from a CSV file and sending them one by one into a queue.

"""

import csv
import time
from queue import Queue


class CSVProducer:
    def __init__(self, csv_path, q, delay=1.0):
        """
        PARAMETERS:
        - csv_path : path to the CSV file (str)
        - q        : queue acting as our 'topic'
        - delay    : time to wait between sending each row (float)

        """
        self.csv_path = csv_path
        self.q = q
        self.delay = delay

    def start(self):
        """
        Read CSV rows and send them to the queue, pausing between rows.
        """
        with open(self.csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print(f"Producing: {row}")
                self.q.put(row)
                time.sleep(self.delay)

# Debugging test

if __name__ == "__main__":
    """
    Run this file alone to test your producer.

    Expected behavior:
    - It should print rows from the CSV file every 'delay' seconds.
    """
    q = Queue()
    producer = CSVProducer("transactions.csv", q, delay=1.0)
    producer.start()
