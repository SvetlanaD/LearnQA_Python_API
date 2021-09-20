import allure

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@allure.feature("User deletion")
class TestUserDelete(BaseCase):

    @allure.suite("Negative")
    def test_delete_user_2_negative(self):
        # login with the user id=2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        auth_sid, token = self.get_user_auth_data(data)

        # try to delete user 2 and make sure that user cannot be deleted
        response = MyRequests.delete(url="/user/2", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, 'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    @allure.suite("Happy path")
    def test_test_delete_user_positive(self):
        # register
        user_id, register_data = self.create_user()

        # login
        auth_sid, token = self.get_user_auth_data(
            data={"email": register_data["email"], "password": register_data["password"]})

        # delete
        response = MyRequests.delete(url=f"/user/{user_id}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response, 200)

        # check that user doesn't exist anymore
        response = MyRequests.get(url=f"/user/{user_id}")
        Assertions.assert_code_status(response, 404)
        Assertions.assert_response_text(response, 'User not found')

    @allure.suite("Negative")
    def test_delete_user_being_authorized_by_another_user(self):
        # register 2 users
        user_id_1, register_data_1 = self.create_user()
        user_id_2, register_data_2 = self.create_user()

        # login with the user 2
        auth_sid, token = self.get_user_auth_data(data={"email": register_data_2["email"], "password": register_data_2["password"]})

        # try to delete user 1
        response = MyRequests.delete(url=f"/user/{user_id_1}", headers={"x-csrf-token": token},
                                     cookies={"auth_sid": auth_sid})
        Assertions.assert_code_status(response, 200)

        # check that user wasn't deleted
        response = MyRequests.get(url=f"/user/{user_id_1}")
        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, '{"username":"learnqa"}')





