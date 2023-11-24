import os

import requests
from dotenv import load_dotenv
load_dotenv()


def telegram_set_webhook():
    # Set telegram webhook
    token = os.environ.get("TELEGRAM_API_TOKEN")
    url = f'https://b209-188-163-9-200.ngrok-free.app/telegram/'

    resp = requests.post(
        f"https://api.telegram.org/bot{token}/setWebhook",
        json={
            "url": url
        }
    )

    print(resp.json())

if __name__ == '__main__':
    telegram_set_webhook()
