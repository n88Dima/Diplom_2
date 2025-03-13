import allure
import requests
from data import Urls, Ingredients

class TestGetOrders:

    @allure.title('Получение заказа не авторизованным пользователем')
    def test_get_user_order_without_auth(self):

        response = requests.get(Urls.GET_ORDERS)

        assert response.status_code == 401
        assert response.json()['message'] == "You should be authorised"


    def test_get_user_order_with_auth_success(self, create_user):
        create_user_data, response_body, status_code = create_user

        access_token = response_body.get('accessToken')
        order = {'ingredients': Ingredients.TEST_INFREDIENTS}
        requests.post(Urls.ORDER_CREATE, headers={"Authorization": access_token}, data=order)

        response = requests.get(Urls.GET_ORDERS, headers={"Authorization": access_token})


        assert response.status_code == 200
        assert response.json()['success'] is True
        assert len(response.json()["orders"]) == 1