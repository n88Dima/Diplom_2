import pytest
import allure
import requests
from data import Urls

class TestUpdateUserData:

    @allure.title('Успешное обновление данных пользователя')
    @pytest.mark.parametrize("update_email, update_name", [
        (None, "Dmitry123"),
        ("lol5@ya.ru", None),
    ])
    def test_update_user_data(self, create_user, update_email, update_name):
        create_user_data, response_data, status_code = create_user
        access_token = response_data['accessToken']
        
        update_data = {}
        if update_email is not None:
            update_data["email"] = update_email
        if update_name is not None:
            update_data["name"] = update_name
        
        response = requests.patch(Urls.USER_UPDATE, headers={"Authorization": access_token}, json=update_data)

        assert response.status_code == 200
        assert response.json().get('success')



    @allure.title('Jбновление данных пользователя без авторизации')
    @pytest.mark.parametrize("update_email, update_name", [
        (None, "Dmitry123"),
        ("lol2@ya.ru", None),
    ])
    def test_update_user_data_without_auth(self, update_email, update_name):
        update_data = {"email": update_email, "name": update_name}
        
        response = requests.patch(Urls.USER_UPDATE, json=update_data)

        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == "You should be authorised"