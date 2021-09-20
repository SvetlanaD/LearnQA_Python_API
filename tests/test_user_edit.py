import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.feature("User editing")
class TestUserEdit(BaseCase):
    @allure.suite("Happy path")
    def test_edit_just_created_user(self):
        # REGISTER
        user_id, register_data = self.create_user()

        # LOGIN
        auth_sid, token = self.get_user_auth_data(
            data={"email": register_data["email"], "password": register_data["password"]})

        # EDIT
        new_name = "Changed name"
        response = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                  data={"firstName": new_name})

        Assertions.assert_code_status(response, 200)

        # GET
        response = MyRequests.get(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})
        Assertions.assert_json_value_by_name(response, "firstName", new_name, "Wrong name of the user after edit")

    @allure.suite("Negative")
    def test_edit_user_unauthorized(self):
        # REGISTER
        user_id = self.create_user()

        # EDIT
        new_name = "Changed name"
        response = MyRequests.put(f"/user/{user_id}",
                                  data={"firstName": new_name})

        Assertions.assert_code_status(response, 404)

    @allure.suite("Negative")
    def test_edit_user_being_authorized_by_another_user(self):
        # REGISTER 2 USERS
        user_id_1, register_data_1 = self.create_user()
        username_1 = register_data_1["username"]

        user_id_2, register_data_2 = self.create_user()

        # LOGIN WITH THE USER 2
        auth_sid, token = self.get_user_auth_data(data={"email": register_data_2["email"], "password": register_data_2["password"]})

        # EDIT "USERNAME" OF USER 1 WITH THE USER 2 AUTHORIZATION DATA
        new_name = "Changed name"
        response = MyRequests.put(f"/user/{user_id_1}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                  data={"username": new_name})
        Assertions.assert_code_status(response, 200)

        response = MyRequests.get(f"/user/{user_id_1}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid})

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_value_by_name(response, "username", username_1,
                                             f"Field 'username' was changed but it shouldn't")

    @allure.suite("Negative")
    def test_edit_user_incorrect_email(self):
        # REGISTER
        user_id, register_data = self.create_user()

        # LOGIN
        auth_sid, token = self.get_user_auth_data(
            data={"email": register_data["email"], "password": register_data["password"]})

        # EDIT
        response = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                  data={"email": "vinkotovexample.ru"})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    @allure.suite("Negative")
    def test_edit_user_incorrect_first_name(self):
        # REGISTER
        user_id, register_data = self.create_user()

        # LOGIN
        auth_sid, token = self.get_user_auth_data(
            data={"email": register_data["email"], "password": register_data["password"]})

        # EDIT
        response = MyRequests.put(f"/user/{user_id}", headers={"x-csrf-token": token}, cookies={"auth_sid": auth_sid},
                                  data={"firstName": "z"})

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, '{"error":"Too short value for field firstName"}')
