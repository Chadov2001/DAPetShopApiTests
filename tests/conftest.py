import pytest
import requests

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
        payload = {
            "id": 10,
            "name": "Doggie",
            "status": "available"
        }
        response = requests.post(url=f'{BASE_URL}/pet', json= payload)
        assert response.status_code == 200
        return response.json()

@pytest.fixture(scope= 'function')
def creation_pet():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}/pet', json= payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope= 'function')
def update_pet():
    payload = {
        "id": 1,
        "name": "Buddy Updated",
        "status": "sold"
    }
    response = requests.put(url=f'{BASE_URL}/pet', json= payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture(scope='function')
def create_pet_id():
    payload = {
        "id": 1,
        "name": "Buddy",
        "status": "available"
    }
    response = requests.post(url=f'{BASE_URL}/pet', json=payload)
    assert response.status_code == 200
    return response.json()['id']

@pytest.fixture(scope='function')
def delete_pet(create_pet_id):
    pet_id = create_pet_id
    response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')
    assert response.status_code == 200



