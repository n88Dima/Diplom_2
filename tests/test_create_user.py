import pytest
import requests
import allure
from data import Urls

class TestCreateUser:
    
    @allure.title("Проверка регистрации пользователя")
    def test_register_user(self,create_user):
        create_user_data, response_data, status_code = create_user
        assert status_code == 200
        assert 'accessToken' in response_data
        assert 'refreshToken' in response_data
        
    
    @allure.title('Регистрация пользователя, который уже зарегистрирован')
    def test_register_exist_user(self,create_user):
        create_user_data,response_data, status_code = create_user
        response = requests.post(Urls.USER_REGISTER, json=create_user_data)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == "User already exists"


    @allure.title('Регистрация пользователя без обязательного параметра(пароль, email, name)')
    @pytest.mark.parametrize("test_user_data", [
        {"email": "", "password": "password", "name": "Dmitry"},
        {"email": "terehov2000@gamil.com", "password": "", "name": "Dmitry"},
        {"email": "terehov2000@gmail.com", "password": "password", "name": ""}
    ])
    def test_create_user_without_required_fields(self,test_user_data):
        response = requests.post(Urls.USER_REGISTER, json=test_user_data)

        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == "Email, password and name are required fields"
