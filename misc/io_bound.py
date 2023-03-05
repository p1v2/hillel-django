import os
from datetime import datetime
from multiprocessing.pool import ThreadPool
# from threading import Thread

import requests
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_USER_ID = os.environ.get("TELEGRAM_USER_ID")


def send_telegram_message(number):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

    body = {
        "chat_id": TELEGRAM_USER_ID,
        "text": f"Hello there from request {number}",
    }
    requests.post(url, json=body)


if __name__ == "__main__":
    start = datetime.now()
    threads = []

    pool = ThreadPool(10)

    results = []
    for i in range(1000):
        # send_telegram_message(i)
        result = pool.apply_async(send_telegram_message, args=(i,))
        results.append(result)

    for result in threads:
        result.join()

    pool.close()

    end = datetime.now()

    print((end - start).total_seconds())
