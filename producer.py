import csv
import time
from queue import Queue


class CSVProducer:
    def __init__(self, csv_path, q, delay=1.0):
        self.csv_path = csv_path
        self.q = q
        self.delay = delay

    def start(self):
        with open(self.csv_path, newline="", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                print(f"Producing: {row}")
                self.q.put(row)
                time.sleep(self.delay)


if __name__ == "__main__":
    q = Queue()
    producer = CSVProducer("transactions.csv", q)
    producer.start()
