import pytest
import requests
import allure
from data import Urls, Ingredients


class TestCreateOrder:
    
    @allure.title('Создание заказа авторизованным пользователем')
    def test_create_order_with_auth(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')
        order = {'ingredients': Ingredients.TEST_INFREDIENTS}
        
        response = requests.post(Urls.ORDER_CREATE, headers={"Authorization": access_token}, data=order)

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Создание заказа неавторизованным пользователем')
    def test_create_order_without_auth(self):
        order = {'ingredients': Ingredients.TEST_INFREDIENTS}
        
        response = requests.post(Urls.ORDER_CREATE, data=order)

        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingredients(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')

        response = requests.post(Urls.ORDER_CREATE, headers={"Authorization": access_token})


        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == "Ingredient ids must be provided"


    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        create_user_data, response_data, status_code = create_user
        access_token = response_data.get('accessToken')

        order = {'ingredients': {123}}
        response = requests.post(Urls.ORDER_CREATE, headers={"Authorization": access_token}, data=order)

        assert response.status_code == 500

    