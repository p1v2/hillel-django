import requests

def test_basic_auth():
    # basic auth
    response = requests.get('http://localhost:8000/api/products/', auth=('vitalii', 'gddgdd'))

    print(response.status_code)
    print(response.json())


def test_token_auth():
    # make request to get token
    response = requests.post('http://localhost:8000/api/auth/', json={'username': 'vitalii', 'password': 'gddgdd'})

    print(response.status_code)
    print(response.json())

    token = response.json()['token']

    # make request with token
    response = requests.get('http://localhost:8000/api/products/', headers={'Authorization': f'Token {token}'})

    print(response.status_code)
    print(response.json())

    # make request without token
    response = requests.get('http://localhost:8000/api/products/')

    print(response.status_code)
    print(response.json())

    response = requests.get('http://localhost:8000/api/products/', headers={'Authorization': f'Token LOLWUT'})

    print(response.status_code)
    print(response.json())


def test_registration():
    registration_data = {
        "username": "user5",
        "password": "aaa1234567!"
    }

    response = requests.post('http://localhost:8000/api/register/', json=registration_data)
    print(response.status_code)
    print(response.json())


def test_get_products():
    token = "9e00da0708bb660352e41e36abd10805bbe8876a"

    # make request with token
    response = requests.get('http://localhost:8000/api/products/', headers={'Authorization': f'Token {token}'})

    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    test_get_products()
