"""
consumer.py
----------------
This file contains the logic for a Consumer that continuously reads messages
from the queue and processes them.

The Consumer waits for events until it receives None as a stop signal.
"""

import time
from queue import Queue


class Consumer:
    def __init__(self, q):
        """
        PARAMETERS:
        - q : the shared queue (simulated topic)

        """
        self.q = q

    def start(self):
        """
        Wait for events from the queue and process them one at a time.
        """
        while True:
            event = self.q.get()
            if event is None:
                break
            print(f"Consumed: {event}")
            self.process(event)

    def process(self, event):
        """
        Convert the amount to a number and simulate a little processing time.
        """
        amount = float(event["amount"])
        print(f"Processed amount: {amount:.2f}")
        time.sleep(0.5)


# Debugging test

if __name__ == "__main__":
    """
    Run this alone to see consumer behavior.

    Note: It will block waiting for messages since no producer is running.
    """
    q = Queue()
    consumer = Consumer(q)
    print("Waiting for events... Press Ctrl+C to stop.")
    consumer.start()
