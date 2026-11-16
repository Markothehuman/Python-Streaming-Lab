import time
from queue import Queue


class Consumer:
    def __init__(self, q):
        self.q = q

    def start(self):
        while True:
            event = self.q.get()
            if event is None:
                break
            print(f"Consumed: {event}")
            self.process(event)

    def process(self, event):
        amount = float(event["amount"])
        print(f"Processed amount: {amount:.2f}")
        time.sleep(0.5)


if __name__ == "__main__":
    q = Queue()
    consumer = Consumer(q)
    print("Waiting for events... Press Ctrl+C to stop.")
    consumer.start()
