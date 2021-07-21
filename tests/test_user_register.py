import random
import string

import pytest
import requests
from datetime import datetime
from lib.base_case import BaseCase
from lib.assertions import Assertions


class TestUserRegister(BaseCase):
    api_create_user = "https://playground.learnqa.ru/api/user/"

    def setup(self):
        base_part = "learnqa"
        domain = "example.com"
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")
        self.email = f"{base_part}{random_part}@{domain}"
        self.payload = {
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "password": "123",
            "email": self.email
        }

    def test_create_user_successfully(self):
        data = self.payload
        response = requests.post(self.api_create_user, data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = self.payload
        email = "vinkotov@example.ru"
        data["email"] = email
        response = requests.post(self.api_create_user, data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, f"Users with email '{email}' already exists")

    def test_create_user_with_incorrect_email(self):
        data = self.payload
        data["email"] = "vinkotovexample.ru"
        response = requests.post(self.api_create_user, data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "Invalid email format")

    def test_create_user_with_short_first_name(self):
        data = self.payload
        data["firstName"] = "a"
        response = requests.post(self.api_create_user, data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'firstName' field is too short")

    def test_create_user_with_long_first_name(self):
        data = self.payload
        data["firstName"] = ''.join(random.choices(string.ascii_letters + string.digits, k=251))
        response = requests.post(self.api_create_user, data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, "The value of 'firstName' field is too long")

    @pytest.mark.parametrize("missing_field", ["username", "firstName", "lastName", "password", "email"])
    def test_create_user_missing_field(self, missing_field):
        data = self.payload
        del data[missing_field]
        response = requests.post(self.api_create_user, data=data)

        Assertions.assert_code_status(response, 400)
        Assertions.assert_response_text(response, f"The following required params are missed: {missing_field}")
