import allure
import jsonschema
import requests # Используется для формирования апи запроса
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
            first_payload = {
                "id": 10,
                "name": "Doggie",
                "status": "available"
            }
        with allure.step('Отправка запроса на создание питомца'):
            response = requests.post(url=f'{BASE_URL}/pet', json = first_payload)

        with allure.step('Проверка статуса ответа и валидации JSON-схемы'):
            assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

        with allure.step('Подготовка данных для второго питомца'):
            second_payload = {
                "id": 1,
                "name": "Dogs",
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }
            with allure.step('Отправка запроса на создание питомца'):
                response = requests.post(url=f'{BASE_URL}/pet', json=second_payload)

            with allure.step('Проверка статуса ответа и валидации JSON-схемы'):
                assert response.status_code == 200, 'Код ответа не совпал с ожидаемым'

            jsonschema.validate(response.json(), PET_SCHEMA)


