from datetime import datetime

import requests


def test_server():
    url = 'http://localhost:8000/api/products'
    headers = {"Authorization": "Token 8c8ae49be58030fd291836e0e5318d3b0c47c48c"}

    start_time = datetime.now()
    response = requests.get(url, headers=headers)
    end_time = datetime.now()

    print(f"Response time: {end_time - start_time}")

    print(response.json())


if __name__ == "__main__":
    test_server()
