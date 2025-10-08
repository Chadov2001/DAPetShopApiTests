import allure
import requests

BASE_URL = 'http://5.181.109.28:9090/api/v3'

@allure.feature('Store')

class TestStore:
    @allure.title('Добавление питомца с подготовленными данными')
    def test_store_add_pet(self):
        with allure.step('Отправка запроса с подготовленными данными'):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": 'true'
            }
            response = requests.post(url=f'{BASE_URL}/store/order', json= payload)
            assert response.status_code == 200

    @allure.title('Получение информации о заказе по ID ')
    def test_info_check_store(self):
        with allure.step('Отправка запроса на получение информации по ID'):
            response = requests.get(url=f'{BASE_URL}/store/order/1')
            assert response.status_code == 200
            assert response.json()['id'] == 1

    @allure.title('Удаление заказа по ID')
    def test_delete_order_store(self):
        with allure.step('Отправка запроса на удаление информации'):
            response = requests.delete(url=f'{BASE_URL}/store/order/1')
            assert response.status_code == 200
        with allure.step('Отправляем запрос на получение информации'):
            response = requests.get(url=f'{BASE_URL}/store/order/1')
            assert response.status_code == 404

    @allure.title('Попытка получить информацию о несуществующем заказе')
    def test_nonexistent_order_store(self):
        with allure.step('Отправляем запрос на получение информации'):
            response = requests.get(url=f'{BASE_URL}/store/order/9999')
            assert response.status_code == 404

    @allure.title('Получение инвентаря магазина')
    def test_obtaining_inv_store(self):
        with allure.step('Отправка запроса на получение инвентаря'):
            response = requests.get(url=f'{BASE_URL}/store/inventory')
            assert response.status_code == 200
            assert response.json()['approved'] == 57
            assert response.json()['delivered'] == 50