"""
pipeline.py
----------------
This file launches BOTH producer and consumer using Python threads to simulate
a real streaming pipeline.

"""

import threading
from pathlib import Path
from queue import Queue
from producer import CSVProducer
from consumer import Consumer


def main():
    """Run both workers, then wait until every CSV row has been processed."""
    q = Queue()
    csv_path = Path(__file__).with_name("transactions.csv")
    producer = CSVProducer(csv_path, q)
    consumer = Consumer(q)

    producer_thread = threading.Thread(target=producer.start, daemon=True)
    consumer_thread = threading.Thread(target=consumer.start, daemon=True)

    consumer_thread.start()
    producer_thread.start()

    # Wait until every row has been sent, then tell the consumer to stop.
    producer_thread.join()
    q.put(None)
    consumer_thread.join()
    print("Pipeline complete: all transactions processed.")


if __name__ == "__main__":
    print("Starting the Python Streaming Pipeline...")
    try:
        main()
    except KeyboardInterrupt:
        print("\nPipeline stopped.")
