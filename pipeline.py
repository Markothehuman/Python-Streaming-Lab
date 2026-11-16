import threading
from queue import Queue
from producer import CSVProducer
from consumer import Consumer


def main():
    q = Queue()
    producer = CSVProducer("transactions.csv", q)
    consumer = Consumer(q)

    producer_thread = threading.Thread(target=producer.start, daemon=True)
    consumer_thread = threading.Thread(target=consumer.start, daemon=True)

    consumer_thread.start()
    producer_thread.start()

    producer_thread.join()
    q.put(None)  # Tell the consumer there are no more rows.
    consumer_thread.join()
    print("Pipeline complete: all transactions processed.")


if __name__ == "__main__":
    print("Starting the Python Streaming Pipeline...")
    try:
        main()
    except KeyboardInterrupt:
        print("\nPipeline stopped.")
