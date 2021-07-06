import requests


class TestEx11:
    @staticmethod
    def test_homework_cookie():
        expected_cookie_value = "hw_value"
        expected_cookie_header = "HomeWork"
        response = requests.get("https://playground.learnqa.ru/api/homework_cookie")
        cookies = response.cookies
        # checking that expected header in returned cookies
        assert expected_cookie_header in cookies, f"No header {expected_cookie_header} in response cookies: {cookies}"

        # checking that expected cookie value returned
        cookie_value = cookies[expected_cookie_header]
        assert cookie_value == expected_cookie_value, f"Returned {expected_cookie_header}: {cookie_value} is not equal to expected {expected_cookie_value}"
