import pytest
import allure
import requests
from data import Urls



class TestLogin:
    

    @allure.title('Авторизация под существующим пользователем')
    def test_login_existing_user(self, create_user):
        create_user_data, response_data, status_code = create_user
        
        response = requests.post(Urls.USER_LOGIN, json={
            "email": create_user_data['email'],
            "password": create_user_data['password']
        })
        
        assert response.status_code == 200
        assert response.json().get('success') is True
        assert all(key in response.json() for key in ('accessToken', 'refreshToken'))
        assert response.json()['user']['email'] == create_user_data['email']
        assert response.json()['user']['name'] == create_user_data['name']


    @allure.title('Логин с неверными учетными данными')

    @pytest.mark.parametrize("test_cases_input", [
        {"email": "wrong@example", "password": "wrongpassword"},
        {"email": "wrongexample.com", "password": "password"},
        {"email": "", "password": "password"},
        {"email": "test@example.com", "password": ""},
        {"email": "", "password": ""}
    ])
    def test_login_invalid_user(self, test_cases_input):
        response = requests.post(Urls.USER_LOGIN, json=test_cases_input)

        
        assert response.status_code == 401, "Статус-код ответа не 401"
        assert response.json().get('success') is False, "Поле 'success' не равно False"
        assert response.json().get('message') == "email or password are incorrect", "Сообщение об ошибке некорректно"
