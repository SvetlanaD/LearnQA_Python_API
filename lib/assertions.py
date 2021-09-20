import allure
from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            with allure.step(f"Checking that response is in JSON format. Response text is '{response.text}'"):
                assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        with allure.step(f"Checking that response JSON has key '{name}'"):
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"
        with allure.step(f"Checking that key {name} has value {expected_value}"):
            assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            with allure.step(f"Checking that response is in JSON format. Response text is '{response.text}'"):
                assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        with allure.step(f"Checking that response JSON has key '{name}'"):
            assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            with allure.step(f"Checking that response is in JSON format. Response text is '{response.text}'"):
                assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        for name in names:
            with allure.step(f"Checking that response JSON has no key '{name}'"):
                assert name in response_as_dict, f"Response JSON doesn't have key '{name}'"

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            with allure.step(f"Checking that response is in JSON format. Response text is '{response.text}'"):
                assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        with allure.step(f"Checking that response JSON has no key '{name}'"):
            assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}' but it's present"

    @staticmethod
    def assert_json_has_no_keys(response: Response, names):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            with allure.step(f"Checking that response is in JSON format. Response text is '{response.text}'"):
                assert False, f"Response isn't in JSON format. Response text is '{response.text}'"
        for name in names:
            with allure.step(f"Checking that response JSON has no key '{name}'"):
                assert name not in response_as_dict, f"Response JSON shouldn't have key '{name}' but it's present"

    @staticmethod
    def assert_code_status(response: Response, expected_status_code):
        with allure.step(f"Checking that response code is {expected_status_code}"):
            assert response.status_code == expected_status_code, \
                f"Unexpected status code! Expected: {expected_status_code}. Actual: {response.status_code}"

    @staticmethod
    def assert_response_text(response: Response, expected_response_text):
        with allure.step(f"Checking that response text is equal to {expected_response_text}"):
            assert response.text == expected_response_text, \
                f"Unexpected response text! Expected: {expected_response_text}. Actual: {response.text}"
