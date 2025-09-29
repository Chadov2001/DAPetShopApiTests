import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("проверка статус кода"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("проверка текстового содержимого"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title('Попытка получить информацию о новом животном')
    def test_get_nonexistent_pet(self):
        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step("проверка статус кода"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step('Подготовка данных для создания питомца'):
            payload = {
                "id": 10,
                "name": "Doggie",
                "status": "available"
            }
        with allure.step('Отправка запроса на создание питомца'):
            response = requests.post(url=f'{BASE_URL}/pet', json=payload)

        with allure.step('Проверка статуса ответа и валидации JSON-схемы'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'
            jsonschema.validate(response.json(), PET_SCHEMA)

        @allure.title("Добавление нового питомца c полными данными")
        def add_pet_with_full_data():
            with allure.step('Подготовка данных для питомца'):
                first_payload = {
                    "id": 1,
                    "name": "Dogs",
                    "photoUrls": ["string"],
                    "tags": [{"id": 0, "name": "string"}],
                    "status": "available"
                }
            with allure.step('Отправка запроса на создание питомца'):
                responses = requests.post(url=f'{BASE_URL}/pet', json= first_payload)

            with allure.step('Проверка статуса ответа и валидации JSON-схемы'):
                assert responses.status_code == 200, 'Код ответа не совпал с ожидаемым'
                jsonschema.validate(response.json(), PET_SCHEMA)

    @allure.title('Получение информации о питомце по ID')
    def test_get_pet_by_id(self, create_pet):
      with allure.step('Получение ID созданного питомца'):
          pet_id = create_pet['id']

      with allure.step('Отправка запроса на получение информации о питомце по ID'):
          response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')

      with allure.step('Проверка статуса ответа и данных питомца'):
          assert response.status_code == 200
          assert response.json()['id'] == pet_id

    @allure.title('Обновление информации о питомце')
    def test_update_pet_info(self, create_pet):
        pet_id = create_pet
        updated_payload = {
            "id": pet_id,
            "name": "Buddy Updated",
            "status": "sold"
        }
        with allure.step("Отправляем запрос на обновление питомца"):
            response = requests.put(url=f'{BASE_URL}/pet', json=updated_payload)
            assert response.status_code == 200

        with allure.step("Проверка обновленных данных питомца"):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 200
            assert response.json()['id'] == pet_id
            assert response.json()['name'] == updated_payload['name']
            assert response.json()['status'] == updated_payload['status']

    @allure.title('Удаление питомца по ID')
    def test_delete_pet_id(self, create_pet):
        pet_id = create_pet
        with allure.step('Отправляем запрос на удаление питомца по ID'):
            response = requests.delete(url=f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 200

        with allure.step('Отправляем запрос на получение информации о питомце'):
            response = requests.get(url=f'{BASE_URL}/pet/{pet_id}')
            assert response.status_code == 404