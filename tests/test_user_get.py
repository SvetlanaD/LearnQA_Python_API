from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserGet(BaseCase):

    def test_get_user_details_not_auth(self):
        response = MyRequests.get("/user/2")
        Assertions.assert_json_has_key(response, "username")
        Assertions.assert_json_has_no_key(response, "firstName")
        Assertions.assert_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post("/user/login", data=data)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get("/user/" + str(user_id_from_auth_method), headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        expected_fields = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_keys(response2, expected_fields)

    def test_get_user_details_auth_as_another_user(self):

        # REGISTER 2 USERS
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user1_email = register_data["email"]
        user1_password = register_data["password"]

        response2 = MyRequests.post("/user/", data=self.prepare_registration_data())
        user2_id = self.get_json_value(response2, "id")

        # GETTING AUTHORIZATION DATA FOR USER1
        response3 = MyRequests.post(url="/user/login", data={'email': user1_email, 'password': user1_password})

        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")

        # GET USER2 INFO WITH USER1 AUTHORIZATION DATA
        response4 = MyRequests.get("/user/" + str(user2_id), headers={"x-csrf-token": token},
                                   cookies={"auth_sid": auth_sid})

        Assertions.assert_json_has_key(response4, "username")
        Assertions.assert_json_has_no_keys(response4, ["id", "email", "firstName", "lastName"])
