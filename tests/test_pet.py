import allure
import requests # Используется для формирования апи запроса

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
def test_get_nonexistent_pet():

        with allure.step('Отправка запроса на получение информации о несуществующем питомце'):
            response = requests.get(url=f'{BASE_URL}/pet/9999')

        with allure.step("проверка статус кода"):
            assert response.status_code == 404, 'Код ответа не совпал с ожидаемым'


